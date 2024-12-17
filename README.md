<h1>Sobre o projeto</h1>
<p>Este projeto foi desenvolvido como parte da disciplina MI — Concorrência e Conectividade do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS). Ele representa um sistema de apostas distribuído, criado para explorar conceitos de concorrência e conectividade em rede de computadores.</p>
<div id = "introducao"> 
  <h1>Introdução</h1>
  <p> 
  Este relatório apresenta o desenvolvimento de um sistema de apostas que permite aos clientes realizar e acompanhar eventos de apostas em tempo real, assim como os resultados, de forma transparente e confiável. Para registrar os eventos e as transações subjacentes, é utilizada uma tecnologia de livro-razão (ledger) distribuído, mais especificamente a blockchain da rede Ethereum. Foi desenvolvida uma aplicação cliente que se conecta à rede blockchain e realiza operações por meio de contratos implementados nela, proporcionando ao usuário uma interface interativa e responsiva, conforme as ações solicitadas. Os dados (registro de transações) são armazenados no livro-razão de cada nó da blockchain. O sistema, por ser capaz de se conectar a uma rede real de blockchain, se beneficia dos mecanismos de controle de transações, como o Proof-of-Stake (PoS). Os resultados gerados demonstram que o sistema consegue gerenciar as apostas de forma inteligente e descentralizada, garantindo a imutabilidade e transparência dos dados.
  </p>
</div>

<h2>Equipe</h2>
<uL>
  <li><a href="https://github.com/DiogoDSJ">Diogo dos Santos de Jesus</a></li>
  <li><a href="https://github.com/eugabrielbr">Gabriel Silva dos Santos</a></li>
</ul>

<h2>Tutor</h2>
<uL>
  <li>Prof. Me. Antonio Augusto Teixeira Ribeiro Coutinho (UEFS)</li>
</ul>

<h2>Fundamentação</h2>
<div id="fundamentacao">

  <h3>Blockchain</h3>
  <p>A blockchain é uma tecnologia inovadora baseada em uma estrutura de dados descentralizada, que organiza informações em blocos encadeados de maneira sequencial e segura. Cada bloco contém um conjunto de transações, e cada transação registrada é criptografada, garantindo que ela seja protegida contra modificações ou fraudes. A principal característica da blockchain é a sua imutabilidade, ou seja, uma vez que um bloco é adicionado à cadeia, ele não pode ser alterado. Isso é garantido por algoritmos de consenso que validam e verificam as transações antes de sua inclusão, como o Proof of Work (PoW) e o Proof of Stake (PoS). Esses algoritmos asseguram que todos os participantes da rede cheguem a um consenso sobre o estado das transações, sem a necessidade de uma autoridade central.</p>
  <p>Além da segurança e imutabilidade, a blockchain é descentralizada, o que significa que não existe um único ponto de falha ou controle. A rede é mantida por diversos nós, ou computadores, distribuídos geograficamente, que colaboram para validar e registrar transações de forma transparente. Esse modelo elimina a necessidade de intermediários, reduzindo custos e aumentando a eficiência das transações. Cada participante da rede pode acessar e verificar as transações, garantindo a transparência e a confiança no sistema.</p>
  <p>No sistema de apostas, a utilização da blockchain oferece diversas vantagens. A principal delas é a transparência, pois todas as apostas, resultados e transações ficam registradas de forma pública e imutável na blockchain, permitindo que qualquer pessoa verifique a integridade dos eventos. Além disso, a descentralização do sistema torna-o mais seguro e resistente a fraudes, pois não depende de uma entidade central para operar. </p>
  <p>Em vez disso, as apostas são validadas por meio de contratos inteligentes, que garantem que as condições de cada aposta sejam cumpridas automaticamente, sem a necessidade de intervenção humana. A blockchain também assegura a segurança das transações, impedindo alterações nos registros de apostas e garantindo que o processo seja justo e transparente para todos os participantes. Dessa forma, ao usar a blockchain em um sistema de apostas, a confiança dos usuários é aumentada, e a possibilidade de manipulação ou erro é reduzida, proporcionando uma experiência mais confiável e segura.
