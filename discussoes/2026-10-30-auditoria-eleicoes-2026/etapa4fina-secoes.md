# Etapa 4 (fina) — Análise por seção pareada 1º × 2º turno (Presidente)

**Fonte:** Boletim de Urna bruto (bweb) dos dois turnos, pareado por
UF+município+zona+seção. **Métrica:** swing = variação (p.p.) do *share* do nº 13
(Lula) sobre válidos entre turnos, por seção. **Cobertura: 28 federações (nacional).**
**Código:** `scripts/analise_secoes_turnos.py` (determinístico, só stdlib).
Seções com <10 válidos em qualquer turno excluídas.

## Resultado por federação

| UF | Seções pareadas | Swing mediano (p.p.) | Desvio |
|---|---:|---:|---:|
| AC | 2,270 | +4.67 | 3.35 |
| AL | 7,101 | +5.89 | 2.43 |
| AM | 8,157 | +6.00 | 2.86 |
| AP | 1,914 | +7.42 | 2.90 |
| BA | 35,476 | +4.83 | 2.87 |
| CE | 23,765 | +5.50 | 2.69 |
| DF | 6,969 | +7.56 | 2.24 |
| ES | 9,844 | +5.68 | 2.54 |
| GO | 15,686 | +9.08 | 2.96 |
| MA | 18,093 | +5.37 | 2.64 |
| MG | 52,062 | +6.89 | 2.89 |
| MS | 7,106 | +5.50 | 2.53 |
| MT | 8,287 | +4.59 | 2.47 |
| PA | 20,827 | +5.12 | 2.91 |
| PB | 10,712 | +5.90 | 2.44 |
| PE | 21,418 | +5.58 | 2.16 |
| PI | 10,225 | +4.67 | 2.83 |
| PR | 27,142 | +6.04 | 2.53 |
| RJ | 37,675 | +7.32 | 2.37 |
| RN | 8,115 | +5.84 | 2.32 |
| RO | 4,698 | +4.21 | 2.71 |
| RR | 1,519 | +4.63 | 2.56 |
| RS | 27,547 | +6.19 | 2.73 |
| SC | 17,326 | +5.32 | 2.34 |
| SE | 5,923 | +6.59 | 2.53 |
| SP | 103,656 | +7.76 | 2.63 |
| TO | 4,384 | +5.18 | 2.56 |
| ZZ (Exterior) | 1,308 | +6.07 | 3.18 |

**28 federações, 499,205 seções pareadas.** Swing mediano do nº 13 (Lula) entre +4.21 e +9.08 p.p. — **positivo em todas as 28 federações**.

## Leitura

1. **Swing positivo em TODAS as 28 federações** (+4,21 a +9,08 p.p.): Lula cresceu de
   forma difusa em todo o país entre turnos. Nenhuma unidade com padrão invertido.
2. **Homogeneidade alta:** desvios por seção numa faixa estreita (2,16–3,35 p.p.) em
   todas as federações — sem bimodalidade ou cauda de injeção de votos.
3. **Simetria** (verificada no piloto): média ≈ mediana; outliers em seções pequenas e
   bidirecionais → variância amostral, não irregularidade direcional.

## Classificação

**Nenhuma anomalia estrutural detectada** em escala nacional (~499 mil seções). O swing
homogêneo e simétrico é consistente com mudança legítima e difusa de preferência entre
turnos. Swing agregado por seção não infere escolha individual (sem falácia ecológica).
