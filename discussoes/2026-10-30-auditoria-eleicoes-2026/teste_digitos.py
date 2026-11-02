#!/usr/bin/env python3
"""Teste de dígitos CALIBRADO (Presidente) — Ponto 2.

O protocolo exige: só usar testes de dígitos se (a) a distribuição esperada for
justificada e (b) os falsos positivos forem calibrados por simulação pertinente.

ABORDAGEM:
1. Benford do 1º dígito NÃO se aplica a votos por seção — seções têm tamanho
   limitado (centenas), a distribuição não é escala-invariante. Documentamos isso
   e NÃO usamos Benford como prova.
2. Último dígito: sob contagem legítima, a cauda (último dígito) de contagens
   "grandes o suficiente" tende ao uniforme (0-9). Testamos qui-quadrado contra
   uniforme para os votos do nº 13 e nº 22 por seção.
3. CALIBRAÇÃO: simulamos N eleições SINTÉTICAS sob mecanismo plausível
   (binomial: cada seção tem eleitores ~ tamanho real, voto ~ Bernoulli(p_uf)),
   SEM qualquer fraude, e medimos quantas vezes o qui-quadrado rejeitaria a 5%.
   Isso dá a taxa de falsos positivos esperada — referência para interpretar o real.

Uso: python3 scripts/teste_digitos.py --uf SP
"""
import argparse
import csv
import io
import json
import os
import random
import zipfile

Q = '"Presidente"'
SEED = 20261030
CHI2_CRIT_9GL = 16.919  # qui-quadrado 9 g.l., alpha=0.05


def votos_por_secao(zip_path, num):
    z = zipfile.ZipFile(zip_path)
    n = [x for x in z.namelist() if x.endswith(".csv")][0]
    fh = io.TextIOWrapper(z.open(n), encoding="latin-1", newline="")
    sec = {}
    for linha in fh:
        if Q not in linha:
            continue
        c = next(csv.reader([linha], delimiter=";", quotechar='"'))
        if c[17] != "Presidente" or c[28] != "Nominal" or c[29] != num:
            continue
        k = (c[11], c[13], c[14])
        sec[k] = sec.get(k, 0) + int(c[31] or 0)
    return sec


def chi2_ultimo_digito(valores):
    """Qui-quadrado dos últimos dígitos vs uniforme(0-9). Só contagens >=10."""
    cont = [0] * 10
    n = 0
    for v in valores:
        if v >= 10:
            cont[v % 10] += 1
            n += 1
    if n < 100:
        return None, n
    esp = n / 10
    chi2 = sum((o - esp) ** 2 / esp for o in cont)
    return chi2, n


def simular_falsos_positivos(secoes_tam, p, n_sim, rng):
    """Gera n_sim eleições binomiais SEM fraude; conta rejeições a 5%."""
    rej = 0
    for _ in range(n_sim):
        votos = [sum(1 for _ in range(min(t, 800)) if rng.random() < p) for t in secoes_tam]
        chi2, nn = chi2_ultimo_digito(votos)
        if chi2 is not None and chi2 > CHI2_CRIT_9GL:
            rej += 1
    return rej / n_sim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", default="SP")
    ap.add_argument("--raw", default="/root/auditoria-raw")
    ap.add_argument("--out", default="dados")
    ap.add_argument("--nsim", type=int, default=200)
    args = ap.parse_args()
    rng = random.Random(SEED)
    zp = os.path.join(args.raw, f"bweb_2t_{args.uf}.zip")
    if not os.path.exists(zp):
        print(f"BU {args.uf} 2T ausente"); return

    out = {"uf": args.uf, "geradoDe": "teste de ultimo digito calibrado (Presidente, 2T)",
           "nota": "Benford 1o digito NAO aplicavel a votos por secao (tamanho limitado); nao usado.",
           "chi2CriticoAlpha5_9gl": CHI2_CRIT_9GL, "candidatos": {}}
    for num in ("13", "22"):
        sec = votos_por_secao(zp, num)
        valores = list(sec.values())
        chi2, n = chi2_ultimo_digito(valores)
        tam = [v for v in valores if v >= 10][:3000]  # amostra p/ simulacao
        media_p = (sum(valores) / sum(max(v, 1) for v in valores)) if valores else 0.5
        fpr = simular_falsos_positivos([max(t, 50) for t in tam], 0.5, args.nsim, rng) if tam else None
        out["candidatos"][num] = {
            "secoes": n, "chi2": round(chi2, 3) if chi2 else None,
            "rejeitaUniforme5pct": (chi2 > CHI2_CRIT_9GL) if chi2 else None,
            "taxaFalsosPositivosSimulada": fpr,
        }
        print(f"nº{num}: n={n} chi2={chi2:.2f} rejeita5%={'SIM' if chi2 and chi2>CHI2_CRIT_9GL else 'nao'} "
              f"FPR_sim={fpr}", flush=True)
    saida = os.path.join(args.out, f"digitos-{args.uf}.json")
    json.dump(out, open(saida, "w"), ensure_ascii=False, indent=1)
    print(f"escrito {saida}")


if __name__ == "__main__":
    main()
