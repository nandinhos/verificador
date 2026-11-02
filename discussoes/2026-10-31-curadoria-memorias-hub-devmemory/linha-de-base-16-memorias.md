# Linha de Base — Inventário Completo das 16 Memórias do Hub Dev-Memory

> **Data do congelamento:** 2026-10-31 22:38 BRT  
> **Comando de validação de totais:** `memory_stats` → 16 totais (9 `lesson`, 7 `best_practice`, 16 `global`).  
> **Método de extração:** Varredura determinística via `memory_list` + `memory_get` individual para obter `validation_status`.

---

## 1. Resumo Quantitativo (`OBSERVED`)

| Métrica | Valor | Detalhes |
|---|---|---|
| **Total de Memórias** | 16 | 100% catalogadas sem mutação |
| **Status `validated`** | 12 | 75% da base |
| **Status `pending`** | 4 | 25% da base (3 DSH + 1 Nextcloud/Redis) |
| **Escopo** | 16 globais | 0 memórias de projeto local |
| **Tipos** | 9 lições / 7 boas práticas | Confere com `memory_stats` |

---

## 2. Tabela de Linha de Base Congelada

| # | ID (UUIDv7) | Tipo | Status | Título | Stack | Recorrência |
|---|---|---|---|---|---|:---:|
| 1 | `01a19496-2ead-7337-b691-312894e4a41a` | `lesson` | **validated** | Tratar url+serverUrl em MCP HTTP como poliglota, nao redundancia | mcp, harness, Muse, antigravity | 1 |
| 2 | `01a19426-df50-70f4-bae8-44d27c247963` | `best_practice` | **validated** | Segurança em Chat: mascaramento obrigatório de tokens e segredos para prevenir vazamento | seguranca, mcp, gemini, antigravity, privacy | 1 |
| 3 | `01a055f6-2110-7118-90ce-7d1009babe16` | `lesson` | **pending** | DSH: skill de preset vai em <dshHome>/skills/ (user-dsh), não em customSkillDirs do preset | DeepSeek Harness, dsh-skill-filesystem, cordis, devorq | 1 |
| 4 | `01a05573-9019-70d7-9db3-cf495a22c617` | `lesson` | **pending** | DSH: agent preset não descobre as próprias skills/ automaticamente | DeepSeek Harness, cordis, agent-presets, skills | 1 |
| 5 | `01a05547-dca6-723c-91fa-6914554bf838` | `lesson` | **pending** | Atualizar lista de modelos DSH (opencode/openrouter): catálogo estático + api por rota | DSH, DeepSeek Harness, pi-ai, opencode, openrouter, YAML, modelos | 1 |
| 6 | `01a04676-9428-72e1-bd1b-18a92aa1c556` | `lesson` | **pending** | Nextcloud docker-compose: sessão Redis pendura index.php | Nextcloud, Docker, docker-compose, Redis, PHP/Apache | 1 |
| 7 | `01a03173-2727-72b7-a529-3826ac4df0f1` | `lesson` | **validated** | Não usar Headroom (proxy CCR) para Gemini/Antigravity — higiene de contexto = context-mode, conhecimento = graphify | Antigravity/Gemini (agy) | 1 |
| 8 | `01a022a2-a688-7308-a268-d62c8b0dc1be` | `lesson` | **validated** | sed -E com [:space:]* em command substitution quebra silenciosamente | Bash, shell, gotcha | 1 |
| 9 | `01a022a2-a3d2-7133-b33b-377991532389` | `best_practice` | **validated** | Estilo de comunicacao do Nando: PT-BR + tabelas + pratico | Comunicacao, agent-behavior | 3 |
| 10 | `01a02296-799e-7075-bbc4-7082f810d07e` | `best_practice` | **validated** | Dev-Memory hub: criar global e memory_promote sao admin-only | Dev-Memory, MCP, governanca | 1 |
| 11 | `01a0228e-e11f-7184-b574-e980eb72e862` | `best_practice` | **validated** | TDD em sandbox pra cada vulnerability identificada em code review | Bash, seguranca, code-review | 1 |
| 12 | `01a0228e-dd84-723c-849b-8aedbdc86b0e` | `lesson` | **validated** | Identificar branch mais atualizado ANTES de criar nova branch | Git, fluxo-dev, devops | 1 |
| 13 | `01a0228e-da0a-70fb-8c69-552aade3f229` | `best_practice` | **validated** | Credenciais em ~/.hermes/credentials/<service>.key com permissao 600 | Hermes, seguranca, devops | 1 |
| 14 | `01a0228e-d2e1-70cd-a99c-c43fdfe07828` | `best_practice` | **validated** | Bloquear over-engineering com WHITELIST explicita antes de implementar | Laravel, PHP, arquitetura | 1 |
| 15 | `019ff9e4-ddd8-7196-b1dd-f6b1fcb2d72a` | `lesson` | **validated** | Skills precisam ser instaladas no profile para funcionarem | Hermes, SKILL.md | 1 |
| 16 | `019f793c-5031-71b4-828f-62ef9c6fe03a` | `best_practice` | **validated** | Corrigir permissão de arquivos criados dentro de containers Docker | Docker, VSCode | 1 |

---

## 3. Observações Relevantes para a Regra de Curadoria

1. **A 4ª memória pendente:** Além das 3 do DSH (`#3`, `#4`, `#5`), existe uma 4ª memória `pending` no hub: a `#6` (`Nextcloud docker-compose: sessão Redis pendura index.php`), criada em 2026-08-28. Ela traz contexto e fix claros, servindo como candidato adicional de validação técnica.
2. **Par de Evolução Técnica (`supersedes`):** 
   - A memória `#4` (`01a05573`) instrui uso de `customSkillDirs` com `!!js`.
   - A memória `#3` (`01a055f6`) instrui expressamente o inverso (*"NÃO usar customSkillDirs no preset"*). Ambas estão atualmente `pending`.
3. **Casos Puros de Governança Já Validados:**
   - `#9` (`01a022a2-a3d2` - Estilo de comunicação) tem recorrência 3 e validação direta de preferência humana.
   - `#10` (`01a02296-799e` - Admin-only no hub) documenta regra de permissão do backend.
