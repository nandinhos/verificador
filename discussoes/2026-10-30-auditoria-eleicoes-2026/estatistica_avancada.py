#!/usr/bin/env python3
"""Estatística avançada do swing por seção (Presidente) — itens 11 e 12.

(11) Triagem de outliers com correção de múltiplas comparações (Benjamini-Hochberg):
     para cada seção pareada, z robusto do swing; p bicaudal ~ normal; conta quantas
     sobrevivem ao controle de FDR a 5% e 1%. Família = todas as seções da UF.
(12) Bootstrap por reamostragem de seções (clusters) — IC 95% do swing mediano.

Swing = Δ share do nº 13 (p.p.) entre turnos, por seção. Seed fixa.
Uso: python3 estatistica_avancada.py --ufs SP,AC,... --raw /root/auditoria-raw --out dados
"""
import argparse
import csv
import io
import json
import math
import os
import random
import statistics
import zipfile

Q = '"Presidente"'
I_MUN, I_ZONA, I_SECAO = 11, 13, 14
I_CARGO, I_TIPO, I_NUM, I_VOTOS = 17, 28, 29, 31
SEED = 20261030


def secoes(zip_path):
    z = zipfile.ZipFile(zip_path)
    nome = [x for x in z.namelist() if x.endswith(".csv")][0]
    fh = io.TextIOWrapper(z.open(nome), encoding="latin-1", newline="")
    sec = {}
    for linha in fh:
        if Q not in linha:
            continue
        c = next(csv.reader([linha], delimiter=";", quotechar='"'))
        if len(c) <= I_VOTOS or c[I_CARGO] != "Presidente":
            continue
        k = (c[I_MUN], c[I_ZONA], c[I_SECAO])
        r = sec.get(k) or sec.setdefault(k, {"v": 0, "v13": 0})
        if c[I_TIPO] == "Nominal":
            v = int(c[I_VOTOS] or 0)
            r["v"] += v
            if c[I_NUM] == "13":
                r["v13"] += v
    return sec


def phi(z):  # cauda normal bicaudal
    return math.erfc(abs(z) / math.sqrt(2))


def bh(pvals, q):
    m = len(pvals)
    sp = sorted(pvals)
    k = 0
    for i, p in enumerate(sp, 1):
        if p <= q * i / m:
            k = i
    return k


def analisar(uf, raw):
    z1 = os.path.join(raw, f"bweb_1t_{uf}.zip")
    z2 = os.path.join(raw, f"bweb_2t_{uf}.zip")
    if not (os.path.exists(z1) and os.path.exists(z2)):
        return {"uf": uf, "status": "ZIP_AUSENTE"}
    s1, s2 = secoes(z1), secoes(z2)
    sw = []
    for k in (set(s1) & set(s2)):
        a, b = s1[k], s2[k]
        if a["v"] >= 10 and b["v"] >= 10:
            sw.append(100 * (b["v13"] / b["v"] - a["v13"] / a["v"]))
    if len(sw) < 50:
        return {"uf": uf, "status": "POUCAS", "n": len(sw)}
    med = statistics.median(sw)
    mad = statistics.median([abs(x - med) for x in sw]) or 1e-9
    zs = [0.6745 * (x - med) / mad for x in sw]
    pvals = [phi(z) for z in zs]
    # bootstrap por reamostragem de seções (clusters)
    rng = random.Random(SEED)
    n = len(sw)
    meds = []
    for _ in range(1000):
        amostra = [sw[rng.randrange(n)] for _ in range(n)]
        meds.append(statistics.median(amostra))
    meds.sort()
    ic = (round(meds[25], 3), round(meds[975], 3))
    return {
        "uf": uf, "status": "OK", "n": n,
        "swingMediano_pp": round(med, 3),
        "swingMedio_pp": round(statistics.fmean(sw), 3),
        "ic95Mediano_pp": ic,
        "sig_FDR5pct": bh(pvals, 0.05),
        "sig_FDR1pct": bh(pvals, 0.01),
        "pctSobreviveFDR5": round(100 * bh(pvals, 0.05) / n, 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ufs", required=True)
    ap.add_argument("--raw", default="/root/auditoria-raw")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    res = []
    for uf in [u.strip().upper() for u in args.ufs.split(",") if u.strip()]:
        print(f"avancada {uf}...", flush=True)
        r = analisar(uf, args.raw)
        res.append(r)
        if r.get("status") == "OK":
            print(f"  n={r['n']} swing_med={r['swingMediano_pp']} IC95={r['ic95Mediano_pp']} "
                  f"FDR5%={r['sig_FDR5pct']} ({r['pctSobreviveFDR5']}%)", flush=True)
        else:
            print(f"  {r['status']}", flush=True)
    saida = os.path.join(args.out, "estatistica-avancada.json")
    json.dump({"geradoDe": "Swing por secao: BH/FDR + bootstrap IC95 (Presidente)",
               "nota": "FDR = secoes 'outlier' sobreviventes ao controle de falsos positivos; seed " + str(SEED),
               "ufs": res}, open(saida, "w"), ensure_ascii=False, indent=1)
    print(f"escrito {saida}")


if __name__ == "__main__":
    main()
