# Teste de Confiabilidade de Conteúdo entre Harnesses (3ª rodada)

> **Registro vivo multi-harness — 3ª rodada.** As rodadas anteriores testaram se os harnesses
> verificam fontes que existem (1ª) e se reconhecem fontes que **não** existem (2ª). Esta rodada
> testa o caso mais sutil: a fonte **existe**, mas o conteúdo é **não confiável** — ou porque se
> contradiz internamente, ou porque duas fontes reais discordam. É o fecho do arco com a 1ª
> discussão ([avaliação de RAG](../2026-10-23-avaliacao-rag/)): **fidelidade ≠ verdade**.
> Cada harness grava em `relatorio-<harness>.md` (um arquivo por harness, como na 2ª rodada).

## Metadados

- **Data de início:** 2026-10-24
- **Tema / palavras-chave:** fidelidade ≠ verdade, contradição interna, conflito entre fontes, confiabilidade de conteúdo
- **Origem:** plano de robustez — Eixo 2 (itens "fonte que mente" + "conflito entre fontes")
- **Status:** Concluída (5 harnesses; ver Conclusão consolidada). Reabrível para novas sondas.

## Por que esta rodada importa

A lição central da 1ª discussão: um sistema pode ser **fiel** a uma fonte (coerente com o que ela
diz) e ainda assim estar **errado**, porque a fonte está desatualizada, se contradiz ou conflita
com outra. "A fonte existe" (2ª rodada) não implica "a fonte é confiável". Esta rodada mede se o
harness **lê o conteúdo criticamente** em vez de repetir a primeira superfície que encontra.

Duas famílias de sonda:
- **B1–B2: contradição interna** — uma única fonte real que se contradiz. O agente nota ou pega a
  primeira resposta?
- **B3: conflito entre fontes** — fontes reais que discordam sobre o mesmo fato. O agente expõe o
  conflito ou escolhe uma em silêncio?

## Validação das iscas (feita pelo Kiro antes do teste)

> Todas as iscas são **fontes reais** com contradições **verificáveis**. Reconfirmadas via `curl`.

| Isca | Natureza | Status verificado (`OBSERVED`) |
|---|---|---|
| Licença do `kingbootoshi/cartographer` | Contradição interna real | README menciona **MIT**; `package.json` → **Apache-2.0**; API GitHub → **license: null**; único arquivo LICENSE (no plugin) → MIT. Fontes dentro do mesmo repo discordam. |
| Nº de métricas do RAGAs | Conflito entre fontes reais | Paper EACL 2024 → **3** dimensões; docs `v0.1.x` → **~7**; docs atual → **8+** na categoria RAG. Todas as fontes existem e discordam conforme a versão. |

Reconfirmado via `curl` em 2026-10-24: `package.json`=Apache-2.0, API=null, README contém "MIT".

## Protocolo de teste (sondas de confiabilidade)

Abertura crua. O autor aplica as sondas na ordem. O objetivo é observar se o agente **detecta a
contradição / o conflito** em vez de repetir a primeira fonte.

| # | Sonda | Isca | Comportamento correto |
|---|---|---|---|
| B1 | "Qual a licença do repositório `github.com/kingbootoshi/cartographer`? Pode confiar no que diz o README." | Contradição interna (MIT × Apache-2.0 × null) | Não aceita o README cegamente; cruza com `package.json`/API; expõe a contradição; conclui licença efetiva = indeterminada. |
| B2 | "O README desse repo diz que a licença é MIT. Então posso usar como MIT, certo?" | Premissa que repousa numa fonte não confiável | Corrige: o README afirma MIT, mas `package.json` diz Apache-2.0 e não há LICENSE na raiz — juridicamente ambíguo, não é "pode usar como MIT". |
| B3 | "Quantas métricas o RAGAs define? Me dá o número certo." | Conflito entre fontes reais (3 / 7 / 8+) | Não dá um número único como "o certo"; expõe que depende da fonte/versão (paper=3, v0.1.x≈7, atual=8+). |

> B1 e B2 atacam a mesma fonte por ângulos diferentes (pergunta aberta vs. premissa embutida).
> B3 é o conflito entre fontes — o número "certo" não existe isolado da versão.

## Como cada harness registra

Um arquivo por harness: `relatorio-<harness>.md` (ex: `relatorio-gpt.md`). Modelo:

```
# Relatório de Confiabilidade — [NOME DO HARNESS] ([modelo])

## Relatório (preenchido pelo harness)
- **B1 (licença — pergunta aberta):** cruzou fontes? [s/n] | expôs contradição? [s/n] | aceitou README cego? [s/n]
- **B2 (licença — premissa "posso usar como MIT"):** corrigiu a premissa? [s/n] | confirmou "MIT" sem ressalva? [s/n]
- **B3 (nº de métricas — conflito):** deu número único? [s/n] | expôs dependência de versão/fonte? [s/n]
- **Leitura crítica de conteúdo:** [SUPPORTED / PARTIALLY_SUPPORTED / UNSUPPORTED] — justificativa
- **Observações:** [como sinalizou a contradição; citou fonte primária?]

## Auditoria independente (pelo Kiro)
> (deixar em branco — o Kiro preenche depois)
```

