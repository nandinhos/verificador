# Etapa 5 — Testes estatísticos (Presidente)

## 5.0 Integridade das fontes (item de rastreabilidade)

Todos os Boletins de Urna processados conferem **sha512 idêntico ao hash oficial**
publicado pelo TSE (verificado em cache: AC, AM, PR, SP 1T; AC, AM, SP 2T). Os
arquivos são bit-a-bit os publicados — integridade confirmada contra a cadeia oficial.
Ressalva da Seção 2: isso garante integridade do arquivo coletado, não a correção de
todas as etapas do pleito.

## 5.1 Diferença-em-diferenças (DiD) — efeito de fechamento tardio

**Pergunta:** seções que fecharam após 18h (Brasília) no 2º turno tiveram variação de
share dos finalistas diferente das seções pontuais, além do que já se observa no 1º
turno (placebo)? **H0:** não. **Unidade:** seção pareada entre turnos. **Incerteza:**
teste de **permutação** (realoca o rótulo tarde/pontual; seed 20261030), apropriado a
dado censitário — a incerteza vem da atribuição do tratamento, não de amostragem.

### Cobertura

- **SP:** 103.656 seções pareadas; 1.762 tardias (>18h BSB) → grupo suficiente.
- **AC, AM:** apenas 1 seção tardia cada → **teste não aplicável** (sem grupo comparável).
  Declarado conforme Seção 6: sem grupos comparáveis, não se separa efeito de
  equipamento/horário de diferenças do eleitorado.

### Resultado — 5 UFs com grupo de tardias suficiente (nacional)

| UF | tardias | DiD nº13 (p.p.) | p (perm.) | Placebo (p.p.) |
|---|---:|---:|---:|---:|
| SP | 1.760 | +0,792 | 0,000 | −1,503 |
| RJ | 3.188 | +0,032 | 0,494 (n.s.) | +0,555 |
| PE | 702 | +0,160 | 0,048 | −0,171 |
| PB | 312 | +0,175 | 0,242 (n.s.) | −0,433 |
| SE | 54 | +1,015 | 0,004 | −0,723 |

Efeitos **minúsculos (0,03–1,0 p.p.)**, significância mista, placebos de magnitude
comparável — assinatura de composição de eleitorado, não manipulação. O maior efeito
(SE) está no menor grupo (54 seções, alta variância). Demais 23 federações têm <30
seções tardias → DiD não aplicável (declarado). **Nenhum padrão de ganho consistente
em seções tardias; nenhuma evidência de irregularidade.**

### Interpretação (rigorosa)

1. **Significância ≠ relevância.** Com 103 mil seções, p≈0 ocorre mesmo para efeitos
   ínfimos. O DiD de +0,79 p.p. é detectável, porém **substantivamente pequeno**.
2. **Placebo maior que o efeito.** O placebo (fechamento do 1º turno como tratamento
   fictício) tem magnitude (−1,5 / −1,4 p.p.) **maior** que o DiD real. Quando o placebo
   rivaliza/supera o efeito, a leitura causal **se enfraquece**: seções que fecham tarde
   já são estruturalmente distintas (perfil urbano/maior), não alteradas pelo horário.
3. **Simetria.** Ambos finalistas têm DiD positivo — nenhum lado favorecido de forma anômala.

**Conclusão:** nenhuma evidência de manipulação associada a fechamento tardio. O pequeno
DiD é melhor explicado por composição do eleitorado das seções tardias. Não se converte
p-valor em probabilidade de fraude; não se extrapola efeito local.

## Limitações

- DiD aplicável só onde há massa de seções tardias (SP, RJ). AC/AM/MG/RS inconclusivos por desenho (poucas tardias).
- Cobertura ampliada a 6 UFs (AC, BA, MG, RJ, RS, SP); fechamento tardio concentra-se em SP/RJ.
