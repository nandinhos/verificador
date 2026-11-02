# Piloto de Consumo em Planos — Demonstração Prática (`hub_briefing` vs `memory_search`)

> **Data de execução:** 2026-10-31 22:48 BRT  
> **Objetivo:** Simular o consumo real de memórias na abertura de um plano de engenharia sob a Regra v1.0, demonstrando a distinção entre premissas (`OBSERVED`) e alertas (`INFERRED`).  
> **Evidências Executadas:** Chamadas reais a `hub_briefing(topic: "DSH")`, `hub_briefing(topic: "MCP")` e `memory_search(query: "DSH")`.

---

## 1. Comportamento Físico das Ferramentas do Hub (`OBSERVED`)

Durante os testes do piloto, foi observada uma distinção arquitetural fundamental no comportamento do backend:

| Ferramenta | O que Retorna | Tratamento do `validation_status` | Risco Epistêmico se Não Houver Regra |
|---|---|---|---|
| **`hub_briefing`** | Pacote consolidado por tópico (`approved_patterns` + `relevant_lessons`). | **Filtra exclusivamente registros `validated`.** As 4 memórias `pending` foram omitidas de `relevant_lessons`. | Baixo: briefing só entrega conhecimento aprovado. |
| **`memory_search`** | Busca híbrida (vetorial + texto) por similaridade. | **Retorna registros `pending` e `validated` misturados** sem projetar o campo `validation_status`. | **ALTO:** Um agente pode ler uma memória `pending` do topo da busca e tratá-la ingenuamente como fato consolidado. |

---

## 2. Demonstração Prática do Consumo na Abertura de Plano

### Cenário 1: Plano de Engenharia Envolvendo o DeepSeek Harness (DSH)

#### 1. Consulta Inicial via `hub_briefing(topic: "DSH")`:
* **Saída Observada:** 7 padrões aprovados + 5 lições relevantes.
* **Achado:** Nenhuma das 3 memórias específicas de DSH apareceu em `relevant_lessons`, pois todas as 3 possuem `validation_status: "pending"` no banco.

#### 2. Busca Complementar via `memory_search(query: "DSH")`:
* **Saída Observada:** A busca retornou no topo:
  1. `01a055f6` (rank 1, similaridade 0.6065) — *user-dsh root*
  2. `01a05573` (rank 2, similaridade 0.5626) — *preset customSkillDirs*
  3. `01a05547` (rank 3, similaridade 0.5117) — *catálogo de modelos*

#### 3. Aplicação Mandatória da Disciplina da Regra v1.0 (§ 3):
O agente executor disparou `memory_get` sobre os resultados e verificou que os 3 registros são `pending`. 

**Como o Plano de Engenharia deve abrir (Contrato Epistêmico):**

```markdown
### Premissas Arquiteturais (`OBSERVED`):
- O hub não possui lições validadas específicas para DSH em `hub_briefing`. As diretrizes globais vigentes (mascaramento de chat, permissão 600 em credenciais) são premissas ativas.

### Alertas Heurísticos / Hipóteses (`INFERRED` - Origem: Hub dev-memory):
> [!WARNING] Alerta de Memória Pendente (01a055f6 e 01a05573):
> Existem duas hipóteses não validadas no hub sobre registro de skills no DSH. A memória mais recente (01a055f6) adverte que NÃO se deve usar `customSkillDirs` no preset porque quebra cópias, recomendando `<dshHome>/skills/`.
> Ação no Plano: O plano NÃO pode assumir nenhuma das duas como fato consumado. Deve incluir uma etapa preliminar de probe rápido (Step 0) para testar a descoberta de skills antes da implementação.
```

---

### Cenário 2: Plano de Engenharia Envolvendo Configuração MCP

#### 1. Consulta via `hub_briefing(topic: "MCP")`:
* **Saída Observada:** A lição `01a19496-2ead-7337-b691-312894e4a41a` (*"Tratar url+serverUrl em MCP HTTP como poliglota, nao redundancia"*) foi retornada formalmente em `relevant_lessons`.
* **Status via `memory_get`:** `validated`.

**Como o Plano de Engenharia deve abrir (Contrato Epistêmico):**

```markdown
### Premissas Arquiteturais (`OBSERVED` - Origem: Hub dev-memory):
- Conforme a lição validada `01a19496`, blocos de configuração MCP HTTP compartilhados entre múltiplos harnesses (Antigravity, Muse) DEVEM declarar obrigatoriamente as chaves `url` e `serverUrl` idênticas para compatibilidade entre dialetos, sendo proibida a remoção de qualquer uma delas sem teste A/B prévio.
```

---

## 3. Conclusão do Piloto de Consumo

O teste comprovou que:
1. `hub_briefing` é a via recomendada para premissas estruturais seguras.
2. `memory_search` requer obrigatoriamente a disciplina do `memory_get` para desambiguar `pending` de `validated`.
3. A regra de consumo da v1.0 protege o desenvolvedor e o agente contra a contaminação acidental de planos por hipóteses não validadas.
