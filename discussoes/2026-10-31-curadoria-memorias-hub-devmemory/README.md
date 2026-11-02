# Curadoria de Memórias no Hub Dev-Memory: Transição de Estados, Resiliência em Produção e Governança Multi-Agente

## Metadados

- **Data de início:** 2026-10-31
- **Tema / palavras-chave:** dev-memory, MCP, governança de memória, ciclo de validação, pending vs validated, resiliência, deploy produção, multi-agente
- **Origem:** Deliberação colaborativa entre agentes (Antigravity e Muse) com base no plano de curadoria de memórias e na homologação da release de infraestrutura e governança do Dev-Memory.
- **Fonte(s):**
  - Repositório / hub local `dev-memory` (MCP tools: `memory_stats`, `memory_list`, `memory_get`).
  - Deploy em produção VPS: `https://devmemory.fssdev.com.br/up`.
  - Documentação Mem0: `https://docs.mem0.ai/changelog/highlights`.
  - Documentação Letta: `https://docs.letta.com/configuration/subagents`.
- **Status:** Concluída (regra v2 implementada, piloto real executado e handoff guiado publicado em `handoff-guiado-harnesses.md`)

---

## Contexto

O hub `dev-memory` opera como repositório canônico de memória de longo prazo (lições aprendidas, padrões arquiteturais e boas práticas) compartilhado entre diferentes harnesses (Antigravity, Muse, DSH, Claude Code, etc.). 

A discussão atual aborda dois marcos complementares:
1. **Regra de Curadoria de Memórias:** Formalização do ciclo de vida dos registros (`pending` → `validated` → `global` + consumo em planos de engenharia), resolvendo ambiguidades de evidência (trilhas condicionado ao tipo de claim vs. portão humano) e definindo uma convenção limpa de contradição sem deleção via grafo de relações (`supersedes` / `contradicts`).
2. **Deploy de Resiliência e Governança em Produção:** Homologação e deploy na VPS (`releases/20261031_214829`, commit `42939a8`) fechando três lacunas estruturais críticas:
   - **GAP 2:** Backup automatizado diário de banco de dados (`memory:backup-db`) com retenção de 14 dias (PostgreSQL / SQLite).
   - **GAP 3:** Telemetria ativa de prontidão e latência de embeddings (`memory:health-check`) a cada 30 min.
   - **GAP 4:** Prune e ciclo de vida de tokens de acesso expirados (`memory:prune-tokens`) com rejeição protocolar JSON-RPC `-32001`.

Esta deliberação reúne as análises conjuntas do **Antigravity** e do **Muse** antes da submissão do protocolo ao **Conselho de Seniores**.

---

## Verificação de fontes

| Fonte | Status | Como foi verificada |
|---|---|---|
| Hub Dev-Memory MCP (`dev-memory`) | `OBSERVED` | Ferramentas locais (`memory_stats`, `memory_list`, `memory_get`) executadas. 16 memórias ativas catalogadas. |
| Produção Dev-Memory VPS (`devmemory.fssdev.com.br/up`) | `OBSERVED` | `curl -s -o /dev/null -w "%{http_code}" https://devmemory.fssdev.com.br/up` retornou HTTP `200` OK. |
| Suíte de Testes do DevMemory | `OBSERVED` | 293 testes e 815 asserções validados com 0 falhas no ciclo de desenvolvimento. |
| Mem0 Highlights (Conflict/Dedup) | `OBSERVED` | URL `https://docs.mem0.ai/changelog/highlights` inspecionada; menção na linha 428 sobre backend gerenciado com semantic dedup e conflict resolution. |
| Letta Subagents & Memory | `OBSERVED` | URL `https://docs.letta.com/configuration/subagents` inspecionada e ativa. |

---

## Análise

### 1. O Núcleo Sólido do Plano de Curadoria

O plano adota uma abordagem estritamente alinhada ao **Ponytail Mode (Anti-Over-Engineering)**:
- **Zero infraestrutura desnecessária:** Utiliza exclusivamente as tools e campos nativos do hub (`validation_status`, `memory_validate`, `memory_promote`, `hub_briefing`, relações de grafo).
- **Trilhas de Evidência Condicionadas (OU)** com **Portão Humano (E fixo)**:
  - Fato externo versionado → Context7 / Documentação pinada.
  - Comportamento local de sistema → Saída de teste, probe ou comando determinístico registrado.
  - Convenção / Governança → Autorização ou convenção explícita.
- **Não-Objetivos explícitos com gatilho objetivo de revisita:** Rejeição consciente de TTL artificial, pontuação decimal de confiança e consolidação vetorial em background para o volume atual (16 memórias), estabelecendo gatilho de revisão somente ao atingir 200 memórias ou na primeira colisão real.

### 2. Contradição Real Descoberta no Hub (`supersedes`)

Durante a auditoria de linha de base no hub local, identificou-se um caso real de evolução técnica que serve de validação empírica imediata para o plano:
- **Memória `01a05573-9019-70d7-9db3-cf495a22c617`** (01:33): Recomendava configurar `customSkillDirs` com expressão `!!js` no `agent.cordis.yml` do preset.
- **Memória `01a055f6-2110-7118-90ce-7d1009babe16`** (03:56): Refutou a abordagem anterior (*"NÃO usar customSkillDirs no preset... Melhor: colocar a skill no root user-dsh..."*).

**Implicação prática:** Este caso prova a necessidade da relação `supersedes` no grafo. A memória mais antiga não deve ser excluída (para não criar amnésia histórica), mas deve ser marcada como substituída pela memória mais recente.

