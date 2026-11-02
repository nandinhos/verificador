# Método MALT no Ecossistema Laravel: Extração Integral e Análise de Enquadramento em Abordagem Paralela

## Metadados

- **Data de início:** 2026-11-02
- **Tema / palavras-chave:** Método MALT, Laravel, Metodologias de Codificação, Modelagem, Ação, Lógica, Testes, Arquitetura de Software, Abordagem Paralela, Vertical Slices
- **Origem:** Mapa Mental no MindMeister compartilhado publicamente
- **Fonte(s):** [MindMeister - Mapa MALT](https://www.mindmeister.com/app/map/3389601437?t=Dc5wErVL8T&m=outline) (ID: 3389601437, Token: Dc5wErVL8T)
- **Status:** Ativa

---

## Contexto

O **Método MALT** é uma metodologia estruturada de codificação voltada primariamente ao ecossistema PHP/Laravel, concebida para mitigar três dores crônicas no ciclo de vida de projetos de software:
1. **Análise Paralisante**: Indecisão diante da flexibilidade do Laravel sobre por onde começar uma funcionalidade.
2. **Código Desorganizado**: Código misturado sem separação física entre transporte HTTP, persistência e regra de negócio.
3. **Dificuldade em Testar**: Aplicações com alto acoplamento que tornam a escrita de testes de unidade e integração complexa e demorada.

O método divide o fluxo em 4 etapas sequenciais representadas pelo acrônimo:
- **M** — Modelagem
- **A** — Ação
- **L** — Lógica
- **T** — Testes

O autor solicitou a extração completa e exata da árvore do mapa mental, bem como uma análise crítica e prática de como o MALT se enquadra na sua dinâmica de codificação com Laravel, explorando uma abordagem paralela (em contraste com o modelo linear tradicional).

---

## Verificação de fontes

| Fonte | Status | Como foi verificada |
|---|---|---|
| Mapa Mental MindMeister (ID: 3389601437) | `OBSERVED` | Acessado via Chrome Headless com Chrome DevTools Protocol (CDP); payload JSON completo interceptado em `https://www.mindmeister.com/app/api/maps/content.json?idea_id=3389601437&share_token=Dc5wErVL8T` (120.638 bytes, 122 nós). |
| Livro Digital de Apoio | `UNKNOWN` | Mencionado como premissa textual no mapa mental ("Leia o livro digital que está como material complementar"), porém sem título, link externo ou arquivo anexado na exportação. |

---

## Análise: Extração Integral das Fases do Método MALT

### 1. Fase `M` — Modelagem
- **Objetivo Central**: Ter a estrutura e a modelagem de dados pronta e implementada no código.
- **Recursos Técnicos**: Desenho no papel/diagrama, Migrations, Models Eloquent e relacionamentos, Factories, Seeders.
- **Bateria de Perguntas (12 Dimensões)**:
  1. *Qual é o objetivo do sistema?* O que o sistema precisa realizar? Qual é o seu propósito principal? Quais são as principais funcionalidades que o sistema precisa oferecer?
  2. *Quais são as entidades principais?* Quais são os principais elementos que precisam ser representados no sistema? (Ex.: Usuários, Pedidos, Produtos). Cada entidade identificada é realmente necessária?
  3. *Quais atributos cada entidade deve ter?* Quais informações precisam ser armazenadas para cada entidade? (Ex.: Nome, Preço, Quantidade, E-mail). Há alguma informação que pode ser derivada ou que depende de outra entidade?
  4. *Como as entidades estão relacionadas entre si?* Como as entidades se conectam? (Ex.: Um usuário pode fazer vários pedidos; um pedido pode ter vários produtos). Qual é a cardinalidade dessas relações? (Ex.: Um para muitos, muitos para muitos).
  5. *Quais são as regras de negócio?* Existem restrições ou regras específicas que precisam ser aplicadas? (Ex.: Um produto só pode pertencer a uma categoria e a uma marca). Como o sistema deve lidar com operações específicas, como adicionar um novo pedido ou calcular o total de um pedido?
  6. *Como os dados serão usados?* Quais operações de CRUD serão realizadas com cada entidade? Quais consultas e relatórios serão necessários? (Ex.: Listar produtos por categoria, pedidos por usuário).
  7. *Como a segurança será gerenciada?* Quem pode acessar ou modificar os dados? (Ex.: Controle de acesso baseado em funções). Quais dados são sensíveis e precisam de proteção adicional?
  8. *Como a performance será gerenciada?* Como o sistema deve escalar? (Ex.: Otimizações para consultas frequentes). Quais índices serão necessários para melhorar a performance de busca?
  9. *Existem requisitos de auditoria ou histórico?* Precisamos armazenar histórico de mudanças? (Ex.: Histórico de pedidos, alterações de preço). Como os registros antigos serão tratados?
  10. *Quais são as necessidades de integração com outros sistemas?* O sistema precisa se integrar a outros sistemas? Como serão feitas essas integrações? Como os dados serão sincronizados entre diferentes sistemas?
  11. *Quais são as expectativas dos stakeholders?* Como os envolvidos no projeto esperam que o sistema funcione? Existem expectativas específicas em termos de funcionalidades, usabilidade ou prazo?
  12. *Como o sistema evoluirá no futuro?* Há considerações para futuras expansões ou novas funcionalidades? Como a modelagem pode ser flexível para futuras mudanças?

### 2. Fase `A` — Ação
- **Objetivo Central**: Garantir que a requisição saia do cliente, chegue no servidor, passe pelos filtros iniciais e volte até o cliente. Tudo o que serve como alicerce para a lógica da aplicação (sem regras de negócio nesta fase).
- **Recursos Técnicos**: Rotas, Controllers (sem regra de negócio, apenas esqueleto/stubs), Middlewares, Policies, Gates, Queues, Jobs, Events, Artisan Commands.
- **Bateria de Perguntas (7 Dimensões)**:
  1. *Quais são os fluxos principais de usuário?* Quais são as principais ações que os usuários precisam realizar no sistema? (Ex.: Fazer login, adicionar itens ao carrinho, finalizar compra). Como os usuários navegam entre diferentes partes da aplicação?
  2. *Como as rotas serão definidas?* Quais são as rotas necessárias para cada funcionalidade? (Ex.: Rotas para CRUD de usuários, produtos, pedidos). As rotas seguem uma convenção consistente e fácil de entender? (Ex.: `/users`, `/orders/{id}`, `/products/{id}/edit`). Existe a necessidade de agrupamento de rotas ou prefixos? (Ex.: `/admin/*`).
  3. *Como os controllers serão estruturados?* Quais controllers serão necessários e quais métodos eles precisam ter? (Ex.: `UserController`, `OrderController`). Cada controller está focado em uma responsabilidade específica? Existe a necessidade de controllers RESTful ou controllers invocáveis (`__invoke`)?
  4. *Como o fluxo de dados será gerenciado entre o frontend e o backend?* Como os dados serão enviados e recebidos entre o cliente e o servidor? (Ex.: JSON via AJAX, formulários HTML). Quais dados precisam ser validados no backend? Como essa validação será feita?
  5. *Como o middleware será utilizado?* Quais funcionalidades ou verificações precisam ser aplicadas de forma transversal? (Ex.: Autenticação, autorização, verificação de CSRF). Existe algum middleware personalizado que precisa ser criado para atender a requisitos específicos?
  6. *Quais permissões e acessos são necessários?* Quais usuários têm permissão para acessar ou modificar determinadas partes da aplicação? (Ex.: Apenas administradores podem gerenciar usuários). Como as políticas de acesso e autorização serão implementadas? (Ex.: Uso de Policies e Gates).
  7. *Como a segurança será implementada nas rotas e ações?* Como garantir que apenas usuários autenticados possam acessar certas rotas? Quais medidas de segurança adicionais são necessárias para proteger os dados enviados e recebidos? (Ex.: HTTPS, validação de entrada).

### 3. Fase `L` — Lógica
- **Objetivo Central**: Garantir que a regra de negócio e o processamento da requisição ocorram conforme os requisitos dos clientes/usuários.
- **Recursos Técnicos**: Controllers (orquestrando), Classes de serviço / Actions dedicadas, Frontend (Views, Livewire, Inertia).
- **Bateria de Perguntas (8 Dimensões)**:
  1. *Quais são as regras de negócio principais?* Quais são as regras e políticas específicas que o sistema precisa seguir? (Ex.: Cálculo de impostos, regras de descontos, verificação de estoque). Como essas regras se aplicam em diferentes partes da aplicação? (Ex.: Regras de validação ao criar ou atualizar registros).
  2. *Como as regras de negócio serão encapsuladas?* Como as regras de negócio podem ser organizadas de maneira modular? (Ex.: Utilização de serviços, Commands, Actions). Como garantir que a lógica de negócio não esteja acoplada diretamente aos controladores ou modelos?
  3. *Como o sistema deve reagir a diferentes estados e condições?* Quais são os estados possíveis para as principais entidades? (Ex.: Status de um pedido: pendente, pago, cancelado). Como o sistema deve responder a diferentes estados ou condições? (Ex.: O que acontece se o estoque de um produto é insuficiente?).
  4. *Como o sistema deve lidar com exceções e erros?* Quais erros são esperados e como eles devem ser tratados? (Ex.: Falha ao conectar a um serviço externo, dados inválidos). Como implementar um tratamento de exceções centralizado que garanta a robustez do sistema?
  5. *Como garantir que a lógica implementada seja eficiente?* Como garantir que as operações intensivas sejam otimizadas? (Ex.: Minimização de loops aninhados, consultas otimizadas). Existe a necessidade de pré-processamento ou caching para melhorar a performance?
  6. *Como garantir a escalabilidade da lógica implementada?* Como a lógica pode ser escalada para lidar com um maior volume de dados ou requisições? (Ex.: Uso de filas, processamento paralelo). Existem gargalos potenciais que podem ser identificados e mitigados desde cedo?
  7. *Como será feita a comunicação entre diferentes partes do sistema?* Como diferentes módulos e componentes da aplicação se comunicarão entre si? (Ex.: Eventos, notificações, mensagens). Como garantir que a comunicação entre partes do sistema seja eficiente e desacoplada?
  8. *Como a lógica será monitorada em produção?* Como monitorar e medir a performance da lógica em um ambiente de produção? (Ex.: Logs detalhados, métricas de performance). Existem alertas e notificações configurados para problemas críticos?

### 4. Fase `T` — Testes
- **Objetivo Central**: Garantir que tudo o que foi desenvolvido até aqui esteja funcionando como deveria e, no futuro, em caso de alteração, continue funcionando como deveria.
- **Recursos Técnicos**: PestPHP, Laravel Dusk.
- **Bateria de Perguntas (5 Dimensões)**:
  1. *Quais são os fluxos de usuário mais importantes?* Quais são os principais fluxos que os usuários irão percorrer na aplicação? (Ex.: Cadastro, compra, checkout). Como garantir que esses fluxos funcionem conforme o esperado em diferentes cenários? (Ex.: Testar diferentes inputs, condições limítrofes).
  2. *Quais funcionalidades críticas precisam ser testadas?* Quais partes do sistema, se falharem, causarão os maiores problemas para os usuários ou o negócio? (Ex.: Processamento de pagamentos, autenticação de usuários). Existem funcionalidades particularmente sensíveis a erros? (Ex.: Cálculos financeiros, manipulação de dados sensíveis).
  3. *Quais integrações precisam ser testadas?* O sistema se integra com serviços externos ou APIs? (Ex.: Gateways de pagamento, serviços de terceiros). Como garantir que essas integrações funcionem corretamente, mesmo quando o serviço externo apresenta falhas ou mudanças?
  4. *Quais cenários de falha devem ser testados?* O que pode dar errado no sistema e como ele deve reagir? (Ex.: Falha ao se conectar ao banco de dados, entradas inválidas). Como garantir que o sistema lida corretamente com erros e exceções?
  5. *Quais são as funcionalidades que mais mudam ou são mais voláteis?* Quais funcionalidades estão em constante evolução ou são frequentemente alteradas? (Ex.: Funcionalidades em desenvolvimento ativo, áreas sujeitas a muitas mudanças de requisitos). Como garantir que essas funcionalidades sejam testadas adequadamente após cada mudança?

---

## Reflexões e Inferências: Enquadramento em Abordagem Paralela com Laravel

### 1. O MALT Tradicional (Linear / Inside-Out)
No desenho original do mapa mental, o MALT opera como um funil horizontal e linear:
```
[Modelagem do Sistema Todo] ──► [Ação / Todas as Rotas] ──► [Lógica de Negócio] ──► [Testes no Final]
```
- **Pontos Fortes**: Excelente para iniciantes ou desenvolvedores solo que travam diante de um projeto novo. Fornece uma ordem cronológica clara de criação de arquivos no Laravel (`make:model -mf` -> `routes/web.php` + `make:controller` -> `Services` -> `Pest`).
- **Limitações do Modelo Linear**:
  - Testes postergados para o final aumentam o risco de retrabalho se a modelagem inicial estiver desalinhada da experiência do usuário.
  - Tenta antecipar todo o esquema relacional antes de saber como a tela e a regra vão de fato consumir os dados.

### 2. A Abordagem Paralela: MALT em Fatias Verticais (Vertical Slice Architecture)
Na dinâmica sênior de desenvolvimento no Laravel, o MALT se potencializa quando deixamos de aplicá-lo em camadas horizontais monolíticas e passamos a executá-lo em **fatias verticais paralelas por Caso de Uso**:

```
                       FATIA VERTICAL (Caso de Uso 1: Ex. "Emitir Nota Fiscal")
                     ┌────────────────────────────────────────────────────────┐
Especificação Prévia ─► [ M (Model/Mig) ] ─► [ A (Route/Livewire) ] ─► [ L (Action) ] ─► [ T (Pest BDD) ]
                     └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                       FATIA VERTICAL (Caso de Uso 2: Ex. "Cancelar Pedido")
                     ┌────────────────────────────────────────────────────────┐
Especificação Prévia ─► [ M (Model/Mig) ] ─► [ A (Route/Livewire) ] ─► [ L (Action) ] ─► [ T (Pest BDD) ]
                     └────────────────────────────────────────────────────────┘
```

Nessa abordagem:
- O `M` é enxuto, modelando apenas as colunas e tabelas estritamente necessárias para aquela fatia (YAGNI).
- O `A` e o `L` são desenvolvidos de ponta a ponta no mesmo ciclo.
- O `T` roda imediatamente ao fechar a fatia, garantindo que o caso de uso esteja verde antes de partir para o próximo.

### 3. MALT Invertido (Outside-In / TDD Guiado por Comportamento)
Na dinâmica do usuário — que prioriza determinismo, testes não-mascarados e ferramentas como o CLEARER Engineering Harness e Ralph Method — o `T` pode atuar em simbiose paralela com o `A`:

1. **`A` + `T` (Fio Condutor)**: Escreve-se primeiro o teste de feature em Pest (`test('administrador pode aprovar pedido pendente')`). O teste dispara a rota (Ação). O teste falha porque a rota ou a modelagem ainda não existem (Vermelho).
2. **`M` (Persistência Mínima)**: Cria-se a migration e o model estritamente necessários para satisfazer o teste.
3. **`L` (Regra Pura)**: Isola-se a regra em uma Action pura (`App\Actions\ApproveOrderAction`). O teste passa (Verde).
4. **Refactor & Hardening**: Refina-se a fatia com polimento sem quebrar o teste.

### 4. Integração com a Stack Moderna do Usuário

| Pilar MALT | Ferramenta / Padrão na sua Rotina | Como se Integra |
|---|---|---|
| **Modelagem (`M`)** | **Laravel Boost MCP** + **Migrations incrementais** | Schemas e relacionamentos são validados via Artisan diretamente no container, com tipagem estrita no PHP 8.4+ e `casts` explícitos. |
| **Ação (`A`)** | **TALL Stack (Livewire v3/v4 / Filament v4/v5)** | O transporte muitas vezes não é um Controller tradicional com Blade, mas um componente Livewire ou Resource do Filament. O `A` garante que o evento/método (`wire:click`, action modal) responde e valida o Form Request. |
| **Lógica (`L`)** | **Actions de Responsabilidade Única & DDD** | Em vez de jogar regras no Controller ou no Model Eloquent, a lógica fica em classes auto-contidas (`app/Actions/`), garantindo transações atômicas (`DB::transaction`) e disparando Events para processos assíncronos. |
| **Testes (`T`)** | **PestPHP + BDD Determinístico** | Testes de integração em memória ou SQLite/banco de teste local cobrindo a tríade: *Happy Path* (fluxo ideal), *Unhappy Path* (validações e exceções) e *Edge Cases* (permissões via Gates/Policies). |

---

## Anexos

1. [`anexos/malt-mindmap-export.json`](./anexos/malt-mindmap-export.json): Extração bruta em formato JSON obtida diretamente da API do MindMeister (122 nós).
2. [`anexos/malt-tree-hierarchy.md`](./anexos/malt-tree-hierarchy.md): Árvore textual hierárquica completa com todos os nós ordenados por rank e parentesco.

---

## Fechamento (contrato de resposta)

```
Resultado:   Registro formal da discussão sobre o Método MALT, consolidação da árvore
             completa de 122 nós extraída da API do MindMeister e mapeamento analítico
             de como enquadrá-lo em uma abordagem paralela (Vertical Slices & Outside-In)
             no ecossistema Laravel.
Evidências:
  OBSERVED:  - Payload JSON da API do MindMeister capturado via CDP Headless (120.638 bytes).
             - 122 nós estruturados com campos 'parentId', 'rank', 'title' e 'note'.
             - Arquivos salvos em discussoes/2026-11-02-metodo-malt-laravel/ e índice raiz atualizado.
  INFERRED:  - O Método MALT tradicional é um modelo Inside-Out em camadas horizontais, mas sua
               maior eficácia com equipes experientes ocorre quando fatiado verticalmente por caso de uso.
  UNKNOWN:   - O conteúdo do livro digital de apoio mencionado nas premissas do mapa mental.
Confiança:   ALTA — transcrição e análise ancoradas em dados brutos observados.
```
