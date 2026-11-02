# Etapa 7 — Pesquisas eleitorais (PesqEle 2026)

**Fonte:** `pesquisas-eleitorais-2026` (CKAN TSE), CSV de registros por UF.

## O que o PesqEle fornece (OBSERVED)

- **1.404 pesquisas presidenciais** registradas em 2026, de **141 institutos**.
- Período de campo (DT_FIM): **11/01/2026 a 24/10/2026** (véspera do 2º turno).
- Campos: empresa, CNPJ, cargo, datas de início/fim/divulgação, nº de entrevistados,
  estatístico responsável, valor, metodologia e plano amostral (texto).

### Institutos por volume de pesquisas presidenciais (top 12)

| Pesquisas | Instituto |
|---:|---|
| 234 | Instituto Verità |
| 116 | Real Time Mídia |
| 111 | Quaest |
| 106 | AtlasIntel |
| 61 | Datafolha |
| 43 | 100% Cidades |
| 33 | DataTrends |
| 30 | Instituto Paraná |
| 28 | Instituto França |
| 25 | SETA |
| 21 | Nexus |
| 21 | Vox Brasil |

## Lacuna declarada (honestidade metodológica — Seção 7)

O PesqEle traz os **registros** das pesquisas, mas **não os percentuais de intenção de
voto** em formato estruturado (estão nos questionários em PDF). Portanto:

- É possível documentar **quem pesquisou, quando, com que amostra e cobertura**.
- **Não** é possível calcular, apenas com estes dados, o **erro absoluto médio, RMSE,
  viés direcional ou erro na diferença** entre candidatos de cada instituto — isso
  exigiria extrair os percentuais dos PDFs de questionário (não feito).

Conforme o protocolo: **não se inventa um ranking de acurácia** sem a base comparável.
Entrega-se o que a evidência sustenta (volume e cobertura) e declara-se a lacuna.

## Observação de interpretação

Divergência entre pesquisa e resultado motiva investigação **metodológica** (amostra,
ponderação, não resposta, indecisos, comparecimento), não é, por si, evidência de
manipulação da votação. O resultado oficial do 2º turno (válidos) foi Lula 51,79% ×
Bolsonaro 48,21% — a comparação com cada pesquisa final fica pendente da extração dos
percentuais.


## Reta final (última semana antes do 2º turno)

72 pesquisas presidenciais de 36 institutos com trabalho de campo encerrado em 18–24/10/2026. Maiores volumes na reta final: Instituto França (8), AtlasIntel (8), Verità (8), Datafolha (4), DataTrends (3), Quaest (3), PoderData (3).

## Pendência

- Extrair percentuais das pesquisas finais (últimos dias de campo) para computar acurácia
  por instituto e o erro na margem.