</p>

<h3>Redes de teste</h3>

<p>Para o desenvolvimento e teste do sistema de apostas, foram utilizadas duas redes distintas: a rede Sepolia e uma rede local de testes com Hardhat.</p>
<p>A rede Sepolia é uma rede de teste pública da blockchain Ethereum, que utiliza o mecanismo de consenso Proof of Stake (PoS). Ao utilizar essa rede, o projeto se beneficia da segurança e integridade proporcionadas pelos validadores da rede. Os validadores são responsáveis pela validação das transações e garantem que as apostas sejam registradas corretamente, mantendo a confiança no processo. Além disso, ao operar em uma rede descentralizada, o sistema de apostas pode ser testado em um ambiente mais próximo da rede principal Ethereum, permitindo uma validação mais robusta e confiável dos contratos inteligentes e das transações realizadas, sem envolver valores reais.</p>
<p>Por outro lado, a rede local de testes com Hardhat foi utilizada para realizar testes rápidos e controlados dentro de um ambiente totalmente controlado. Com ela, o sistema é capaz de criar contas automaticamente, com valores já depositados, permitindo que as apostas sejam realizadas de forma ágil e sem a necessidade de interagir com redes externas. O controle total sobre os saldos e participantes proporciona flexibilidade para testar diversos cenários de apostas e transações em tempo real, sem custos ou complicações. Essa rede local oferece um ambiente ideal para simulações de apostas, onde o comportamento do sistema pode ser ajustado e monitorado com precisão, garantindo a confiança nas operações realizadas no sistema.</p>

<h3>Proof of Stake (PoS)</h3>

<p>A Proof of Stake (PoS) é um mecanismo de consenso utilizado em várias blockchains, incluindo a rede Sepolia, que é uma das redes de teste do Ethereum. Ao contrário do Proof of Work (PoW), que depende de mineração com alta utilização de energia, o PoS oferece uma alternativa mais eficiente e sustentável. Na rede Sepolia, o PoS funciona por meio de validadores, que são responsáveis por validar transações e criar novos blocos, sendo selecionados de acordo com a quantidade de ETH que possuem em staking. Quanto maior a quantidade de ETH que um validador tem em staking, maior é a probabilidade de ser escolhido para propor ou validar um bloco.</p>
<p>A principal vantagem do PoS está no fato de que ele não exige grande poder computacional, como ocorre no PoW, o que resulta em um consumo de energia muito mais baixo. Além disso, o PoS incentiva a segurança e a descentralização, pois qualquer pessoa com ETH pode se tornar um validador e participar do processo de validação. Em troca da validação de blocos, os validadores recebem recompensas em ETH, que servem como incentivo para garantir o bom funcionamento da rede.</p>
<p>Quando implementado na rede pública do Ethereum, como a Sepolia, o Proof of Stake oferece uma série de benefícios para o projeto, como uma maior eficiência energética, custos reduzidos e um processo de consenso mais acessível e descentralizado. Esses benefícios são especialmente importantes para a aplicação em um ambiente de blockchain, proporcionando uma rede mais segura, econômica e escalável. O projeto, ao ser executado em uma rede pública como a Sepolia, pode aproveitar essas vantagens do PoS, resultando em uma implementação mais eficiente e sustentável.</p>

<h3>Web3</h3>

