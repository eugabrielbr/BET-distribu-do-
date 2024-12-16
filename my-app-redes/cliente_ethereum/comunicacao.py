from iota_sdk import Client,MnemonicSecretManager,SecretManager,CoinType,AddressAndAmount,NodeIndexerAPI,hex_to_utf8, utf8_to_hex
from mnemonic import Mnemonic
import requests
from time import sleep
import json
import hashlib
import datetime
from web3 import Web3,AsyncWeb3
from dotenv import load_dotenv
import os 


abi_cara_ou_coroa = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "jogador1",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "valorAposta",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "enum CaraOuCoroa.Escolha",
          "name": "escolha",
          "type": "uint8"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "dataLimite",
          "type": "uint256"
        }
      ],
      "name": "ApostaCriada",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        }
      ],
      "name": "ApostaEncerrada",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "jogador",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "enum CaraOuCoroa.Escolha",
          "name": "escolha",
          "type": "uint8"
        }
      ],
      "name": "ApostaParticipante",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "valorPremio",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "address[]",
          "name": "vencedores",
          "type": "address[]"
        },
        {
          "indexed": False,
          "internalType": "enum CaraOuCoroa.Escolha",
          "name": "resultado",
          "type": "uint8"
        }
      ],
      "name": "JogoFinalizado",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "name": "apostas",
      "outputs": [
        {
          "internalType": "address",
          "name": "jogador1",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "valorAposta",
          "type": "uint256"
        },
        {
          "internalType": "enum CaraOuCoroa.StatusJogo",
          "name": "statusJogo",
          "type": "uint8"
        },
        {
          "internalType": "uint256",
          "name": "dataLimite",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "apostasPorJogador",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "enum CaraOuCoroa.Escolha",
          "name": "_escolha",
          "type": "uint8"
        },
        {
          "internalType": "uint256",
          "name": "_dataLimite",
          "type": "uint256"
        }
      ],
      "name": "criarAposta",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        }
      ],
      "name": "encerrarAposta",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        },
        {
          "internalType": "enum CaraOuCoroa.Escolha",
          "name": "_escolha",
          "type": "uint8"
        }
      ],
      "name": "participarAposta",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "apostaId",
          "type": "bytes32"
        }
      ],
      "name": "resolverJogo",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]

load_dotenv()
#infura_url = f'https://sepolia.infura.io/v3/{os.getenv("KEY_API")}'
infura_url = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(infura_url))

def get_eth_to_brl():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=brl"
    response = requests.get(url)
    data = response.json()
    return data['ethereum']['brl']



def gerar_evento_id(infos):
    # Concatenar os dados que compõem o evento para formar uma string única
    time_stamp = datetime.datetime.now()
    dados_evento = f"{infos}"
    
    # Gerar o hash SHA-256
    evento_id = hashlib.sha256(dados_evento.encode('utf-8')).hexdigest()
    
    return evento_id

def test_contract(): #verificando se há contrato ativo

    infura_url = f'https://sepolia.infura.io/v3/{os.getenv("KEY_API")}'
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # Endereço do contrato
    contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

    # Verificar se o contrato existe (se o código foi implantado na rede)
    contract_code = web3.eth.get_code(contract_address)
    if contract_code != '0x':
        print("Contrato encontrado e implantado com sucesso!")
    else:
        print("Nenhum contrato encontrado nesse endereço.")


#funcao que usa contrato para transacao, serve apenas para servir de guia para outras
def testeTransfer(addressOrigem,addressDestino,contractAddress,privateKey):

    address = w3.to_checksum_address(contractAddress)
    addressOrigem = w3.to_checksum_address(addressOrigem)
    addressDestino = w3.to_checksum_address(addressDestino)

    abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True ,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True ,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_to",
                "type": "address"
            }
        ],
        "name": "transferEther",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]
    # Conta e chave privada (NUNCA exponha a chave em produção!)
    from_account = addressOrigem
    private_key = privateKey

    # Endereço para onde enviar Ether
    to_account = addressDestino

    # Criar uma instância do contrato
    contract = w3.eth.contract(address=address, abi=abi)

    # Valor a ser enviado (em Wei)
    value_in_wei = w3.to_wei(0.01, "ether")  # Exemplo: 0.01 Ether


    gas_estimate = contract.functions.transferEther(to_account).estimate_gas({
    "from": from_account,
    "value": value_in_wei
})


    # Construir a transação
    transaction = contract.functions.transferEther(to_account).build_transaction({
        "chainId": 11155111,  # ID da rede Sepolia
        "from": from_account,
        "value": value_in_wei,
        "gas": gas_estimate,
        "gasPrice": Web3.to_wei("10", "gwei"),
        "nonce": w3.eth.get_transaction_count(from_account),
    })

    # Assinar a transação
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

    # Enviar a transação
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transação enviada. Hash: {tx_hash.hex()}")

    # Esperar a confirmação
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transação confirmada. Detalhes:")
    print(receipt)


