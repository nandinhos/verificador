# Como testar se uma resposta de IA baseada em documentos está correta (avaliação de RAG)

## Metadados

- **Data de início:** 2026-10-23
- **Tema / palavras-chave:** avaliação de RAG, evals, fidelidade, GraphRAG, Agentic RAG, modelos de decisão calibrados
- **Origem:** artigo
- **Fonte(s):** Andre Fonseca (AI Engineer, System4u Technology and Innovation) — artigo publicado em 2026-10-23
- **Status:** Ativa

## Contexto

O artigo trata de como avaliar sistemas RAG (Retrieval-Augmented Generation). Tese
central: uma resposta "bem escrita" não prova estar correta. É preciso **decompor**
a avaliação em dimensões para descobrir *em qual etapa* o erro surgiu, em vez de um
único índice de "qualidade".

Dimensões propostas (baseadas no trabalho RAGAs):

- **Relevância do contexto** — os trechos recuperados são focados e úteis?
- **Fidelidade** — as afirmações da resposta são sustentadas pelos trechos?
- **Relevância da resposta** — o texto atende ao que foi perguntado?

O artigo também defende: casos de teste reais (incluindo casos difíceis e de
abstenção), verificação de cada afirmação contra evidência, automação como triagem
(não veredito), e limites de aprovação proporcionais ao impacto do erro.

## Verificação de fontes

> Aplicação da Seção 3 do PROTOCOLO. As duas referências citadas pelo artigo foram
> verificadas via busca web nesta sessão.

| Fonte | Status | Como foi verificada |
|---|---|---|
| RAGAs — "Automated Evaluation of Retrieval Augmented Generation", EACL 2024 | `OBSERVED` | Confirmado em `aclanthology.org/2024.eacl-demo.16/`. É uma **demo paper** (nuance: não artigo principal). As três dimensões citadas batem com o paper. |
| Projeto NIST "Building Evaluation Probes into Agentic AI", ~abril/2026 | `OBSERVED` | Confirmado em `nist.gov/programs-projects/building-evaluation-probes-agentic-ai`. Descrição do NIST ("audit trail... factual claims... human-curated corpus") bate com a paráfrase do artigo. |

**Conclusão parcial:** o artigo é factualmente honesto — não inventa fontes. Isso
permite discutir o conteúdo sem desconfiar da fundação.

## Análise

**O que o artigo acerta (núcleo sólido):**
A decomposição recuperação → fidelidade → relevância transforma sintoma ("resposta
ruim") em diagnóstico ("qual etapa falhou"). A camada tripla (determinístico →
avaliação automática → revisão humana por amostragem) é madura, e reconhecer que
"um avaliador baseado em outro modelo também pode errar" é uma honestidade rara.

**Nuances e lacunas (os parênteses que agregam):**

1. **Fidelidade ≠ verdade.** As métricas medem coerência resposta↔trecho, não
   trecho↔realidade. Um sistema pode ser 100% fiel a um documento errado/desatualizado.
   Limite estrutural: nenhuma das três métricas pega "documento certo-recuperado,
   errado-no-conteúdo". Saída: tratar vigência e corretude da fonte como etapa própria.

2. **O gabarito envelhece como a base.** O conjunto de "resultados esperados" sofre
   do mesmo problema de desatualização que quer detectar. Deve ser versionado junto
   ao corpus e revisado no mesmo ciclo, senão vira dívida técnica silenciosa.

3. **Abstenção é o caso mais revelador.** Fazer o sistema dizer "não há evidência" é
   tecnicamente mais difícil que responder (modelos são treinados para ser prestativos).
   É o caso que melhor mede maturidade e o mais subtestado.

4. **Não existe score universal de RAG.** A frase do artigo — "a nota aceitável
   depende do impacto do erro" — implica que o limite de aprovação é decisão de
   **risco/governança**, não de engenharia. Contradiz a indústria que vende "score de RAG".

## Reflexões e inferências

**Evals como camada de arquitetura (não só teste).** A camada de "avaliação automática"
está deixando de ser etapa de teste para virar componente do sistema. Hoje usa-se
LLM-as-judge (gerador de texto reaproveitado para julgar), com dois problemas:
custo/latência e **erros correlacionados** com o gerador (se juiz e gerador são da
mesma família, o juiz valida a alucinação do gerador).

