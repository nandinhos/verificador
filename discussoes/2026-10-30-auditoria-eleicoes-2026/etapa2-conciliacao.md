# Etapa 2 — Conciliação BU bruto × resultado oficial (Presidente)

**Data de corte:** 2026-10-30 · **Escopo:** 27 UFs + ZZ (Exterior, 28ª unidade) ·
1º e 2º turnos = **56 execuções** · **Fonte:** Boletim de Urna (bweb) × resultado
oficial agregado por federação (`-u.json`), ambos do TSE.

## Método

Para cada federação/turno: baixa o BU bruto, reconstrói do zero a soma — só do
cargo Presidente — de votos nominais por candidato, brancos, nulos, aptos e
comparecimento (aptos/comparecimento uma vez por seção), e confronta com os totais
do `-u.json` oficial. Processamento em streaming de disco (`--descartar`): pico de
disco = maior arquivo, não a soma (servidor com 4 GB livres). Código:
`scripts/conciliacao.py` (determinístico, só stdlib).

## Resultado geral

| | n |
|---|---|
| Execuções | 56 |
| Conciliam (diferença zero em todos os campos) | 27 |
| Divergem — padrão nº 28 (1º turno) | 27 |
| Divergem — ZZ/Exterior (distinto) | 2 |
| Erros/indisponível | 0 |

Todos os **2º turnos continentais conciliam perfeitamente**. Os campos seções,
aptos, comparecimento, brancos e nulos conciliam em todas as 54 execuções
continentais; a única diferença continental é nos válidos do candidato nº 28.

## Achado AUD-001 — candidato nº 28, exclusivamente no 1º turno (27/27 UFs)

- **Classificação:** inconsistência de dados **explicada por evento documentado** — não fraude.
- **Evidência:** diferença concentrada no nº 28, só no 1º turno, em **todas as 27 UFs
  continentais** (de +14 em RR a +1.355 em SP; total continental ≈ 5,2 mil votos). O
  2º turno concilia. Na lista oficial os candidatos saltam de 27 para 29 — o nº 28
  **não consta** dos válidos oficiais, mas o BU registra votos digitados nele.
- **Identidade (OBSERVED):** o nº 28 consta no BU como **LEONARDO AVALANCHE**; o dataset consulta_cand 2026 lista **dois** registros no nº 28 (Pablo Marçal e Leonardo Avalanche).
- **Interpretação (INFERRED, confiança média):** nenhum dos dois consta dos válidos oficiais (lista salta 27->29). Consistente com indeferimento/substituição, MAS a situação formal de candidatura NÃO está divulgada no dataset público (CD_SITUACAO=-3, DS=#NE) — não comprovável por essa via.
- **Materialidade:** imaterial; nenhum finalista (13, 22) afetado.
- **Status:** RESOLVIDO quanto à identidade; decisão formal de registro (DivulgaCand) fica como anexo documental.

## Achado AUD-002 — ZZ (Exterior): seções e aptos a menos no BU

- **Evidência:** ZZ 1T → seções −42, aptos −495 (válidos divergem só pelo nº 28, +123);
  ZZ 2T → seções −43, aptos −525, **válidos/brancos/nulos conciliam**. Ou seja, o BU
  bruto do exterior tem menos seções/aptos que o oficial, mas os votos válidos fecham.
- **Interpretação (INFERRED):** seções do exterior cujo BU não entrou no arquivo bweb
  (apuração/totalização por outro meio em alguns postos consulares), embora contabilizadas
  no agregado oficial. **Não** se deve ler como ausência real da seção na totalização.
- **Classificação:** inconsistência de cobertura de dados a investigar (Seção 8); sem
  impacto em votos válidos no 2º turno.
- **Caracterizado (OBSERVED):** BU ZZ 2T tem **1.308 seções** vs **1.351** no oficial (−43), 144 postos/países; válidos conciliam (seções ausentes têm contribuição nula aos válidos).
- **Pendência:** listar exatamente as 43 seções (requer detalhamento por seção do oficial ZZ).

## Notas operacionais (transparência)

- PR 1T e RR 2T falharam por rede transitória na 1ª passada; re-executados com sucesso
  (ambos conferem o padrão esperado). Nenhuma lacuna real de publicação foi confirmada.

## Limite de independência

Concordância BU × agregado demonstra **consistência interna da publicação do TSE** —
condição necessária, não verificação independente de todas as etapas do pleito.
Ausência de divergência não prova a inexistência de toda irregularidade possível.
