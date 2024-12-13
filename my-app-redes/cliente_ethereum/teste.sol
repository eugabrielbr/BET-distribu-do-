// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CaraOuCoroa {

    enum Escolha { NENHUMA, CARA, COROA }
    enum StatusJogo { NAO_INICIADO, ESPERANDO_JOGADORES, FINALIZADO }

    struct Aposta {
        address jogador1;
        uint256 valorAposta;
        Escolha[] escolhas;
        address[] jogadores;
        StatusJogo statusJogo;
    }
     

    mapping(bytes32 => Aposta) public apostas;
    mapping(address => bytes32) public apostasPorJogador;

    // Eventos
    event ApostaCriada(bytes32 apostaId, address jogador1, uint256 valorAposta);
    event ApostaParticipante(bytes32 apostaId, address jogador, Escolha escolha);
    event JogoFinalizado(bytes32 apostaId, uint256 valorPremio, address[] vencedores);
    event ApostaEncerrada(bytes32 apostaId);

    modifier semApostaAtiva(address jogador) {
        require(apostasPorJogador[jogador] == 0, "Jogador ja possui uma aposta ativa");
        _;
    }

    modifier apostaExistente(bytes32 apostaId) {
        require(apostas[apostaId].jogador1 != address(0), "Aposta nao encontrada");
        _; 
    }

    modifier jogoEmAndamento(bytes32 apostaId) {
        require(apostas[apostaId].statusJogo == StatusJogo.ESPERANDO_JOGADORES, "Jogo nao esta em andamento");
        _;
    }

    modifier jogoFinalizado(bytes32 apostaId) {
        require(apostas[apostaId].statusJogo == StatusJogo.FINALIZADO, "Jogo nao foi finalizado");
        _;
    }

    // Criar uma nova aposta
    function criarAposta(Escolha _escolha) public payable semApostaAtiva(msg.sender) {
        require(msg.value >= 0.001 ether, "Aposta minima e 0.001 ETH");

        bytes32 apostaId = keccak256(abi.encodePacked(msg.sender, block.timestamp));
        Aposta storage aposta = apostas[apostaId];

        aposta.jogador1 = msg.sender;
        aposta.valorAposta = msg.value;
        aposta.statusJogo = StatusJogo.ESPERANDO_JOGADORES;


        apostas[apostaId].escolhas.push(_escolha);
        apostas[apostaId].jogadores.push(msg.sender); // O jogador criador é adicionado à lista de jogadores

        apostasPorJogador[msg.sender] = apostaId;

        emit ApostaCriada(apostaId, msg.sender, msg.value);
    }

    // Participar de uma aposta
    function participarAposta(bytes32 apostaId, Escolha _escolha) public payable apostaExistente(apostaId) jogoEmAndamento(apostaId) semApostaAtiva(msg.sender) {
        Aposta storage aposta = apostas[apostaId];

        require(aposta.jogadores.length < 10, "Limite de 10 jogadores atingido");
        require(msg.value == aposta.valorAposta, "O valor da aposta deve ser o mesmo do criador");

        aposta.jogadores.push(msg.sender);
        aposta.escolhas.push(_escolha);
        apostasPorJogador[msg.sender] = apostaId;

        emit ApostaParticipante(apostaId, msg.sender, _escolha);

        // Se 10 jogadores participaram, o jogo é finalizado
        if (aposta.jogadores.length == 10) {
            aposta.statusJogo = StatusJogo.FINALIZADO;
            resolverJogo(apostaId);
        }
    }

    // Resolver o jogo
    function resolverJogo(bytes32 apostaId) public apostaExistente(apostaId) jogoFinalizado(apostaId) {
        Aposta storage aposta = apostas[apostaId];

        uint256 resultado = random() % 2; // 0 para CARA, 1 para COROA
        Escolha escolhaResultado = resultado == 0 ? Escolha.CARA : Escolha.COROA;

        address[] memory vencedores;
        uint256 totalVencedores = 0;
        uint256 premioTotal = aposta.valorAposta * aposta.jogadores.length;

        // Verificar vencedores
        for (uint256 i = 0; i < aposta.jogadores.length; i++) {
            if (aposta.escolhas[i] == escolhaResultado) {
                vencedores[totalVencedores] = aposta.jogadores[i];
                totalVencedores++;
            }
        }

        // Se houver vencedores, dividir o prêmio entre eles
        if (totalVencedores > 0) {
            uint256 premioPorVencedor = premioTotal / totalVencedores;
            for (uint256 i = 0; i < totalVencedores; i++) {
                address payable vencedor = payable(vencedores[i]);
                vencedor.transfer(premioPorVencedor);
            }
        } else {
            // Se não houver vencedores, devolver o prêmio para todos
            for (uint256 i = 0; i < aposta.jogadores.length; i++) {
                address payable jogador = payable(aposta.jogadores[i]);
                jogador.transfer(aposta.valorAposta);
            }
        }

        emit JogoFinalizado(apostaId, premioTotal, vencedores);

        // Remover a aposta e resetar estados
        for (uint256 i = 0; i < aposta.jogadores.length; i++) {
            delete apostasPorJogador[aposta.jogadores[i]];
        }
        delete apostas[apostaId];
    }

    // Função para encerrar a aposta
    // Função para encerrar a aposta
    function encerrarAposta(bytes32 apostaId) public apostaExistente(apostaId) {
        Aposta storage aposta = apostas[apostaId];

        require(msg.sender == aposta.jogador1, "Somente o jogador que criou a aposta pode encerra-la!");
        require(aposta.jogadores.length >= 1, "E necessario ter pelo menos um jogador para encerrar a aposta");

        aposta.statusJogo = StatusJogo.FINALIZADO;
        resolverJogo(apostaId);

        emit ApostaEncerrada(apostaId);
    }


    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, msg.sender)));
    }
}
