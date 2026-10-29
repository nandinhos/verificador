# Arquitetura e Superfícies do Google Antigravity (App 2.0, IDE, CLI, Extensions & SDK)

## Metadados

- **Data de início:** 2026-10-28
- **Tema / palavras-chave:** Google Antigravity, AGY, Antigravity 2.0, Antigravity IDE, Antigravity CLI, Antigravity SDK, Customizations, Harness, CEH
- **Origem:** Reflexão própria e investigação da arquitetura local da ferramenta para otimização do harness acoplado ao projeto
- **Fonte(s):** Documentação interna embutida (`antigravity_guide`, `agy-customizations`, `google-antigravity-sdk`) e inspeção direta do filesystem (`/home/nandodev/.gemini/`)
- **Status:** Ativa

## Contexto

Investigação profunda sobre as diferenças arquiteturais, casos de uso ideais e localizações nativas em disco entre as cinco superfícies/componentes do ecossistema Google Antigravity:

1. **Antigravity App (Antigravity 2.0)**
2. **Antigravity IDE**
3. **Antigravity CLI (`agy`)**
4. **IDE Extensions vs. AGY Customizations (Plugins, Skills, Rules, Hooks, Sidecars)**
5. **Antigravity SDK (`google-antigravity` Python SDK)**

O objetivo é consolidar o entendimento determinístico da plataforma para extrair o máximo potencial de cada superfície em sinergia com o harness do autor (CLEARER Engineering Harness / Beer & Code Harness) e com o protocolo deste repositório.

## Verificação de fontes

| Fonte | Status | Como foi verificada |
|---|---|---|
| `~/.gemini/antigravity/builtin/skills/antigravity_guide/SKILL.md` e `references/{app,ide,cli,sdk}.md` | `OBSERVED` | Leitura direta dos arquivos de documentação embutidos na instalação local do Antigravity. |
| `~/.gemini/antigravity/builtin/skills/agy-customizations/SKILL.md` | `OBSERVED` | Leitura direta da especificação do sistema de customização, descoberta e ordem de precedência. |
| `~/.gemini/config/plugins/google-antigravity-sdk/skills/google-antigravity-sdk/{SKILL.md,references/architecture.md}` | `OBSERVED` | Leitura direta da skill oficial do Python SDK instalada no ambiente local. |
| Estrutura física em `/home/nandodev/.gemini/` e `/home/nandodev/.local/bin/agy` | `OBSERVED` | Inspeção via `ls -la` comprovando diretórios, binários e symlinks entre `antigravity`, `antigravity-ide` e `antigravity-cli`. |

## Análise

### 1. Mapeamento Comparativo das 5 Superfícies (`OBSERVED`)

