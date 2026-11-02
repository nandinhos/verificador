# Engenharia Reversa do replica-skill e Guia de Adaptação para o Harness Kiro

> Discussão registrada sobre a análise profunda do repositório `replica-skill` (Jake Schincariol), documentando seus 11 módulos, 6 ferramentas determinísticas em Python Stdlib e a estratégia de adaptação e replicação para o harness Kiro.

## Metadados

- **Data de início:** 2026-11-01
- **Tema / palavras-chave:** engenharia reversa, clean-room replica, claude skills, kiro harness, python stdlib, determinismo, app clone
- **Origem:** Repositório GitHub [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill.git)
- **Fonte(s):** Repositório público `Jakeschincariol/replica-skill`, commit `77c9436fb3d18c3d58169efb8caf4fe906b0dc51`, [opusjake.ai](https://opusjake.ai)
- **Status:** Ativa (Pronta para continuidade com outro agente no Kiro)

## Contexto

O usuário solicitou uma análise do repositório `https://github.com/Jakeschincariol/replica-skill.git` e a persistência estruturada do estudo (incluindo a mini-aula técnica gerada) para permitir que outro agente assuma a tarefa e implemente a adaptação desse kit de habilidades dentro do **harness Kiro** (`.kiro/skills/`, steering files e CLI).

O `replica-skill` propõe uma abordagem *clean-room* para replicar aplicações SaaS e produtos digitais:
- Reconstruir **o que a aplicação faz e as jornadas do usuário**, nunca os ativos proprietários (código-fonte original, marcas, logos ou cópias textuais).
- 11 habilidades sequenciais integradas em pipeline através da pasta de estado `replica/`.
- 6 ferramentas de auditoria e medição em Python 3.8+ sem nenhuma dependência de terceiros (`pip install`), executadas localmente e sem conexões de rede.

## Verificação de fontes

| Fonte | Status | Como foi verificada |
|---|---|---|
| Repositório `Jakeschincariol/replica-skill.git` | `OBSERVED` | Clonado em sandbox (`/tmp/repo-analysis-replica`), commit `77c9436f`, inspecionado diretamente. |
| Suíte de testes oficial (`tests/`) | `OBSERVED` | Executada via `python3 -m unittest discover -s tests -v`: 57 testes passaram em 0.456s, exit code 0. |
| Grafo AST via Graphify | `OBSERVED` | Mapeado em modo `--code-only`: 187 nós, 278 arestas, 15 comunidades e 0 ciclos de importação. |
| Manifesto Claude Plugin (`.claude-plugin/plugin.json`) | `OBSERVED` | Lidos e verificados: `version 1.0.0`, author `Jake Schincariol`, licença `MIT`. |
| Estrutura do Kiro Harness (`.kiro/skills/` e steering) | `OBSERVED` | Especificações padrão do Kiro observadas no subsistema de skills do ambiente local. |

## Análise

### 1. O Pipeline de 11 Skills

O pipeline funciona como uma esteira de produção incremental:

```text
1. /replica-recon        -> Gera replica/recon.md, replica/features.csv e screens de referência.
2. /replica-architect    -> Gera replica/architecture.md (schema SQL, stack e APIs).
3. /replica-design       -> Gera replica/tokens.json e valida acessibilidade WCAG.
4. /replica-build        -> Implementa as telas guiando-se pelo features.csv.
5. /replica-backend      -> Constrói auth, banco de dados, webhooks e Stripe.
6. /replica-test         -> Cria replica/test-plan.md e executa specs Playwright.
7. /replica-diff         -> Mede paridade funcional e layout agnóstico de cor.
8. /replica-entrepreneur -> Minera queixas de clientes reais e cria diferencial de mercado.
9. /replica-brand        -> Sanitiza código e define nova identidade independente.
10. /replica-launch      -> Elabora landing page e audita listagem de app store.
11. /replica-deploy      -> Valida checklist preflight.md e configura produção.
```

### 2. As 6 Ferramentas Determinísticas (Zero External Deps)

1. **`replica-diff/imgdiff.py` (457 linhas):**
   - Implementa decodificador de PNG próprio em Python puro (`struct` + `zlib`), contornando a dependência do Pillow/OpenCV.
   - Aplica detecção de bordas (gradiente de Sobel simplificado) e calcula densidade de componentes em grade celular.
   - **Propósito:** Compara layout estrutural sem penalizar mudanças de cor introduzidas pelo novo design system do clone.
2. **`replica-diff/parity.py` (229 linhas):**
   - Lê a matriz `features.csv` e aplica pesos: `must=3`, `should=2`, `could=1`.
   - Incorpora opcionalmente 20% do score estrutural do `imgdiff.py` (80% features + 20% visual).
   - Bloqueia o release com status *"not shippable"* caso qualquer requisito `must` esteja pendente.
3. **`replica-brand/sweep.py` (178 linhas):**
   - Scanner regex de alta precisão que busca o nome do concorrente, domínios e códigos hexadecimais em todo o código-fonte (inclusive em nomes de variáveis e classes como `CalendlySync`).
   - Retorna exit code 1 se encontrar vestígios da marca original, servindo como quality gate bloqueante.
4. **`replica-design/contrast.py` (158 linhas):**
   - Calcula luminância relativa WCAG 2.1 e afere conformidade AA (4.5:1) e AAA (7:1) em tokens de design JSON.
5. **`replica-entrepreneur/reviews.py` (312 linhas):**
   - Agrupador de reviews com decay temporal (>18 meses = 50% de peso).
   - Exige URL obrigatória e proíbe IA de inventar ou parafrasear queixas (todas as citações são substrings literais do CSV).
6. **`replica-launch/listing.py` (243 linhas):**
   - Linter para textos de App Store / Google Play, com contagem grapheme de emojis, bloqueio de superlativos ("#1", "best") e checagem de palavras-chave duplicadas.

## Plano de Adaptação para o Harness Kiro

Para o agente que dará continuidade e replicará/adaptará o pacote no **Kiro**, os seguintes passos determinísticos devem ser executados:

### Passo 1: Mapeamento de Diretórios do Kiro
No Kiro IDE/CLI, as habilidades e comandos operam nos seguintes caminhos padrão:
- **Skills do Projeto:** `.kiro/skills/<skill-name>/SKILL.md` (ou globais em `~/.kiro/skills/`).
- **Steering Files:** `.kiro/steering/` ou arquivos `.kiro/rules/*.md`.
- **Scripts Executáveis:** Mantidos em subpastas ou agrupados em `.kiro/bin/` / `.kiro/scripts/`.

### Passo 2: Conversão de Frontmatter e Comandos
As skills do repositório original usam o padrão Claude Code com prefixos de barra (`/replica-recon`, etc.).
No Kiro:
1. Manter o frontmatter YAML padrão:
   ```yaml
   ---
   name: kiro-replica-recon
   description: >-
     Engenharia reversa clean-room para Kiro...
   ---
   ```
2. Garantir compatibilidade com o formato de invocação do Kiro (seja por menção explícita de skill, prompt de steering ou slash-command).

### Passo 3: Portabilidade dos Scripts Python
Os 6 scripts (`imgdiff.py`, `parity.py`, `sweep.py`, `contrast.py`, `reviews.py`, `listing.py`) são **100% agnósticos de harness**, pois não possuem dependência de nenhum SDK específico. Eles podem ser copiados diretamente e invocados via linha de comando ou integrados como ferramentas de workspace no Kiro.

### Passo 4: Estrutura da Pasta de Estado do Projeto
Preservar a convenção de artefatos em `replica/`:
- `replica/recon.md`
- `replica/features.csv`
- `replica/architecture.md`
- `replica/tokens.json`
- `replica/feedback.md`
- `replica/parity.md`

## Anexos

Os arquivos gerados durante a análise detalhada encontram-se salvos nesta pasta de discussão:
- 🖥️ [repository-mini-class.html](./repository-mini-class.html): Mini-aula interativa standalone (HTML premium com SVG e CSS embutidos).
- 📊 [repository-inventory.json](./repository-inventory.json): Inventário estruturado em JSON com nós AST, classes, testes e comandos.
- 📄 [analysis-summary.md](./analysis-summary.md): Sumário executivo técnico auditável.

## Nota de continuidade / reverificação pendente

> Destino de continuidade definido pelo autor: a adaptação será feita no **harness
> DeepSeek** (uso de profiles distintos), não no Kiro. Esta pasta permanece como
> **registro/handoff**. Antes de tratar qualquer item abaixo como fato consolidado,
> o próximo agente deve reverificá-lo — as classificações seguem o PROTOCOLO.

1. **Scripts Python não estão nesta pasta (`UNKNOWN` localmente).** Os documentos
   descrevem os 6 utilitários (nomes, linhas, propósito), mas os **arquivos-fonte não
   foram persistidos aqui**. Para obtê-los é necessário **reclonar**
   `https://github.com/Jakeschincariol/replica-skill.git` (commit `77c9436f` segundo
   este README). Não é possível copiá-los a partir das descrições em markdown.

2. **Claims `OBSERVED` herdadas de outra sessão não são reverificáveis neste ambiente.**
   O sandbox `/tmp/repo-analysis-replica` **não existe mais** (`NOT FOUND` ao checar).
   Logo, para quem retomar, o status correto destas afirmações é **"a reverificar ao
   reclonar"**, não fato consolidado:
   - `57 testes unittest verdes em 0.456s, exit code 0`;
   - grafo AST `187 nós / 278 arestas / 15 comunidades / 0 ciclos`;
   - commit `77c9436f`, licença MIT, `version 1.0.0`.

   Reverificação sugerida após reclonar: `python3 -m unittest discover -s tests -v`.

3. **Portabilidade "100% agnóstica" é `INFERRED`, não `OBSERVED`.** Nenhum dos 6 scripts
   foi executado dentro do Kiro ou do DeepSeek até aqui. A afirmação de portabilidade
   depende apenas da stdlib do Python 3.8+, mas só vira `OBSERVED` após execução real
   no harness de destino.

4. **Local de instalação (fora do repo de discussões).** Este repositório é de
   *discussões*; artefatos operacionais (skills + scripts executáveis) devem viver no
   ambiente de destino (profiles do DeepSeek, ou `~/.kiro/skills/` global / projeto-alvo
   no caso do Kiro), não dentro desta pasta.

## Fechamento (contrato de resposta)

```
Resultado:   Engenharia reversa do replica-skill documentada e persistida em discussoes/. Handoff pronto para continuidade no harness DeepSeek (profiles distintos). Portabilidade ainda NÃO executada.
Evidências:
  OBSERVED (nesta sessão):  Pasta de discussão com 4 artefatos (README, analysis-summary, repository-inventory.json, repository-mini-class.html) presentes e internamente consistentes; Python 3.12 disponível no ambiente; sandbox /tmp/repo-analysis-replica NOT FOUND; .kiro/skills/ e os 6 scripts NÃO presentes neste repositório.
  OBSERVED (herdado de sessão anterior — a REVERIFICAR ao reclonar):  Clone no commit 77c9436f; 57 testes unittest verdes (exit 0 em 0.456s); AST 187 nós / 278 arestas / 0 ciclos via Graphify. Não reverificável neste ambiente (sandbox removido).
  INFERRED:  Os 6 utilitários (Python stdlib 3.8+) são portáveis sem reescrita; só vira OBSERVED após execução real no harness de destino. Namespace e local de instalação a definir no DeepSeek.
  UNKNOWN:   Manter namespace `replica-*` ou adotar outro; estrutura exata de profiles no DeepSeek.
Confiança:   MÉDIA — a documentação e os artefatos estão consolidados e consistentes (OBSERVED), mas as evidências de execução (testes/AST/commit) são herdadas e não foram reverificadas nesta sessão, e a portabilidade ainda não foi executada.
```
