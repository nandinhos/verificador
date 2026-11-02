# Qualidade — Testes, Dígitos Calibrados e Assinatura Digital

## 1. Suite de testes automatizados

**Arquivo:** `tests/test_auditoria.py` (stdlib `unittest`, sem dependências).
**Resultado:** **11/11 testes OK** (`Ran 11 tests ... OK`).

Cobre as funções críticas dos scripts com entradas de resultado conhecido:

| Grupo | Testes |
|---|---|
| Benjamini-Hochberg (`bh`) | todos significativos, nenhum, monotonia de q, caso clássico |
| Normal bicaudal (`phi`) | simetria, P(\|Z\|>1,96)≈0,05 |
| Diferença-em-diferenças (`did`) | DiD nulo sem efeito; DiD = +10 p.p. com efeito injetado |
| MAD/z robusto (`mad_z`) | mediana no centro; outlier com \|z\|>3 |
| **Identidade contábil (dados reais)** | comparecimento = válidos+brancos+nulos em **todas** as seções de AC 2T (0 violações) |

O teste de identidade contábil roda sobre o BU real e **falharia se houvesse corrupção de
parsing ou de dados** — é a salvaguarda de integridade do pipeline.

## 2. Teste de dígitos CALIBRADO

**Arquivo:** `scripts/teste_digitos.py`. **Piloto:** SP 2T (103 mil seções).

Conforme o protocolo (só usar dígitos se a distribuição esperada for justificada e os
falsos positivos calibrados):

- **Benford do 1º dígito NÃO é usado** — votos por seção têm tamanho limitado (centenas),
  a distribuição não é escala-invariante; Benford geraria falsos alarmes. Declarado.
- **Último dígito** (qui-quadrado vs. uniforme 0-9, só contagens ≥10):

| Candidato | Seções | χ² | Crítico (9 g.l., α=5%) | Rejeita uniforme? | FPR simulada |
|---|---:|---:|---:|:---:|---:|
| nº 13 | 103.649 | 8,63 | 16,92 | não | 0,04 |
| nº 22 | 103.612 | 7,65 | 16,92 | não | 0,05 |

- **Calibração por simulação:** 200 eleições sintéticas sob mecanismo binomial **sem
  fraude** produziram taxa de rejeição de **0,04–0,05** — igual ao α=5% nominal. O teste
  está **bem calibrado** (nem super-sensível nem cego).

**Conclusão:** os últimos dígitos são compatíveis com uniforme; nenhum sinal anômalo.
Resultado defensável porque o teste foi calibrado, não aplicado cegamente.

## 3. Assinatura digital dos arquivos de urna

**Fonte:** `resultados-2026-arquivos-transmitidos-para-totalizacao` (pacote `arqurnatot`,
com `.dat`=BU/RDV/imgBU, `.vsc`=assinatura, `.jez`=log). **Piloto:** RR 1T.

| | n |
|---|---:|
| Urnas/seções | 1.519 |
| Assinaturas `.vsc` | 1.519 |
| Logs `.jez` | 1.519 |
| Arquivos `.dat` | 4.557 (= 1.519 × 3) |
| Cobertura de assinatura | **100% (1 `.vsc` por urna)** |

- O `.vsc` começa com `30 82…` = **ASN.1 DER SEQUENCE** (envelope criptográfico VSCMR do
  TSE) — confirma **assinatura digital estruturada**, não mero hash.
- O total de assinaturas (1.519) **coincide** com as seções de RR na Etapa 6 (CEFT) —
  verificação cruzada de cobertura.

**Limitação (blocker de ferramenta, não de dados):** a validação criptográfica completa
da cadeia (assinatura × certificado raiz do TSE) exige o parser VSCMR e os certificados
oficiais, fora do escopo stdlib. Constatados: presença por urna, integridade estrutural
ASN.1 e cobertura total. O briefing distingue hash (já verificado, sha512) de assinatura
validada — aqui avançamos até a **presença e estrutura** da assinatura.