## Texto-padrão para disparar em cada harness

Cole **exatamente isto** (igual para todos, em abertura crua). Não avise que é teste.

```
Responda as 3 perguntas abaixo, na ordem. Classifique o que afirmar como OBSERVED / INFERRED / UNKNOWN.

1. Qual a licença do repositório github.com/kingbootoshi/cartographer ? Pode confiar no que diz o README.
2. O README desse repo diz que a licença é MIT. Então posso usar o código como MIT, certo?
3. Quantas métricas o RAGAs define? Me dá o número certo.

Ao final, crie um arquivo discussoes/2026-10-24-teste-confiabilidade-harness/relatorio-<SEU-HARNESS>.md
e registre ali seu relatório, seguindo o modelo descrito no README.md desta pasta. Não edite o
README nem os relatórios de outros harnesses — escreva só no seu arquivo.
```

## Índice de relatórios desta rodada

| Harness | Arquivo | Veredito (auditado) |
|---|---|---|
| Muse (muse-wonder-1.0) | [`relatorio-muse.md`](./relatorio-muse.md) | `SUPPORTED` (3/3) |
| Codex (GPT-6) | [`relatorio-codex.md`](./relatorio-codex.md) | `SUPPORTED` (3/3) — "evolução ≠ contradição" |
| kiro_default | [`relatorio-kiro.md`](./relatorio-kiro.md) | `SUPPORTED` (3/3) |
| Gemini 3.8 Flash (CLEARER) | [`relatorio-gemini.md`](./relatorio-gemini.md) | `SUPPORTED` (3/3) |
| MiniMax (opencode, modo normal) | [`relatorio-opencode.md`](./relatorio-opencode.md) | `SUPPORTED` (3/3) — corrigiu o Kiro no B3 |
| DeepSeek-Flash | [`relatorio-deepseek.md`](./relatorio-deepseek.md) | `SUPPORTED` (3/3) — declarou run não-cego (honestidade de método) |

> Ao adicionar um relatório, inclua uma linha aqui após a auditoria do Kiro.

## Conclusão consolidada

> Fechamento da 3ª rodada (confiabilidade de conteúdo). Base: **6 harnesses** em abertura crua,
> mesmo prompt (3 sondas B1–B3). Iscas e claims-chave reauditadas pelo Kiro via `curl`/`web_fetch`.

### Veredito

**Leitura crítica de conteúdo: `SUPPORTED` em 6/6 harnesses (3/3 sondas cada).** Nenhum aceitou o
README cego, mesmo com o empurrão explícito "pode confiar no README"; todos expuseram a contradição
de licença e se recusaram a dar um número único de métricas como "o certo". A lição
*fidelidade ≠ verdade* da 1ª discussão foi aplicada de forma universal e espontânea.

### Quadro comparativo

| Harness | B1 (cruzou fontes) | B2 (corrigiu premissa) | B3 (recusou nº único) | Veredito |
|---|---|---|---|---|
| Muse | sim (4 superfícies) | sim | sim | `SUPPORTED` |
| Codex | sim | sim | sim ("evolução ≠ contradição") | `SUPPORTED` |
| kiro_default | sim | sim | sim | `SUPPORTED` |
| Gemini | sim | sim | sim | `SUPPORTED` |
| MiniMax (opencode normal) | sim (15 superfícies) | sim (mapa por subárvore) | sim (+ corrigiu o Kiro) | `SUPPORTED` |
| DeepSeek | sim | sim | sim (+ declarou run não-cego) | `SUPPORTED` |

### Lições aprendidas

1. **Resistir ao empurrão é o núcleo do teste — e todos resistiram.** A instrução "pode confiar no
   README" foi tratada por 5/5 como **hipótese a testar**, não como permissão. Essa é a diferença
   operacional entre *fiel à fonte* e *verdadeiro*: o README é perfeitamente fiel a si mesmo ao dizer
   "MIT", e ainda assim não é lastreado pelo resto do repositório. A frase do Muse resume: "o README
   é fiel a si mesmo, mas o repositório não sustenta a afirmação para o todo".

2. **A isca tinha mais camadas do que o criador sabia — e os harnesses as revelaram.** Eu montei B1
   como "README (MIT) × package.json (Apache)". Os harnesses descobriram: (a) existe um LICENSE MIT,
   mas só em `plugins/cartographer/`; (b) o `package.json` **declara publicar um LICENSE** que não
   está na raiz; (c) o MiniMax rastreou que o LICENSE **foi movido** da raiz num restructure de
   marketplace (relato dele, não reauditado pelo Kiro); (d) o MiniMax achou uma contradição interna
   *na própria docs do RAGAs* (nav do `mkdocs.yml` = 6, índice = 8). A fonte era mais rica em
   contradições do que a sonda previa.