| Componente | Natureza Técnica | Aplicação Ideal no Fluxo | Localização Nativa no Linux (`OBSERVED`) |
|---|---|---|---|
| **Antigravity App (Antigravity 2.0)** | Aplicação Desktop Electron standalone (independente de IDE). | **Orquestração & Revisão Profunda**: gestão multi-projeto, *Scheduled Tasks* (cron/timers), acompanhamento de subagentes em paralelo e leitura focada no *HTML Auxiliary Pane* (Artifacts com Mermaid/LaTeX, Background Tasks, Subagents, Files Changed). | **App Data:** `/home/nandodev/.gemini/antigravity/` |
| **Antigravity IDE** | Editor AI-first standalone (baseado no VS Code). | **Codificação In-Loco**: escrita e edição de código assistida por 3 modalidades: Passiva (*Antigravity Tab* / *Supercomplete* / *Tab to Jump*), Instrutiva (`Ctrl+I` inline) e Colaborativa (Sidebar Chat, *Inline Code Lenses* e *Visual Diff Overlays*). | **App Data:** `/home/nandodev/.gemini/antigravity-ide/`<br>**Config/Server:** `~/.antigravity/`, `~/.antigravity-ide-server/`, `~/.config/Antigravity/` |
| **Antigravity CLI (`agy`)** | Binário nativo compilado (~227 MB) com interface TUI e modo headless. | **Terminal, Automação Shell e SSH**: execução ultrarrápida no terminal, composição em scripts bash, servidores remotos e invocação por bancas multi-agente (`conselho-seniores`). | **Binário:** `/home/nandodev/.local/bin/agy`<br>**App Data & Config:** `/home/nandodev/.gemini/antigravity-cli/` (`settings.json`, `keybindings.json`, `statusline.sh`) |
| **IDE Extensions vs. AGY Customizations** | Duas camadas:<br>1. Extensões VSIX do editor (LSP, linter, temas).<br>2. Customizações do Agente (Rules, Skills, Plugins, Hooks, MCPs, Sidecars). | **Acoplamento do Harness**: enquanto extensões VSIX auxiliam apenas o editor visual na IDE, as customizações em `~/.gemini/config/` e `<repo>/.agents/` moldam o comportamento do agente em **todas** as superfícies. | **Customizações Globais:** `/home/nandodev/.gemini/config/` (`plugins/`, `skills/`, `rules/`, `hooks/`, `sidecars/`)<br>**Dados de Plugins:** `~/.gemini/antigravity/plugin_data/` |
| **Antigravity SDK (`google-antigravity`)** | Pacote Python (`pip install google-antigravity`) com binário do runtime embutido. | **Agentes Programáticos em Código Python**: instanciar `Agent`, `Conversation` e `Connection` dentro de scripts/aplicações Python, com suporte a Gemini API, Vertex AI, modelos locais (`LiteRTAgentConfig` / `LocalOpenAIAgentConfig`), Pydantic *Structured Output* e políticas de segurança programáticas. | **Ambiente Python:** `venv` do projeto (`import google.antigravity`)<br>**Docs locais:** `~/.gemini/config/plugins/google-antigravity-sdk/` |

### 2. Unificação de Memória e Estado via Symlinks (`OBSERVED`)

A inspeção física em `/home/nandodev/.gemini/` revelou um detalhe arquitetural determinante na máquina do autor:

- Tanto `/home/nandodev/.gemini/antigravity/` (App 2.0) quanto `/home/nandodev/.gemini/antigravity-ide/` (IDE) possuem symlinks simbólicos para:
  - `brain -> /home/nandodev/.gemini/antigravity-cli/brain`
  - `conversations -> /home/nandodev/.gemini/antigravity-cli/conversations`
  - `annotations -> /home/nandodev/.gemini/antigravity-cli/annotations`
  - `knowledge -> /home/nandodev/.gemini/antigravity-cli/knowledge`
- **Implicação prática:** Toda conversa, artefato gerado no `brain/<conversation-id>` e item de memória iniciado na **Antigravity IDE** ou na **CLI (`agy`)** fica imediatamente acessível no **Antigravity 2.0 (App)** sem perda de estado.

### 3. Ordem de Precedência do Sistema de Customização (`OBSERVED`)

Quando o agente carrega o harness do usuário, ele resolve conflitos seguindo estritamente a hierarquia (da maior para a menor prioridade):

1. **Workspace Project**: Descoberta hierárquica subindo do diretório atual até a raiz do repositório (`AGENTS.md`, `GEMINI.md`, `.agents/rules/`, `.agents/skills/`).
2. **Declared Configurations**: Arquivos `skills.json` ou `plugins.json` declarados no workspace.
3. **Global Discovery**: `/home/nandodev/.gemini/config/` (onde residem `clearer-engineering`, `hooks.json`, `guard_destructive.py` e skills globais).
4. **Built-in Customizations**: Skills nativas empacotadas em `~/.gemini/antigravity/builtin/skills/`.
5. **Global Declared Configurations**: Configurações JSON globais.

## Reflexões e inferências
 
- **Divisão Ótima de Trabalho (Antigravity 2.0 vs. Antigravity IDE):**
  - Para este repositório (`verificador-deterministico`), cujo foco é investigação, leitura crítica de fontes, geração de relatórios determinísticos e orquestração de subagentes, o **Antigravity 2.0 (App)** é a superfície superior porque dedica a tela ao *Chat Canvas* e ao *HTML Auxiliary Pane* (visualização rica de artefatos e subagentes), livre de distrações de edição de código.
  - A **Antigravity IDE** deve ser reservada para momentos de implementação pesada em código-fonte, onde *Antigravity Tab*, *Supercomplete*, `Ctrl+I` e *Code Lenses* aceleram a escrita.
