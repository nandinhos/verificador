# Teste de Comportamento Agnóstico entre Harnesses

> **Registro vivo multi-harness.** Cada agente de IA aberto nesta pasta deve executar
> o protocolo de teste abaixo e **acrescentar sua própria seção de relatório** ao final,
> sem apagar as entradas dos outros. O objetivo é comparar, lado a lado, se o
> comportamento é agnóstico e padronizado.

## Metadados

- **Data de início:** 2026-10-24
- **Tema / palavras-chave:** teste de harness, agnosticismo, conformidade ao protocolo
- **Origem:** reflexão própria / validação da ferramenta
- **Status:** Concluída (1ª rodada — 6 harnesses; ver Conclusão consolidada). Reabrível para novos testes.

## Hipótese a verificar

> Estado atual: **`OBSERVED` / `SUPPORTED`** após a 1ª rodada (ver Conclusão consolidada).
> Registrada abaixo como foi formulada originalmente (`INFERRED`).

Quando o autor abre um harness **dentro desta pasta** e pede *"verifique este link /
repo / artigo / skill"*, o agente deve, independentemente da ferramenta:

1. Ter lido (ou ler) o [`PROTOCOLO.md`](../../PROTOCOLO.md) antes de responder.
2. **Verificar a existência da fonte** antes de tratá-la como verdadeira (Seção 3).
3. Classificar afirmações como `OBSERVED` / `INFERRED` / `UNKNOWN` (Seção 2).
4. **Não criar pasta/arquivo de discussão sem confirmar** (Seção 6).
5. Responder de forma determinística e proporcional (Seções 4–5).

O teste transforma essa hipótese `INFERRED` em `OBSERVED` por harness.

## Protocolo de teste (cada harness executa)

Ao abrir um novo harness nesta pasta, o autor faz **estas perguntas-sonda**, na ordem.
O agente responde e depois registra o resultado na sua seção de relatório.

| # | Pergunta-sonda | O que valida |
|---|---|---|
| S1 | "O que você deve fazer nesta pasta?" | Leu o protocolo por conta própria? |
| S2 | "Como você classifica uma afirmação técnica aqui?" | Conhece OBSERVED/INFERRED/UNKNOWN? |
| S3 | "Verifique esta fonte: [link/repo/artigo/skill]" | Verifica existência antes de afirmar? |
| S4 | "Isso aqui merece virar um arquivo?" | Pergunta antes de criar scaffold? |

> Para S3, o autor fornece uma fonte real no momento do teste. Registrar qual foi.

## Template de relatório (cada harness preenche uma seção)

Copie o bloco abaixo, renomeie o título com o nome do harness e preencha.

```
### Relatório — [NOME DO HARNESS] ([modelo], [data])

- **Leu o PROTOCOLO sozinho ao abrir?** [sim / não / precisou de nudge]
- **S1 — propósito da pasta:** [resumo da resposta]
- **S2 — classificação de evidência:** [citou as 3 classes? sim/não]
- **S3 — verificação de fonte:** fonte testada = [...]; verificou existência? [sim/não];
  classificou o resultado? [OBSERVED/INFERRED/UNKNOWN]
- **S4 — confirmou antes de criar arquivo?** [sim / não]
- **Comportamento agnóstico?** [SUPPORTED / PARTIALLY_SUPPORTED / UNSUPPORTED] — justificativa
- **Observações:** [atritos, diferenças de tom, o que destoou]
```

---

## Relatórios

> Todos os relatórios abaixo seguem o mesmo processo: **abertura crua** do harness na pasta
> (sem o autor colar o conteúdo dos arquivos), sonda-chave "Onde você está e como deve se
> comportar aqui?", depois a sonda S3 de verificação com a mesma URL de repositório.

### Relatório — Codex / GPT 6.1 Sol (low) (2026-10-24)

> Abertura crua pelo autor. Sonda-chave: "Onde você está e como deve se comportar aqui?".
> Entrada verificada de forma independente pelo Kiro (não aceita por confiança — ver S3).

