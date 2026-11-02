# Resumo Executivo — Auditoria Independente das Eleições 2026 (Presidente)

**Data de corte:** 2026-10-30 · **Escopo:** eleição presidencial, 1º e 2º turnos ·
**Fontes:** TSE (resultados.tse.jus.br, cdn.tse.jus.br, dadosabertos.tse.jus.br).
**Reprodutível:** código em `scripts/`, dados em `dados/`, brutos verificados por sha512.

## Conclusão principal

**Nos dados examinados, não há indício de fraude ou manipulação do resultado.** Todas as
discrepâncias encontradas têm explicação documentada (candidatura indeferida; cobertura
do BU no exterior). A reversão entre turnos é aritmeticamente explicada e as identidades
contábeis fecham. Testes estatísticos de fechamento tardio não mostram efeito relevante.

**Limite (declarado):** concordância entre Boletim de Urna e resultado oficial demonstra
**consistência interna da publicação do TSE** — condição necessária, não verificação
independente de todas as etapas do pleito (voto, urna, transmissão física). Ausência de
anomalia detectada não prova inexistência de toda irregularidade possível.

## O que foi verificado (com evidência)

| Etapa | O que | Resultado |
|---|---|---|
| 2 | Conciliação BU × oficial, **28 federações** × 2 turnos (56 execuções) | 27 conciliam; demais explicadas (AUD-001/002) |
| 4 | Comparação 1º×2º turno nacional | Reversão aritmeticamente explicada; identidades fecham |
| 4-fina | Swing por seção — **28 federações (~499 mil seções)** | Swing +4,2 a +9,1 p.p., positivo em TODAS; homogêneo; sem anomalia |
| 5 | DiD fechamento tardio + placebo (**5 UFs**: SP, RJ, PE, PB, SE) | Efeitos minúsculos (0,03–1,0 p.p.), placebo comparável; sem padrão |
| 6 | Correspondência urnas esperadas × efetivadas (**28 federações**) | 27/28 completas; **0 urnas não transmitidas** no país |
| 7 | Registro de pesquisas (PesqEle) | 1.404 pesquisas, 141 institutos; acurácia pendente (lacuna declarada) |
| 5-av | BH/FDR + bootstrap do swing por seção (12 UFs) | 0,0–1,5% sobrevivem ao FDR 5%; ICs estreitos e positivos |
| — | Integridade sha512 (inventário, 39 BUs em cache) | 100% conferem; hash oficial presente 56/56 |

## Tabela de achados

| ID | Achado | Classificação | Magnitude | Confiança | Próxima verificação |
|---|---|---|---|---|---|
| AUD-001 | Candidato nº 28 (Leonardo Avalanche, PRTB) presente no BU, ausente dos válidos oficiais, só no 1º turno, em todas as UFs | Inconsistência de dados por evento documentado (candidatura indeferida) — **não fraude** | ~5,2 mil votos (imaterial; não afeta finalistas) | Alta | Decisão formal de registro (DivulgaCand) |
| AUD-002 | ZZ/Exterior: BU tem ~42-43 seções a menos que o oficial; 1 posto (Trípoli) só no 1T | Inconsistência de cobertura de dados (empacotamento do BU do exterior) — **não anomalia de resultado** | 0 em votos válidos (conciliam) | Média | Detalhamento seção-a-seção do oficial ZZ |

## Resultado oficial (contexto, totalização final)

- 1º turno: Bolsonaro (22) 47,03% × Lula (13) 45,16% — ao 2º turno.
- 2º turno: **Lula (13) 51,79% × Bolsonaro (22) 48,21%** — Lula eleito. 100% das 499.248 seções.

## Qualidade e robustez

- Suite de testes automatizados: 11/11 OK (BH, DiD, phi, mad_z, identidade contábil em dados reais).
- Teste de último dígito calibrado (SP): χ² abaixo do crítico; FPR simulada ≈ 5%. Benford 1º dígito não aplicável (declarado).
- Assinatura digital: 100% das urnas de RR com .vsc (ASN.1/DER); validação de cadeia completa requer ferramenta oficial.

## Testes que NÃO encontraram anomalia (registro, Seção 9)

- Conciliação de votos: 7 campos × 28 federações conciliam (exceto nº 28, explicado).
- Swing por seção (28 federações, ~499 mil seções): positivo e homogêneo em todas; outliers em seções pequenas e bidirecionais.
- DiD fechamento tardio (5 UFs): efeitos 0,03–1,0 p.p., não significativos de forma consistente, placebos comparáveis.
- Completude de transmissão: 0 urnas não transmitidas nacional; 27/28 UFs 100% (ZZ com particularidade consular).
