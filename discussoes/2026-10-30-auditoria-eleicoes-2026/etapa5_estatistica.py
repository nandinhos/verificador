#!/usr/bin/env python3
"""Etapa 5 — testes estatísticos (Presidente, seções pareadas entre turnos).

(1) Diferença-em-diferenças (DiD) do efeito de FECHAMENTO TARDIO:
    hipótese nula = seções que fecharam após 18h (Brasília) no 2º turno não
    tiveram variação de share diferente das pontuais, além do placebo do 1º turno.
    Reporta DiD em p.p. por finalista (13, 22) e o placebo.
(2) Outliers de swing com correção de múltiplas comparações (Benjamini-Hochberg):
    conta quantas seções sobrevivem ao controle de FDR a 5% — triagem, não prova.

Unidade: seção (UF+municipio+zona+secao). Incerteza: como são censitárias,
o teste é de PERMUTAÇÃO (realoca o rótulo tarde/pontual) — a incerteza vem do
processo de atribuição do tratamento, não de amostragem. Seed fixa.

Uso: python3 etapa5_estatistica.py --ufs AC,AM,SP --raw /root/auditoria-raw --out dados
"""
import argparse
import csv
import io
import json
import os
import random
import statistics
import zipfile

Q = '"Presidente"'
I_MUN, I_ZONA, I_SECAO = 11, 13, 14
I_CARGO, I_COMP, I_TIPO, I_NUM, I_VOTOS = 17, 23, 28, 29, 31
I_ABERT, I_ENCERR = 39, 40
OFFSET_BSB = {"AC": 2, "AM": 1, "RR": 1, "RO": 1, "MT": 1, "MS": 1}
TARDE_MIN = 18 * 60  # fechamento após 18h Brasília = "tardia"
SEED = 20261030


def minutos_bsb(ts, uf):
    try:
        h, m, s = (int(x) for x in ts[11:19].split(":"))
    except Exception:
        return None
    return h * 60 + m + OFFSET_BSB.get(uf, 0) * 60


def secoes_uf(zip_path, uf):
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
        r = sec.get(k)
        if r is None:
            r = sec[k] = {"validos": 0, "v13": 0, "v22": 0,
                          "fech": minutos_bsb(c[I_ENCERR].strip('"'), uf)}
        if c[I_TIPO] == "Nominal":
            v = int(c[I_VOTOS] or 0)
            r["validos"] += v
            if c[I_NUM] == "13":
                r["v13"] += v
            elif c[I_NUM] == "22":
                r["v22"] += v
    return sec


def shares(sec, chaves, num):
    tot = val = 0
    for k in chaves:
        tot += sec[k][f"v{num}"]
        val += sec[k]["validos"]
    return (tot / val) if val else 0.0


def did(s1, s2, num, trat):
    """DiD em p.p.: (atu_tarde-ant_tarde)-(atu_pont-ant_pont)."""
    comuns = [k for k in (set(s1) & set(s2))
              if s1[k]["validos"] >= 10 and s2[k]["validos"] >= 10]
    tarde = [k for k in comuns if trat(k)]
    pont = [k for k in comuns if not trat(k)]
    if len(tarde) < 30 or len(pont) < 30:
        return None
    d = ((shares(s2, tarde, num) - shares(s1, tarde, num))
         - (shares(s2, pont, num) - shares(s1, pont, num)))
    return 100 * d, len(tarde), len(pont)


