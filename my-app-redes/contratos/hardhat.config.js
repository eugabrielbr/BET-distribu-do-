require("@nomiclabs/hardhat-ethers");
require("@nomiclabs/hardhat-etherscan");
require("dotenv").config();
require("@nomiclabs/hardhat-waffle");

module.exports = {
  solidity: "0.8.20",
  networks: {
    hardhat: {
      chainId: 1337, // Usando o Chain ID 1337, padrão do Hardhat Network
    },
    localhost: {
      url: "http://0.0.0.0:8545", // URL do nó local
      accounts: ['0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'] // Contas pré-carregadas para interagir com a rede
    },
  },
};
