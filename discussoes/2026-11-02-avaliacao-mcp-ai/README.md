# mcp.ai sob auditoria: o agregador MCP, seus critérios de segurança e o risco de vazamento — com o desvio IndexNow

## Metadados

- **Data de início:** 2026-11-02
- **Tema / palavras-chave:** mcp.ai, agregador MCP, OAuth/OIDC, token estático, Open Finance, Pluggy, Composio, WhatsApp bridge, LGPD, vazamento de credenciais, llms.txt, IndexNow, premissa falsa, teste anedótico
- **Origem:** pedido de análise do autor sobre https://mcp.ai/pt-br (divulgado em grupo técnico) + alegação posterior, no mesmo grupo, de que seria necessário usar o IndexNow em conjunto "para melhores respostas"
- **Fonte(s):**
  - https://mcp.ai/pt-br, /privacy, /terms, /llms.txt, /index.md, /explore.md e páginas por conector (/gmail, /whatsapp, /banco, /instagram, /nubank)
  - https://api.mcp.ai — metadata OAuth, handshake MCP, `tools/list`, `tools/call authenticate` (sem conta)
  - https://banco.mcp.ai — página do produto de Open Finance
  - https://app.mcp.ai/login — fluxo de entrada
  - BrasilAPI (CNPJ 20.873.739/0001-15), RDAP do registro .ai, API do GitHub, hn.algolia.com
  - https://www.pluggy.ai/sobre e https://docs.composio.dev/docs/security/overview (upstreams)
  - https://www.indexnow.org/ e /faq; documentação da Indexing API do Google
  - https://llmstxt.org/ (spec v2); https://platform.openai.com/docs/bots; https://www.pluggy.ai/precos
  - Prints do grupo "Beer And Code" (Anexos 1 e 2)
- **Status:** Concluída (com três UNKNOWNs explicitados)

---

## Contexto

O mcp.ai foi apresentado em um grupo como "um link, todos os conectores": um endpoint MCP único que agrega Gmail, Google Drive/Sheets, WhatsApp, Open Finance (bancos brasileiros) e mais ~2.271 conectores. O pedido original tinha quatro partes:

1. Como a ferramenta funciona.
2. Quais são os critérios de segurança dela.
3. Se existe risco de vazamento de informação.
4. Se ela realmente entrega o que promete — e se é seguro usá-la.

Depois, uma segunda mensagem do grupo afirmou que seria preciso usar **outra** ferramenta em conjunto — o https://www.indexnow.org/ — "para ter as melhores respostas e aproveitamento de alto nível". Isso virou uma verificação separada: adicional, necessário, ou nenhuma das duas coisas?

Uma terceira frente apareceu na mesma thread: a alegação de que seria preciso usar `llms.txt` **e** IndexNow para que uma IA encontrasse conteúdo próprio, com um relato de teste que "funcionou". Isso é tratado no **Adendo**, ao final, junto com o teste do Banco MCP em duas contas e a observação de que o mcp.ai usa a Pluggy como intermediador.

Toda a coleta foi feita **sem criar conta**. O que exige conta (execução com dados reais, tela de consentimento do Google, criptografia em repouso) está marcado como `UNKNOWN`.

---

## Verificação de fontes

