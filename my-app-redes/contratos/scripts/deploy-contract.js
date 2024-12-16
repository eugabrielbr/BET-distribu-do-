 async function main() {

  // Carregando o contrato a ser implantado
  const MeuContrato = await ethers.getContractFactory("CaraOuCoroa");

  // Fazendo o deploy do contrato
  const contrato = await MeuContrato.deploy({
    gasLimit: 3000000, // Ajuste o limite de gas conforme necessário
    gasPrice: ethers.utils.parseUnits("50", "gwei") // Ajuste o gasPrice conforme necessário
}); 

  console.log("Contrato implantado em:", contrato.address);


    // Listener para o evento ApostaCriada
    contrato.on("ApostaCriada", (...args) => {
      console.log("Evento ApostaCriada disparado!");
      //console.log("Argumentos:", args); // Mostra todos os argumentos
      // Para um formato mais legível
      const [apostaId, jogador1, valorAposta, escolha] = args;
      console.log(`Aposta Criada! ID da aposta: ${apostaId}, Jogador 1: ${jogador1}, Valor da aposta: ${valorAposta}, Escolha: ${escolha}`);
    });
  
    // Listener para o evento ApostaParticipante
    contrato.on("ApostaParticipante", (...args) => {
      console.log("Evento ApostaParticipante disparado!");
  
        // Para um formato mais legível
        const [apostaId, jogador, escolha] = args;
        console.log(`Aposta registrada! ID da aposta: ${apostaId}, Jogador: ${jogador}, Escolha: ${escolha}`);
      });
  
    // Listener para o evento JogoFinalizado
    contrato.on("JogoFinalizado", (...args) => {
      console.log("Evento JogoFinalizado disparado!");
      //console.log("Argumentos:", args); // Mostra todos os argumentos
      // Para um formato mais legível
      const [apostaId, valorPremio, vencedores,resultado] = args;
      console.log(`Jogo Finalizado! ID da aposta: ${apostaId}, Valor do prêmio:: ${valorPremio}, Vencedores: ${vencedores}, Resultado${resultado} (1 = CARA, 2 = COROA)`);
    });

    // Listener para o evento JogoFinalizado
    contrato.on("ApostaEncerrada", (...args) => {
      console.log("Evento ApostaEncerrada disparado!");
      //console.log("Argumentos:", args); // Mostra todos os argumentos
      // Para um formato mais legível
      const [apostaId] = args;
      console.log(`Aposta encerrada! ID da aposta: ${apostaId}`);
    });
  
  
    console.log("Ouvindo eventos...");
  
    // Manter o script rodando indefinidamente
    while (true) {
      // O loop vai ficar rodando até que você o pare manualmente
      await new Promise(resolve => setTimeout(resolve, 20000));  // A cada 10 segundos
    }
  }

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

