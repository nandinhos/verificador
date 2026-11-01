# Regra de Curadoria de Memórias no Hub Dev-Memory (v2.0)

> **Documento Canônico de Especificação Técnica e Governança Epistêmica.**  
> Homologado com ressalvas pelo Conselho de Seniores (Codex, Muse, Agy) e calibrado pelo Desenvolvedor.  
> **Pronto para implementação no backend Dev-Memory via Muse Code.**

---

## 1. Estados, Escopos e Transições

O ciclo de vida das memórias no hub é modelado em dois eixos ortogonais: **Escopo** (`scope`) e **Status de Validação** (`validation_status`).

### 1.1 Tabela de Estados

| Campo | Valores Permitidos | Significado |
|---|---|---|
| **`scope`** | `project` | Conhecimento circunscrito ao workspace ou repositório de origem. |
| | `global` | Conhecimento canônico cross-harness compartilhado (Antigravity, Muse, DSH, Claude Code). |
| **`validation_status`** | `pending` | Memória capturada sem comprovação formal completa; consumida como alerta `INFERRED`. |
| | `validated` | Memória aprovada por requisitos determinísticos ou revisão humana; consumida como premissa `OBSERVED`. |
| | `deprecated` | Memória historicamente superada ou refutada por relação `supersedes`; excluída de briefings automáticos. |

### 1.2 Diagrama de Transição de Estados

```
                          [ Ingestão: memory_create ]
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
   [ Cumpre Requisitos Formais                           [ Requisitos Incompletos /
     de Validação Automática ]                             Heurísticas / Governança ]
            │                                                     │
            ▼                                                     ▼
 ┌──────────────────────┐                              ┌──────────────────────┐
 │ Status: validated    │                              │ Status: pending      │
 │ Scope:  project      │                              │ Scope:  project      │
 └──────────┬───────────┘                              └──────────┬───────────┘
            │                                                     │
            │                                      ┌──────────────┴──────────────┐
            │                                      ▼                             ▼
            │                            [ Validação Explícita         [ Validação Web
            │                              no Projeto / Chat ]           na Plataforma ]
            │                                      │                             │
            │                                      └──────────────┬──────────────┘
            │                                                     │
            │                                                     ▼
            │                                          ┌──────────────────────┐
            │                                          │ Status: validated    │
            │                                          │ Scope:  project      │
            │                                          └──────────┬───────────┘
            │                                                     │
            └──────────────────────────┬──────────────────────────┘
                                       │
                     [ Portão Admin / Plataforma Web ]
                                       │
                                       ▼
                           ┌───────────────────────┐
                           │ Status: validated     │
                           │ Scope:  global        │
                           └───────────┬───────────┘
                                       │
                         [ Registro de supersedes ]
                                       │
                                       ▼
                           ┌───────────────────────┐
                           │ Status: deprecated    │
                           │ Scope:  global        │ ◄── Excluída de hub_briefing
                           └───────────────────────┘
```

---

## 2. Mecanismo Híbrido de Validação (Fast-Track vs. Review Gate)

### 2.1 Validação Automática no Projeto (`Fast-Track` Local)

Uma memória recém-criada é promovida imediatamente para `validation_status: "validated"` no escopo `project` se, e somente se, atender cumulativamente aos requisitos específicos da sua trilha:

#### Requisitos da Trilha B (Comportamento Local de Sistema):
1. **Probe com Exit Code 0:** Execução de probe, comando ou teste automatizado no repositório finalizado com código de retorno `0`.
2. **Asserção Não-Vazia:** O log ou saída deve conter asserção explícita comprovando o comportamento (proibido validar apenas porque o comando não abortou).
3. **Manifesto Mínimo de Plataforma:** O registro deve conter os metadados de execução:
   - Sistema e arquitetura (`uname -sm`, ex: `Linux x86_64`).
   - Interpretador ou runtime (`bash 5.2`, `python 3.12`, `php 8.3`).
   - Commit hash ou tag de referência do repositório.
4. **Sanitização Zero-Leak:** Ausência total de credenciais, chaves privadas ou tokens em texto plano.

#### Requisitos da Trilha A (Fato Externo Versionado):
1. **Documentação Pinada:** Citação de RFC, documentação oficial ou Context7 com versão exata do pacote/protocolo.
2. **Teste de Integração Local:** Teste determinístico aprovado contra o serviço/API real no ambiente do projeto.

---

### 2.2 Validação Pendente (`Fallback Review-Gated`)

Se qualquer um dos requisitos formais acima não for cumprido no momento da criação, a memória nasce compulsoriamente como:
- `validation_status: "pending"`
- `scope: "project"`

