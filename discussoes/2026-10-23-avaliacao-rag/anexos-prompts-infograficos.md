# Anexos — Prompts de Infográfico e DNA Visual

> Anexos da discussão [avaliação de RAG](./README.md). Série visual
> "Corporate-Tech Infographic", paisagem 16:9, rótulos em pt-BR.

## DNA Visual — Padrão "Corporate-Tech Infographic"

Bloco reutilizável (colar no final de qualquer prompt de imagem para manter a
identidade visual consistente em toda a série):

```
Visual style — "Corporate-Tech Infographic" standard:
Minimalist flat-design, corporate-tech, high clarity, no photorealism, no clutter,
generous white space. Landscape 16:9. Color palette: white and soft gray base,
light blue (primary), teal (secondary), deep indigo (accent), soft grays for lines
and secondary elements. Clean readable sans-serif typography with clear hierarchy
(strong title, light subtitle, short captions). Flat line-style icons, no heavy
shadows. Diagrams use arrows, connected nodes, loops and decision diamonds with
short labeled edges. Balanced panels or columns. Optional bottom strip for a
progression gradient or highlight banner. Minimal, explanatory text. All visible
text in Brazilian Portuguese, exactly as written.
```

Resumo da paleta:
- Base/fundo: branco e cinza-claro
- Primária: azul-claro
- Secundária: teal
- Acento/destaque: indigo profundo
- Neutros: cinza suave para linhas e ícones secundários

## Prompt 1 — Comparativo: RAG Simples × GraphRAG × Agentic RAG

```
Create a clean, modern landscape infographic (16:9) comparing three RAG architectures,
arranged side by side in three vertical panels of equal width. Minimalist flat-design
style, professional color palette (blues, teals, soft grays), generous white space,
clear icons, minimal text, readable sans-serif typography. All visible text must be in
Brazilian Portuguese exactly as written below.

Title at the top: "RAG: Três Níveis de Busca de Evidência"

Panel 1 — title "RAG Simples" (color accent: light blue)
Diagram: a question icon → single arrow → a stack of documents → arrow → answer.
Caption: "Busca única. Recupera trechos relevantes uma vez e responde. Rápido e barato,
mas falha quando a resposta está dividida entre fontes."

Panel 2 — title "GraphRAG" (color accent: teal)
Diagram: a question icon → a connected node graph (circles linked by labeled edges,
e.g. Pessoa→Cargo→Limite) → answer.
Caption: "Conhecimento como grafo. Modela entidades e suas relações, percorrendo fatos
conectados em vários saltos. Ideal para perguntas complexas e interligadas."

Panel 3 — title "Agentic RAG" (color accent: deep indigo)
Diagram: a question icon → a loop/cycle arrow showing busca → verifica evidência →
re-busca → answer, with a small decision diamond labeled "evidência suficiente?".
Caption: "Agente iterativo. Busca em etapas, verifica se a evidência é suficiente,
re-busca quando necessário e sabe dizer 'não sei'. Mais confiável, custo maior."

Bottom strip: a simple left-to-right gradient bar labeled "Simplicidade e Velocidade"
on the left and "Precisão e Profundidade de Raciocínio" on the right, showing
progression across the three panels.

Visual style: corporate-tech, infographic, high clarity, no photorealism, no clutter.
```

## Prompt 2 — Continuação: Agentic GraphRAG (combinação)

```
Create a clean, modern landscape infographic (16:9) as a continuation of a previous RAG
comparison series. Same visual language: minimalist flat-design, professional color
palette (blues, teals, soft grays, with a deep indigo accent), generous white space,
clear icons, minimal text, readable sans-serif typography. All visible text must be in
Brazilian Portuguese exactly as written below.

Title at the top: "Agentic GraphRAG: a Combinação"
Subtitle below it: "Um agente iterativo raciocinando sobre um grafo de conhecimento"

Center — main diagram:
A question icon on the left feeding into a central cycle/loop. The loop connects to a
knowledge graph (circles linked by labeled edges, e.g. Pessoa→Cargo→Limite). The loop
has three stages labeled in Portuguese: "buscar no grafo" → "verificar evidência" →
"re-buscar se insuficiente", with a small decision diamond labeled "evidência
suficiente?" that exits to an answer icon on the right labeled "resposta" (and an
alternate exit labeled "não sei").

Two supporting columns below the main diagram:

Left column, header "O que cada um contribui":
- Icon of a graph + text: "GraphRAG → estrutura: fatos já conectados por relações,
  saltos multi-hop viram arestas."
- Icon of a loop + text: "Agentic → controle: decide quantos saltos dar, quando parar
  e quando admitir falta de evidência."

Right column, header "Custo":
- Icon of a building block + text: "Construção (uma vez): cara — extrair entidades e
  relações da base."
- Icon of a gauge + text: "Por consulta: adaptativo — gasta mais só nas perguntas
  difíceis, pode economizar tokens."

Bottom strip: a highlighted banner in Portuguese: "Ideal quando o erro é caro: jurídico,
financeiro, compliance e procedimentos com exceções."

Visual style: corporate-tech, infographic, high clarity, no photorealism, no clutter.
Keep it visually consistent with a three-panel RAG comparison infographic that precedes it.
```
