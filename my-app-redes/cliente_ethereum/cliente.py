import os
import sys 
from eth_utils import is_address, is_checksum_address
from web3 import Web3
from dotenv import load_dotenv
from time import sleep
import comunicacao
from web3.middleware import ExtraDataToPOAMiddleware

load_dotenv()
#infura_url = f'https://sepolia.infura.io/v3/{os.getenv("KEY_API")}'
infura_url = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
endereco_contrato = '0x5fbdb2315678afecb367f032d93f642f64180aa3'

def limpar_tela():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_evento():
    
    print("EVENTOS DISPONÍVEIS")

    print("\n1. Cara ou coroa")
    print("2. Número da sorte\n")

    game = input("Insira o tipo de evento: ")

    if game == "1":
        
       ""



def validate_ethereum_address(address):
    # Verifica se o endereço é válido
    if not is_address(address):
        return "Endereço inválido!"
    
    # Verifica o checksum (se for misto em maiúsculas/minúsculas)
    if address.startswith("0x") and not is_checksum_address(address):
        return "Endereço válido, mas sem checksum (ou com checksum incorreto)!"
    
    return "Endereço válido!"

def login():

    print("1. Login")
    print("2. Registrar-se\n")
    option = input()
    
    try:

        if option == "1":

            public_key = input("Digite seu endereço: ")
        
            validacao = w3.is_address(public_key)

            if validacao:
                return public_key
            else:
                return False
            
        elif option == "2": 
            
            account = w3.eth.account.create()
            

            limpar_tela()
            print(f'Sua carteira tem a seguinte chave privada: \n\n"{account._private_key}" e o seguinte endereço "{account._public_key}"')
            print("\nGuarde a chave. Ela é importante para efetuar operações no sistema")
            input("\nPressione qualquer tecla para continuar")
            return account.public_key
            
    
    except ValueError as e:

        print(e)
        return False

def menu(ethbalance,brlbalance):

    print("="*23)
    print(f"|  BET - distribuída  |               saldo atual: {ethbalance:.5f} ETH ({brlbalance:.2f} R$)" )
    print("="*23)

    print("\n1. Apostar em um evento")
    print("2. Cadastrar eventos")
    print("3. Verificar resultados")
    print("4. Adicionar créditos")
    print("5. Ver histórico")
    print("6. Sair\n")
    
    opcao = input("Escolha uma das opções: ")

    return opcao

def main():
    '''
    O ledge so armazena transacoes, logo o cliente nao é registrado diretamente; todos os seus dados sao coletados a partir das
    transacoes

    tem que haver uma forma do cliente inserir uma senha, mas ela nao pode ser guardada no ledge, entao, onde guardar?
    '''

    cliente = login()
    
    if cliente:
        
        balance = w3.eth.get_balance(cliente)
        eth_balance = w3.from_wei(balance, 'ether')

    else:
        print("Cliente inválido. Tente novamente!")
        sys.exit()

    convert_reais = eth_balance * comunicacao.get_eth_to_brl()
    
    limpar_tela()

    while True: 

        opcao = menu(eth_balance,convert_reais)
        
        if opcao == "1": 
            
            sla = comunicacao.criarAposta(endereco_contrato,'0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80','0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',1)
        elif opcao == "2":
            
            limpar_tela()

            #sla2 = comunicacao.revert('0xfd7ad7ffd6e8a709ac861a0d9b03867231cee250','3aee31e8c3302e621f1f9e46306038771bf51694cff879b1e4de98d1e5f12d64','0xAeC09227112DA8Be78bcc80931256fb3401d95ff');
            sla3 = comunicacao.aceitarAposta(endereco_contrato,'0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d','0x70997970C51812dc3A010C7d01b50e0d17dc79C8',2,'0x28da634c4d3567fc4f257584dfb509a57dae900c5d2165badb00c85d4c7ba08a')

        elif opcao == "3":
            ''
        elif opcao == "6":
            limpar_tela()
            sys.exit()
        
        else:
            limpar_tela()
            print("\nOpção inválida! Tente novamente.\n")
            


if __name__ == "__main__":

    main()