| Fonte | Status | Como foi verificada |
|---|---|---|
| mcp.ai (site, políticas, docs para agentes) | `OBSERVED` | HTTP 200; conteúdo lido em HTML e em markdown (`Accept: text/markdown`) |
| api.mcp.ai (comportamento em produção) | `OBSERVED` | `initialize`, `tools/list` e `authenticate` executados em 2026-11-02; headers e metadata OAuth capturados (ver [evidencias-comandos.md](./evidencias-comandos.md)) |
| DL WEB LTDA / CNPJ 20.873.739/0001-15 | `OBSERVED` | BrasilAPI retorna razão social, situação ATIVA, CNAE, capital e quadro societário; dados batem com /privacy e /terms |
| Domínio mcp.ai | `OBSERVED` | RDAP: registro 2019-02-16, transferência 2024-11-26, WHOIS privado (Domains By Proxy), NS Cloudflare |
| banco.mcp.ai (alegações de segurança do Open Finance) | `OBSERVED` (texto) / `UNKNOWN` (implementação) | Página lida integralmente; afirmações não auditáveis de fora |
| Pluggy como provedor upstream | `OBSERVED` | Handshake expõe `Adapters: ... pluggy v1.7.11`; Pluggy declara licença de Iniciadora de Pagamentos no BCB em /sobre |
| Composio como upstream de Gmail | `OBSERVED` (docs) | `/gmail/llms.txt` diz "By: Composio · official"; metadata do catálogo diz que "a plataforma fornece o app OAuth" — as duas afirmações coexistem sem detalhe |
| IndexNow | `OBSERVED` | Definição e lista de buscadores suportados lidas em indexnow.org; FAQ cita Bing, Naver, Seznam, Yandex, Yep e endpoint Amazon; Google não aparece |
| Google não suporta IndexNow | `OBSERVED` (ausência) / `UNKNOWN` (mudança recente) | Lista oficial do IndexNow não inclui Google; documentação da Indexing API do Google não menciona IndexNow |
| llms.txt (spec) | `OBSERVED` | https://llmstxt.org/ — proposta de Jeremy Howard publicada em 03/09/2024, v2 em 10/08/2026 |
| Crawlers da OpenAI | `OBSERVED` (ausência) | https://platform.openai.com/docs/bots descreve `OAI-SearchBot`, `GPTBot` e `robots.txt`; llms.txt aparece apenas como índice da própria documentação |
| Pluggy — planos e limites | `OBSERVED` | https://www.pluggy.ai/precos — API para empresas a partir de R$ 2.500/mês; Meu Pluggy é portal pessoal gratuito |
| Prints do grupo "Beer And Code" | `OBSERVED` | Imagens anexadas (Anexos 1 e 2); falas transcritas no Adendo |
| Funcionamento ponta a ponta com contas reais | `UNKNOWN` | Exigiria conta e consentimento; não foi feito |

---

## Análise

### 1. Identidade e sinais de maturidade

O serviço é operado pela **DL WEB LTDA** (CNPJ 20.873.739/0001-15), em Campo Grande/MS, ativa desde 2014, CNAE de "portais, provedores de conteúdo e outros serviços de informação na internet", capital social de R$ 100 mil e **um único sócio-administrador**. `OBSERVED`

O domínio `mcp.ai` é de 2019, mas foi **transferido em 26/11/2024** e está sob WHOIS privado — ou seja, a idade do domínio não é a idade do produto. `OBSERVED`

Infra: site em Next.js/Vercel, API em Express atrás de Cloudflare (com CORS `*`), analytics Umami e pixel da OpenAI no site de marketing. `OBSERVED`

Isso não desqualifica o produto. Mas, para uma decisão de segurança, significa: **empresa pequena, produto recente, sem histórico público de auditoria** — o que aumenta o peso do que não é verificável.

### 2. Arquitetura e fluxo de dados

O fluxo real, verificado:

1. Você instala **um** servidor MCP remoto (`https://api.mcp.ai/install`), que se identifica como "Console" v0.9.405.
2. Autentica por OAuth — metadata pública com PKCE `S256`, registro dinâmico de clientes, JWT `RS256` (kid `mcp-ai-1`) e escopos `mcp:read`, `mcp:execute`, `integrations:read`. `OBSERVED`
3. Alternativa para agentes sem navegador: abrir `app.mcp.ai/agent-auth`, **copiar um Bearer JWT e colar no chat**. `OBSERVED`
4. O Console expõe **55 ferramentas**: 19 de Open Finance, 15 de Discord e um bloco `console_*` que permite ao agente **buscar, instalar e invocar conectores novos sozinho** (`console_search`, `console_mcp_install`, `console_invoke`). `OBSERVED`
5. Cada conector tem endpoint próprio (`/p_gmail`, `/p_whatsapp`, `/banco`, `/p_nubank`) e também API REST autenticada por chave `sk_live_…`.