- **Potencial de Evolução (Antigravity SDK + Verificador Determinístico):**
  - O `google-antigravity` Python SDK permite transformar o protocolo deste repositório (`PROTOCOLO.md`) em um pipeline Python executável e auditável, combinando *Constrained Decoding* (Pydantic schemas) com subagentes isolados em sandbox.

### Síntese das 3 Frentes Analisadas (`OBSERVED`)

1. **Frente 1 (Customizações & Precedência):**
   - O Antigravity prioriza o Workspace Project (`AGENTS.md` / `PROTOCOLO.md`) sobre o Global (`~/.gemini/config/`), permitindo regras contextuais estritas sem poluir a configuração global.
   - Os hooks do Antigravity operam sob 6 eventos (`SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`).
2. **Frente 2 (Antigravity Python SDK):**
   - Desacoplamento arquitetural em `Agent`, `Conversation` e `Connection`.
   - Suporte nativo a *Constrained Decoding* via Pydantic (`response_schema`), subagentes com teto de profundidade (`max_subagent_depth`) e políticas declarativas com predicados (`policy.deny(..., when=...)`) e OS sandboxing.
3. **Frente 3 (Ergonomia App 2.0 & agy CLI):**
   - No Antigravity 2.0, o painel *Overview* integra VCS Git nativo (`Review` com *Agent Edits*, *Uncommitted* e *Branch* vs. `origin/main`), navegador de arquivos (`Files`) e terminal embutido (`Terminal`).
   - Sinergia perfeita com o binário compilado `agy` (CLI), compartilhando a mesma base de estado via symlinks.

## Ponto de Convergência & Implementação (Anti-Over-Engineering)

Ao confrontar as 3 frentes contra os princípios de **Staff Engineering** e a **Escada de Decisão Ponytail v5**:
- O Python SDK (Frente 2) e a Ergonomia da UI (Frente 3) foram identificados como over-engineering se incorporados diretamente ao core do harness.
- A **única oportunidade cirúrgica de alto valor e baixo blast radius** foi a criação de um **Stop Hook** no harness (`clearer-engineering`).

### A Entrega Implementada: `ceh-stop-guard`
- **Script:** `clearer-engineering/scripts/ceh-stop-guard.py`
- **Manifesto:** `clearer-engineering/hooks.json` atualizado com o evento `Stop` (timeout: 10s).
- **Comportamento:** Ao final do turno (`NO_TOOL_CALL`), se o agente realizou alterações em arquivos mas não emitiu o `Response Contract` com evidências `OBSERVED`, o hook intercepta deterministricamente com `"decision": "continue"` e instrui o fechamento auditável.
- **Testes Determinísticos:** Suíte unitária criada em `test_stop_guard.py` com 4 cenários (100% PASS), validada pela suíte rápida de empacotamento (`test_package.py`).
- **Instalação Local:** Sincronizado para `~/.gemini/config/plugins/clearer-engineering/scripts/ceh-stop-guard.py` e ativado em `~/.gemini/config/hooks.json`.

## Status da Discussão

- **Concluída com Implementação**: Arquitetura dissecada, frentes mapeadas e melhoria cirúrgica commitada na branch `dev` do repositório `clearer-engineering-harness`.

## Fechamento (contrato de resposta)

```
Resultado:   Discussão consolidada com a análise exaustiva das 3 frentes e implementação cirúrgica do hook ceh-stop-guard na branch dev do clearer-engineering-harness, ativado no Antigravity 2.0.
Evidências:
  OBSERVED:  - clearer-engineering/scripts/ceh-stop-guard.py criado e testado (4/4 PASS em test_stop_guard.py).
             - clearer-engineering/hooks.json atualizado e validado contra test_package.py (6/6 PASS).
             - Commit 8055f52 gerado na branch dev de /home/nandodev/projects/clearer-engineering-harness.
             - ~/.gemini/config/hooks.json atualizado com o ceh-stop-guard ativo globalmente no Antigravity 2.0.
  INFERRED:  - O fechamento do loop de engenharia do CEH agora é garantido tanto no início das ferramentas (safety-gate) quanto no encerramento da resposta (stop-guard).
  UNKNOWN:   - Nenhum.
Confiança:   ALTA — ciclo completo validado com suíte de testes determinísticos e commit limpo.
```

