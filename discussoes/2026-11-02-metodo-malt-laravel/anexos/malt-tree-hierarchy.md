- **MÉTODO MALT**
  - **O método**
    - **Modelagem**
      - **Objetivo: Ter a estrutura e amodelagem de dados pronta eimplementada no código.**
      - **Recursos mais usados nessa etapa:Desenho no papel/diagrama,Migrations, Models erelacionamentos, Factories,Seeders**
      - **Questões a fazer a si mesmo e aosenvolvidos**
        - **1. Qual é o objetivo do sistema?**
          - **Quais são as principais funcionalidades que o sistema precisa oferecer?**
          - **O que o sistema precisa realizar? Qual é o seu propósito principal?**
        - **2. Quais são as entidades principais?**
          - **Quais são os principais elementos que precisam ser representados no sistema? (Ex.: Usuários, Pedidos, Produtos)**
          - **Cada entidade identificada é realmente necessária?**
        - **3. Quais atributos cada entidade deve ter?**
          - **Quais informações precisam ser armazenadas para cada entidade? (Ex.: Nome, Preço, Quantidade, E-mail)**
          - **Há alguma informação que pode ser derivada ou que depende de outra entidade?**
        - **4. Como as entidades estão relacionadas entre si?**
          - **Como as entidades se conectam? (Ex.: Um usuário pode fazer vários pedidos; um pedido pode ter vários produtos)**
          - **Qual é a cardinalidade dessas relações? (Ex.: Um para muitos, muitos para muitos)**
        - **5. Quais são as regras de negócio?**
          - **Existem restrições ou regras específicas que precisam ser aplicadas? (Ex.: Um produto só pode pertencer a uma categoria e a uma marca)**
          - **Como o sistema deve lidar com operações específicas, como adicionar um novo pedido ou calcular o total de um pedido?**
        - **6. Como os dados serão usados?**
          - **Quais operações de CRUD (Criar, Ler, Atualizar, Deletar) serão realizadas com cada entidade?**
          - **Quais consultas e relatórios serão necessários? (Ex.: Listar produtos por categoria, pedidos por usuário)**
        - **7. Como a segurança será gerenciada?**
          - **Quem pode acessar ou modificar os dados? (Ex.: Controle de acesso baseado em funções)**
          - **Quais dados são sensíveis e precisam de proteção adicional?**
        - **8. Como a performance será gerenciada?**
          - **Como o sistema deve escalar? (Ex.: Otimizações para consultas frequentes)**
          - **Quais índices serão necessários para melhorar a performance de busca?**
        - **9. Existem requisitos de auditoria ou histórico?**
          - **Precisamos armazenar histórico de mudanças? (Ex.: Histórico de pedidos, alterações de preço)**
          - **Como os registros antigos serão tratados?**
        - **10. Quais são as necessidades de integração com outros sistemas?**
          - **O sistema precisa se integrar a outros sistemas? Como serão feitas essas integrações?**
          - **Como os dados serão sincronizados entre diferentes sistemas?**
        - **11. Quais são as expectativas dos stakeholders?**
          - **Como os envolvidos no projeto esperam que o sistema funcione?**
          - **Existem expectativas específicas em termos de funcionalidades, usabilidade ou prazo?**
        - **12. Como o sistema evoluirá no futuro?**
          - **Há considerações para futuras expansões ou novas funcionalidades?**
          - **Como a modelagem pode ser flexível para futuras mudanças?**
    - **Ação**
      - **Objetivo: Garantir que a requisiçãosaia do cliente, chegue no servidor, passe pelos filtros iniciais e volteaté o cliente.