O tráfego, portanto, é: **cliente de IA → api.mcp.ai → upstream (Pluggy, Composio/Google, bridge própria) → de volta ao modelo**. O conteúdo passa pela infraestrutura deles em texto claro no nível de aplicação. `INFERRED` (a topologia é `OBSERVED`; o detalhe de hospedagem interna não).

Detalhe operacional que vale registrar: o servidor só aceita `tools/call` depois da notificação `notifications/initialized`; sem ela responde "Session not found". `OBSERVED`

### 3. O que promete × o que entrega

| Promessa | Evidência | Classe |
|---|---|---|
| "100+ servidores MCP" | O catálogo declara **2.271 conectores**, mas há páginas por banco (`/nubank`, `/itau` → `p_nubank`, `p_itau`) e milhares de páginas `/p/…` no sitemap. Integrações realmente distintas ficam na casa das centenas | `OBSERVED` (contagem e duplicação) / `INFERRED` (quantas são distintas) |
| "5 idiomas" | en, es, pt-br, zh, ko | `OBSERVED` |
| "Open Finance regulado pelo BACEN" | O acesso é via **Pluggy**, que declara licença de Iniciadora de Pagamentos no BCB. O perímetro regulado (e o consentimento) está na Pluggy; o mcp.ai é cliente dela, **fora** desse perímetro | `OBSERVED` (Pluggy no handshake) / `INFERRED` (posição do mcp.ai) |
| "Read-only, não move dinheiro" | As 19 ferramentas de Open Finance são de consulta; não existe endpoint de Pix/transferência | `OBSERVED` |
| "Seguro, via OAuth" | O OAuth existe e está correto no essencial — mas o caminho recomendado para agentes usa um **JWT estático** | `OBSERVED` |
| "Não armazenamos o conteúdo" | **Contradito pela própria documentação**: o WhatsApp mantém arquivo local com busca full-text (FTS5) e backfill de histórico; anexos de Gmail sobem para S3 (`s3key`) | `OBSERVED` (docs) / `INFERRED` (roda na infra deles) |
| "Funciona em qualquer cliente MCP" | Protocolo responde e o fluxo de autenticação existe; execução com dados reais não testada | `UNKNOWN` |

### 4. Critérios de segurança: o que existe e o que falta

**Existe (declarado, parte verificável):**
- TLS 1.3+, criptografia de credenciais em repouso com AES-256-GCM (declarado na página do banco).
- OAuth com PKCE S256, JWKS RS256, escopos declarados, endpoint de revogação.
- Retenção definida: tokens até 30 dias após desconexão; logs de ferramentas até 90 dias; faturamento 5 anos.
- 2FA (TOTP), passkey e step-up — **no produto bancário** — mais consentimento Open Finance revogável no banco.
- Política LGPD com controlador identificado, bases legais e DPO (`privacidade@mcp.ai`).

**Não encontrei (ausência observada nas páginas consultadas; não é prova de inexistência global):**
- SOC 2, ISO 27001 ou qualquer certificação independente.
- Página de segurança real: `/security`, `/trust`, `/dpa` retornam a página genérica do app (soft 404).
- `security.txt` válido (o caminho devolve HTML do site, não o arquivo).
- Status page (`status.mcp.ai` não resolve) e histórico de incidentes.
- Lista pública de suboperadores, DPA público e política de divulgação de vulnerabilidades.
- Cláusula de notificação de incidente (LGPD, art. 48).

**Contrato:** "as is", responsabilidade limitada ao maior valor entre 12 meses de mensalidade e **R$ 1.000**, foro de Campo Grande/MS. `OBSERVED`

Isso importa porque desloca o risco econômico: em caso de incidente, o fornecedor responde por muito pouco.

### 5. Risco de vazamento de informação

O risco concreto não é "alguém invadir o mcp.ai". É a combinação de concentração de acesso com credencial de longa duração:

1. **Token que não expira.** A própria ferramenta responde: *"The token does not expire… add it to your MCP server's config as a header"*. Um único Bearer estático dá acesso a Gmail (ler e enviar), dados bancários, WhatsApp e Instagram. Se vazar por config sincronizado, print, dotfile ou histórico de chat, o atacante não precisa atacar ninguém. `OBSERVED`
2. **Token colado no chat.** O fluxo "rápido" manda colar o JWT na conversa — ele passa a viver no transcript do provedor de modelo. `OBSERVED`
3. **Conectores não oficiais.** WhatsApp é bridge multi-device por QR, com proxy "recomendado para evitar bloqueio de IP" — ou seja, sessão roda no servidor deles, histórico fica lá e o uso contraria os termos do WhatsApp. Instagram aceita **usuário e senha** (com 2FA) e automatiza follow/like. `OBSERVED` (docs) / `INFERRED` (risco de bloqueio)
4. **Cadeia de terceiros.** A política cita Composio, Google, Stripe, hospedagem/CDN e e-mail transacional como suboperadores; o Gmail é "By: Composio". Cada elo é mais um lugar onde o conteúdo existe. `OBSERVED`
5. **Multi-tenant e compartilhamento.** A página do banco vende compartilhar a conversa do Claude para terceiros consultarem seus dados ("Coworking"). É feature — e é vetor. `OBSERVED`
6. **LGPD.** Ao conectar WhatsApp, você passa a tratar dados de **terceiros** (seus contatos). Você vira controlador; o mcp.ai se declara operador, mas não oferece DPA público. Para uso empresarial, é lacuna. `INFERRED`

**Matriz por conector**

| Conector | Risco | Por quê |
|---|---|---|
| Banco (Open Finance) | **Médio-baixo** | read-only, consentimento revogável no banco, rail regulado; o risco é o token e o compartilhamento de conversa |
| Gmail / Drive / Sheets | **Alto** | leitura total + envio; e-mail é a chave-mestra de reset de senhas |
| WhatsApp | **Alto** | bridge não oficial, histórico armazenado, bloqueio possível, dados de terceiros |
| Instagram | **Alto** | custódia de senha + automação contra os termos da plataforma |

### 6. Veredito e checklist de uso

**Seguro com escopo.** Para Open Finance read-only, em conta dedicada, com os controles abaixo. **Arriscado** para caixa de e-mail corporativa, WhatsApp pessoal ou conta de cliente sem due diligence prévia.

1. Nunca cole o JWT no chat — use header no cliente, em máquina com disco criptografado.
2. Confirme se existe 2FA para a conta mcp.ai (a página do banco promete; para a conta principal é `UNKNOWN`).
3. Antes de conectar Gmail, verifique **o nome e o selo de verificação do app** na tela de consentimento do Google.
4. Prefira chaves de guest/workspace com escopo mínimo a um token de dono.
5. Revogue no painel **e** no provedor (Google/banco); tokens duram até 30 dias após desconexão.
6. Uso corporativo: exigir DPA, lista de suboperadores, região de hospedagem e resposta a incidente antes de conectar dado de cliente.
7. Tratar link `mcp.ai/u/…` e o JWT como segredo de produção.

### 7. IndexNow: nem adicional, nem necessário

A alegação do grupo é uma **premissa falsa por categoria**: IndexNow não pertence à pilha MCP.

- **O que é:** protocolo de ping em que o dono de um site avisa buscadores de que uma URL foi criada, alterada ou removida, para acelerar o rastreamento. `OBSERVED` (indexnow.org)
- **Quem suporta:** Microsoft Bing, Naver, Seznam.cz, Yandex, Yep e o endpoint da Amazon (Amazonbot). **Google não consta** — e a documentação da Indexing API do Google não menciona IndexNow. `OBSERVED` (lista oficial e ausência na doc) / `UNKNOWN` (se mudou em 2026)
- **Relação com o mcp.ai:** nenhuma. O `llms.txt` do mcp.ai não menciona IndexNow, e não há chamada de API que o IndexNow faria dentro de um fluxo de agente. `OBSERVED`
- **De onde vem a confusão:** a própria FAQ do IndexNow diz que ele "helps keep your content current in AI-powered search results" — indexação para busca com IA (o Copilot usa o índice do Bing). Isso é descobribilidade de conteúdo, não precisão de resposta. Somado ao homônimo "index" (indexação web × índice vetorial de RAG), produz a frase do grupo.