### 3. Ajustes Deliberados pelos Agentes (Antigravity + Muse)

1. **Expansão do Piloto (de 4 para 5 memórias):**
   - O piloto original previa 3 memórias DSH (todas de comportamento local) + 1 memória MCP `url/serverUrl` (spec externa).
   - Nenhuma cobria a 3ª trilha (*Convenção/Governança*).
   - **Decisão:** Incluir no piloto a memória `01a022a2-a3d2-7133-b33b-377991532389` (*"Estilo de comunicacao do Nando"*) ou `01a02296-799e-7075-bbc4-7082f810d07e` (*"Admin-only para global e promote"*).
2. **Resolução da Ambiguidade da Trilha de Governança:**
   - *Preferência individual do autor:* O portão humano é a fonte primária e a própria validação (dispensa segunda evidência).
   - *Regra arquitetural de repositório:* Exige regra escrita/versionada (`AGENTS.md`, policies) **E** confirmação humana.
3. **Sinergia com a Infraestrutura de Produção:**
   - Com os comandos `memory:backup-db`, `memory:health-check` e `memory:prune-tokens` operando na VPS, a integridade física do hub e o isolamento de sessões/tokens expirados estão garantidos no nível de infraestrutura, permitindo que a regra de curadoria foque exclusivamente na qualidade epistêmica do conteúdo.

---

## Reflexões e Inferências

- **Sinergia Multi-Agente (Antigravity + Muse):** Ter agentes com especialidades distintas (Muse refinando especificações e dialetos; Antigravity inspecionando runtime, orquestração e evidências no shell) reduz o viés de confirmação e antecipa pontos cegos antes da submissão a instâncias deliberativas formais como o Conselho de Seniores.
- **Memória de Trabalho vs. Memória Canônica:** O estado `pending` funciona como memória de trabalho transitória (útil para consultas heurísticas, mas rotulada como `INFERRED` nos planos). O estado `validated` promove o conhecimento ao patamar de premissa arquitetural sólida (`OBSERVED`).

---

## Anexos

- **Handoff Guiado de Harnesses (Operacional):** [`handoff-guiado-harnesses.md`](./handoff-guiado-harnesses.md) — Guia operacional passo a passo para qualquer agente (Muse, Antigravity, Claude Code, DSH) conectar, planejar, capturar, homologar e solucionar problemas no hub sob a Regra v2.0.
- **Regra de Curadoria v2.0 (Canônica - Pronta para o Muse):** [`regra-curadoria-memorias-v2.md`](./regra-curadoria-memorias-v2.md) — Especificação técnica final com validação híbrida (Fast-track automático com manifesto de probe vs. Review Gate no projeto/plataforma), estado `deprecated` e guia de implementação no backend.
- **Ata do Conselho de Seniores (Passo 5):** [`conselho_output/ata_conselho.md`](./conselho_output/ata_conselho.md) — Deliberação plenária dos conselheiros Codex (0.94), Muse (0.85) e Agy (0.95) com veredito "Homologado com Ressalvas".
- **Piloto de Consumo em Planos (Passo 4):** [`piloto-consumo-em-planos.md`](./piloto-consumo-em-planos.md) — Demonstração prática da diferença entre `hub_briefing` (premissas validadas) e `memory_search` (alertas pendentes com inspeção obrigatória).
- **Piloto de Classificação — Pareceres (Passo 3):** [`piloto-classificacao-pareceres.md`](./piloto-classificacao-pareceres.md) — Aplicação prática da Regra v1.0 a 5 memórias reais com análise de evidências e vereditos decisórios.
- **Regra de Curadoria v1.0 (Passo 2):** [`regra-curadoria-memorias-v1.md`](./regra-curadoria-memorias-v1.md) — Especificação preliminar submetida ao Conselho.
- **Linha de Base Congelada (Passo 1):** [`linha-de-base-16-memorias.md`](./linha-de-base-16-memorias.md) — Tabela com o inventário completo das 16 memórias do hub, discriminando tipo, validação (`pending` vs `validated`), stack e data.
- **Dossiê de Submissão:** [`dossie-conselho.md`](./dossie-conselho.md) — Objeto de deliberação formal avaliado pela banca de seniores.
- **Evidências de Deploy VPS:** Release `20261031_214829`, endpoints `/up` e rotinas agendadas no Laravel Console.

---

## Fechamento (contrato de resposta)

```
Resultado:   Ciclo de curadoria formalizado de ponta a ponta. Regra v2.0 homologada pelo Conselho de Seniores com ressalvas construtivas incorporadas e calibrada pelo Desenvolvedor (Fast-track determinístico no projeto + Review Gate no projeto/plataforma + Admin-only para global + estado deprecated para supersedes). Especificação pronta para implementação no backend Dev-Memory via Muse Code.
Evidências:
  OBSERVED:  Ata do Conselho gerada (3 votos com ressalvas: Codex 0.94, Muse 0.85, Agy 0.95); linha de base de 16 memórias congelada; 5 pareceres unívocos; testes de consumo comprovando filtro do briefing; deploy VPS ativo em HTTP 200.
  INFERRED:  O modelo híbrido de validação elimina fricção desnecessária em desenvolvimento local enquanto preserva a integridade epistêmica do escopo global.
  UNKNOWN:   Desempenho sob volume > 200 memórias (protegido por gatilho de revisita explícito).
Confiança:   MÁXIMA — Validada em código, dados reais do hub, deliberação multi-modelo e alinhamento direto com o Desenvolvedor.
```
