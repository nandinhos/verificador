# Handoff Guiado — Consumir o Hub Dev-Memory em Qualquer Harness

> Guia operacional passo a passo para um agente (Muse, Antigravity, Claude Code,
> DSH) conectar ao hub, planejar com memória, capturar lições e curá-las sob a
> **Regra de Curadoria v2.0** (`regra-curadoria-memorias-v2.md` nesta pasta).
> Tudo aqui foi executado de verdade em 2026-10-31/11-01; afirmações marcadas
> `OBSERVED` têm evidência executável registrada na discussão.

---

## 1. Visão em 30 segundos

- Hub remoto (Streamable HTTP): `https://devmemory.fssdev.com.br/api/mcp`, auth `Bearer <token>`.
- Ciclo da memória: nasce `pending` (hipótese) → `validated` (premissa) → promoção a
  `global` só por admin. Contradição não deleta: vira `superseded` via relação.
- Ao planejar: `hub_briefing` primeiro (só premissas). `memory_search` descobre, mas
  confira `validation_status` (a busca já projeta o campo) antes de usar.
- Ao capturar: sem prova → `pending` honesto. Com probe (Trilha B) ou referência
  pinada + probe (Trilha A) → nasce `validated` no escopo `project` (fast-track).

## 2. Pré-requisitos (todas as harnesses)

1. **Token MCP** emitido no painel do hub, vinculado a um projeto. Tipos:
   - *Projeto*: lê `global` + próprias; só altera memórias do próprio projeto.
   - *Operador/admin*: altera `global`, promove escopo. `OBSERVED`: token de projeto
     tentando validar memória global recebe `Memória não encontrada` (por desenho).
2. Nunca cole a chave em chat/log/commit. Painel e arquivos de config locais apenas.
3. User-Agent de navegador ou próprio: a borda (Cloudflare 1010) bane UA default de
   script (`python-urllib`). Clientes MCP normais não sofrem isso.

## 3. Conectar, por harness

### 3.1 Muse

Arquivo: `~/.config/muse/settings.json` (global do usuário, não `.mcp.json`):

```json
"mcpServers": {
  "dev-memory": {
    "type": "http",
    "url": "https://devmemory.fssdev.com.br/api/mcp",
    "headers": { "Authorization": "Bearer <TOKEN>" }
  }
}
```

Salvar e **relançar o `muse`** (config salva ≠ sessão atual). Sinal de sucesso:
tools `memory_*`/`hub_briefing` nativas na sessão; `memory_stats` responde.

### 3.2 Antigravity (agy)

Arquivo: `~/.gemini/antigravity/mcp_config.json`. O cliente lê `url` (canônica,
spec 2025-03-26) e aceita `serverUrl` legada; em bloco **compartilhado** entre
harnesses, declare as duas idênticas (compatibilidade poliglota — discutido em
`../2026-10-31-mcp-url-vs-serverurl/`):

```json
"dev-memory": {
  "serverUrl": "https://devmemory.fssdev.com.br/api/mcp",
  "url": "https://devmemory.fssdev.com.br/api/mcp",
  "headers": { "Authorization": "Bearer <TOKEN>" }
}
```

### 3.3 Claude Code

Arquivo: `.mcp.json` na raiz do projeto consumidor:

```json
{
  "mcpServers": {
    "dev-memory": {
      "type": "http",
      "url": "https://devmemory.fssdev.com.br/api/mcp",
      "headers": { "Authorization": "Bearer <TOKEN>" }
    }
  }
}
```

Claude Code lê `url` (não `serverUrl`). Exceção: ao desenvolver o próprio hub,
usa-se stdio local (`php artisan mcp:serve`) — esse é o `.mcp.json` dentro do
repo `dev-memory`, não o de consumo.

### 3.4 DSH (DeepSeek Harness)

