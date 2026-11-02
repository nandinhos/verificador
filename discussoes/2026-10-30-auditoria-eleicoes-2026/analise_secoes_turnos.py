#!/usr/bin/env python3
"""Etapa 4 fina — comparação por seção pareada 1º x 2º turno (Presidente).

Para cada UF: lê o BU bruto dos dois turnos, agrega por seção
(UF+municipio+zona+secao) os votos dos finalistas nacionais (13 e 22),
válidos e comparecimento. Pareia as seções presentes nos dois turnos e
calcula o swing (variação do share do nº 13 entre turnos). Faz triagem de
outliers por desvio robusto (MAD), SEM tratá-los como prova — apenas
sinalização para inspeção (Seção 5/8 do protocolo).

Saída: agregados por UF + lista de seções-outlier (top-k por |z robusto|).
Não expõe microdados: grava só contagens agregadas e as chaves dos outliers.

Uso: python3 analise_secoes_turnos.py --ufs AC --raw /root/auditoria-raw --out dados
"""
import argparse
import csv
import io
import json
import os
import statistics
import zipfile

FIN = ("13", "22")
Q = '"Presidente"'
I_MUN, I_ZONA, I_SECAO = 11, 13, 14
I_CARGO, I_COMP, I_TIPO, I_NUM, I_VOTOS = 17, 23, 28, 29, 31


def secoes_uf(zip_path):
    """chave -> {comp, validos, v13, v22}."""
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
            r = sec[k] = {"comp": int(c[I_COMP] or 0), "validos": 0, "v13": 0, "v22": 0}
        if c[I_TIPO] == "Nominal":
            v = int(c[I_VOTOS] or 0)
            r["validos"] += v
            if c[I_NUM] == "13":
                r["v13"] += v
            elif c[I_NUM] == "22":
                r["v22"] += v
    return sec


def mad_z(valores):
    """z robusto por mediana/MAD. Retorna (mediana, mad, funcao_z)."""
    med = statistics.median(valores)
    mad = statistics.median([abs(v - med) for v in valores]) or 1e-9
    return med, mad, lambda x: 0.6745 * (x - med) / mad


def analisar_uf(uf, raw):
    z1 = os.path.join(raw, f"bweb_1t_{uf}.zip")
    z2 = os.path.join(raw, f"bweb_2t_{uf}.zip")
    if not (os.path.exists(z1) and os.path.exists(z2)):
        return {"uf": uf, "status": "ZIP_AUSENTE"}
    s1, s2 = secoes_uf(z1), secoes_uf(z2)
    comuns = set(s1) & set(s2)
    swings = []
    detalhe = []
    for k in comuns:
        a, b = s1[k], s2[k]
        if a["validos"] < 10 or b["validos"] < 10:
            continue  # seções minúsculas distorcem share; fora da triagem
        sh1 = a["v13"] / a["validos"]
        sh2 = b["v13"] / b["validos"]
        swing = 100 * (sh2 - sh1)  # p.p. de ganho do nº13 entre turnos
        swings.append(swing)
        detalhe.append((k, swing, b["validos"]))
    if len(swings) < 30:
        return {"uf": uf, "status": "POUCAS_SECOES", "pareadas": len(comuns)}
    med, mad, z = mad_z(swings)
    outliers = sorted(detalhe, key=lambda t: -abs(z(t[1])))[:15]
    return {
        "uf": uf, "status": "OK",
        "secoes1t": len(s1), "secoes2t": len(s2), "pareadas": len(comuns),
        "usadas": len(swings),
        "swingMediano_pp": round(med, 3),
        "swingMedio_pp": round(statistics.fmean(swings), 3),
        "swingDesvio_pp": round(statistics.pstdev(swings), 3),
        "mad_pp": round(mad, 3),
        "outliers": [
            {"secao": "-".join(k), "swing_pp": round(sw, 2),
             "zRobusto": round(z(sw), 2), "validos2t": vv}
            for k, sw, vv in outliers
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ufs", default="AC")
    ap.add_argument("--raw", default="/root/auditoria-raw")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    out = []
    for uf in [u.strip().upper() for u in args.ufs.split(",") if u.strip()]:
        print(f"analisando {uf}...", flush=True)
        r = analisar_uf(uf, args.raw)
        if r.get("status") == "OK":
            print(f"  pareadas={r['pareadas']} swing_med={r['swingMediano_pp']}pp "
                  f"desvio={r['swingDesvio_pp']}pp", flush=True)
        else:
            print(f"  {r['status']}", flush=True)
        out.append(r)
    saida = os.path.join(args.out, "secoes-turnos.json")
    with open(saida, "w", encoding="utf-8") as fh:
        json.dump({"geradoDe": "BU bruto 1T x 2T por seção (Presidente); swing = Δ share nº13 (p.p.)",
                   "nota": "Outlier = triagem por MAD, não prova de irregularidade.",
                   "ufs": out}, fh, ensure_ascii=False, indent=1)
    print(f"escrito {saida}")


if __name__ == "__main__":
    main()
