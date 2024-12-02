import os
import sys 
import random
import hashlib
import flask 
import jogos
import comunicacao
from iota_sdk import Client,MnemonicSecretManager,SecretManager,CoinType,AddressAndAmount,NodeIndexerAPI
from mnemonic import Mnemonic


client = Client(nodes=['https://api.testnet.shimmer.network'])
mnemo = Mnemonic("english")


def limpar_tela():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_evento():
    
    print("EVENTOS DISPONÍVEIS")

    print("\n1. Cara ou coroa")
    print("2. Número da sorte\n")

    game = input("Insira o tipo de evento:")


def login():

    print("1. Login")
    print("2. Registrar-se\n")
    option = input()
    
    try:

        if option == "1":

            private_key = input("Digite sua chave de acesso: ")
            frase = MnemonicSecretManager(private_key)
            frase_to_str = str(frase['mnemonic'])
       
            validacao = mnemo.check(frase_to_str)

            if validacao:
                return frase_to_str
            else:
                return False
            
        elif option == "2": 
            
            carteira_aleatoria = comunicacao.generate_private_key()
            carteira_aleatoria = str(carteira_aleatoria['mnemonic'])
            private_key_carteira_aleatoria = comunicacao.generate_public_keys(carteira_aleatoria,0,1)

            limpar_tela()
            print(f'Sua carteira tem a seguinte chave privada: \n\n"{carteira_aleatoria}"')
            print("\nGuarde a chave. Ela é importante para efetuar operações no sistema")
            input("\nPressione qualquer tecla para continuar")
            return carteira_aleatoria
            
    
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
        
        cliente_chave = comunicacao.generate_public_keys(cliente,0,1)
        
        if cliente_chave[0]:

            cliente_saldo = comunicacao.check_balance(cliente_chave[0])
        else:
            print("Erro ao acessar chave pública")
            sys.exit()

    else:
        print("Cliente inválido. Tente novamente!")
        sys.exit()


    convert_reais = comunicacao.shimmer_para_reais(cliente_saldo[0])
    
    limpar_tela()

    while True: 

        print("="*23)
        print(f"|  BET - distribuída  |               saldo atual: {cliente_saldo[0]} ({convert_reais:.2f} R$)" )
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
            limpar_tela() 
            
            data = {"status": "aberto",
                    "valor_min_aposta": "xxxx",
                    "data_criacao":"xxxx",
                    "data_validade":"xxxx",
                    "tipo_evento":"xxxx",
            }

            eventoid = comunicacao.gerar_evento_id(data)

            new_data = {"status": "aberto",
                    "valor_min_aposta": "xxxx",
                    "data_criacao":"xxxx",
                    "data_validade":"xxxx",
                    "tipo_evento":"xxxx",
                    "id_evento": eventoid
            }


            blockid = comunicacao.postar_evento_aposta(new_data)
          

            input()
            limpar_tela() 


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


    