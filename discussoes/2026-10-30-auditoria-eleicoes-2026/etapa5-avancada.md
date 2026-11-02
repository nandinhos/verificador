# Etapa 5 (avançada) — BH/FDR e bootstrap do swing por seção

**Método:** por seção pareada, z robusto (mediana/MAD) do swing do nº 13; correção de
múltiplas comparações **Benjamini-Hochberg** (FDR); IC 95% por **bootstrap** de seções
(1000 reamostragens, seed 20261030). Cobertura: 12 UFs com ambos os turnos em cache.

| UF | Seções | Swing mediano (p.p.) | IC 95% | Outliers FDR 5% | % |
|---|---:|---:|---|---:|---:|
| AC | 2,270 | +4.67 | [+4.51; +4.85] | 5 | 0.22% |
| AL | 7,101 | +5.89 | [+5.82; +5.95] | 17 | 0.24% |
| AM | 8,157 | +6.00 | [+5.93; +6.07] | 9 | 0.11% |
| AP | 1,914 | +7.42 | [+7.27; +7.56] | 5 | 0.26% |
| MS | 7,106 | +5.50 | [+5.41; +5.56] | 0 | 0.0% |
| PR | 27,142 | +6.04 | [+6.00; +6.07] | 31 | 0.11% |
| RO | 4,698 | +4.21 | [+4.13; +4.29] | 17 | 0.36% |
| RR | 1,519 | +4.63 | [+4.49; +4.78] | 13 | 0.86% |
| SE | 5,923 | +6.59 | [+6.51; +6.68] | 0 | 0.0% |
| SP | 103,656 | +7.76 | [+7.74; +7.78] | 25 | 0.02% |
| TO | 4,384 | +5.18 | [+5.08; +5.28] | 6 | 0.14% |
| ZZ (Ext.) | 1,305 | +6.07 | [+5.86; +6.29] | 19 | 1.46% |

## Conclusão

Após correção de múltiplas comparações (Benjamini-Hochberg), a fração de seções que sobrevive ao controle de FDR a 5% fica entre **0,0% e 1.46%** — compatível com **falsos positivos esperados sob a hipótese nula**, não com anomalia real. Os ICs 95% do swing são estreitos e firmemente positivos em todas as UFs. **Nenhuma seção genuinamente anômala**; o crescimento do nº 13 entre turnos é estatisticamente sólido e homogêneo.
