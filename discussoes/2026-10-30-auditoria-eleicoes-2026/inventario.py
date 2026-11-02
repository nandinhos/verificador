#!/usr/bin/env python3
"""Inventário consolidado e verificação de integridade (Presidente).

Para cada federação×turno: registra URL, hash oficial (.sha512). Se o BU está
em cache local, calcula sha512 local e confronta. Saída: dados/inventario.json.
"""
import hashlib
import json
import os
import urllib.request

UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO ZZ".split()
ST = {"1t": "051020261403", "2t": "261020260742"}
BASE = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/buweb/bweb_{t}_{uf}_{s}.zip"
RAW = "/root/auditoria-raw"
UA = {"User-Agent": "Mozilla/5.0"}


def hash_oficial(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url + ".sha512", headers=UA), timeout=30)
        return r.read().decode().split()[0]
    except Exception:
        return None


def sha512_local(path):
    h = hashlib.sha512()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


inv = []
conferem = cache = 0
for uf in UFS:
    for t in ("1t", "2t"):
        url = BASE.format(t=t, uf=uf, s=ST[t])
        of = hash_oficial(url)
        local_path = os.path.join(RAW, f"bweb_{t}_{uf}.zip")
        entry = {"federacao": uf, "turno": t, "url": url, "cargo": "Presidente",
                 "hashOficial": of, "hashLocal": None, "confere": None, "emCache": False}
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            cache += 1
            hl = sha512_local(local_path)
            entry.update(emCache=True, hashLocal=hl, confere=(hl == of))
            if hl == of:
                conferem += 1
            print(f"{uf} {t}: cache, sha512 {'OK' if hl == of else 'DIVERGE'}", flush=True)
        inv.append(entry)

saida = "/var/www/verificador-independente/dados/inventario.json"
json.dump({"geradoDe": "Inventario de BUs (Presidente) com hash oficial x local",
           "resumo": {"total": len(inv), "emCache": cache, "conferem": conferem,
                      "hashOficialPresente": sum(1 for e in inv if e["hashOficial"])},
           "itens": inv}, open(saida, "w"), ensure_ascii=False, indent=1)
print(f"\nhash oficial presente: {sum(1 for e in inv if e['hashOficial'])}/{len(inv)}")
print(f"em cache: {cache} | conferem sha512: {conferem}/{cache}")
print(f"escrito {saida}")
