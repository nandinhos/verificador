# Regra de Curadoria de Memórias no Hub Dev-Memory (v1.0)

> **Documento de especificação técnica e governança epistêmica.**  
> Define os estados, transições, trilhas de evidência, portões de aprovação e disciplina de consumo de memórias compartilhadas no ecossistema multi-harness (Antigravity, Muse, DSH, Claude Code).

---

## 1. Estados e Ciclo de Vida

Toda memória persistida no hub `dev-memory` percorre um ciclo formal de maturidade baseado em dois eixos ortogonais: **Escopo** (`scope`) e **Validação** (`validation_status`).

```
                [ memory_create ]
                        │
                        ▼
            ┌───────────────────────┐
            │   Status: pending     │ ◄─── Captura sem fricção (higiene local)
            │   Scope:  project     │      Consumo em planos: INFERRED (alerta)
            └───────────┬───────────┘
                        │
         [ Trilhas de Evidência + Gate Humano ]
                        │
                        ▼
            ┌───────────────────────┐
            │   Status: validated   │ ◄─── memory_validate
            │   Scope:  project     │      Consumo em planos: OBSERVED (premissa local)
            └───────────┬───────────┘
                        │
                 [ Gate Admin ]
                        │
                        ▼
            ┌───────────────────────┐
            │   Status: validated   │ ◄─── memory_promote (admin-only)
            │   Scope:  global      │      Conhecimento canônico cross-harness
            └───────────────────────┘
```

### Invariantes de Estado:
1. **Captura sem fricção:** Nenhuma memória nova é bloqueada na ingestão. Ela nasce como `pending` com custo zero de validação.
2. **Promover exige validação prévia:** É proibido promover ao escopo `global` uma memória com status `pending`.
3. **Admin-only no escopo global:** `memory_promote` e criação direta de memórias globais são restritas a tokens administrativos. Agentes operando com tokens padrão criam em `project` e submetem para promoção humana.

---

## 2. As Trilhas de Evidência & O Portão Humano

Para transitar de `pending` para `validated` (`memory_validate`), o registro deve cumprir a fórmula decisória:

$$\text{Validação} = (\text{Trilha A} \lor \text{Trilha B} \lor \text{Trilha C}) \land \text{Portão Humano}$$

### 2.1 As 3 Trilhas de Evidência (OU Condicional)

A trilha exigida é determinada estritamente pela **natureza do claim principal**:

| Trilha | Tipo de Claim | Evidência Mandatória Requerida | Juiz / Fonte da Verdade |
|---|---|---|---|
| **Trilha A** | **Fato Externo Versionado** (APIs de terceiros, specs, libs, protocolos, formatos) | Consulta a documentação oficial pinada na versão exata (Context7, doc oficial) **OU** teste de integração contra o serviço real. Sem confirmação executável local, a regra externa permanece como hipótese `INFERRED`. | Context7 MCP / Docs oficiais / RFC |
| **Trilha B** | **Comportamento Local de Sistema** (gotchas de SO, shell, Docker, flags de build, timeouts, traps) | Execução registrada de comando, script probe ou teste determinístico em sandbox reproduzindo sintoma e fix com `Exit Code 0`. | Saída bruta de terminal (`OBSERVED`) |
| **Trilha C** | **Convenção e Governança** (diretrizes de código, estilo, segurança de equipe, preferências) | Subdividida em 2 categorias:<br>1. *Preferência pessoal do autor* (tom, idioma, estilo Telegram): Validação direta pelo autor (o portão humano é a evidência primária).<br>2. *Regra arquitetural de repositório* (ex: "proibido raw queries", "permissão 0600 em chaves"): Regra escrita e versionada (`AGENTS.md`, policies) citando arquivo e linha. | Política versionada no Git ou autorização direta |

### 2.2 O Portão Humano (E Fixo)
- Toda validação exige confirmação humana explícita.
- Nenhuma IA ou agente autônomo pode auto-validar suas próprias memórias sem aprovação humana registrada no chat ou no painel.

### 2.3 Regra da Memória Mista (Anti-Contaminação)
Se uma lição contiver claims de mais de uma trilha (ex: um gotcha local de Docker que depende de uma spec externa do Redis):
- **Opção 1 (Conjunção):** Deve satisfazer o operador lógico $\mathbf{E}$ entre todas as trilhas envolvidas (Trilha A $\land$ Trilha B $\land$ Humano).
- **Opção 2 (Desmembramento - Recomendada):** Fatiar em 2 memórias atômicas separadas conectadas por relação no grafo (`relates_to`).

---

## 3. Disciplina de Consumo ao Planejar

Quando um agente abre um plano de engenharia e consulta o hub (`hub_briefing` ou `memory_search`), a categorização epistemológica das lições recebidas é obrigatória:

1. **Memória com `validation_status: "validated"`:**
   - Tratada como **Premissa Concreta (`OBSERVED`)**.
   - Incorporada diretamente na arquitetura e nas restrições do plano.
2. **Memória com `validation_status: "pending"`:**
   - Tratada como **Alerta Heurístico (`INFERRED`)**.
   - Proibido adotar como fato consolidado. O plano deve registrar como hipótese a ser verificada por um probe antes da implementação: *"Alerta pendente do hub requer teste prévio"*.

---

## 4. Tratamento de Contradição sem Deleção (Grafo de Relações)

Quando uma nova lição ou fato técnico refuta, corrige ou atualiza uma memória existente:

1. **Proibição de Deleção Amnésica:** NUNCA deletar a memória antiga. O histórico de decisões erradas ou de comportamentos de versões anteriores é patrimônio epistêmico do time.
2. **Uso de Arestas Semânticas:**
   - Criar relação `supersedes` da memória nova apontando para a antiga (ex: Memória Nova $\xrightarrow{\text{supersedes}}$ Memória Antiga).
   - Se houver conflito não resolvido entre duas hipóteses concorrentes, vincular ambas com `contradicts`.
3. **Consumo de Memória Substituída:**
   - Ao recuperar uma memória que possua aresta de entrada `supersedes`, o agente deve desconsiderar a recomendação antiga e adotar a nova, citando a relação.

---

## 5. Não-Objetivos & Gatilhos de Revisita (Anti-Over-Engineering)

Fica formalmente estabelecido que **NÃO** serão implementados nesta fase:
- Scores de relevância probabilística ou decaimento temporal (decay/TTL).
- Algoritmos de consolidação semântica autônoma em segundo plano (sleep-time dreaming).
- Mecanismos de bitemporalidade em banco de dados.

### Gatilhos Objetivos para Revisão da Regra:
1. O hub ultrapassar **200 memórias** ativas.
2. Ocorrer a primeira **contradição real entre duas memórias validadas** sem relação de grafo prévia.
3. Um plano de produção ser **contaminado ou quebrado por uma memória pendente tratada como fato**.