**Conclusão:** não é adicional nem necessário. É ortogonal. Usá-lo faz sentido se você publica site/docs e quer indexação rápida no Bing/Yandex; não melhora a resposta de um agente.

**O que de fato melhora precisão em setup MCP:** contrato das ferramentas (descrição, tipos, exemplos, erros), escopo mínimo de conectores habilitados, qualidade do dado de origem e avaliação medida com conjunto de perguntas e resposta esperada — a mesma linha da discussão [2026-10-23-avaliacao-rag](../2026-10-23-avaliacao-rag/).

---

## Reflexões e inferências

- **O agregador é a personificação do "confused deputy".** A spec do MCP dedica uma seção inteira ao problema: um intermediário com credenciais de vários serviços, atendendo pedidos de um cliente que não é o dono da credencial. O mcp.ai não é inseguro por ser agregador — mas agregador concentra risco por definição, e é exatamente aí que o usuário deveria olhar primeiro.
- **Token eterno é decisão de produto, não descuido.** A conveniência ("não precisa reparear") foi comprada com uma credencial estática que protege Gmail + banco + WhatsApp. É uma troca defensável para uma demo e difícil de defender para produção.
- **Catálogo inflado não é fraude técnica, é marketing.** 2.271 páginas com dezenas de wrappers do mesmo backend (por banco, por prefeitura, por prompt) distorcem a percepção de cobertura. A pergunta certa não é "quantos conectores", é "quais são mantidos, por quem e com qual contrato".
- **A frase do grupo é o padrão "adicione mais uma ferramenta".** Recomendação sem mecanismo causal ("X junto com Y melhora a resposta") é o tipo de afirmação que este repositório existe para checar: qual chamada de API o IndexNow faria dentro do fluxo do agente? Nenhuma.
- **O que sobra de valor no mcp.ai** é o problema que ele resolve: OAuth, roteamento e atualização de conectores atrás de uma URL. Isso é trabalho real. O que falta é o que não se vê: certificação, transparência de suboperadores, rotação de credencial e um DPA.

---

## Adendo — o que o grupo afirmou sobre llms.txt, IndexNow e o teste com duas contas

> Registrado em 2026-11-02, a partir de prints do grupo "Beer And Code" (Anexos 1 e 2).
> Participantes citados: Lucas Carvalho, Lucas Souza (VIRGU) e Marcos Blanco.

### Contexto do adendo

Na mesma thread em que o mcp.ai foi divulgado, o grupo passou a discutir **como fazer uma IA encontrar conteúdo próprio**. Lucas Carvalho publicou um blog com `llms.txt`, afirmou que "a OpenAI está usando" e que "além desse arquivo precisa usar o IndexNow". Marcos Blanco levantou duas objeções úteis: "é especulação que isso funciona" e "eles usam a Pluggy como intermediador". Lucas também relatou um teste do Banco MCP com duas contas de baixo movimento.

São seis afirmações de naturezas diferentes, e o valor do registro está em separá-las.

### As seis afirmações e seus veredictos

| # | Afirmação no grupo | Veredicto | Classe |
|---|---|---|---|
| 1 | "llms.txt faz a IA renderizar o conteúdo, parecido com sitemap.xml" | Parcialmente falso — é outra camada, não é sitemap | `OBSERVED` |
| 2 | "A OpenAI está usando; testei a busca e funcionou" | Não demonstrado (confunde publicar com consumir) | `INFERRED` |
| 3 | "Além desse arquivo precisa usar o IndexNow" | Falso — ortogonal | `OBSERVED` |
| 4 | "O mcp.ai usa a Pluggy como intermediador" | Verdadeiro | `OBSERVED` |
| 5 | "Uso meu Pluggy de graça, mas tem limitações" | Verdadeiro | `OBSERVED` |
| 6 | "Testei com duas contas e gerou análise completa" | Plausível, mas não mede precisão | `INFERRED` |