Mecânica própria já documentada no repo do harness
(`deepseek-harness/dsh-dev-memory-integration.md`): plugin nativo
`@deepseek-ai/dsh-mcp-client`, uma instância por servidor no
`~/.dsh/profiles/web/cordis.patch.yml` via `- insert:`, transporte
`streamable-http` pro mesmo endpoint. Tools viram `mcp__dev-memory__*`.
Siga aquele documento para o patch exato; os fluxos da Seção 4 são idênticos.

## 4. Fluxos operacionais (passo a passo)

### 4.1 Abrir um plano com memória

1. `hub_briefing(stack, description)` — devolve riscos, padrões e lições **validadas**.
   Trate tudo como premissa (`OBSERVED`).
2. Se o tema for específico e o briefing vier pobre, complemente com
   `memory_search(query)`. Para cada resultado que for usar, leia o
   `validation_status` projetado na busca:
   - `validated` → premissa.
   - `pending` → alerta `INFERRED`: o plano **não** assume como fato; inclua um
     probe preliminar (Step 0) que confirme ou refute antes de implementar.
   - `superseded` → histórico anti-regressão; nunca recomende como padrão ativo.
3. Declare no plano as duas listas explicitamente (Premissas `OBSERVED` ×
   Alertas `INFERRED` com IDs). Modelo executado: `piloto-consumo-em-planos.md`.

### 4.2 Capturar uma lição (formato canônico)

Título ≤ 80 chars (imperativo), `type` ∈ `error|lesson|best_practice`, `stack`,
e descrição com as 4 seções: **1. Sintoma/Contexto · 2. Causa Raiz ·
3. Solução Canônica · 4. Regra de Prevenção**. Sem segredo no texto (o hub
sanitiza na ingestão, mas fast-track exige zero-leak na origem).

Escolha a trilha pelo tipo de afirmação (**OU** condicional) — e o portão
humano é **E** fixo para promover a `global`:

| Trilha | Quando | Para nascer `validated` (fast-track, só `project`) |
|---|---|---|
| **B — Comportamento local** | gotcha de stack/harness/container provado rodando | `probe_exit_code: 0` + `probe_platform` (ex: `Linux x86_64 php 8.4 <commit>`) + `probe_output_hash` |
| **A — Fato externo** | comportamento de API/doc upstream | `official_reference` (URL) + `reference_version` (pin exato) + probe de integração (`probe_exit_code: 0` + `probe_output_hash`) |
| **C — Convenção/governança** | preferência, padrão do autor | não há fast-track: nasce `pending`, valida por homologação humana |

Sem os campos da trilha (ou com segredo detectado), nasce `pending` — isso é o
comportamento correto, não um erro. A resposta do `memory_create` devolve o
`validation_status` final; `memory_get` expõe a trilha em `validation_evidence`.

### 4.3 Homologar uma pendente (Review Gate)

1. **No chat:** o desenvolvedor diz "homologar a memória X" → o agente chama
   `memory_validate(id)`. Só funciona se o token puder escrever nela
   (projeto próprio ou operador).
2. **No painel web:** abrir a memória → **VALIDAR MEMÓRIA**. Busca do painel é
   por título/descrição (não por ID); atalho: `/memories/<UUID>` direto.
3. Promoção a `global`: **somente admin** (painel ou credencial de operador).
   Token de projeto recebe erro explícito — crie em `project` e peça a promoção.

### 4.4 Aposentar uma memória superada (`supersedes`)

1. Propor a relação: tool `relation_extract_propose` (origem = nova, destino =
   antiga, `relation_hint: supersedes`) — depende do motor de IA no ar; ou
   determinístico via servidor quando a decisão já é humana (precedente:
   aresta criada por script com `origin=HUMAN`, `confidence=1.0`).
2. Aprovar no painel em **Propostas de Relação** (ou no detalhe da memória).
   Ao aprovar, a antiga vira `superseded` automaticamente e sai do briefing.
   **Nunca delete** a antiga: ela é o histórico anti-regressão.
