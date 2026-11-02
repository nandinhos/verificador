#!/usr/bin/env python3
"""Agrega votos nacionais de Presidente por turno/candidato (eleições históricas).

Lê votacao_candidato_munzona_{ano}.zip (todos os CSVs por UF), soma QT_VOTOS_NOMINAIS
do cargo Presidente por turno e candidato. Saída acumulada em dados/historico-presidente.json.

Uso: python3 historico.py --ano 2022
"""
import argparse
import csv
import io
import json
import os
import zipfile

I_TURNO, I_CARGO, I_NUM, I_NOME, I_VOTOS = 5, 17, 19, 21, 45
RAW = "/root/auditoria-raw"
OUT = "/var/www/verificador-independente/dados/historico-presidente.json"


I_VOTOS_VAL = 47  # QT_VOTOS_NOMINAIS_VALIDOS (evita dupla contagem por destinação/trânsito)


def agrega(zip_path):
    import time
    z = zipfile.ZipFile(zip_path)
    import re
    # Presidente só existe nos agregados nacionais. _BR.csv tem apenas presidente
    # (rápido). _BRASIL.csv é o mesmo dado + outros cargos. Usamos só _BR.csv.
    csvs = [n for n in z.namelist() if re.search(r"_BR\.csv$", n, re.I)]
    if not csvs:  # fallback: alguns anos usam _BRASIL
        csvs = [n for n in z.namelist() if re.search(r"_BRASIL\.csv$", n, re.I)]
    dados = {"1": {}, "2": {}}
    t0 = time.time(); lidas = 0
    for idx, nome in enumerate(csvs, 1):
        fh = io.TextIOWrapper(z.open(nome), encoding="latin-1", newline="")
        rd = csv.reader(fh, delimiter=";", quotechar='"')
        hdr = next(rd)
        col = {c: i for i, c in enumerate(hdr)}
        iT, iC, iN, iNo = col["NR_TURNO"], col["DS_CARGO"], col["NR_CANDIDATO"], col["NM_URNA_CANDIDATO"]
        # votos: prefere NOMINAIS_VALIDOS; cai para NOMINAIS (layouts antigos)
        iV = col.get("QT_VOTOS_NOMINAIS_VALIDOS", col.get("QT_VOTOS_NOMINAIS"))
        mx = max(iT, iC, iN, iNo, iV)
        for row in rd:
            lidas += 1
            if lidas % 2_000_000 == 0:
                print(f"    [{idx}/{len(csvs)}] {lidas:,} linhas, {lidas/(time.time()-t0):,.0f} l/s", flush=True)
            if len(row) <= mx or row[iC] != "Presidente":
                continue
            t = row[iT]
            if t not in dados:
                continue
            d = dados[t].setdefault(row[iN], {"nome": row[iNo], "votos": 0})
            try:
                d["votos"] += int(row[iV] or 0)
            except ValueError:
                pass
        print(f"    CSV {idx}/{len(csvs)} ok ({nome.split('/')[-1]})", flush=True)
    print(f"    FIM: {lidas:,} linhas em {time.time()-t0:.0f}s", flush=True)
    return dados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ano", required=True)
    args = ap.parse_args()
    zp = os.path.join(RAW, f"vcmz_{args.ano}.zip")
    if not os.path.exists(zp):
        print(f"ZIP {zp} ausente"); return
    dados = agrega(zp)
    # top-2 do 2º turno (ou do 1º se não houver 2º)
    base = dados["2"] if dados["2"] else dados["1"]
    finalistas = sorted(base, key=lambda n: -base[n]["votos"])[:2]
    saida = {}
    if os.path.exists(OUT):
        saida = json.load(open(OUT))
    reg = {}
    for t in ("1", "2"):
        if not dados[t]:
            continue
        tot = sum(v["votos"] for v in dados[t].values())
        reg[f"t{t}"] = {"validos": tot,
                        "cands": {n: {"nome": dados[t][n]["nome"], "votos": dados[t][n]["votos"],
                                      "pct": round(100 * dados[t][n]["votos"] / tot, 2)}
                                  for n in dados[t]}}
    reg["finalistas"] = finalistas
    saida[args.ano] = reg
    json.dump(saida, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"{args.ano} finalistas={finalistas}")
    for t in ("1", "2"):
        if f"t{t}" in reg:
            for n in finalistas:
                c = reg[f"t{t}"]["cands"].get(n)
                if c:
                    print(f"  {t}T nº{n} {c['nome'][:20]:20} {c['votos']:>12,} ({c['pct']}%)")


if __name__ == "__main__":
    main()