def criarAposta(contractAddress,privateKey,addressFrom,escolha,valor_aposta,data):

    address = w3.to_checksum_address(contractAddress)
    contract_abi = abi_cara_ou_coroa
    addressFrom = w3.to_checksum_address(addressFrom)

    # Crie o objeto do contrato
    contract = w3.eth.contract(address=address, abi=contract_abi)

    # Defina a chave privada do jogador
    private_key = privateKey
    from_account = addressFrom

    gas_estimate = contract.functions.criarAposta(escolha,data).estimate_gas({
    "from": from_account,
    "escolha": escolha,
    "dataaa": data,
    "value": w3.to_wei(valor_aposta, "ether")
})

    # Criar Aposta - Jogador 1
    transaction = contract.functions.criarAposta(escolha,data).build_transaction({
        "from": from_account,
        "value": w3.to_wei(valor_aposta, "ether"),
        "gas": gas_estimate,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(from_account),
    })

    # Assine e envie a transação
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Criando aposta. Transação Hash: {w3.to_hex(txn_hash)}")
   
    print(f"Esperando confimação da transação. Aguarde...")
    confirmarIndexacao(txn_hash)


def aceitarAposta(contractAddress,privateKey,addressFrom,escolha,idAposta,valor_aposta): 
    
  
    address = w3.to_checksum_address(contractAddress)
    contract_abi = abi_cara_ou_coroa

    addressFrom = w3.to_checksum_address(addressFrom)

    # Crie o objeto do contrato
    contract = w3.eth.contract(address=address, abi=contract_abi)

    # Defina a chave privada do jogador
    private_key = privateKey
    from_account = addressFrom

    gas_estimate = contract.functions.participarAposta(idAposta,escolha).estimate_gas({
    "from": from_account,
    "escolha": escolha,
    "idAposta": idAposta,
    "value": w3.to_wei(valor_aposta, "ether")
 })

    transaction = contract.functions.participarAposta(idAposta,escolha).build_transaction({
        "from": from_account,
        "value": w3.to_wei(valor_aposta, "ether"),
        "gas": gas_estimate,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(from_account),
    })

    # Assine e envie a transação
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Aceitando aposta. Transação Hash: {w3.to_hex(txn_hash)}")
    print(f"Esperando confimação da transação. Aguarde...")
    confirmarIndexacao(txn_hash)


def revert(contractAddress,privateKey,addressFrom):
    
    message = "Qualquer string que você quiser enviar"
    encoded_data = w3.to_hex(message.encode('utf-8'))

    address = w3.to_checksum_address(contractAddress)
    contract_abi = abi_cara_ou_coroa
    addressFrom = w3.to_checksum_address(addressFrom)

    contract = w3.eth.contract(address=address, abi=contract_abi)

    # Defina a chave privada do jogador
    private_key = privateKey
    from_account = addressFrom


    gas_estimate = contract.functions.revertStates().estimate_gas({
    "from": from_account,
})
    print(gas_estimate)

    transaction = contract.functions.revertStates().build_transaction({
        "from": from_account,
        "gas": gas_estimate,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(from_account),
    

    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Revertendo apostas! Transação Hash: {w3.to_hex(txn_hash)}")



def confirmarIndexacao(tx_hash):

    cont = 0
    tx_receipt = None
      
    while cont <= 20 :
    # Tenta obter o recibo da transação
      try:
          
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
          
      except:
        ""
      

      if tx_receipt is not None:
        print("\nTransação confirmada!")
        print(f"Bloco: {tx_receipt['blockNumber']}\n")
        return tx_receipt

      # Aguardar antes de tentar novamente
      cont += 1
      sleep(15)

    print("Houve algum erro, tente novamente mais tarde")


def encerrarAposta(contractAddress,privateKey,addressFrom,idAposta):
    

    address = w3.to_checksum_address(contractAddress)
    contract_abi = abi_cara_ou_coroa

    addressFrom = w3.to_checksum_address(addressFrom)

    # Crie o objeto do contrato
    contract = w3.eth.contract(address=address, abi=contract_abi)

    # Defina a chave privada do jogador
    private_key = privateKey
    from_account = addressFrom
     
    gas_estimate = contract.functions.encerrarAposta(idAposta).estimate_gas({
    "from": from_account,
    "idAposta": idAposta,
  })
    
    transaction = contract.functions.encerrarAposta(idAposta).build_transaction({
        "from": from_account,
        "gas": gas_estimate,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(from_account),
    })
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Encerrando aposta! Transação Hash: {w3.to_hex(txn_hash)}")
    confirmarIndexacao(txn_hash)
    