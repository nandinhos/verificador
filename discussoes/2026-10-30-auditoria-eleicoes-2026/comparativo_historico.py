#!/usr/bin/env python3
"""Consolida 4 eleições (2014,2018,2022,2026) e calcula métricas comparativas.

- Adiciona 2026 ao histórico a partir de por-uf.json (agregado nacional).
- Para cada ciclo: líder do 1T, vencedor do 2T, se houve VIRADA, crescimento %
  de cada finalista (2T/1T), bolo dos eliminados e quanto cada um capturou.
Saída: dados/historico-comparativo.json
"""
import json

HIST = "/var/www/verificador-independente/dados/historico-presidente.json"
PORUF = "/var/www/verificador-independente/dados/por-uf.json"
OUT = "/var/www/verificador-independente/dados/historico-comparativo.json"

d = json.load(open(HIST))

# --- adicionar 2026 do por-uf.json (soma nacional) ---
p = json.load(open(PORUF))
t1 = {"v13": 0, "v22": 0, "validos": 0}
t2 = {"v13": 0, "v22": 0, "validos": 0}
for r in p.values():
    if r.get("t1"):
        t1["v13"] += r["t1"]["v13"]; t1["v22"] += r["t1"]["v22"]; t1["validos"] += r["t1"]["validos"]
    if r.get("t2"):
        t2["v13"] += r["t2"]["v13"]; t2["v22"] += r["t2"]["v22"]; t2["validos"] += r["t2"]["validos"]
d["2026"] = {
    "t1": {"validos": t1["validos"], "cands": {
        "22": {"nome": "FLAVIO BOLSONARO", "votos": t1["v22"], "pct": round(100 * t1["v22"] / t1["validos"], 2)},
        "13": {"nome": "LULA", "votos": t1["v13"], "pct": round(100 * t1["v13"] / t1["validos"], 2)}}},
    "t2": {"validos": t2["validos"], "cands": {
        "13": {"nome": "LULA", "votos": t2["v13"], "pct": round(100 * t2["v13"] / t2["validos"], 2)},
        "22": {"nome": "FLAVIO BOLSONARO", "votos": t2["v22"], "pct": round(100 * t2["v22"] / t2["validos"], 2)}}},
    "finalistas": ["13", "22"],
}

comp = {}
for ano in sorted(d):
    r = d[ano]
    if "t1" not in r or "t2" not in r:
        continue
    c1, c2 = r["t1"]["cands"], r["t2"]["cands"]
    fin = r["finalistas"]
    # líder do 1T (entre todos) e vencedor do 2T
    lider1 = max(c1, key=lambda n: c1[n]["votos"])
    venc2 = max(c2, key=lambda n: c2[n]["votos"])
    virada = lider1 != venc2
    # crescimento % de cada finalista
    cresc = {}
    for n in fin:
        v1 = c1.get(n, {}).get("votos", 0)
        v2 = c2.get(n, {}).get("votos", 0)
        cresc[n] = {"nome": c2.get(n, c1.get(n, {})).get("nome", n),
                    "v1": v1, "v2": v2,
                    "crescPct": round(100 * (v2 - v1) / v1, 2) if v1 else None,
                    "pct1": c1.get(n, {}).get("pct"), "pct2": c2.get(n, {}).get("pct")}
    # bolo dos eliminados no 1T = válidos 1T - soma finalistas 1T
    bolo = r["t1"]["validos"] - sum(c1.get(n, {}).get("votos", 0) for n in fin)
    ganho = {n: cresc[n]["v2"] - cresc[n]["v1"] for n in fin}
    comp[ano] = {
        "lider1T": {"num": lider1, "nome": c1[lider1]["nome"], "pct": c1[lider1]["pct"]},
        "vencedor2T": {"num": venc2, "nome": c2[venc2]["nome"], "pct": c2[venc2]["pct"]},
        "houveVirada": virada,
        "crescimento": cresc,
        "boloEliminados": bolo,
        "ganho2T": ganho,
    }

json.dump({"geradoDe": "Comparativo das 4 ultimas eleicoes presidenciais (TSE)", "ciclos": comp},
          open(OUT, "w"), ensure_ascii=False, indent=1)

print(f"{'ANO':5} {'LÍDER 1T':18} {'VENCEU 2T':18} VIRADA?  cresc_venc2T")
for ano in sorted(comp):
    c = comp[ano]
    vn = c["vencedor2T"]["num"]
    cv = c["crescimento"].get(vn, {}).get("crescPct")
    cl = c["crescimento"].get(c["lider1T"]["num"], {}).get("crescPct")
    print(f"{ano:5} {c['lider1T']['nome'][:18]:18} {c['vencedor2T']['nome'][:18]:18} "
          f"{'SIM' if c['houveVirada'] else 'não':7} venc:{cv}% lider1T:{cl}%")
