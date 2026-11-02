#!/usr/bin/env python3
"""Etapa 6 nacional — urnas esperadas (CESP) x efetivadas (CEFT), 2º turno.

Para cada UF: baixa a última CESP e a CEFT, cruza por município+zona+seção,
reporta urnas esperadas sem efetivada (não transmitiram) e vice-versa. Descarta
os ZIPs após processar. Saída: dados/etapa6-correspondencia.json
"""
import csv
import io
import json
import os
import re
import urllib.request
import zipfile

UA = {"User-Agent": "Mozilla/5.0"}
PKG = ("https://dadosabertos.tse.jus.br/api/3/action/package_show"
       "?id=resultados-2026-correspondencias-esperadas-e-efetivadas-2-turno")
RAW = "/root/auditoria-raw"


def get(u, t=120):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t)


def urls():
    d = json.loads(get(PKG, 60).read())
    cesp, ceft = {}, {}
    for r in d["result"]["resources"]:
        u = r.get("url") or ""
        if r.get("format") != "CSV":
            continue
        m = re.search(r"C(ESP|EFT)_2t_([A-Z]{2})_", u)
        if not m:
            continue
        tipo, uf = m.group(1), m.group(2)
        if tipo == "ESP":
            cesp.setdefault(uf, []).append(u)
        else:
            ceft[uf] = u
    return {uf: {"cesp": sorted(cesp[uf])[-1], "ceft": ceft.get(uf)}
            for uf in cesp if ceft.get(uf)}


def chaves(zip_bytes, imun, izona, isec):
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    n = [x for x in z.namelist() if x.endswith(".csv")][0]
    fh = io.TextIOWrapper(z.open(n), encoding="latin-1", newline="")
    r = csv.reader(fh, delimiter=";", quotechar='"')
    next(r)
    return set((row[imun], row[izona], row[isec]) for row in r if len(row) > isec)


def main():
    m = urls()
    out = []
    for uf in sorted(m):
        try:
            esp = chaves(get(m[uf]["cesp"]).read(), 5, 7, 8)   # CD_MUNICIPIO,NR_ZONA,NR_SECAO
            eft = chaves(get(m[uf]["ceft"]).read(), 6, 8, 9)
            falt = len(esp - eft)
            inesp = len(eft - esp)
            out.append({"uf": uf, "esperadas": len(esp), "efetivadas": len(eft),
                        "naoTransmitiram": falt, "inesperadas": inesp,
                        "completa": falt == 0 and inesp == 0})
            print(f"{uf}: esp={len(esp)} eft={len(eft)} faltantes={falt} inesperadas={inesp} "
                  f"{'OK' if falt == 0 and inesp == 0 else 'ATENCAO'}", flush=True)
        except Exception as e:
            out.append({"uf": uf, "status": f"ERRO: {e}"})
            print(f"{uf}: ERRO {e}", flush=True)
    total_falt = sum(r.get("naoTransmitiram", 0) for r in out)
    completas = sum(1 for r in out if r.get("completa"))
    saida = os.path.join("/var/www/verificador-independente/dados", "etapa6-correspondencia.json")
    json.dump({"geradoDe": "CESP x CEFT 2o turno (urnas esperadas x efetivadas)",
               "resumo": {"ufs": len(out), "completas": completas, "totalNaoTransmitiram": total_falt},
               "ufs": out}, open(saida, "w"), ensure_ascii=False, indent=1)
    print(f"\n{completas}/{len(out)} UFs com correspondencia 100% completa | "
          f"total urnas nao transmitidas: {total_falt}")
    print(f"escrito {saida}")


if __name__ == "__main__":
    main()