Modelos de decisão calibrados resolvem os dois. Exemplo verificado nesta sessão:

| Fonte | Status | Verificação |
|---|---|---|
| JEV (TypeSafe AI) — modelo "System One" | `OBSERVED` | `arxiv.org/html/2609.37647v1`, `victordibia.com/explainers/jev/`, `arize.com/blog/typesafe-jev-llm-judge/`. Não gera texto; retorna probabilidade calibrada `P(critério \| estado)`. Latência reportada 70–500ms; critérios definidos em runtime. |

JEV mede fidelidade como **probabilidade calibrada** em vez de prosa, é de outra
arquitetura (quebra a correlação de erros) e é barato o bastante para rodar por
chamada em produção — exatamente a trilha de auditoria que o NIST persegue.

**Além do RAG — escada de maturidade, não substituição.** `INFERRED` a partir das
fontes abaixo: não há tecnologia que aposente o RAG; há gradação sobre a mesma ideia
(buscar evidência e ancorar a resposta).

| Abordagem | Status | Fonte / nota |
|---|---|---|
| GraphRAG (conhecimento como grafo, multi-hop) | `OBSERVED` | `arxiv.org/abs/2504.05478`, `arxiv.org/abs/2604.09666v1`. Forte em raciocínio multi-hop; custo de construção maior. |
| Agentic RAG (busca iterativa, verifica suficiência, re-busca) | `OBSERVED` | `arxiv.org/abs/2601.21162v1` (A2RAG). Cobre o caso de abstenção. |
| Agentic GraphRAG (combinação) | `OBSERVED` | `arxiv.org/abs/2507.21892v2`, `arxiv.org/abs/2606.25656v1`. Agente iterativo sobre grafo de conhecimento. |

**Multi-hop (definição prática):** pergunta cuja resposta exige saltos encadeados,
onde a resposta de um salto vira a pergunta do próximo (ex: "quem aprovou a última
compra tem alçada para a próxima de R$ 80 mil?" → achar a pessoa → achar o cargo →
achar o limite → comparar). RAG simples falha porque busca uma vez; GraphRAG modela
os saltos como arestas do grafo.

**Custo da combinação Agentic GraphRAG** (`OBSERVED` nas fontes):
- Construção (offline, uma vez): cara — extrair entidades e relações da base.
- Por consulta (online): não necessariamente explode. "Is GraphRAG Needed?"
  (`arxiv.org/abs/2606.25656v1`) reporta **redução de 19–53% no uso de tokens** com
  engenharia de contexto; A2RAG dispara refinamento caro **só quando a evidência é
  insuficiente** — custo proporcional à dificuldade, não fixo no pior caso.

## Anexos

- Prompts de infográfico (série "Corporate-Tech Infographic", paisagem 16:9):
  (1) comparativo RAG Simples × GraphRAG × Agentic RAG; (2) continuação Agentic GraphRAG.
- DNA visual padrão definido na sessão (paleta: branco/cinza base, azul-claro primário,
  teal secundário, indigo de acento; flat-design; rótulos em pt-BR).

> Nota: os arquivos de imagem e os prompts completos podem ser salvos nesta pasta
> conforme forem gerados.

## Fechamento (contrato de resposta)

```
Resultado:   Artigo verificado como factualmente honesto; análise identificou 4 lacunas
             acionáveis e conectou o tema à evolução de arquitetura (evals como camada,
             JEV, GraphRAG/Agentic RAG).
Evidências:
  OBSERVED:  RAGAs/EACL 2024, NIST probes/2026, JEV/TypeSafe, GraphRAG, Agentic RAG,
             A2RAG, "Is GraphRAG Needed?" — todas confirmadas via busca web nesta sessão.
  INFERRED:  "Além do RAG" é escada de maturidade, não substituição; evals migrando de
             teste para componente de arquitetura.
  UNKNOWN:   Números de custo em produção para um caso concreto específico; eficácia do
             JEV como juiz de fidelidade medida em benchmark independente de RAG.
Confiança:   ALTA para fontes e definições; MÉDIA para projeções de custo (dependem de caso).
```