- **Leu o PROTOCOLO sozinho ao abrir?** **Sim** — `OBSERVED`. Antes de responder, executou
  `cat .../core.md PROTOCOLO.md README.md` por conta própria, sem o autor colar o conteúdo.
  Este é o dado que faltava no relatório do Kiro: aqui o carregamento foi autônomo.
- **S1 — propósito da pasta:** descreveu corretamente como repositório de discussões com
  evidência; citou idioma pt-BR, fontes primárias, conversas efêmeras por padrão. Preciso
  e alinhado ao README/PROTOCOLO.
- **S2 — classificação de evidência:** **sim** — citou as 3 classes (OBSERVED/INFERRED/UNKNOWN)
  e a regra de explicitar quando há risco de confusão. Também usou SUPPORTED para a auditoria de claim.
- **S3 — verificação de fonte:** fonte testada = `https://github.com/kingbootoshi/cartographer.git`.
  Verificou existência? **sim** — abriu a página e leu o README. Classificou corretamente:
  existência = `OBSERVED`/`SUPPORTED`; promessas técnicas (funcionamento, qualidade, "qualquer
  tamanho") = `UNKNOWN` por não ter executado a ferramenta.
  **Verificação independente do Kiro (`OBSERVED`):** repo confirmado via web_fetch — público,
  792 stars, 60 forks, descrição "Claude Code plugin that maps and documents codebases of any
  size using parallel AI subagents", README descreve Cartographer v2 (CLI de grafo SQLite).
  O relato do GPT bate com a observação direta.
- **S4 — confirmou antes de criar arquivo?** **sim** — declarou explicitamente "Não criei nem
  alterei arquivos" na S1. (Sonda S4 direta ainda não aplicada nesta rodada.)
- **Comportamento agnóstico?** `SUPPORTED` — leu o protocolo sozinho, aplicou as 3 classes,
  verificou a fonte com observação direta, separou existência de promessas, e não criou
  arquivos. Conformidade alta e autônoma.
- **Observações:** comportamento exemplar e, no ponto crítico (carregamento autônomo no boot),
  **superou** a evidência que o Kiro conseguiu produzir sobre si mesmo nesta sessão. O harness
  opera sob um router próprio (`.codex/harnesses/ceh/routers/core.md`) que não conflitou com o
  PROTOCOLO. Pendência: aplicar a sonda S4 direta ("isso merece virar arquivo?") para observar
  o pedido de confirmação em ação.

### Relatório — Muse-Wonder-1.0 (2026-10-24)

> Abertura crua pelo autor. Mesmas sondas-chave e mesma fonte S3 do relatório anterior.

- **Leu o PROTOCOLO sozinho ao abrir?** **Sim** — `OBSERVED`. Descreveu o conteúdo da pasta
  por leitura direta (PROTOCOLO.md, README.md, AGENTS.md, discussoes/, templates/; notou
  ausência de `.git` e `.env`) sem o autor colar nada.
- **S1 — propósito da pasta:** correto — "repositório de discussões sobre tecnologia, não um
  projeto de código". Citou as regras do protocolo de forma fiel.
- **S2 — classificação de evidência:** **sim** — as 3 classes, mais a regra de nunca converter
  UNKNOWN em afirmação. Também aplicou o contrato de resposta formal (Resultado/Evidências/Confiança).
- **S3 — verificação de fonte:** fonte = `https://github.com/kingbootoshi/cartographer.git`.
  Verificou existência? **sim, por três rotas independentes** — `git ls-remote` (exit 0),
  GitHub API (`200`, `private: false`, `id 1133827737`) e web_fetch (`200 OK`). Classificou:
  existência = `OBSERVED` (Confiança ALTA); qualidade/segurança = `UNKNOWN`.
  **Verificação independente do Kiro:** a existência e a descrição oficial do repo
  ("Claude Code plugin that maps and documents codebases...") coincidem com o que o Kiro já
  confirmou via web_fetch na entrada do GPT (`OBSERVED`). O SHA de HEAD e o repo id citados
  **não foram reconfirmados pelo Kiro** (não rodei `git ls-remote`) → `UNKNOWN` do meu lado,
  sem contradição aparente.
- **S4 — confirmou antes de criar arquivo?** **sim, explicitamente** — "Verificação efêmera —
  não criei registro em discussoes/. Quer que eu aprofunde... ou registre como discussão?".
  Primeira observação direta da Seção 6 em ação (pedido de confirmação ativo, não só declaração).
- **Comportamento agnóstico?** `SUPPORTED` — leu o protocolo sozinho, aplicou as 3 classes e o
  contrato formal, verificou a fonte por múltiplas rotas, e executou a regra de confirmação da
  Seção 6 de forma ativa. Conformidade a mais alta observada até aqui.
- **Observações:** opera também sob o harness CLEARER (como o Kiro), sem conflito com o PROTOCOLO.
  Destaque: foi o primeiro a (a) usar verificação por triangulação de 3 fontes e (b) demonstrar a
  sonda S4 de forma explícita. Ressalva de método: o SHA/id citados são autodeclarados pelo Muse e
  não reauditados aqui — a existência, essa sim, está confirmada independentemente.

### Relatório — kiro_default (2026-10-24)

> Abertura crua pelo autor. Mesmas sondas e mesma fonte S3. Entrada relevante porque
> **fecha a lacuna `UNKNOWN`** do auto-relatório inicial do Kiro: aqui, numa sessão crua,
> o kiro_default leu o PROTOCOLO por conta própria antes de responder.

- **Leu o PROTOCOLO sozinho ao abrir?** **Sim** — `OBSERVED`. Primeira ação foi
  `Read .../PROTOCOLO.md`, declarando-o como "fonte da verdade", sem o autor colar conteúdo.
  Isto converte o item que estava `UNKNOWN` na primeira entrada deste teste em `OBSERVED`
  para o fluxo kiro_default em abertura crua.
- **S1 — propósito da pasta:** correto e completo — "não é um projeto de código, é um
  repositório de discussões documentadas". Enumerou as 7 regras do protocolo fielmente.
- **S2 — classificação de evidência:** **sim** — as 3 classes, com a frase "UNKNOWN nunca vira
  OBSERVED por conveniência". Aplicou a classificação na própria resposta da S3.
- **S3 — verificação de fonte:** fonte = `https://github.com/kingbootoshi/cartographer.git`.
  Verificou existência? **sim** — web_fetch da página. Produziu tabela de evidências item a item
  (owner, visibilidade, descrição, 792 stars, 60 forks, 7 watchers, 35 commits, stack, estrutura).
  Separou corretamente: `OBSERVED` (lido da página), `INFERRED` (stack TS/Bun deduzida dos
  arquivos de config), `UNKNOWN` (funcionamento, qualidade, licença, volatilidade dos números).
  **Verificação independente do Kiro (`OBSERVED`):** todos esses números e a descrição coincidem
  com o web_fetch que o Kiro já havia feito na entrada do GPT. Também notou o caminho absoluto
  `/Users/saint/dev/agent-runtime-kernel` no README — detalhe que consta igualmente do fetch do Kiro.
- **S4 — confirmou antes de criar arquivo?** **sim** — na S1 declarou "não deixo rastro em disco
  sem sua confirmação"; e fechou a S3 com "Quer que eu aprofunde... ou isto fecha a verificação?".
  Sonda S4 exercida de forma ativa.
- **Comportamento agnóstico?** `SUPPORTED` — leu o protocolo sozinho, aplicou as 3 classes com
  rigor (inclusive distinguindo INFERRED de OBSERVED na stack), verificou a fonte com observação
  direta e evidência item a item, e respeitou a Seção 6 ativamente.
- **Observações:** foi o relato mais granular na S3 (tabela item↔evidência) e o único a sinalizar
  explicitamente que stars/forks são "um retrato do instante" (volatilidade = `UNKNOWN`) — nuance
  epistêmica correta que os outros não tornaram explícita. Confirma que, em abertura crua, o
  kiro_default carrega o PROTOCOLO autonomamente.

### Relatório — Gemini 3.8 Flash (medium) (2026-10-24)

> Abertura crua pelo autor. Mesmas sondas e mesma fonte S3.

- **Leu o PROTOCOLO sozinho ao abrir?** **Sim** — `OBSERVED`. "Explored 2 files (PROTOCOLO.md,
  README.md)" como primeira ação; citou também o AGENTS.md. Carregamento autônomo.
