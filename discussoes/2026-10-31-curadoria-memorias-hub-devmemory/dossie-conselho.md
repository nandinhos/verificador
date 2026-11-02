# Dossiê de Submissão ao Conselho de Seniores: Regra de Curadoria de Memórias no Hub Dev-Memory (v1.0)

## 1. Identificação e Contexto
- **Objeto:** Formalização da regra de transição de estados (`pending` → `validated` → `global`) e disciplina de consumo em planos no hub `dev-memory`.
- **Origem:** Deliberação colaborativa entre Antigravity e Muse, ancorada no estado físico do hub e na homologação da release `20261031_214829` em produção VPS (`https://devmemory.fssdev.com.br/up` respondendo HTTP 200).
- **Linha de Base Congelada:** 16 memórias ativas catalogadas (12 `validated`, 4 `pending`, 100% no escopo `global`).

---

## 2. A Regra de Curadoria Proposta (v1.0)

### 2.1 Equação Decisória de Validação:
$$\text{Validação} = (\text{Trilha A [Fato Externo]} \lor \text{Trilha B [Comportamento Local]} \lor \text{Trilha C [Governança]}) \land \text{Portão Humano}$$

* **Trilha A (Fato Externo Versionado):** Exige Context7 / documentação oficial pinada na versão exata OU teste de integração contra serviço real.
* **Trilha B (Comportamento Local de Sistema):** Exige probe executado ou teste determinístico em sandbox registrando comando e saída (`Exit code 0`).
* **Trilha C (Convenção / Governança):**
  - *Preferência Pessoal do Autor:* O autor humano é a fonte primária inegociável (1x confirmação humana direta).
  - *Regra Arquitetural de Repositório:* Exige política escrita versionada no Git (`AGENTS.md`, guidelines) **E** confirmação humana.
* **Portão Humano (E Fixo):** Mandatório em todas as transições para `validated`. Proibida a auto-validação autônoma por IA.
* **Memórias Mistas:** Exige conjunção $\mathbf{E}$ entre as trilhas envolvidas ou desmembramento atômico conectado por relação.

### 2.2 Disciplina de Consumo ao Planejar:
- `validation_status: "validated"` $\rightarrow$ Premissa de arquitetura (`OBSERVED`).
- `validation_status: "pending"` $\rightarrow$ Alerta heurístico (`INFERRED`), exigindo probe prévio antes de codificar.

### 2.3 Contradição sem Deleção (Grafo de Relações):
- Proibida a exclusão amnésica de memórias refutadas.
- Aplicação mandatória da aresta `supersedes` no grafo apontando da memória nova para a antiga.

---

## 3. Evidências Empíricas dos Pilotos Realizados

1. **Piloto de Classificação (5 memórias reais):**
   - `01a19496` (`url+serverUrl` MCP): Classificada como CONFORME (benchmark de spec externa + probe).
   - `01a055f6` (DSH user-dsh root): Parecer PROMOVÍVEL (probe registrado).
   - `01a05573` (DSH preset com `!!js`): Parecer SUBSTITUÍDA / NÃO PROMOVÍVEL (candidata a receber `supersedes` da `01a055f6`).
   - `01a05547` (DSH sync models): Parecer PROMOVÍVEL CONDICIONADA (script existente no repositório).
   - `01a022a2-a3d2` (Estilo de comunicação): Classificada como CONFORME (benchmark Trilha C.1).
2. **Piloto de Consumo em Planos:**
   - Comprovou-se que `hub_briefing` filtra e entrega apenas lições `validated` (12 memórias).
   - Comprovou-se que `memory_search` retorna `pending` e `validated` misturados sem projetar status, tornando mandatório o uso de `memory_get` para rotular premissa vs alerta.

---

## 4. Quesitos para Deliberação do Conselho

1. **Quesito 1 (Completude Decisória):** A fórmula decisória baseada em 3 trilhas disjuntivas com portão humano conjuntivo é suficiente para prevenir tanto a contaminação por falsos fatos quanto a burocracia excessiva?
2. **Quesito 2 (Governança e Portão Humano):** A distinção entre preferência individual do autor (1x aprovação direta) e regra arquitetural de repositório (regra commitada + humano) resolve adequadamente o risco de redundância circular?
3. **Quesito 3 (Grafo e Rastreabilidade):** A convenção de `supersedes` sem deleção física atende ao Ponytail Mode para repositórios com menos de 200 memórias?
