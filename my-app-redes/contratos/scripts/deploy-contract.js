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
  
    // Listener para o evento ApostaAceita
    contrato.on("ApostaAceita", (...args) => {
      console.log("Evento ApostaAceita disparado!");
      //console.log("Argumentos:", args); // Mostra todos os argumentos
      // Para um formato mais legível
      const [apostaId, jogador2] = args;
      console.log(`Aposta Aceita! ID da aposta: ${apostaId}, Jogador 2: ${jogador2}`);
    });
  
    // Listener para o evento JogoFinalizado
    contrato.on("JogoFinalizado", (...args) => {
      console.log("Evento JogoFinalizado disparado!");
      //console.log("Argumentos:", args); // Mostra todos os argumentos
      // Para um formato mais legível
      const [apostaId, vencedor, valorPremio] = args;
      console.log(`Jogo Finalizado! ID da aposta: ${apostaId}, Vencedor: ${vencedor}, Valor do prêmio: ${valorPremio}`);
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

