# Verificador Determinístico de Discussões

> Um espaço pessoal, agnóstico de ferramenta, para discutir, refletir e investigar
> temas de tecnologia — com uma regra inegociável: **toda afirmação relevante precisa
> de evidência classificada.**

> **Agente de IA:** antes de responder qualquer coisa nesta pasta, leia e siga o
> [`PROTOCOLO.md`](./PROTOCOLO.md). Resumo da ponte em [`AGENTS.md`](./AGENTS.md).

## Finalidade

Esta pasta é um **repositório de discussões**. Aqui entram artigos, repositórios,
links, ideias e reflexões sobre o mundo da tecnologia. Cada tema interessante vira
uma **discussão** documentada.

O diferencial não é guardar conteúdo — é **como o conteúdo é tratado**:

- Nada de "parece bom" ou "deve funcionar". Afirmações são classificadas como
  `OBSERVED`, `INFERRED` ou `UNKNOWN`.
- Fontes citadas são **verificadas**, não assumidas. Referência inventada é falha grave.
- A resposta mais valiosa é a mais **determinística e amparada em evidência**, não a
  mais longa ou a mais eloquente.

Qualquer agente de IA (harness) — Kiro, Claude, Cursor, Copilot, ou outro — deve
conseguir abrir esta pasta, ler o [PROTOCOLO.md](./PROTOCOLO.md) e entender
imediatamente como proceder, responder e pesquisar. O protocolo é **agnóstico por
design**: não depende de nenhuma ferramenta, modelo ou configuração específica.

## Como usar

1. **Começando uma discussão nova?** Nem toda conversa precisa virar arquivo. Uma
   dúvida rápida pode ser **efêmera** (sem registro). Se o tema merece ser revisitado,
   registre: copie [`templates/discussao.template.md`](./templates/discussao.template.md)
   para uma pasta nova dentro de `discussoes/`, com nome semântico (ver convenção abaixo).
2. **É um agente de IA abrindo esta pasta?** Leia o [PROTOCOLO.md](./PROTOCOLO.md) primeiro.
   Ele define a dinâmica de resposta, pesquisa e evidência — e a regra de **confirmar
   antes de criar scaffold** (Seção 6: efêmera vs. registrada).
3. **Quer revisitar um tema?** Navegue pelo [Índice de Discussões](#índice-de-discussões).

## Convenção de nomes

Cada discussão vive em `discussoes/AAAA-MM-DD-tema-semantico/`:

- `AAAA-MM-DD` — data de início da discussão (ordena cronologicamente).
- `tema-semantico` — palavras-chave em kebab-case que descrevem o assunto.

Exemplo: `discussoes/2026-10-23-avaliacao-rag/`

Cada pasta contém pelo menos um `README.md` seguindo o template. Anexos (imagens,
prompts, trechos de código, PDFs) ficam na mesma pasta.

## Estrutura

```
verificador-deterministico/
├── README.md                     # este arquivo — finalidade e índice
├── PROTOCOLO.md                  # regras agnósticas: como proceder, responder, pesquisar
├── templates/
│   └── discussao.template.md     # molde para cada nova discussão
└── discussoes/
    └── 2026-10-23-avaliacao-rag/ # discussões, uma pasta por tema
        └── README.md
```

## Índice de Discussões

| Data | Tema | Pasta | Status |
|---|---|---|---|
| 2026-10-23 | Como testar se uma resposta de IA baseada em documentos está correta (avaliação de RAG) | [`2026-10-23-avaliacao-rag`](./discussoes/2026-10-23-avaliacao-rag/) | Ativa |
| 2026-10-24 | Teste de comportamento agnóstico entre harnesses (registro vivo multi-harness) | [`2026-10-24-teste-agnostico-harness`](./discussoes/2026-10-24-teste-agnostico-harness/) | Concluída (1ª rodada) |
| 2026-10-24 | Teste de abstenção entre harnesses (fonte inexistente / premissa falsa) | [`2026-10-24-teste-abstencao-harness`](./discussoes/2026-10-24-teste-abstencao-harness/) | Concluída (2ª rodada) |
| 2026-10-24 | Teste de confiabilidade de conteúdo (fonte que se contradiz / conflito entre fontes) | [`2026-10-24-teste-confiabilidade-harness`](./discussoes/2026-10-24-teste-confiabilidade-harness/) | Concluída (3ª rodada) |
| 2026-10-24 | Teste de resistência adversarial (injeção de instrução / prompt injection) | [`2026-10-24-teste-adversarial-harness`](./discussoes/2026-10-24-teste-adversarial-harness/) | Concluída (4ª rodada) |

> Ao criar uma nova discussão, adicione uma linha nesta tabela.
