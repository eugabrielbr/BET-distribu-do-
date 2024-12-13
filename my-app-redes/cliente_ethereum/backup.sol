// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CaraOuCoroa {

    enum Escolha { NENHUMA, CARA, COROA }
    enum StatusJogo { NAO_INICIADO, ESPERANDO_JOGADOR2, FINALIZADO }

    struct Aposta {
        address jogador1;
        address jogador2;
        uint256 valorAposta;
        Escolha escolhaJogador1;
        Escolha escolhaJogador2;
        StatusJogo statusJogo;
    }

    mapping(bytes32 => Aposta) public apostas;
    mapping(address => bytes32) public apostasPorJogador;

    // Eventos
    event ApostaCriada(bytes32 apostaId, address jogador1, uint256 valorAposta, Escolha escolha);
    event ApostaAceita(bytes32 apostaId, address jogador2);
    event JogoFinalizado(bytes32 apostaId, address vencedor, uint256 valorPremio);

    modifier semApostaAtiva(address jogador) {
        require(apostasPorJogador[jogador] == 0, "Jogador ja possui uma aposta ativa");
        _;
    }

    modifier apostaExistente(bytes32 apostaId) {
        require(apostas[apostaId].jogador1 != address(0), "Aposta nao encontrada");
        _;
    }

    modifier somenteJogador1(bytes32 apostaId) {
        require(msg.sender == apostas[apostaId].jogador1, "Apenas o jogador 1 pode chamar esta funcao");
        _;
    }

    modifier somenteJogador2(bytes32 apostaId) {
        require(msg.sender == apostas[apostaId].jogador2, "Apenas o jogador 2 pode chamar esta funcao");
        _;
    }

    modifier jogoEmAndamento(bytes32 apostaId) {
        require(apostas[apostaId].statusJogo == StatusJogo.ESPERANDO_JOGADOR2, "Jogo nao esta em andamento");
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

        apostas[apostaId] = Aposta({
            jogador1: msg.sender,
            jogador2: address(0),
            valorAposta: msg.value,
            escolhaJogador1: _escolha,
            escolhaJogador2: Escolha.NENHUMA,
            statusJogo: StatusJogo.ESPERANDO_JOGADOR2
        });

        apostasPorJogador[msg.sender] = apostaId;

        emit ApostaCriada(apostaId, msg.sender, msg.value, _escolha);
    }

    // Jogador 2 aceita a aposta
    function aceitarAposta(bytes32 apostaId, Escolha _escolha) public payable apostaExistente(apostaId) jogoEmAndamento(apostaId) semApostaAtiva(msg.sender) {
        Aposta storage aposta = apostas[apostaId];

        require(msg.sender != aposta.jogador1, "Jogador 1 nao pode aceitar a propria aposta");
        require(msg.value == aposta.valorAposta, "Jogador 2 deve apostar o mesmo valor de Jogador 1");
        require(_escolha != aposta.escolhaJogador1, "Jogador 1 ja escolheu esta opcao!");

        aposta.jogador2 = msg.sender;
        aposta.escolhaJogador2 = _escolha;
        aposta.statusJogo = StatusJogo.FINALIZADO;

        apostasPorJogador[msg.sender] = apostaId;

        emit ApostaAceita(apostaId, msg.sender);
        resolverJogo(apostaId);
    }

    // Resolver o jogo
    function resolverJogo(bytes32 apostaId) public payable apostaExistente(apostaId) jogoFinalizado(apostaId) {
        Aposta storage aposta = apostas[apostaId];

        uint256 resultado = random() % 2; // 0 para CARA, 1 para COROA

        address vencedor;
        if (resultado == 0) {
            if (aposta.escolhaJogador1 == Escolha.CARA) {
                vencedor = aposta.jogador1;
            } else {
                vencedor = aposta.jogador2;
            }
        } else {
            if (aposta.escolhaJogador1 == Escolha.COROA) {
                vencedor = aposta.jogador1;
            } else {
                vencedor = aposta.jogador2;
            }
        }

        address payable vencedor_transfer = payable(vencedor);

        // Transferir a aposta para o vencedor
        vencedor_transfer.transfer(aposta.valorAposta * 2);

        emit JogoFinalizado(apostaId, vencedor, aposta.valorAposta * 2);

        // Remover a aposta e resetar estados
        delete apostasPorJogador[aposta.jogador1];
        delete apostasPorJogador[aposta.jogador2];
        delete apostas[apostaId];
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, msg.sender)));
    }
}