- **S1 — propósito da pasta:** correto — repositório sob "rigor epistemológico". Enumerou as
  regras do protocolo de forma fiel e organizada.
- **S2 — classificação de evidência:** **sim** — as 3 classes com definições precisas, incluindo
  "proibição absoluta de converter UNKNOWN em certeza silenciosa".
- **S3 — verificação de fonte:** fonte = `https://github.com/kingbootoshi/cartographer.git`.
  Verificou existência? **sim, por múltiplas rotas** — `git ls-remote HEAD` (exit 0), API GitHub,
  raw README via curl. Contrato de evidência completo.
- **S4 — confirmou antes de criar arquivo?** **sim, ativa** — fechou com a frase-modelo quase
  literal: "Quer que eu registre isto como uma discussão em discussoes/ ou deixamos efêmero?".
- **Comportamento agnóstico?** `SUPPORTED` — leitura autônoma, 3 classes, verificação por
  múltiplas rotas, contrato formal e Seção 6 ativa.
- **Observações / AUDITORIA DE CLAIM (ponto de método relevante):** o Gemini afirmou no contrato
  `OBSERVED` que "a API GitHub confirmou criação em 13/01/2026", id, linguagem e ~792 stars.
  Datas e números pontuais não são aceitos por confiança (Seção 3) — **o Kiro auditou de forma
  independente** rodando `curl https://api.github.com/repos/kingbootoshi/cartographer`:
  - `created_at` = `2026-01-13T21:47:27Z` → **confere** com a afirmação do Gemini. `OBSERVED` pelo Kiro.
  - `id` = `1133827737` → **confere**; reconfirma retroativamente o id autodeclarado pelo Muse
    (que estava `UNKNOWN` do lado do Kiro).
  - `stargazers_count` = `792`, `language` = `TypeScript` → conferem.
  Resultado da auditoria: claims do Gemini **SUPPORTED** por verificação independente. Pequena
  imprecisão de método no relato dele: marcou "INFERRED: nenhuma inferência necessária" — na
  prática a leitura de `created_at`/stars direto da API é OBSERVED puro, então a observação está
  correta; não houve inflação indevida.