Tudo o que serve como alicercepara a lógica da aplicação.**
      - **Recursos mais usados nessa etapa:Rotas, Controllers (sem a regra denegócio nessa etapa),Middlewares, Polices, Gates,Queues, Jobs, Events, ArtisanCommands**
      - **Questões a fazer a si mesmo e aosenvolvidos**
        - **1. Quais são os fluxos principais de usuário?**
          - **Como os usuários navegam entre diferentes partes da aplicação?**
          - **Quais são as principais ações que os usuários precisam realizar no sistema? (Ex.: Fazer login, adicionar itens ao carrinho, finalizar compra)**
        - **2. Como as rotas serão definidas?**
          - **Existe a necessidade de agrupamento de rotas ou prefixos? (Ex.: /admin/* para rotas de administração)**
          - **Quais são as rotas necessárias para cada funcionalidade? (Ex.: Rotas para CRUD de usuários, produtos, pedidos)**
          - **As rotas seguem uma convenção consistente e fácil de entender? (Ex.: /users, /orders/{id}, /products/{id}/edit)**
        - **3. Como os controllers serão estruturados?**
          - **Quais controllers serão necessários e quais métodos eles precisam ter? (Ex.: UserController, OrderController)**
          - **Cada controllers está focado em uma responsabilidade específica?**
          - **Existe a necessidade de controllers RESTful ou controllers invocáveis?**
        - **4. Como o fluxo de dados será gerenciado entre o frontend e o backend?**
          - **Como os dados serão enviados e recebidos entre o cliente e o servidor? (Ex.: JSON via AJAX, formulários HTML)**
          - **Quais dados precisam ser validados no backend? Como essa validação será feita?**
        - **5. Como o middleware será utilizado?**
          - **Quais funcionalidades ou verificações precisam ser aplicadas de forma transversal? (Ex.: Autenticação, autorização, verificação de CSRF)**
          - **Existe algum middleware personalizado que precisa ser criado para atender a requisitos específicos?**
        - **6. Quais permissões e acessos são necessários?**
          - **Quais usuários têm permissão para acessar ou modificar determinadas partes da aplicação? (Ex.: Apenas administradores podem gerenciar usuários)**
          - **Como as políticas de acesso e autorização serão implementadas? (Ex.: Uso de Policies e Gates)**
        - **7. Como a segurança será implementada nas rotas e ações?**
          - **Como garantir que apenas usuários autenticados possam acessar certas rotas?**
          - **Quais medidas de segurança adicionais são necessárias para proteger os dados enviados e recebidos? (Ex.: HTTPS, validação de entrada)**
    - **Lógica**
      - **Objetivo: Garantir que a regra denegócio e o processamento darequisição ocorra conforme osrequisitos dos clientes/usuários.**
      - **Recursos mais usados nessa etapa:Controllers (com as regras denegócio), Classes de serviço,Frontend**
      - **Questões a fazer a si mesmo e aosenvolvidos**
        - **1. Quais são as regras de negócio principais?**
          - **Como essas regras de negócio se aplicam em diferentes partes da aplicação? (Ex.: Regras de validação ao criar ou atualizar registros)**
          - **Quais são as regras e políticas específicas que o sistema precisa seguir? (Ex.: Cálculo de impostos, regras de descontos, verificação de estoque)**
        - **2. Como as regras de negócio serão encapsuladas?**
          - **Como as regras de negócio podem ser organizadas de maneira modular? (Ex.: Utilização de serviços, Commands)**
          - **Como garantir que a lógica de negócio não esteja acoplada diretamente aos controladores ou modelos?**
        - **3. Como o sistema deve reagir a diferentes estados e condições?**
          - **Quais são os estados possíveis para as principais entidades? (Ex.: Status de um pedido: pendente, pago, cancelado)**
          - **Como o sistema deve responder a diferentes estados ou condições? (Ex.: O que acontece se o estoque de um produto é insuficiente?)**
        - **4. Como o sistema deve lidar com exceções e erros?**
          - **Quais erros são esperados e como eles devem ser tratados? (Ex.: Falha ao conectar a um serviço externo, dados inválidos)**
          - **Como implementar um tratamento de exceções centralizado que garanta a robustez do sistema?**
        - **5. Como garantir que a lógica implementada seja eficiente?**
          - **Como garantir que as operações intensivas sejam otimizadas? (Ex.: Minimização de loops aninhados, consultas otimizadas)**
          - **Existe a necessidade de pré-processamento ou caching para melhorar a performance?**
        - **6. Como garantir a escalabilidade da lógica implementada?**
          - **Como a lógica pode ser escalada para lidar com um maior volume de dados ou requisições? (Ex.: Uso de filas, processamento paralelo)**
          - **Existem gargalos potenciais que podem ser identificados e mitigados desde cedo?**
        - **7. Como será feita a comunicação entre diferentes partes do sistema?**
          - **Como diferentes módulos e componentes da aplicação se comunicarão entre si? (Ex.: Eventos, notificações, mensagens)**
          - **Como garantir que a comunicação entre partes do sistema seja eficiente e desacoplada?**
        - **8. Como a lógica será monitorada em produção?**
          - **Como monitorar e medir a performance da lógica em um ambiente de produção? (Ex.: Logs detalhados, métricas de performance)**
          - **Existem alertas e notificações configurados para problemas críticos?**
    - **Testes**
      - **Objetivo: Garantir que tudo o quefoi desenvolvido até aqui estejafuncionando como deveria e nofuturo em caso de alteração, quecontinue funcionando comodeveria.**
      - **Recursos mais usados nessa etapa:PestPHP, Dusk**
      - **Questões a fazer a si mesmo e aosenvolvidos**
        - **1. Quais são os fluxos de usuáriomais importantes?**
          - **Quais são os principais fluxos queos usuários irão percorrer naaplicação? (Ex.: Cadastro, compra,checkout)**
          - **Como garantir que esses fluxosfuncionem conforme o esperadoem diferentes cenários? (Ex.: Testardiferentes inputs, condiçõeslimítrofes)**
        - **2. Quais funcionalidades críticasprecisam ser testadas?**
          - **Existem funcionalidades que sãoparticularmente sensíveis a erros?(Ex.: Cálculos financeiros,manipulação de dados sensíveis)**
          - **Quais partes do sistema, sefalharem, causarão os maioresproblemas para os usuários ou onegócio? (Ex.: Processamento depagamentos, autenticação deusuários)**
        - **3. Quais integrações precisam sertestadas?**
          - **O sistema se integra com serviçosexternos ou APIs? (Ex.: Gatewaysde pagamento, serviços deterceiros)**
          - **Como garantir que essasintegrações funcionemcorretamente, mesmo quando oserviço externo apresenta falhas oumudanças?**
        - **5. Quais cenários de falha devemser testados?**
          - **O que pode dar errado no sistemae como ele deve reagir? (Ex.: Falhaao se conectar ao banco de dados,entradas inválidas)**
          - **Como garantir que o sistema lidacorretamente com erros eexceções?**
        - **6. Quais são as funcionalidadesque mais mudam ou são maisvoláteis?**
          - **Quais funcionalidades estão emconstante evolução ou sãofrequentemente alteradas? (Ex.:Funcionalidades ainda emdesenvolvimento ativo, áreassujeitas a muitas mudanças derequisitos)**
          - **Como garantir que essasfuncionalidades sejam testadasadequadamente após cadamudança?**
  - **Por quê e como surgiu?**
    - **Desenvolver com Laravel oferecemuita flexibilidade, mas essamesma flexibilidade pode levar aindecisões e confusões. O MétodoMALT foi criado para fornecer umaestrutura clara e organizada,ajudando desenvolvedores a evitaros desafios comuns como análiseparalisante, código desorganizadoe dificuldade em testar. Ao seguiro Método MALT, você economizatempo, evita retrabalhos e garanteum código limpo e de altaqualidade.**
    - **O Método MALT foi criado pararesolver problemas reais queenfrentamos no desenvolvimentode software. Alguns dos principaisdesafios que nos levaram adesenvolver este método incluem:

Análise Paralisante: A liberdadeoferecida pelo Laravel pode levar aindecisões, especialmente quandonão sabemos por onde começar.
Código Desorganizado: Sem umaestrutura clara, o código pode setornar confuso e difícil de manter.
Dificuldade em Testar: Escrevertestes para um códigodesorganizado é complicado, oque deixa a aplicação vulnerável aerros.**
  - **Premissas**
    - **Não adianta tentar aprender oMALT sem entender como oLaravel funciona, portanto, nãopule etapas**
    - **Leia o livro digital que está comomaterial complementar, ele é umcomplemento**