3. Confiança baixa da IA (0.2–0.3) em `supports` é aceitável (só navegação);
   em `supersedes`/`contradicts`, confiança baixa = rejeitar e investigar.

## 5. Operação contínua (motor de IA e modelos)

- O motor (ingestão, relações, skills, veredito doc) fala **Anthropic Messages**
  (`POST /v1/messages`, `x-api-key`). Provedor atual: OpenCode Go
  (`https://opencode.ai/inference/go/anthropic`), configurado no painel em
  Configurações → Motor de Curadoria (sobrepõe o `.env`).
- **Cadeia de modelos:** gratuitos primeiro, pagos baratos depois. O comando
  `php artisan memory:models-check` (semanal, segundas 06:00) descobre os
  modelos vivos de preço 0 (até 3), executa as 3 tarefas reais do motor por
  candidato e reordena: capaz → não-checado → reprovado. Free "limited time"
  que sumir cai sozinho; falha em runtime (402/429/5xx/JSON) também derruba
  para o próximo na hora.
- Embeddings são independentes: Ollama local na VPS (`nomic-embed-text`).
  Trocar o motor de curadoria não afeta a busca semântica.

## 6. Troubleshooting (tudo `OBSERVED` nesta discussão)

| Sintoma | Causa provada | Correção |
|---|---|---|
| `HTTP 400 MissingSessionID` no teste do motor | OpenCode Go exige `x-opencode-session` | já corrigido no código (header + User-Agent); se voltar, confira o deploy |
| `HTTP 402` ao propor relação/ingerir | créditos do provedor anterior (MiniMax direto) | trocar provedor/chave no painel ou aguardar cota; relações têm via determinística (4.4.1) |
| `Memória não encontrada` ao validar | token de projeto em memória `global` (só leitura) | validar no painel como admin ou com token operador |
| `403 Cloudflare 1010` em script | User-Agent default banido na borda | usar UA próprio/de navegador nos probes |
| Busca do painel não acha por ID | busca é título/descrição apenas | URL direta `/memories/<UUID>` |
| Painel local ≠ produção | `localhost:9587` é a stack Docker local (banco separado) | produção é só `devmemory.fssdev.com.br`; token de um não vale no outro |
| Push bloqueado (CEH CI Gate) | certificado `.ceh/last-ci-run.json` de outro commit | rodar o `test-runner.sh` do CLEARER no HEAD (worktree limpa) e repetir o push **sem** pipe/redirecionamento no comando |

## 7. Assumptions / Missing Information / Recomendações

- **Assumptions:** um token por projeto/harness; painel e MCP apontam para a
  mesma VPS; scheduler ativo na VPS (cron `schedule:run`).
- **Missing Information:** comportamento do hub acima de ~200 memórias e sob
  contradição entre validadas (sem amostra ainda — gatilhos de revisita da
  regra v2 §anti-over-engineering).
- **Recomendações:** manter o probe semanal como única fonte de ordem da
  cadeia; tratar qualquer `pending` antiga (>30 dias) em faxina trimestral de
  Review Gate; registrar no hub (como `pending`) toda lição nova de operação
  deste próprio fluxo.

## Fechamento (contrato de resposta)

```
Resultado:   Handoff executável por qualquer harness: conectar (4 dialetos),
             planejar com premissa/alerta, capturar por trilha, homologar e
             aposentar sem deletar — com operação de modelos auto-mantida.
Evidências:
  OBSERVED:  configs reais lidas (Muse settings, Antigravity mcp_config,
             .mcp.json, doc DSH); fluxos 4.1–4.4 executados no piloto real;
             troubleshooting reproduzido item a item em prod.
  INFERRED:  template Claude Code http como forma canônica de consumo
             (exemplo local do repo é stdio, só para desenvolver o hub).
  UNKNOWN:   duração dos modelos free "limited time"; comportamento em
             volume >200 memórias.
Confiança:   ALTA — cada passo tem execução registrada nesta discussão.
```