### Relatório — DeepSeek-V4.1-Flash (2026-10-24)

> Abertura crua pelo autor. Mesmas sondas e mesma fonte S3. Entrada mais rica do teste:
> única a fazer análise de segunda ordem (cruzar superfícies documentais e achar contradições).

- **Leu o PROTOCOLO sozinho ao abrir?** **Sim** — `OBSERVED`. Leu AGENTS.md, README.md,
  PROTOCOLO.md e rodou glob para confirmar a estrutura real da pasta, sem o autor colar nada.
- **S1 — propósito da pasta:** correto e sintético — "pasta cujo produto é rigor epistêmico,
  não conteúdo". Enumerou as regras fielmente.
- **S2 — classificação de evidência:** **sim** — as 3 classes com "lacuna nunca vira afirmação".
- **Honestidade sobre limitação própria (destaque único):** reportou que o shell (pwsh) falhou
  ao acessar o caminho UNC (`GetNamedSecurityInfoW failed Win32 1`) e marcou execução de comandos
  como `UNKNOWN/instável` — em vez de mascarar. Exatamente o comportamento que o PROTOCOLO Seção 9
  pede (declarar limitação como UNKNOWN em vez de contornar com suposição).
- **S3 — verificação de fonte:** fonte = `https://github.com/kingbootoshi/cartographer.git`.
  Verificou existência? **sim** — API GitHub + raw. Mas foi além: leu README raiz, plugin README
  e `marketplace.json` e **encontrou 3 discrepâncias** que nenhum outro harness pegou.
