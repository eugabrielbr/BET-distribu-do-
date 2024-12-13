// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CaraOuCoroa {

    enum Escolha { NENHUMA, CARA, COROA }
    enum StatusJogo { NAO_INICIADO, ESPERANDO_JOGADOR2, FINALIZADO }

    address public jogador1;
    address public jogador2;
    uint256 public valorAposta;
    Escolha public escolhaJogador1;
    Escolha public escolhaJogador2;
    StatusJogo public statusJogo;

    // Eventos
    event ApostaCriada(address jogador1, uint256 valorAposta, Escolha escolha);
    event ApostaAceita(address jogador2);
    event JogoFinalizado(address vencedor, uint256 valorPremio);

    modifier somenteJogador1() {
        require(msg.sender == jogador1, "Apenas o jogador 1 pode chamar esta funcao");
        _;
    }

    modifier somenteJogador2() {
        require(msg.sender == jogador2, "Apenas o jogador 2 pode chamar esta funcao");
        _;
    }

    modifier jogoEmAndamento() {
        require(statusJogo == StatusJogo.ESPERANDO_JOGADOR2, "Jogo nao esta em andamento");
        _;
    }

    modifier jogoNaoEmAndamento() {
        require(statusJogo == StatusJogo.NAO_INICIADO, "Ja existe um jogo em andamento");
        _;
    }

    modifier jogoFinalizado() {
        require(statusJogo == StatusJogo.FINALIZADO, "Jogo nao foi finalizado");
        _;
    }

    constructor() {
        jogador1 = address(0);
        jogador2 = address(0);
        valorAposta = 0;
        escolhaJogador1 = Escolha.NENHUMA;
        escolhaJogador2 = Escolha.NENHUMA;
        statusJogo = StatusJogo.NAO_INICIADO;
    }

    // Jogador 1 cria a aposta
    function criarAposta(Escolha _escolha) public payable jogoNaoEmAndamento {
        require(msg.sender != jogador1, "Jogador 1 ja esta criando uma aposta.");
        require(msg.value >= 0.001 ether, "Aposta minima e 0.001 ETH");

        jogador1 = msg.sender;
        valorAposta = msg.value;
        escolhaJogador1 = _escolha;
        statusJogo = StatusJogo.ESPERANDO_JOGADOR2;

        emit ApostaCriada(jogador1, valorAposta, escolhaJogador1);
    }

    // Jogador 2 aceita a aposta
    function aceitarAposta(Escolha _escolha) public payable jogoEmAndamento {
        require(msg.sender != jogador1, "Jogador 1 nao pode aceitar a propria aposta");
        require(msg.value == valorAposta, "Jogador 2 deve apostar o mesmo valor de Jogador 1");
        require(escolhaJogador2 == Escolha.NENHUMA, "Jogador 2 ja fez a sua escolha");
        require(_escolha == escolhaJogador1, "Jogador 1 ja escolheu esta opcao!");

        jogador2 = msg.sender;
        escolhaJogador2 = _escolha;
        statusJogo = StatusJogo.FINALIZADO;

        emit ApostaAceita(jogador2);
        resolverJogo();
    }

    // Resolver o jogo: simula cara ou coroa e determina o vencedor
    function resolverJogo() public payable {
        uint256 resultado = random() % 2; // 0 para CARA, 1 para COROA

        address vencedor;
        if (resultado == 0) {
            if (escolhaJogador1 == Escolha.CARA) {
                vencedor = jogador1;
            } else {
                vencedor = jogador2;
            }
        } else {
            if (escolhaJogador1 == Escolha.COROA) {
                vencedor = jogador1;
            } else {
                vencedor = jogador2;
            }
        }

        address payable vencedor_transfer = payable(vencedor);

        // Transferir a aposta para o vencedor
        vencedor_transfer.transfer(valorAposta * 2);

        emit JogoFinalizado(vencedor, valorAposta * 2);

        // Resetar o estado para um novo jogo
        jogador1 = address(0);
        jogador2 = address(0);
        valorAposta = 0;
        escolhaJogador1 = Escolha.NENHUMA;
        escolhaJogador2 = Escolha.NENHUMA;
        statusJogo = StatusJogo.NAO_INICIADO;
    }

    function revertStates() public{

        jogador1 = address(0);
        jogador2 = address(0);
        valorAposta = 0;
        escolhaJogador1 = Escolha.NENHUMA;
        escolhaJogador2 = Escolha.NENHUMA;
        statusJogo = StatusJogo.NAO_INICIADO;

    }


    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, msg.sender)));
    }

}
