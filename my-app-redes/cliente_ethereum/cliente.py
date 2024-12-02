import os
import sys 
from eth_utils import is_address, is_checksum_address
from web3 import Web3
from dotenv import load_dotenv

import comunicacao

load_dotenv()
infura_url = f'https://sepolia.infura.io/v3/{os.getenv("KEY_API")}'
w3 = Web3(Web3.HTTPProvider(infura_url))

def limpar_tela():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_evento():
    
    print("EVENTOS DISPONÍVEIS")

    print("\n1. Cara ou coroa")
    print("2. Número da sorte\n")

    game = input("Insira o tipo de evento:")

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

        print("="*23)
        print(f"|  BET - distribuída  |               saldo atual: {eth_balance} ({convert_reais:.2f} R$)" )
        print("="*23)

        print("\n1. Apostar em um evento")
        print("2. Cadastrar eventos")
        print("3. Verificar resultados")
        print("4. Adicionar créditos")
        print("5. Ver histórico")
        print("6. Sair\n")
        
        opcao = input("Escolha uma das opções: ")

        if opcao == "1": 
            
            ''
        elif opcao == "2":
            ''


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