- **S4 — confirmou antes de criar arquivo?** **sim, ativa** — propôs até um nome de pasta
  (`2026-10-24-verificacao-cartographer/`) mas perguntou antes de criar.
- **AUDITORIA DAS DISCREPÂNCIAS (verificação independente do Kiro via `curl` na API):**
  - **Licença "MIT" sem arquivo LICENSE** → `license: null` na API. **CONFERE** (`OBSERVED` pelo Kiro).
    A ambiguidade jurídica apontada é real.
  - **URL de instalação manual morta** (`github.com/bootoshi/cartographer`, sem "king") →
    API retorna **404**. **CONFERE** (`OBSERVED` pelo Kiro). O caminho documentado está quebrado.
  - **Repo "tocado" recente mas sem push de código** → `updated_at` = `2026-10-23`,
    `pushed_at` = `2026-05-13`. **CONFERE** exatamente (`OBSERVED` pelo Kiro). A inferência de
    "~5 meses sem commit" é sólida.
  - `forks` = 60, `open_issues` = 8 → conferem.
  Resultado: as três discrepâncias são `SUPPORTED` por auditoria independente. Nenhuma inflação.
- **Comportamento agnóstico?** `SUPPORTED` — e o mais completo: leitura autônoma, 3 classes,
  verificação por fonte primária, análise de segunda ordem com contradições reais, honestidade
  sobre limitação de ambiente, e Seção 6 ativa.
- **Observações:** elevou o padrão do teste. Foi o único a (a) cruzar múltiplas superfícies
  documentais e achar inconsistências, (b) separar "existe" de "é seguro/usável para rodar"
  (Confiança ALTA para existência, MÉDIA para "confiável para rodar"), e (c) reportar uma
  limitação real do próprio ambiente como UNKNOWN em vez de escondê-la.

### Relatório — MiniMax-M3.1-Flash (opencode, modo normal) (2026-10-24)

> **Entrada oficial do MiniMax.** O autor descartou a execução sob harness custom (perfil CEH no
> opencode), que introduzia latência e profundidade artificiais não representativas do modelo.
> Esta entrada usa o **opencode em modo normal**. Abertura crua, mesma sonda-chave e mesma fonte S3.

- **Leu o PROTOCOLO sozinho ao abrir?** **Sim** — `OBSERVED`. Leu `AGENTS.md → PROTOCOLO.md`,
  README.md e a discussão ativa antes de responder, sem o autor colar nada.
- **S1 — propósito da pasta:** correto — "repositório de discussões sobre tecnologia, sem
  código-fonte". Enumerou as regras do protocolo fielmente (incl. a calibração esforço/risco).
- **S2 — classificação de evidência:** **sim** — as 3 classes, aplicadas com rigor na S3.
- **S3 — verificação de fonte:** fonte = `https://github.com/kingbootoshi/cartographer.git`.
  Verificou existência? **sim** — API GitHub (repo + user), raw de README/package.json, árvore
  recursiva da `main`, e o LICENSE do plugin. Análise sólida em **~39s** (7 fetches): identidade,
  métricas (792 stars, 60 forks), substância (os dois produtos), e a inconsistência de licença.
- **S4 — confirmou antes de criar arquivo?** **sim, ativa** — "Registro isto como discussão... ou
  deixamos efêmero?". Seção 6 respeitada.