#### Como a Memória Pendente é Validada:
1. **No Projeto (In-Session):** O desenvolvedor emite aprovação explícita no chat (`"homologar a memória X"`), autorizando o agente a invocar `memory_validate(id)`.
2. **Na Plataforma (Web Admin):** O desenvolvedor acessa o painel web administrativo do Dev-Memory (`https://devmemory.fssdev.com.br`) e clica em validar.

---

### 2.3 Salvaguarda Inviolável: Escopo Global

- A promoção para `scope: global` permanece **estritamente restrita a administradores** (`admin-only`).
- Nenhuma IA ou agente autônomo pode auto-promover memórias locais para o escopo global.
- A promoção para global deve ser deliberada na plataforma web ou via credencial administrativa, auditando a portabilidade do conhecimento para outros sistemas.

---

## 3. Máquina de Substituição e Depreciação (`supersedes`)

Quando uma nova lição refuta ou atualiza uma memória validada existente:

1. **Aresta no Grafo:** O agente cria a relação semântica:
   $$\text{Memória Nova} \xrightarrow{\text{supersedes}} \text{Memória Antiga}$$
2. **Transição para Deprecated:** No momento em que a aresta `supersedes` é confirmada:
   - A memória antiga transita para `validation_status: "deprecated"`.
   - A memória antiga **NUNCA** é deletada do banco de dados (preservação do patrimônio epistêmico).
3. **Isolamento de Briefing:** O endpoint `hub_briefing` ignora sumariamente qualquer registro com status `deprecated`, impedindo que lições obsoletas colidam com regras vigentes.

---

## 4. Disciplina de Consumo ao Planejar

Ao consultar o hub na fase de planejamento de tarefas:

1. **`validated`:** Injetada como **Premissa Arquitetural (`OBSERVED`)**. Deve ser respeitada diretamente no código e nas decisões.
2. **`pending`:** Injetada como **Alerta Heurístico (`INFERRED`)**. O agente é proibido de assumi-la como verdade sem executar um probe preliminar (Step 0) no início da tarefa.
3. **`deprecated`:** Injetada apenas para **Contexto Histórico / Prevenção de Regressão**. Não pode ser recomendada como padrão ativo.

---

## 5. Especificação de Implementação no Backend (Guia para o Muse)

Para o agente **Muse** implementar as melhorias no repositório do `dev-memory`:

### 5.1 Schema do Banco de Dados
- Estender o enum de `validation_status` na tabela `memories`:
  ```sql
  -- pending, validated, deprecated
  ALTER TYPE validation_status_enum ADD VALUE IF NOT EXISTS 'deprecated';
  ```

### 5.2 Endpoint / Tool `memory_search`
- **Requisito Ergonomico:** Adicionar obrigatoriamente a propriedade `validation_status` no JSON de retorno de cada item retornado por `memory_search`, evitando chamadas secundárias de `memory_get`:
  ```json
  {
    "id": "01a055f6-...",
    "title": "...",
    "validation_status": "pending",
    "scope": "global",
    "similarity": 0.6065
  }
  ```

### 5.3 Endpoint / Tool `hub_briefing`
- Garantir que a query do briefing filtre exclusivamente memórias ativas:
  ```sql
  WHERE validation_status = 'validated' 
    AND id NOT IN (SELECT target_id FROM relations WHERE type = 'supersedes')
  ```

### 5.4 Tool `memory_create` (Fast-Track)
- Permitir que agentes enviem metadados de probe (`probe_exit_code`, `probe_platform`, `probe_output_hash`) no payload de criação. Se válidos, o backend persiste diretamente como `validation_status: "validated"` e `scope: "project"`.

---

## 6. Nota de Implementação (2026-10-31, Muse)

Implementado no backend `dev-memory-laravel` (branch `dev`), com **uma divergência
homologada pelo Desenvolvedor**: o estado `deprecated` (§1.1/§5.1) foi mapeado para o
estado já existente **`superseded`** (`ValidationStatus::SUPERSEDED`, CHECK e UI prontos).
O SQL `ALTER TYPE ... ADD VALUE 'deprecated'` não se aplica: `validation_status` é
`string` + CHECK, sem tipo enum no Postgres. Demais itens: §5.2 (projeção em
`memory_search`), §5.3 (exclusão de alvos `supersedes` no briefing), §5.4 (fast-track
com zero-leak via `CaptureSanitizer`) e §3 (transição na aprovação da relação, sem
deleção) implementados com testes em `tests/Feature/CurationV2Test.php`.
Complemento homologado na mesma rodada: trilha de auditoria persistida em
`validation_evidence` (JSON: track/probe/plataforma/hash/versão) +
`validated_at`/`validated_by=fast-track:*`, e Trilha A automática
(`official_reference` + `reference_version` pinada + probe de integração).