<p>
A biblioteca Web3 é uma ferramenta essencial para a interação com blockchains baseadas na tecnologia Ethereum. Ela fornece uma interface de programação (API) que permite que desenvolvedores criem aplicações descentralizadas (DApps), realizem transações, gerenciem contratos inteligentes e interajam com redes blockchain de forma programática.</p>
<p>Entre suas principais funcionalidades, destaca-se a capacidade de conectar aplicações a nós da blockchain, sejam eles locais, remotos ou fornecidos por serviços como Infura ou Alchemy. Essa conectividade permite interagir com contratos inteligentes implantados na rede, possibilitando a leitura de dados, a execução de funções e o envio de transações. A Web3 também permite a gestão de contas, como a criação de carteiras digitais, a assinatura de transações e a verificação de assinaturas digitais. Adicionalmente, a biblioteca oferece métodos para acessar informações da blockchain, como saldos de contas, estados de contratos e históricos de transações, proporcionando uma interface prática e eficiente para desenvolvedores.</p>
<p>O uso da Web3 traz diversos benefícios significativos. Ela abstrai a complexidade inerente ao protocolo Ethereum, simplificando o desenvolvimento e permitindo que os programadores se concentrem nos aspectos inovadores de suas aplicações. Além disso, sua ampla adoção no ecossistema Ethereum garante acesso a uma rica documentação, suporte da comunidade e recursos que aceleram o desenvolvimento. Outro ponto positivo é sua compatibilidade com redes que utilizam a Ethereum Virtual Machine (EVM), como Binance Smart Chain e Polygon, expandindo as possibilidades de integração e aplicação.</p>


</div>


<h2>Metodologia</h2>
<div id="metodologia">

<h3>Contas</h3>

<p>O sistema utiliza carteiras Ethereum como a carteira padrão para os usuários, permitindo que realizem depósitos e saques da mesma forma que em uma rede Ethereum convencional. Essa integração proporciona uma experiência segura e familiar, aproveitando as vantagens da blockchain, como a transparência e imutabilidade das transações. Um benefício adicional é que o sistema realiza a verificação do saldo da carteira do usuário no momento do login, garantindo que o valor esteja sempre atualizado. Além disso, o sistema converte automaticamente o saldo para reais, oferecendo uma visão clara e acessível do valor disponível para o usuário, facilitando a interação com o sistema.</p>
<p>O sistema também permite o registro de novas carteiras Ethereum, criando uma experiência completa para o usuário. Ao registrar uma nova carteira, o sistema gera e retorna tanto a chave pública quanto a chave privada, garantindo que o usuário tenha total controle sobre sua carteira. A chave pública é utilizada para receber depósitos, enquanto a chave privada é crucial para a realização de transações e saques, sendo sempre fornecida ao usuário de forma segura. Isso garante que o sistema não apenas suporte a integração com carteiras Ethereum, mas também facilite a criação de novas carteiras de forma simples e segura.</p>

<h3>Contrato</h3>

<p>O contrato inteligente desenvolvido para a rede Ethereum e utilizado no sistema permite que os usuários criem apostas de cara ou coroa, proporcionando uma experiência interativa e segura. Nesse sistema, vários jogadores podem participar da mesma aposta, escolhendo entre "cara" ou "coroa" e depositando um valor no contrato na expectativa de que outros jogadores se juntem. Contudo, o contrato impõe algumas regras que garantem a integridade e o bom funcionamento das apostas.</p>
<p>Uma dessas regras é que um jogador não pode participar de mais de uma aposta simultaneamente. Isso evita que um jogador acumule apostas em aberto e assegura que ele esteja comprometido com uma única aposta por vez. Além disso, o contrato impede que um jogador aceite sua própria aposta, garantindo que sempre haja um adversário para a disputa. Para criar uma nova aposta, o jogador deve finalizar a aposta anterior, evitando que múltiplas apostas fiquem abertas ao mesmo tempo.</p>
<p>Outro requisito essencial do contrato é que existe um valor mínimo para cada aposta, e o jogador só pode criar uma aposta ou participar de uma existente se tiver saldo suficiente na carteira para cobrir o valor exigido. O jogador também é obrigado a depositar um valor e escolher seu lado (cara ou coroa) no evento criado antes de concluir sua participação.</p>
<p>Além disso, cada ação realizada dentro do contrato, seja a criação, aceitação, finalização da aposta ou distribuição dos valores, emite um evento na blockchain. Isso garante que todos os participantes possam acompanhar, em tempo real, o andamento da aposta, desde a sua criação até a finalização e a distribuição dos valores aos vencedores. Dessa forma, o contrato assegura transparência e confiança em cada etapa do processo, proporcionando uma experiência justa e segura para todos os envolvidos.</p>

<h3>Eventos</h3>

