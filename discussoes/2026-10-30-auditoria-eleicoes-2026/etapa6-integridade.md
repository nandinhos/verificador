# Etapa 6 — Integridade de transmissão (urnas esperadas × efetivadas)

**Fonte:** `resultados-2026-correspondencias-esperadas-e-efetivadas-2-turno` (CESP/CEFT), TSE.
**Método:** cruzamento por município+zona+seção, 2º turno. **Cobertura: 28 federações.**
**Código:** `scripts/etapa6_correspondencia.py`.

## Resultado nacional

| | n |
|---|---:|
| Federações com correspondência 100% completa | **27 / 28** |
| Urnas que não transmitiram (nacional) | **0** |
| Exceção | ZZ (Exterior): 29 urnas "inesperadas" |

Toda urna esperada no território nacional transmitiu seu boletim — **zero faltantes**.
Os totais por UF coincidem com as seções da conciliação de votos (verificação cruzada).

### ZZ (Exterior)

1.310 efetivadas vs 1.281 esperadas → 29 "inesperadas". Ligado ao AUD-002
(particularidade dos postos consulares). Não é anomalia de transmissão no território;
votos válidos conciliam.

## Nota técnica

Para PA e PE, o recurso rotulado "CSV" mais recente no catálogo era, na verdade, um
arquivo de hash (158 bytes); corrigido filtrando por extensão `.zip`. Ambos conciliam 100%.

## Fechamento tardio (horário de encerramento)

A maioria esmagadora das seções fecha às 17h (Brasília); fechamento tardio (>18h) é raro
e concentrado em SP e RJ. Teste DiD associado na Etapa 5.

## Limitações

- Logs do GEDAI e arquivos transmitidos para totalização (disponíveis no CKAN) permitiriam
  aprofundar — pendente. Sem reconstrução de escolha individual (RDV não é cronológico).
