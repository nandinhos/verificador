# Piloto de Classificação — Pareceres Formais da Regra de Curadoria v1.0

> **Data de execução:** 2026-10-31 22:47 BRT  
> **Objetivo:** Aplicar a Regra de Curadoria v1.0 a 5 memórias reais do hub sem realizar mutações no banco (`dry-run` deliberativo).  
> **Critério de Validade:** Cada parecer cita obrigatoriamente o UUIDv7, o tipo de claim, a trilha aplicada, a evidência executável observada e o veredito decisório.

---

## 1. Tabela-Resumo dos Pareceres

| # | ID (UUIDv7) | Trilha da Regra v1 | Status Atual | Veredito do Parecer | Ação Decisória Recomendada |
|---|---|:---:|:---:|:---:|---|
| **1** | `01a19496-2ead-7337-b691-312894e4a41a`<br>*(MCP url+serverUrl)* | **Trilha A / B** (Mista) | `validated` | **CONFORME**<br>(Benchmark de Controle) | Manter como referência canônica validada. |
| **2** | `01a055f6-2110-7118-90ce-7d1009babe16`<br>*(DSH skill user-dsh root)* | **Trilha B** (Local) | `pending` | **PROMOVÍVEL** | Promover a `validated` após OK humano; criar aresta `supersedes` para `#3`. |
| **3** | `01a05573-9019-70d7-9db3-cf495a22c617`<br>*(DSH preset customSkillDirs)* | **Trilha B** (Local) | `pending` | **SUBSTITUÍDA**<br>(Não promovível) | Manter como registro histórico; apontar `supersedes` vindo de `#2`. |
| **4** | `01a05547-dca6-723c-91fa-6914554bf838`<br>*(DSH sync models catálogo)* | **Trilha B** (Local) | `pending` | **PROMOVÍVEL CONDICIONADA** | Promover a `validated` mediante verificação do script probe citado e OK humano. |
| **5** | `01a022a2-a3d2-7133-b33b-377991532389`<br>*(Estilo de comunicação)* | **Trilha C.1** (Governança) | `validated` | **CONFORME**<br>(Benchmark C.1) | Manter validada; governada por preferência explícita do autor. |

---

## 2. Pareceres Técnicos Detalhados

### Caso 1: `01a19496-2ead-7337-b691-312894e4a41a`
* **Título:** Tratar `url+serverUrl` em MCP HTTP como poliglota, não redundância.
* **Tipo de Claim:** Misto (Spec de transporte Streamable HTTP + Comportamento multi-harness Muse/Antigravity).
* **Trilhas Aplicadas:** Trilha A (Fato Externo) $\land$ Trilha B (Comportamento Local).
* **Evidências Observadas (`OBSERVED`):**
  - Trilha A: Especificação oficial do protocolo MCP (transporte Streamable HTTP de 2025-03-26 define `url`).
  - Trilha B: Teste A/B documentado no Muse (`initialize` e `tools/list` retornando HTTP 200) e compatibilidade com Antigravity (`mcp_servers.md:59-71`).
* **Veredito:** **CONFORME (APROVADA COMO BENCHMARK)**. Demonstra que a conjunção de trilhas foi plenamente atendida no ciclo de vida anterior.

---

### Caso 2: `01a055f6-2110-7118-90ce-7d1009babe16`
* **Título:** DSH: skill de preset vai em `<dshHome>/skills/` (user-dsh), não em `customSkillDirs` do preset.
* **Tipo de Claim:** Comportamento Local de Sistema (Sistema de arquivos e loader do DeepSeek Harness).
* **Trilha Aplicada:** Trilha B (Comportamento Local).
* **Evidências Observadas (`OBSERVED`):**
  - Probe físico do `FileSystemSkillProvider` com configuração default descobriu `devorq` via `user-dsh` (rank 400).
  - Script idempotente documentado: `scripts/install-dsh-preset.sh`.
* **Veredito:** **PROMOVÍVEL A VALIDATED**.
* **Condição de Execução:** O portão humano deve confirmar a promoção e acionar a ferramenta de grafo para estabelecer que esta memória substitui a memória `#3` (`01a05573`).

---

### Caso 3: `01a05573-9019-70d7-9db3-cf495a22c617`
* **Título:** DSH: agent preset não descobre as próprias `skills/` automaticamente.
* **Tipo de Claim:** Comportamento Local de Sistema (Loader Yaml/Cordis com `!!js`).
* **Trilha Aplicada:** Trilha B (Comportamento Local).
* **Análise Crítica:** Esta memória formulou a solução inicial (uso de `customSkillDirs` com interpolação `!!js`). Duas horas depois, a memória `#2` (`01a055f6`) descobriu que `customSkillDirs` hardcodava o ID do preset e falhava em cópias. Portanto, a recomendação técnica desta memória está **obsoleta e refutada**.
* **Veredito:** **NÃO PROMOVÍVEL COMO RECOMENDAÇÃO ATIVA (SUBSTITUÍDA)**.
* **Ação Conforme Regra v1 (§ 4):** Fica proibido deletar o registro. A memória permanece no hub com status `superseded` (ou vinculada via aresta de entrada `supersedes`), servindo de histórico contra regressão.

---

### Caso 4: `01a05547-dca6-723c-91fa-6914554bf838`
* **Título:** Atualizar lista de modelos DSH (opencode/openrouter): catálogo estático + api por rota.
* **Tipo de Claim:** Comportamento Local de Sistema (Estrutura de dados do pacote `@earendil-works/pi-ai` e script de sincronização).
* **Trilha Aplicada:** Trilha B (Comportamento Local).
* **Evidências Observadas (`OBSERVED`):**
  - Script de sincronização declarado: `scripts/dsh-sync-models/dsh-sync-models.py` no repositório `deepseek-harness`.
  - Tratamento determinístico de flags `--dump-yaml` e criação resiliente de `.ref_*.json`.
* **Veredito:** **PROMOVÍVEL CONDICIONADA**.
* **Condição de Execução:** Validação humana simples de que o script permanece funcional no repositório referenciado.

---

### Caso 5: `01a022a2-a3d2-7133-b33b-377991532389`
* **Título:** Estilo de comunicacao do Nando: PT-BR + tabelas + pratico.
* **Tipo de Claim:** Governança / Preferência Pessoal do Autor.
* **Trilha Aplicada:** Trilha C.1 (Governança — Preferência Individual).
* **Evidências Observadas (`OBSERVED`):**
  - Registro de `recurrence_count: 3` no banco.
  - O próprio autor humano é a fonte primária inegociável de suas preferências de comunicação.
* **Veredito:** **CONFORME (BENCHMARK DE GOVERNANÇA)**. Demonstra que a Trilha C.1 requer apenas a confirmação humana direta para atingir o estado `validated`.

---

## 3. Avaliação dos Critérios de Sucesso do Piloto

1. **Classificação sem ambiguidade:** Todos os 5 casos foram classificados e receberam veredito unívoco sem nenhum caso de indecisão ou *"não sei"*.
2. **Resolução de Contradição:** O conflito DSH (`#2` vs `#3`) foi resolvido sem deletar histórico, validando na prática o mecanismo de `supersedes`.
3. **Ausência de Mutações:** O piloto operou 100% como `dry-run` documental, preservando o banco intacto.