<p>O sistema de apostas foi desenvolvido para permitir a criação de eventos de forma interativa e transparente, com a emissão de notificações para todas as ações importantes do processo. Ao criar uma aposta, o jogador criador deixa o evento em aberto, permitindo que até 9 outros jogadores entrem. Essa notificação é emitida em tempo real, garantindo que todos os participantes acompanhem a criação e a disponibilidade para novas entradas.</p>
<p>Durante o processo, o jogador criador tem a capacidade de encerrar o evento a qualquer momento. Caso o número mínimo de jogadores seja atingido, o evento segue com os participantes registrados e a aposta é finalizada conforme as regras definidas. Se apenas o jogador criador se inscrever, ele poderá encerrar a aposta, e o valor apostado será devolvido automaticamente. Nesse caso, se ele ganhar, receberá o prêmio, mas se não houver vencedores, o dinheiro também é devolvido, sendo contabilizado como "sem ganhadores".</p>
<p>As ações de criação, aceitação e finalização da aposta geram notificações que são visíveis em tempo real. Isso garante que todas as interações sejam acompanhadas por todos os participantes e observadores, promovendo transparência e uma experiência dinâmica e interativa.</p>

<h3>Apostas</h3>

<p>O sistema de apostas funciona da seguinte forma: um jogador pode criar uma aposta especificando um valor em Ether e sua escolha (cara ou coroa). Essa transação é enviada para o contrato inteligente, que armazena as informações da aposta e emite o evento "ApostaCriada". Outro jogador pode, então, aceitar essa aposta, também enviando o mesmo valor em Ether e selecionando sua escolha. O contrato inteligente, ao receber a aceitação, emite o evento "ApostaAceita", confirmando a entrada do segundo jogador na aposta.</p>

<p>Após a aceitação, o jogo pode ser finalizado. Isso é feito por meio da função resolverJogo, que determina o vencedor com base em uma lógica definida no contrato. O vencedor recebe o prêmio total, e o evento "JogoFinalizado" é emitido com os detalhes da aposta, o vencedor e o valor do prêmio. Em caso de necessidade, há também a possibilidade de reverter estados utilizando a função revert, que pode corrigir inconsistências no contrato.</p>

<h3>Simulação</h3>

<p>O código é capaz de simular eventos em tempo real devido à sua abordagem de escuta contínua de eventos na blockchain. Ele utiliza filtros de eventos do contrato inteligente, como ApostaCriada, ApostaAceita, e JogoFinalizado, que monitoram novos eventos conforme eles ocorrem. Essa técnica permite que o código capture instantaneamente as transações e mudanças de estado dentro do contrato inteligente.</p>

<p>Além disso, o uso de uma thread dedicada para a escuta de eventos garante que o processo de escuta e processamento ocorra paralelamente ao script principal. Isso significa que, mesmo enquanto o resto do programa está executando outras tarefas ou aguardando por entrada do usuário, ele ainda pode detectar e processar eventos na blockchain em tempo real.</p>

<p>Por fim, a função get_new_entries() é crucial para a simulação em tempo real, pois permite ao código verificar continuamente por novos eventos, garantindo que mudanças e atualizações no contrato inteligente sejam refletidas instantaneamente no sistema simulado. Essa capacidade de responder a mudanças em tempo real é fundamental para a simulação realista de um sistema baseado em blockchain.</p>

<h3>Odds</h3>

<p>O sistema implementado garante o cálculo correto das odds das apostas e a distribuição proporcional dos prêmios aos jogadores, considerando que o valor apostado por cada participante é fixo e igual para todos. Essa uniformidade no valor das apostas simplifica o cálculo das probabilidades e assegura a equidade entre os jogadores.</p>

<p>A definição das odds é feita com base na quantidade de jogadores que escolhem cada lado (cara ou coroa). Como o valor apostado é o mesmo para todos, as odds refletem diretamente a proporção de jogadores em cada opção. Por exemplo, se mais jogadores apostam em "cara" do que em "coroa", aqueles que escolheram "coroa" têm maiores chances de retorno, pois o prêmio total será dividido entre um grupo menor de vencedores.</p>