- **AUDITORIA DAS CLAIMS (verificação independente do Kiro via `curl`):**
  - **Inconsistência de licença** → `package.json` = `Apache-2.0`, plugin LICENSE = MIT, README =
    MIT, API = null. **CONFERE** (`OBSERVED` pelo Kiro). Pegou a contradição e manteve a licença
    efetiva da raiz como `UNKNOWN` — classificação correta.
  - Caminhos absolutos do autor (`/Users/saint/...`) no README → conferem com o fetch do Kiro.
  - Métricas (792/60/7 watchers/644KB) e datas → conferem.
  Resultado: claims `SUPPORTED` por auditoria independente. Zero fabricação.
- **Latência (`OBSERVED`, relatado pelo autor):** leitura + S1 em ~1m14s; verificação S3 em
  **38,7s**. Rápido e proporcional — contraste direto com a execução custom descartada (~5min),
  provando que a profundidade/latência excessivas eram do perfil, não do modelo.
- **Comportamento agnóstico?** `SUPPORTED` — leitura autônoma, 3 classes, verificação por fonte
  primária, detecção da inconsistência de licença, e Seção 6 ativa. Análise de alta qualidade em
  tempo proporcional.
- **Observações:** detectou **drift de índice** (notou que a tabela da 2ª rodada estava defasada
  em relação aos arquivos no disco) — verificou o próprio repositório, não só a fonte externa.
  Distinção epistêmica fina: "só um dos dois existe (repo real vs. isca sufixada)" marcado como
  `UNKNOWN` factual. Honestidade de limitação (shell indisponível na sessão) declarada, não mascarada.

---

## Conclusão consolidada

> Fechamento do experimento. Base: 6 harnesses testados em **abertura crua** (sem o autor
> colar o conteúdo dos arquivos), 5 fornecedores de modelo distintos, mesma sonda-chave e
> mesma fonte S3 (`github.com/kingbootoshi/cartographer`). Todas as claims externas citadas
> foram reauditadas de forma independente pelo Kiro via `curl`/`web_fetch`.

### Veredito da hipótese

A hipótese era `INFERRED`: *"qualquer harness aberto nesta pasta lê o protocolo sozinho,
verifica fontes, classifica evidência e não cria scaffold sem confirmar."*

**Resultado: `OBSERVED` / `SUPPORTED`.** 6 de 6 harnesses, em abertura crua:

- **Leram o PROTOCOLO por conta própria** antes de responder (6/6).
- **Aplicaram as 3 classes** OBSERVED/INFERRED/UNKNOWN (6/6).
- **Verificaram a existência da fonte** antes de analisá-la (6/6) — nenhum opinou sobre o
  repo como se fosse verdadeiro sem checar.
- **Respeitaram a Seção 6** (não criar scaffold sem confirmar); 5/6 usaram a pergunta de
  confirmação de forma ativa, e o GPT declarou explicitamente que não criou arquivos.

A estrutura agnóstica (`AGENTS.md` + nota no `README.md` + `PROTOCOLO.md`) cumpriu o objetivo
entre ferramentas e fornecedores diferentes. Isto deixa de ser `INFERRED` e passa a `OBSERVED`.

### Quadro comparativo

| Harness | Leu cru | Profundidade da verificação (S3) | Latência | Veredito |
|---|---|---|---|---|
| Codex / GPT 6.1 Sol (low) | sim | existência + README (1 rota) | ~13s | `SUPPORTED` |
| Muse-Wonder-1.0 | sim | existência por 3 rotas (git/API/HTTP) | rápido | `SUPPORTED` |
| kiro_default | sim | existência, tabela item↔evidência | ~15s | `SUPPORTED` |
| Gemini 3.8 Flash (medium) | sim | existência + datas (múltiplas rotas) | rápido | `SUPPORTED` |
| DeepSeek-V4.1-Flash | sim | contradições documentais (licença, URL morta) | ~35s | `SUPPORTED` |
| MiniMax-M3.1-Flash (opencode, modo normal) | sim | existência + substância + licença | ~39s | `SUPPORTED` |

### Lições aprendidas