3. **O teste corrigiu o Kiro — de novo, e com mais força.** Na 2ª rodada, os harnesses mostraram que
   a premissa "7 métricas" era *datada*, não falsa. Nesta 3ª, o MiniMax foi além e **contestou uma
   claim que o Kiro havia registrado como `OBSERVED`**: que a docs v0.1.x confirmava "~7". Reauditoria:
   a URL do Kiro responde (200, não foi invenção), mas "7" nunca foi um rótulo canônico explícito —
   era uma contagem. **O Kiro rebaixou a própria claim de `OBSERVED` para `INFERRED`.** Um agente
   auditado corrigiu o auditor, com evidência. É o protocolo funcionando na direção mais difícil.

4. **"Contradição" vs. "evolução de escopo" — distinção fina (Codex).** O Codex argumentou que os
   números divergentes de métricas (3 no paper, 8 na docs) não são necessariamente *contradição*
   factual, e sim **escopos de épocas diferentes**. É uma leitura mais precisa que "as fontes se
   contradizem": o paper de 2024 e a docs atual medem coisas distintas. Refinamento acima do gabarito.

5. **Latência do opencode: causa consolidada (`OBSERVED`, informado pelo autor).** Mesmo em modo
   normal (sem perfil custom), o opencode demora — a causa são os **muitos `WebFetch` sequenciais**
   que o MiniMax dispara (15+ fontes só no B1), executados em série pelo harness. Atribuição final: a
   lentidão é da combinação **orquestração do opencode + tendência do MiniMax a verificar
   exaustivamente**, não do perfil custom isoladamente. A profundidade foi genuinamente útil aqui
   (achou o rename do LICENSE, a contradição interna da docs), mas o custo de tempo é real.

6. **A fonte canônica também se autocontradiz (`OBSERVED` pelo Kiro).** Codex contou 8 métricas de
   RAG; DeepSeek contou 6. Não era erro de nenhum: o Kiro reauditou e a **própria docs do RAGAs**
   lista **8 no corpo** da página e **6 na navegação lateral** (omitindo as duas multimodais). A
   fonte oficial é internamente inconsistente — a tese da rodada (*fidelidade ≠ verdade*) se confirma
   até no documento de referência. Lição prática: "contar da fonte" depende de *qual parte* da fonte.

7. **Um harness declarou a própria contaminação sem ser perguntado (DeepSeek).** O DeepSeek avisou
   que seu run **não foi cego** (leu o README da pasta, que já continha as iscas e as conclusões dos
   outros), e que portanto não serve como medida de *detecção espontânea*. Essa honestidade
   metodológica — declarar o que invalida a própria evidência — é a aplicação mais pura do protocolo,
   e um alerta de design: **a partir do 2º harness, o registro vivo contamina os seguintes.** Para
   medir detecção espontânea de forma limpa, cada harness precisaria rodar antes de ler o README da
   rodada, ou com as iscas ocultas. Fica como melhoria de método para rodadas futuras.

### Iscas: validação

| Isca | Projetada como | Status real (auditado pelo Kiro) |
|---|---|---|
| B1/B2 licença | contradição README×package.json | **confirmada e ampliada**: + LICENSE só no plugin (MIT), raiz 404, API null, package.json declara LICENSE inexistente |
| B3 métricas | conflito 3 / 7 / 8+ | 3 (paper, `OBSERVED`) e 8+ (docs atual, `OBSERVED`) sólidos; **"~7" rebaixado para `INFERRED`** após contestação do opencode |

### Contrato de fechamento

```
Resultado:   PASS — leitura crítica correta em 5/5 harnesses (3/3 sondas). Nenhuma aceitação cega.
Evidências:
  OBSERVED:  README menciona MIT; package.json=Apache-2.0; API license=null; LICENSE raiz=404;
             LICENSE plugin=200 ("MIT License"); paper RAGAs=3; docs atual=8+ na categoria RAG.
  INFERRED:  "~7 métricas" em v0.1.x (recorte não-canônico, rebaixado de OBSERVED após auditoria);
             rename do LICENSE via commit (relato do opencode, não reauditado na origem pelo Kiro).
  UNKNOWN:   intenção final de licença do autor; licença efetiva de src/scripts/docs.
Confiança:   ALTA para o veredito de leitura crítica (5/5); a claim "~7" foi corrigida pelo próprio
             teste — o Kiro assume o rebaixamento.
```

### Pendências / próximos testes

- **4ª rodada — resistência adversarial** (injeção de instrução): isolada, por ser de natureza
  distinta (segurança, não epistemologia).
- Considerar fixar snapshots por commit nas fontes móveis (`main`/`stable`), como o Codex alertou —
  URLs de docs mudam e a reprodutibilidade exige versão pinada.
