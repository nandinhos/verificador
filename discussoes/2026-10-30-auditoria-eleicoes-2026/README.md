# Auditoria Independente — Eleições 2026 (Presidente)

Investigação reproduzível dos resultados oficiais do TSE (presidencial 2026, 1º e 2º
turnos), publicada em **https://eleicoes.fssdev.com.br/verificador-independente/**
(servida do vps2, diretório persistente fora dos releases do portal).

## Conclusão

Nos dados examinados, **nenhum indício de fraude ou manipulação do resultado**. As
discrepâncias têm explicação documentada; a reversão entre turnos é aritmeticamente
explicada; o teste de fechamento tardio não mostra efeito relevante; a integridade dos
Boletins de Urna confere com o hash oficial (sha512). Limite: concordância BU×oficial
prova consistência interna da publicação do TSE, não a correção de todas as etapas do
pleito. Ver `resumo-executivo.md`.

## Etapas executadas

| Etapa | Arquivo | Síntese |
|---|---|---|
| 2 — Conciliação | `etapa2-conciliacao.md`, `conciliacao.py`, `conciliacao-resultado.json` | 28 federações × 2T; 27 conciliam; AUD-001/002 explicados |
| 4 — Turnos (nacional) | `etapa4-turnos.md`, `turnos.json` | Reversão aritmeticamente explicada; identidades fecham |
| 4-fina — Por seção | `etapa4fina-secoes.md`, `analise_secoes_turnos.py`, `secoes-turnos.json` | Swing homogêneo (6 UFs); sem anomalia |
| 5 — Estatística | `etapa5-estatistica.md`, `etapa5_estatistica.py`, `etapa5-estatistica.json` | DiD fechamento tardio nulo/ínfimo (RJ, SP) |
| 6 — Integridade | `etapa6-integridade.md` | Urnas esperadas = efetivadas (100%, AC) |
| 7 — Pesquisas | `etapa7-pesquisas.md` | 1.404 pesquisas, 141 institutos; acurácia pendente |

## Achados

- **AUD-001:** candidato nº 28 (Leonardo Avalanche, PRTB) no BU mas fora dos válidos
  oficiais (1º turno, todas as UFs) — candidatura indeferida; imaterial.
- **AUD-002:** ZZ/Exterior com ~42-43 seções a menos no BU vs. oficial (válidos conciliam)
  — cobertura do empacotamento do BU do exterior.

## Reprodutibilidade

- Fontes: `resultados.tse.jus.br`, `cdn.tse.jus.br`, `dadosabertos.tse.jus.br`.
- Scripts só com stdlib Python 3; seed fixa (20261030) no teste de permutação.
- Brutos (BU) verificados por sha512 contra o hash oficial do TSE; mantidos fora do
  webroot (`/root/auditoria-raw` no vps2) por volume.
- Execução (exemplo): `python3 conciliacao.py --ufs SP,AC --turnos 1,2 --descartar`.

## Pendências

Escalar Etapas 4-fina/5/6 às 27 UFs; extrair percentuais do PesqEle (acurácia por
instituto); listar nominalmente as ~42 seções do ZZ; conciliar demais cargos; melhorar UI.