<p>A redistribuição dos prêmios ocorre automaticamente após o encerramento da aposta, de acordo com o resultado final (cara ou coroa). O valor total das apostas, menos possíveis taxas, é distribuído igualmente entre os jogadores que escolheram o lado vencedor. Como todos os participantes apostam o mesmo valor, a divisão do prêmio é feita de forma simples e direta, sem necessidade de cálculos adicionais relacionados a diferentes montantes apostados.</p>

<h3>Contabilidade</h3>

<p>Cada ação no sistema, como a criação de uma aposta ou a resolução de um jogo, é registrada e emitida como um evento. Isso garante que todos os participantes estejam cientes das transações ocorrendo e das alterações nos saldos. Os eventos também servem para comunicar diretamente mudanças de estado no contrato inteligente, como a finalização de uma aposta ou a distribuição de prêmios, facilitando a auditoria e o controle das transações.</p>

<p>Além disso, a validação de endereços e as verificações de segurança incorporadas ao sistema ajudam a prevenir transações fraudulentas. A função de validar endereços verifica se o endereço público do usuário é válido e, opcionalmente, se ele está no formato de checksum. Essas verificações ajudam a garantir que apenas endereços legítimos possam interagir com o contrato, aumentando a integridade das transações.</p>

<p>A implementação das funções criarAposta e resolverJogo também é crucial para garantir a integridade do sistema. Elas utilizam o contrato inteligente para efetuar transações de criação e resolução de apostas, o que significa que todas as interações com o blockchain são realizadas de forma segura. As funções constroem e assinam transações corretamente, o que impede que transações fraudulentas ou mal-formadas sejam executadas. Isso é particularmente importante para a criação de apostas, onde o saldo do jogador é bloqueado no contrato inteligente, e para a resolução de jogos, onde os prêmios são distribuídos de acordo com os resultados calculados.</p>

<h3>Publicação</h3>

<p>No tópico de publicação, é importante destacar que o sistema foi desenvolvido para garantir a privacidade e o controle de acesso ao histórico das apostas. Diferentemente de sistemas que permitem a visualização completa de todos os eventos ou transações realizadas, este sistema só possibilita o acesso ao histórico de uma aposta específica mediante o uso do seu identificador único (ID).</p>

<p>Essa abordagem significa que não é possível listar todas as apostas realizadas indiscriminadamente. Para consultar informações sobre uma aposta, o usuário precisa fornecer o ID correspondente, o que restringe o acesso aos dados apenas àqueles que possuem esse identificador. Essa funcionalidade não apenas limita o escopo das consultas, mas também reforça a segurança e privacidade das informações no sistema, evitando acessos não autorizados ou análises em larga escala sem o devido consentimento.</p>

<p>O uso do ID como chave de acesso promove um controle mais preciso sobre quais apostas podem ser consultadas e por quem, alinhando-se às boas práticas de proteção de dados e privacidade em sistemas distribuídos e baseados em blockchain. Dessa forma, a transparência sobre os resultados é mantida, mas sem expor o histórico completo das transações de forma aberta.</p>

</div>
  
<h2>Conclusão</h2>
<div id="conclusao">

<p>O projeto de sistema de apostas distribuído desenvolvido dentro da disciplina MI — Concorrência e Conectividade do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS) implementou todos os requisitos e funcionalidades solicitados. O sistema utiliza a tecnologia de blockchain, especificamente a rede Ethereum, para garantir a transparência, segurança e imutabilidade das transações. A implementação de contratos inteligentes permite que todas as apostas e transações sejam registradas automaticamente na blockchain, proporcionando uma experiência justa e transparente para os usuários. Além disso, o uso do Proof of Stake (PoS) na rede Sepolia oferece eficiência energética e redução de custos, enquanto a biblioteca Web3 facilita a interação programática com a blockchain. A capacidade do sistema em simular eventos em tempo real através de filtros de eventos e a escuta contínua dos mesmos assegura que todos os participantes possam acompanhar os resultados e mudanças nas apostas em tempo real.</p>
