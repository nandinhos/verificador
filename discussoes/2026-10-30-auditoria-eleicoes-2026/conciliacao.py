#!/usr/bin/env python3
"""Verificador Independente — conciliação BU bruto x resultado oficial (Presidente).

Para cada UF/turno:
  1. baixa o Boletim de Urna (bweb) do TSE (cache em RAW);
  2. reconstrói, só do cargo Presidente, a soma por seção de:
     votos nominais por número, brancos, nulos, aptos e comparecimento
     (aptos/comparecimento contados UMA vez por seção — repetem por linha de cargo);
  3. baixa o resultado oficial agregado da UF (-u.json) e confronta os totais;
  4. grava diferencas absolutas em JSON.

Classificação epistêmica: diferença 0 => consistência interna da publicação
do TSE (mesmo publicador em dois formatos), NÃO prova independente do pleito.

Uso: python3 conciliacao.py --ufs SP,AC,AM,BA --turnos 1,2 --out <dir>
"""
import argparse
import csv
import io
import json
import os
import sys
import urllib.request
import zipfile

CDN = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/buweb"
CKAN = "https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-2026-boletim-de-urna"
RESULT = "https://resultados.tse.jus.br/oficial/ele2026/{ele}/dados/{uf}/{uf}-c0001-e00{ele}-u.json"
ELE = {1: 6257, 2: 6258}  # Presidente 1T / 2T
UA = {"User-Agent": "Mozilla/5.0 (verificador-independente)"}

# Índices do CSV bweb (mapeados do cabeçalho oficial).
I_TURNO, I_UF, I_MUN, I_ZONA, I_SECAO = 7, 10, 11, 13, 14
I_CARGO, I_APTOS, I_COMP = 17, 22, 23
I_TIPO, I_NUM, I_VOTOS = 28, 29, 31


def _get(url, timeout=600):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)


def url_bu(uf, turno):
    if turno == 1:
        return f"{CDN}/bweb_1t_{uf.upper()}_051020261403.zip"
    cat = json.loads(_get(CKAN, 60).read())
    for r in cat["result"].get("resources", []):
        u = r.get("url") or ""
        if f"_2t_{uf.upper()}_" in u and u.endswith(".zip"):
            return u
    return None


def baixar(uf, turno, rawdir):
    """Retorna (caminho, baixou_agora). baixou_agora=True se não estava em cache."""
    dest = os.path.join(rawdir, f"bweb_{turno}t_{uf.upper()}.zip")
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest, False
    url = url_bu(uf, turno)
    if not url:
        return None, False
    with _get(url) as r, open(dest, "wb") as fh:
        fh.write(r.read())
    return dest, True


def reconstruir(zip_path, label=""):
    """Soma do BU bruto, só Presidente. Retorna agregados da UF.

    Pré-filtra por substring ';Presidente;' antes do parse CSV completo
    (SP tem ~8 GB e 5 cargos; sem o filtro, parsear tudo leva mais de 1h).
    Emite heartbeat de progresso para distinguir 'lento' de 'travado'.
    """
    import time
    z = zipfile.ZipFile(zip_path)
    nome = [n for n in z.namelist() if n.endswith(".csv")][0]
    fh = io.TextIOWrapper(z.open(nome), encoding="latin-1", newline="")
    nominais, brancos, nulos = {}, 0, 0
    secoes = {}  # chave -> (aptos, comparecimento) contados 1x
    lidas = casadas = 0
    t0 = time.time()
    for linha in fh:
        lidas += 1
        if lidas % 2_000_000 == 0:
            dt = time.time() - t0
            print(f"    [{label}] {lidas:,} linhas, {casadas:,} Presidente, "
                  f"{len(secoes):,} secoes, {lidas/dt:,.0f} l/s", flush=True)
        if '"Presidente"' not in linha:
            continue
        campos = next(csv.reader([linha], delimiter=";", quotechar='"'))
        if len(campos) <= I_VOTOS or campos[I_CARGO] != "Presidente":
            continue
        casadas += 1
        chave = (campos[I_MUN], campos[I_ZONA], campos[I_SECAO])
        if chave not in secoes:
            secoes[chave] = (int(campos[I_APTOS] or 0), int(campos[I_COMP] or 0))
        tipo = campos[I_TIPO]
        v = int(campos[I_VOTOS] or 0)
        if tipo == "Nominal":
            nominais[campos[I_NUM]] = nominais.get(campos[I_NUM], 0) + v
        elif tipo == "Branco":
            brancos += v
        elif tipo == "Nulo":
            nulos += v
    print(f"    [{label}] FIM: {lidas:,} linhas, {len(secoes):,} secoes, "
          f"{time.time()-t0:.0f}s", flush=True)
    aptos = sum(a for a, _ in secoes.values())
    comp = sum(c for _, c in secoes.values())
    validos = sum(nominais.values())
    return {
        "secoes": len(secoes), "aptos": aptos, "comparecimento": comp,
        "validos": validos, "brancos": brancos, "nulos": nulos,
        "nominais": nominais,
    }