def perm_pvalue(s1, s2, num, trat, obs, comuns, n_perm=1000):
    """p de permutação otimizado: arrays numéricos + somas sobre índices.

    Pré-extrai (v1, val1, v2, val2) por seção. DiD = (v2t/val2t - v1t/val1t)
    - (v2p/val2p - v1p/val1p). Cada permutação realoca o rótulo tarde e soma
    só os acumuladores do grupo tarde (o pontual = total - tarde). O(n) por perm.
    """
    rng = random.Random(SEED)
    v1 = [s1[k][f"v{num}"] for k in comuns]
    a1 = [s1[k]["validos"] for k in comuns]
    v2 = [s2[k][f"v{num}"] for k in comuns]
    a2 = [s2[k]["validos"] for k in comuns]
    n = len(comuns)
    tot_v1, tot_a1, tot_v2, tot_a2 = sum(v1), sum(a1), sum(v2), sum(a2)
    ntarde = sum(1 for k in comuns if trat(k))

    def did_de(idx):
        sv1 = sum(v1[i] for i in idx); sa1 = sum(a1[i] for i in idx)
        sv2 = sum(v2[i] for i in idx); sa2 = sum(a2[i] for i in idx)
        sh_t = (sv2 / sa2 if sa2 else 0) - (sv1 / sa1 if sa1 else 0)
        pv1, pa1 = tot_v1 - sv1, tot_a1 - sa1
        pv2, pa2 = tot_v2 - sv2, tot_a2 - sa2
        sh_p = (pv2 / pa2 if pa2 else 0) - (pv1 / pa1 if pa1 else 0)
        return 100 * (sh_t - sh_p)

    todos = list(range(n))
    extremos = 0
    for _ in range(n_perm):
        if abs(did_de(rng.sample(todos, ntarde))) >= abs(obs):
            extremos += 1
    return extremos / n_perm


def bh_fdr(pvals, q=0.05):
    """Benjamini-Hochberg: nº de hipóteses significativas a FDR=q."""
    m = len(pvals)
    ordenados = sorted(pvals)
    k = 0
    for i, p in enumerate(ordenados, 1):
        if p <= q * i / m:
            k = i
    return k


def analisar(uf, raw):
    z1 = os.path.join(raw, f"bweb_1t_{uf}.zip")
    z2 = os.path.join(raw, f"bweb_2t_{uf}.zip")
    if not (os.path.exists(z1) and os.path.exists(z2)):
        return {"uf": uf, "status": "ZIP_AUSENTE"}
    s1, s2 = secoes_uf(z1, uf), secoes_uf(z2, uf)
    comuns = [k for k in (set(s1) & set(s2))
              if s1[k]["validos"] >= 10 and s2[k]["validos"] >= 10
              and s2[k]["fech"] is not None]
    trat = lambda k: (s2[k]["fech"] or 0) > TARDE_MIN   # tratamento: fechou tarde no 2T
    plac = lambda k: (s1[k]["fech"] or 0) > TARDE_MIN   # placebo: fechou tarde no 1T
    out = {"uf": uf, "status": "OK", "secoesPareadas": len(comuns),
           "tardias2t": sum(1 for k in comuns if trat(k))}
    for num in ("13", "22"):
        real = did(s1, s2, num, trat)
        placebo = did(s1, s2, num, plac)
        if real:
            p = perm_pvalue(s1, s2, num, trat, real[0], comuns, 500)
            out[f"did_{num}"] = {"pp": round(real[0], 3), "tardias": real[1],
                                 "pontuais": real[2], "pPermutacao": round(p, 4),
                                 "placebo_pp": round(placebo[0], 3) if placebo else None}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ufs", default="AC,AM,SP")
    ap.add_argument("--raw", default="/root/auditoria-raw")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    res = []
    for uf in [u.strip().upper() for u in args.ufs.split(",") if u.strip()]:
        print(f"Etapa5 {uf}...", flush=True)
        r = analisar(uf, args.raw)
        res.append(r)
        if r.get("status") == "OK":
            for num in ("13", "22"):
                d = r.get(f"did_{num}")
                if d:
                    print(f"  DiD no{num}: {d['pp']:+.3f} p.p. (p_perm={d['pPermutacao']}, "
                          f"placebo={d['placebo_pp']})", flush=True)
        else:
            print(f"  {r['status']}", flush=True)
    saida = os.path.join(args.out, "etapa5-estatistica.json")
    with open(saida, "w", encoding="utf-8") as fh:
        json.dump({"geradoDe": "DiD fechamento tardio (>18h BSB) com placebo 1T; teste de permutacao",
                   "hipoteseNula": "seções tardias não variam share além do placebo",
                   "seed": SEED, "ufs": res}, fh, ensure_ascii=False, indent=1)
    print(f"escrito {saida}")


if __name__ == "__main__":
    main()