### 1. llms.txt não é sitemap

`OBSERVED` em https://llmstxt.org/: é uma **proposta** de Jeremy Howard publicada em 03/09/2024 e revisada para v2 em 10/08/2026, descrita como *"a proposal to standardise on using an /llms.txt file to provide information to help agents use a website"*.

- **Sitemap** informa ao crawler *quais URLs existem* — sinal de indexação reconhecido por Google e Bing.
- **llms.txt** informa ao agente *o que ler primeiro e como usar o site* — um README em markdown com links curados, que pressupõe que alguém **já decidiu** abrir aquele domínio.

São camadas diferentes. Nenhuma substitui a outra e nenhuma garante recuperação.

### 2. "A OpenAI está usando" — o que é verdade

Verdadeiro no sentido de **publicar**: a OpenAI mantém um `llms.txt` para a própria documentação — a página https://platform.openai.com/docs/bots diz "For the complete documentation index, see llms.txt". `OBSERVED`. A Anthropic também serve `docs.anthropic.com/llms.txt` (baixado e verificado). `OBSERVED`

Não demonstrado no sentido de **consumir**: a documentação oficial dos crawlers da OpenAI descreve `OAI-SearchBot` (busca no ChatGPT), `GPTBot` (treinamento) e `robots.txt` como o controle de acesso — **sem menção a llms.txt como sinal de indexação ou recuperação**. `OBSERVED` (ausência na documentação)

Ou seja: os laboratórios publicam llms.txt para os agentes deles; isso não significa que o buscador deles leia o seu.

### 3. O teste de busca não fecha a causalidade

"Fiz uma busca no ChatGPT, apareceu meu post, então o llms.txt funcionou" tem quatro confundidores:

1. A página **já era rastreada** antes do arquivo.
2. **n = 1 consulta** não distingue mecanismo de coincidência.
3. A busca do ChatGPT combina rastreamento, índice e o próprio modelo — a citação pode vir da relevância, não do arquivo.
4. **Viés de confirmação**: consultar o próprio blog é o teste mais fácil que existe.

Protocolo que fecha a dúvida (barato):

1. Filtrar o **log de acesso do servidor** por `OAI-SearchBot`, `GPTBot` e `Googlebot`; se `GET /llms.txt` nunca aparece, nenhum deles leu o arquivo.
2. Publicar uma URL **não linkada e fora do sitemap** e verificar se ela aparece em busca anônima.
3. A/B: duas páginas equivalentes, uma com llms.txt apontando, outra sem; comparar em 2–4 semanas.

### 4. IndexNow

Já tratado na seção 7. Reforço para o contexto do grupo: não existe chamada de API que ligue llms.txt ao IndexNow. São camadas distintas e nenhuma exige a outra. "Precisa usar o IndexNow além do arquivo" é frase sem mecanismo.

### 5. O que o grupo acertou