def oficial(uf, turno):
    ele = ELE[turno]
    u = json.loads(_get(RESULT.format(ele=ele, uf=uf.lower()), 60).read())
    s, e, v = u.get("s", {}), u.get("e", {}), u.get("v", {})
    toi = lambda x: int(str(x or "0").replace(".", "") or 0)
    nominais = {}
    for carg in u.get("carg", []):
        for agr in carg.get("agr", []):
            for par in agr.get("par", []):
                for c in par.get("cand", []):
                    nominais[c.get("n")] = toi(c.get("vap"))
    return {
        "secoes": toi(s.get("ts")), "aptos": toi(e.get("te")),
        "comparecimento": toi(v.get("tv")), "validos": toi(v.get("vv")),
        "brancos": toi(v.get("vb")), "nulos": toi(v.get("vn") or v.get("tvn")),
        "nominais": nominais, "totalizacaoFinal": u.get("tf") == "s",
    }


def conciliar(uf, turno, rawdir, descartar=False):
    zp, baixou = baixar(uf, turno, rawdir)
    if not zp:
        return {"uf": uf, "turno": turno, "status": "BU_INDISPONIVEL"}
    rec = reconstruir(zp, f"{uf} {turno}T")
    ofi = oficial(uf, turno)
    if descartar and baixou:
        try:
            os.remove(zp)
            print(f"    [{uf} {turno}T] ZIP descartado (streaming de disco)", flush=True)
        except OSError:
            pass
    campos = ["secoes", "aptos", "comparecimento", "validos", "brancos", "nulos"]
    difs = {k: rec[k] - ofi[k] for k in campos}
    nums = set(rec["nominais"]) | set(ofi["nominais"])
    dif_cand = {n: rec["nominais"].get(n, 0) - ofi["nominais"].get(n, 0) for n in nums}
    dif_cand = {n: d for n, d in dif_cand.items() if d != 0}
    return {
        "uf": uf, "turno": turno, "status": "OK",
        "totalizacaoFinal": ofi.get("totalizacaoFinal"),
        "reconstruido": {k: rec[k] for k in campos},
        "oficial": {k: ofi[k] for k in campos},
        "diferencaAbsoluta": difs,
        "diferencaPorCandidato": dif_cand,
        "concilia": all(v == 0 for v in difs.values()) and not dif_cand,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ufs", default="SP,AC,AM,BA")
    ap.add_argument("--turnos", default="1,2")
    ap.add_argument("--raw", default="/root/auditoria-raw")
    ap.add_argument("--out", default=".")
    ap.add_argument("--descartar", action="store_true", help="remove ZIP recém-baixado após conciliar")
    args = ap.parse_args()
    os.makedirs(args.raw, exist_ok=True)
    os.makedirs(args.out, exist_ok=True)
    ufs = [x.strip().upper() for x in args.ufs.split(",") if x.strip()]
    turnos = [int(t) for t in args.turnos.split(",")]
    resultados = []
    for t in turnos:
        for uf in ufs:
            print(f"conciliando {uf} {t}T...", flush=True)
            try:
                r = conciliar(uf, t, args.raw, args.descartar)
            except Exception as e:
                r = {"uf": uf, "turno": t, "status": f"ERRO: {e}"}
            resultados.append(r)
            if r.get("status") == "OK":
                tag = "CONCILIA" if r["concilia"] else "DIVERGE"
                print(f"  {tag} dif={r['diferencaAbsoluta']}", flush=True)
    saida = os.path.join(args.out, "conciliacao-resultado.json")
    with open(saida, "w", encoding="utf-8") as fh:
        json.dump({"geradoDe": "BU bruto x resultado oficial TSE (Presidente)",
                   "resultados": resultados}, fh, ensure_ascii=False, indent=1)
    print(f"escrito {saida}")


if __name__ == "__main__":
    main()