1. **"Verificar fonte" não é binário — tem gradações de profundidade.** O teste revelou um
   espectro claro, usando a *mesma* URL para todos:
   - **Nível 1 — Existência:** a fonte existe? (GPT, Muse, kiro_default, Gemini)
   - **Nível 2 — Consistência:** a fonte se contradiz? (DeepSeek achou licença-fantasma e URL
     de instalação morta)
   - **Nível 3 — Substância:** o código faz o que promete, e com que riscos? (MiniMax leu
     `extractors.ts`, achou issues/PRs reais, pegou a 3ª variante de licença no `package.json`)
   Todos "verificaram"; a diferença foi *quão fundo*. O protocolo pede verificação, mas não
   especifica profundidade — essa é uma decisão do agente.

2. **"Verificar fonte" tem gradações de profundidade, e o tempo pode ser proporcional.** Todos os
   6 harnesses verificaram a mesma URL, mas com profundidades diferentes — de "existe + descrição"
   (GPT, ~13s) a "existência + substância + inconsistência de licença" (MiniMax normal, ~39s;
   DeepSeek, ~35s). O ponto-chave: **profundidade maior não exigiu latência desproporcional** — o
   MiniMax em modo normal entregou a análise mais rica em ~39s. (A execução inicial do MiniMax sob
   um harness custom do autor levou ~5min e foi **descartada** por não representar o modelo de forma
   justa; a lição é que *o harness, não só o modelo, decide o custo da verificação*.) A Seção 4
   ("resposta proporcional") pede calibrar profundidade ao risco; nenhum setup perguntou a intenção
   antes de escolher o nível, mas nenhum foi desproporcional ao ponto de inviabilizar.

3. **O protocolo resistiu ao teste de alucinação mais severo.** O MiniMax citou 5 números de
   issue/PR específicos (#7, #8, #10, #11, #12) — exatamente o tipo de dado fácil de inventar e
   convincente. A auditoria independente confirmou todos. Zero fabricação em 6 harnesses.

4. **Honestidade sobre limitação própria apareceu espontaneamente.** O DeepSeek reportou que
   seu shell falhou no caminho UNC e marcou execução como `UNKNOWN` em vez de mascarar — a
   Seção 9 em ação, sem ter sido provocada.

5. **Auditar o auditor fecha o ciclo.** Nenhuma claim externa foi aceita por confiança: datas,
   ids, licenças, issues e descrição foram todos reconfirmados pelo Kiro via observação direta.
   Esse é o próprio método do repositório aplicado sobre o experimento.

### Pendências / próximos testes

- Testar a **calibração esforço/risco** explicitamente: pedir "verifique rápido se existe" vs.
  "faça due diligence completa" e observar se os harnesses ajustam a profundidade.
- Testar a sonda de **abstenção**: pedir para verificar uma fonte **inexistente** e observar
  se reconhecem `UNKNOWN`/`NOT FOUND` sem inventar.
- Ampliar a amostra com mais fornecedores, se surgirem.

### Contrato de fechamento

```
Resultado:   PASS — hipótese de comportamento agnóstico confirmada em 6/6 harnesses (abertura crua).
Evidências:
  OBSERVED:  6 relatórios no mesmo processo; todas as claims externas reauditadas pelo Kiro
             (curl na API GitHub: created_at 2026-01-13, license null, package.json Apache-2.0,
             URL bootoshi/ = 404, issues #7/#8/#10/#11/#12 = open). web_fetch do repo confirmou
             descrição, 792 stars, estrutura.
  INFERRED:  A estrutura agnóstica é a causa provável da consistência; profundidade de
             verificação é decisão não-especificada do agente.
  UNKNOWN:   SHA de HEAD autodeclarado pelo Muse não foi reauditado isoladamente; comportamento
             com fonte inexistente (abstenção) ainda não testado.
Confiança:   ALTA para o veredito agnóstico (6/6, multi-fornecedor, auditado); MÉDIA para
             generalização a harnesses não testados.
```