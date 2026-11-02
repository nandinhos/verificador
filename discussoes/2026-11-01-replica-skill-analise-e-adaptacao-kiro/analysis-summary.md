# Sumário Executivo de Engenharia Reversa: `replica-skill`

- **Repositório:** [https://github.com/Jakeschincariol/replica-skill.git](https://github.com/Jakeschincariol/replica-skill.git)
- **Commit Auditado:** `77c9436fb3d18c3d58169efb8caf4fe906b0dc51`
- **Autor:** Jake Schincariol ([opusjake.ai](https://opusjake.ai))
- **Licença:** MIT
- **Ambiente de Auditoria:** Sandbox isolado em `/tmp/repo-analysis-replica`
- **Data da Auditoria:** 2026-11-01

---

## 1. Veredito Geral & Arquitetura Comprovada (`OBSERVED`)

O repositório `replica-skill` implementa uma **esteira completa de 11 habilidades (Skills) especializadas para Claude Code e agentes de IA**, cujo propósito é realizar **engenharia reversa e reconstrução "clean-room" de aplicações SaaS e produtos digitais existentes**, transformando-as em novos produtos comerciais autônomos.

Diferente de geradores de código ingênuos ou scrapers tradicionais, o projeto baseia-se em dois pilares fundamentais:
1. **Engenharia Clean-Room Ética e Legal:** O sistema reconstrói **apenas comportamentos, fluxos de usuário e modelos de dados**, proibindo estritamente a cópia de código proprietário, logotipos, cópias literais ou dados de terceiros.
2. **Engenharia de Software Minimalista & Determinística (Ponytail Mode puro):** Todo o ferramental de auditoria (6 utilitários CLI) foi escrito **exclusivamente com a biblioteca padrão do Python 3.8+**, sem nenhuma dependência externa de pacotes (`no pip install`), sem chamadas de rede externas e com execução determinística em menos de 0.5 segundo.

---

## 2. A Tríade Metodológica: O Pipeline de 11 Etapas

As 11 skills são desenhadas para serem executadas em pipeline sequencial, onde cada etapa consome os artefatos gerados pela etapa anterior no diretório `replica/`:

```
/replica-recon ──► /replica-architect ──► /replica-design ──► /replica-build
      │                                                           │
      ▼                                                           ▼
/replica-deploy ◄── /replica-launch ◄── /replica-brand ◄── /replica-backend
      ▲                                                           │
      │                                                           ▼
      └────────── /replica-entrepreneur ◄── /replica-diff ◄── /replica-test
```

### Detalhamento das Etapas:
1. **`/replica-recon`**: Engenharia reversa superficial e profunda via fontes públicas (telas, fluxos, componentes, `features.csv` e `recon-map.md`).
2. **`/replica-architect`**: Especificação do stack técnico, modelo relacional SQL com constraints e contratos de API (`architecture.md`).
3. **`/replica-design`**: Reconstrução de tokens de design, tipografia, paleta e verificação de conformidade WCAG (`tokens.json` e `contrast.py`).
4. **`/replica-build`**: Implementação das telas e jornadas guiada pelas prioridades do `features.csv`.
5. **`/replica-backend`**: Modelagem de autenticação, banco de dados, webhooks e pagamentos (Stripe).
6. **`/replica-test`**: Elaboração de matriz de testes E2E com Playwright e triagem rigorosa de bugs (`S1/S2` são bloqueantes).
7. **`/replica-diff`**: Medição objetiva de paridade funcional ponderada (`parity.py`) e comparação de layout agnóstica de cor (`imgdiff.py`).
8. **`/replica-entrepreneur`**: Mineração de reviews reais de clientes insatisfeitos com o produto original (`reviews.py`), ranqueando dores e gerando proposta única de valor.
9. **`/replica-brand`**: Rebranding completo (novo nome, cores, voz) e varredura de segurança contra resquícios da marca original (`sweep.py`).
10. **`/replica-launch`**: Criação da landing page, modelo de precificação e validação de regras de publicação de lojas móveis (`listing.py`).
11. **`/replica-deploy`**: Checklist de pré-lançamento (`preflight.md`), configuração DNS (SPF, DKIM, DMARC) e go-live.

---

## 3. Os 6 Utilitários Determinísticos (Python Stdlib)

| Utilitário | Arquivo | Linhas | Algoritmo / Mecânica Central |
|---|---|---|---|
| **Layout Diff** | `replica-diff/imgdiff.py` | 457 | Parser completo de PNG (chunks `IHDR`/`IDAT`/`PLTE` com descompactação via `zlib` e filtros Paeth) + detector de bordas de gradiente em grid para comparar layouts ignorando variações de cores. |
| **Parity Scorer** | `replica-diff/parity.py` | 229 | Matriz de paridade ponderada (Must: 3, Should: 2, Could: 1). Permite compor 80% do score de features com 20% do score visual do `imgdiff`. |
| **Brand Sweep** | `replica-brand/sweep.py` | 178 | Varredura regex no codebase por nomes, domínios e valores hexadecimais de cor do concorrente (exclui `.git`, `node_modules` e caches). |
| **Contrast Checker** | `replica-design/contrast.py` | 158 | Cálculo de luminância relativa e proporções de contraste WCAG 2.1 (mínimo 4.5:1 para texto normal, 3:1 para grande). |
| **Review Feedback** | `replica-entrepreneur/reviews.py` | 312 | Ranqueamento de queixas de usuários com decay temporal (>18 meses = peso pela metade), links obrigatórios e extração exata de citações. |
| **Store Linter** | `replica-launch/listing.py` | 243 | Validador de restrições de lojas (tamanho de títulos, contagem grapheme de emojis, bloqueio de superlativos como "#1" e detecção do concorrente). |

---

## 4. Evidência de Testes (`OBSERVED`)

A suíte canônica do repositório foi executada de forma não-mascarada no ambiente sandbox:

- **Comando:** `python3 -m unittest discover -s tests -v`
- **Exit Code:** `0`
- **Resultados:** `Ran 57 tests in 0.456s - OK`
- **Distribuição dos Testes:**
  - `test_contrast_listing.py`: 12 testes (contraste de tokens, limites de loja, emojis).
  - `test_imgdiff.py`: 14 testes (leitura e escrita de PNG, filtros Paeth, escala de cinza, gradiente de borda, redimensionamento).
  - `test_parity.py`: 10 testes (cálculo ponderado, tratamento de erros, mesclagem visual).
  - `test_repo.py`: 5 testes (integridade de frontmatter das 11 skills, conformidade do README, validação de em-dashes).
  - `test_reviews.py`: 11 testes (citações exatas, ponderação de notas, penalidade de tempo, agrupamento de temas).
  - `test_sweep.py`: 5 testes (limpeza de marca, correspondência de hex curto/longo, exclusão de diretórios de build).

---

## 5. Avaliação Crítica & Maturidade de Engenharia

### Pontos Fortes Notáveis:
1. **Zero Bloat & Dependências Nulas:** Nenhuma dependência externa (`pip install`) foi necessária para toda a suíte de ferramentas complexas (incluindo processamento de imagens PNG).
2. **Alta Fidelidade Epistemológica:** O utilitário `reviews.py` descarta qualquer avaliação sem link real e proíbe IA de parafrasear ou inventar queixas.
3. **Guardrails Jurídicos e de Rebrand:** `sweep.py` impede que o desenvolvedor cometa a imprudência de subir um clone com nomes de variáveis internas ou cores que identifiquem a aplicação original.
4. **Respeito aos Limites Cognitivos:** A separação em 11 skills fatiadas evita contexto sobrecarregado nos agentes.

### Oportunidades de Evolução / Débitos Técnicos:
1. **Suporte a Imagens PNG Interlaçadas:** O parser customizado de PNG em `imgdiff.py` rejeita imagens interlaçadas com erro amigável, exigindo que o usuário re-salve o PNG sem entrelaçamento.
2. **Detecção de Grapheme Clusters Complexos:** Em `listing.py`, a contagem de emojis foi implementada com heurística interna baseada em ordinais Unicode; sequências ZWJ ultra-complexas podem se comportar com ligeira discrepância sem a lib `unicodedata` com suporte a grapheme clusters modernos.
