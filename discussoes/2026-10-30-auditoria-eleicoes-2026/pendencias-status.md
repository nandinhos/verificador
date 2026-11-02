# Status das pendências (Presidente) — execução

| # | Pendência | Status | Observação |
|---|---|---|---|
| 1 | Rótulos de UF no mapa | **CONCLUÍDO** | centroides calculados dos paths SVG; rótulos renderizados |
| 2 | Dispersão margem × swing | **CONCLUÍDO** | SVG com 28 pontos (UF); sem relação sistemática |
| 3 | Interatividade (clique na UF) | **CONCLUÍDO** | clique no mapa destaca linha da tabela |
| 4 | Histograma de swing por seção | **CONCLUÍDO** | SP 103.656 seções, 33 bins; unimodal/simétrico |
| 6 | Acurácia das pesquisas | **PARCIAL (blocker de dados)** | reta final (72 pesq/36 institutos) extraída; percentuais só em PDF não-estruturado — TSE não publica em formato tabular |
| 8 | Listar seções do ZZ | **CONCLUÍDO (corrigido)** | BU 1.308 vs CESP 1.281: BU tem +27, 0 ausentes; o -43 era vs `ts` oficial (1.351), contabilização distinta |
| 9 | Registro formal do nº 28 | **PARCIAL (blocker de dados)** | nº 28 tem 2 registros (Pablo Marçal, Leonardo Avalanche); situação não divulgada no dataset público (CD_SITUACAO=-3, DS=#NE) |
| 10 | Análise espacial/robustez | **CONCLUÍDO** | swing homogêneo; sem cluster anômalo |
| 11 | Correção múltiplas comparações (BH/FDR) | **CONCLUÍDO** | 0,0–1,5% das seções sobrevivem ao FDR 5% (12 UFs) |
| 12 | Bootstrap IC do swing | **CONCLUÍDO** | ICs 95% estreitos e positivos (1000 reamostragens, seed fixa) |
| 13 | Hash de todas as federações | **CONCLUÍDO** | 39/39 em cache conferem; hash oficial 56/56 presente |
| 14 | Inventário consolidado | **CONCLUÍDO** | `dados/inventario.json` |
| 15 | Limite de independência | **PERMANENTE** | declarado em todos os relatórios |

## Blockers de dados (não de esforço)

- **Item 6:** o TSE publica no PesqEle apenas os registros das pesquisas; os percentuais
  de intenção de voto estão em PDFs de questionário não estruturados. Extração confiável
  inviável; não se inventa métrica de acurácia.
- **Item 9:** a situação de deferimento/indeferimento não é divulgada de forma utilizável
  no dataset público (consulta_cand traz CD_SITUACAO=-3). DivulgaCand API retorna 403.

Ambos documentados; nenhuma conclusão da auditoria depende deles.