- **"Usam a Pluggy como intermediador"** — confirmado pelo handshake do servidor MCP (`Adapters: ... pluggy v1.7.11`). `OBSERVED`
- **"Uso meu Pluggy de graça, mas tem limitações"** — confere: o **Meu Pluggy** é portal pessoal gratuito; a **API** para empresas começa em R$ 2.500/mês, e a própria página admite teto de conexões no conector pessoal e o custo de migrar depois. `OBSERVED` (https://www.pluggy.ai/precos)
- **"A solução é incrível mas dá um medo"** — objeção correta, e é a mesma conclusão da análise principal: o risco não está na Pluggy (regulada pelo BCB como ITP), está no token estático do mcp.ai que concentra Gmail, banco e WhatsApp.

### 6. O que o teste com duas contas mede

"Peguei duas contas que não uso muito, pedi para analisar e gerou uma análise completa" demonstra que o **pipeline funciona** — não que os números estejam certos. Dois problemas de desenho:

- Contas de baixo movimento são o **caso fácil**: menos transações, menos ambiguidade, menos erro de categorização.
- **Sem gabarito**, "análise completa" elogia o texto, não o dado. Resposta confiante e errada tem a mesma aparência de resposta confiante e certa.

Teste de 5 minutos: pedir saldo, fatura em aberto e os 3 maiores gastos do mês e **comparar com o extrato no app do banco**. Se bater nos três, o conector entrega; se divergir, aparece onde.

Vale registrar o acerto metodológico dele: o "prompt BASE" restrito a *"somente consulte e analise"* é a prática correta — reduz escopo e erro, e é o mesmo princípio de escopo mínimo de ferramentas discutido na seção 4.

### 7. Implicações práticas

**Para um blog que quer ser encontrado por IA:**
- Manter `llms.txt` — custo baixo, ajuda o agente que já chegou ao domínio (é o mesmo padrão que o próprio mcp.ai usa: seu `llms.txt` é um guia de instalação para agentes).
- Publicar **sitemap** e permitir `OAI-SearchBot`/`GPTBot` no `robots.txt` — é isso que governa a entrada nos índices.
- IndexNow: útil para Bing/Yandex; irrelevante para Google e para LLM.
- Medir por log, não por impressão de busca.

**Para o uso do Banco MCP:**
- Manter prompt base restritivo, conta dedicada e 2FA.
- Conferir 3 números contra o app do banco antes de confiar.
- Tratar o JWT como segredo de produção — nunca colar no chat.

### Fechamento do adendo

~~~
Resultado:   o grupo misturou três camadas (indexação de site, documentação para agentes e
             dados bancários) e tratou um teste anedótico como prova. Das seis afirmações,
             duas são verdadeiras, uma é falsa e três são plausíveis mas não demonstradas.

Evidências:
  OBSERVED:  spec do llms.txt (v2, ago/2026); OpenAI publica o seu e documenta apenas
             robots.txt/OAI-SearchBot; lista do IndexNow sem Google; adapter Pluggy no
             handshake do mcp.ai; preços e limites da Pluggy.
  INFERRED:  o resultado de busca do Lucas é explicável por crawl/indexação normal.
  UNKNOWN:   se algum provedor consome llms.txt de terceiros hoje (não documentado); se o
             teste de duas contas bate com o extrato real do banco.

Confiança:   ALTA no mecanismo; MÉDIA no diagnóstico do teste individual.
~~~

---

## Publicação

No ar em **https://check.fssdev.com.br** (VPS `srv084270`, nginx 1.24, Ubuntu 24.04).

| Item | Estado |
|---|---|
| Conteúdo | site estático em `/var/www/check.fssdev.com.br` (dono `www-data`), mais o PDF em `/relatorio.pdf` |
| TLS | Let's Encrypt ECDSA, emitido em 02/11/2026, válido até 31/01/2027 |
| Cabeçalhos | CSP `default-src 'none'` com `self` apenas para estilo, script, fonte e imagem; HSTS; `nosniff`; `X-Frame-Options: DENY`; `Referrer-Policy`; `Permissions-Policy`; `X-Robots-Tag: noindex` |
| Superfície | só arquivos estáticos: sem formulário, sem upload, sem CGI; dotfiles negados; `server_tokens off` |
| Build | sem dependências externas — fonte Instrument Serif auto-hospedada, CSS e JS próprios |

Configuração versionada em [`deploy/`](./deploy/): vhost de estágio (HTTP), vhost final, script idempotente e notas. Para republicar depois de editar o site: `deploy/deploy.sh files`.

**Pendências de plataforma** (dependem do painel da Cloudflare, não do servidor):

1. Confirmar SSL/TLS em **Full (strict)** — hoje a origem tem certificado válido, então os dois modos funcionam, mas só Full (strict) valida a cadeia.
2. Seis subdomínios ainda publicam o IP de origem — `events`, `eventshomologacao`, `matchenginelinkedn`, `nextcloud`, `reportshtml` e `transcricoesyoutube` resolvem para `201.46.120.198`. Enquanto eles existirem sem proxy, esconder a origem é parcial.
3. O `robots.txt` do domínio é servido pela Cloudflare (política de Content Signals); o `Disallow` do origin não chega à borda. A proteção efetiva contra indexação é o `X-Robots-Tag`.

---

## Anexos

- [evidencias-comandos.md](./evidencias-comandos.md) — saídas brutas: metadata OAuth, handshake MCP, lista das 55 ferramentas, resposta da tool `authenticate`, headers de `mcp.ai` e `api.mcp.ai`, JSON do CNPJ.
- [anexo-grupo-1-llms-txt.png](./anexo-grupo-1-llms-txt.png) — print do grupo: llms.txt do blog, "a OpenAI está usando", "precisa usar o IndexNow".
- [anexo-grupo-2-indexnow-pluggy.png](./anexo-grupo-2-indexnow-pluggy.png) — print do grupo: teste com duas contas, "usam a Pluggy como intermediador", "meu Pluggy de graça".

**Versão para apresentação** (mesmo conteúdo, diagramado):

- [relatorio.html](./relatorio.html) — página editorial autocontida (CSS embutido, sem dependências externas); abre em qualquer navegador e imprime bem.
- [relatorio.pdf](./relatorio.pdf) — a mesma peça em PDF, 7 páginas, gerada por impressão headless do HTML.
- [`site/`](./site/) — versão publicada em produção: `index.html`, `assets/` (CSS, JS, fonte) e `robots.txt`.
- [`deploy/`](./deploy/) — vhosts do nginx, notas operacionais e `deploy.sh`.

---

## Fechamento (contrato de resposta)

~~~
Resultado:   mcp.ai é infraestrutura real (agregador MCP funcional) operada por empresa
             pequena, sem certificações públicas, com credencial estática de longa duração
             e conectores não oficiais. Seguro com escopo (Open Finance read-only);
             arriscado para e-mail/WhatsApp/Instagram com dados sensíveis. IndexNow é
             ortogonal: nem adicional, nem necessário.

Evidências:
  OBSERVED:  CNPJ e situação na Receita; RDAP do domínio; handshake MCP e 55 ferramentas;
             metadata OAuth (PKCE S256, RS256, DCR); token "que não expira"; docs de
             WhatsApp (arquivo local + FTS5), Gmail (S3/s3key, user_id delegado) e
             Instagram (usuário+senha); políticas de privacidade/termos com retenção e
             limite de R$ 1.000; ausência de /security, security.txt, status page,
             SOC 2/ISO; lista de buscadores do IndexNow sem Google.

  INFERRED:  arquivo de WhatsApp roda na infraestrutura deles; perímetro regulado do Open
             Finance termina na Pluggy; catálogo de 2.271 inclui dezenas de wrappers do
             mesmo backend; confusão do grupo vem do "AI-powered search results" da FAQ.

  UNKNOWN:   criptografia em repouso (não auditável de fora); nome/verificação do app OAuth
             do Google; se a DL WEB é participante ou subcontratada no Open Finance;
             histórico de incidentes; funcionamento ponta a ponta com conta real.

Confiança:   ALTA no que foi observado diretamente; MÉDIA nas inferências de fluxo de
             dados; BAIXA em qualquer afirmação sobre a segurança interna do fornecedor.
~~~

## Perguntas abertas (como fechar cada UNKNOWN)

1. **App OAuth do Google** — abrir a tela de consentimento de uma conta de teste e registrar nome do app, selo de verificação e escopos pedidos.
2. **Participação no Open Finance** — pedir por escrito à Pluggy e ao mcp.ai o papel contratual (participante, subcontratado ou cliente) e o contrato de tratamento de dados.
3. **Retenção real de conteúdo** — solicitar, via LGPD (art. 18), a confirmação de tratamento e a lista de suboperadores; comparar com o que a política declara.
4. **Ponta a ponta** — executar uma consulta real de Open Finance em conta descartável e medir latência, completude e erros.
