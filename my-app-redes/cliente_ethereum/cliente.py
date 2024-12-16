import os
import sys 
from eth_utils import is_address, is_checksum_address
from web3 import Web3
from dotenv import load_dotenv
from time import sleep
import comunicacao
from web3.middleware import ExtraDataToPOAMiddleware
from eventos import ouvir_eventos,sair_func,getHistorico
import threading
import queue
from datetime import datetime
import re

load_dotenv()
#infura_url = f'https://sepolia.infura.io/v3/{os.getenv("KEY_API")}'
infura_url = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
endereco_contrato = '0x0165878A594ca255338adfa4d48449f69242Eb8F' 
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

            public_key = input("Digite seu endereço público: ")
                    
            validacao = w3.is_address(public_key)

            if validacao:

                print("\nPara realizar transações, é necessário informar sua chave privada. Obs: não compartilhe esta chave com ninguem.\n")
                private_key = input("Digite sua chave privada: ")
                return (public_key,private_key)
            else:
                return False
            
        elif option == "2": 
            
            account = w3.eth.account.create()
            

            limpar_tela()
            print(f'Sua carteira tem a seguinte chave privada: \n\n"{account._private_key}" e o seguinte endereço "{account._public_key}"')
            print("\nGuarde a chave. Ela é importante para efetuar operações no sistema")
            input("\nPressione qualquer tecla para continuar")
            return (account.public_key,account._private_key)
            
    
    except ValueError as e:

        print(e)
        return False

def menu(ethbalance,brlbalance):

    print("="*23)
    print(f"|  BET - distribuída  |               saldo atual: {ethbalance:.5f} ETH ({brlbalance:.2f} R$)" )
    print("="*23)

    print("\n1. Cadastrar eventos")
    print("2. Apostar em um evento")
    print("3. Encerrar evento")
    print("4. Ver eventos disponíveis")
    print("5. Ver histórico de uma aposta")
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

        cliente_private_key = cliente[1]
        cliente = cliente[0]
        
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
            
            limpar_tela()
            print("No momento, apenas o jogo CARA ou COROA esta disponível!\n")
            valorAposta = float(input("Insira o valor da aposta (ETH): "))
            caraOuCoroa = int(input("Escolha CARA (1) ou COROA(2): "))
            dia = int(input("Insira o dia: "))
            mes = int(input("Insira o mes: "))
            ano = int(input("Insira o ano: "))
            hora = int(input("Insira a hora: "))
            minutos = int(input("Insira os minutos: "))
            
            data_limite = datetime(ano,mes,dia,hora,minutos,0)
            timestamp_limite = int(data_limite.timestamp())
            
            sla = comunicacao.criarAposta(endereco_contrato,cliente_private_key,cliente,caraOuCoroa,valorAposta,timestamp_limite)
        
        elif opcao == "2":
            
            limpar_tela()
            idAposta = input("Insira o ID do evento que deseja participar: ")
            caraOuCoroa = int(input("Escolha CARA (1) ou COROA(2): "))
            print("Para confirmar, digite o valor exigido na aposta.\nObs.: valores diferentes resultaram no cancelamento da aposta")
            valorAposta = input("\n")
            sla3 = comunicacao.aceitarAposta(endereco_contrato,cliente_private_key,cliente,caraOuCoroa,idAposta,valorAposta)

        elif opcao == "3":
            limpar_tela()
            idAposta = input("Insira o ID do evento que deseja encerrar: ")
            sla4 = comunicacao.encerrarAposta(endereco_contrato,cliente_private_key,cliente,idAposta) #fazer esse aq
            
        elif opcao == "4":
            limpar_tela()
            # essa opcao e eficiente apenas em rede local, na rede publica vale mais a pena criar listas de registro no contrato
            
            event_ouvir_thread = threading.Thread(target=ouvir_eventos, args=(-1,))
            event_ouvir_thread.daemon = True  # Para que a thread termine quando o programa principal terminar
            event_ouvir_thread.start()
            event_ouvir_thread.join()
            
            # parametros args
            # 0 = todos os eventos, mas nao printa nada
            # 1 = ApostaCriada
            # 2 = ApostaParticipante
            # 3 = JogoFinalizado
            # 4 = ApostaEncerrada
            # -1 = todos os eventos mas so printa eventos disponiveis
            # -2 = todos os eventos mas nao printa nada
            
            limpar_tela()
        
        elif opcao == "5":
            limpar_tela()
            
            idAposta = input("Insira o ID do evento que deseja ver o historico: ")
            resultado_queue = queue.Queue()
            event_ouvir_thread2 = threading.Thread(target=ouvir_eventos, args=(-2,))
            event_ouvir_thread2.daemon = True  # Para que a thread termine quando o programa principal terminar
            event_ouvir_thread2.start()
            sleep(2)
            lista_anti_repeticao = []
            
            listaHistorico = getHistorico(idAposta);
            
            if listaHistorico != []:
                
                for i in listaHistorico:
                    
                    if isinstance(i, list):
                        for j in i:
                            if j[0] not in lista_anti_repeticao:  
                                print(j[1],"\n")
                            lista_anti_repeticao.append(j[0])
                    else:
                        print(i,"\n")
                        
            else: 
                print("Não há nenhum histórico registrado para este ID")
            
                
            
                
            event_ouvir_thread2.join()

            
    
        elif opcao == "6":
            limpar_tela()
            
            sys.exit()
        
        
        else:
            limpar_tela()
            print("\nOpção inválida! Tente novamente.\n")
            


if __name__ == "__main__":

    main()
