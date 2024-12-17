import time
import json
from web3 import Web3
import threading
import signal
from datetime import datetime, timedelta
import pytz

# Conectando-se ao nó local (ajuste a URL, se necessário)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
sair = threading.Event()
dic_historico_aposta_criada = {}
dic_historico_aposta_finalizada = {}
dic_historico_aposta_encerrada = {}
dic_historico_aposta_participantes = {}
list_finalizados = [] 
type = None



def signal_handler(sig, frame):
    pass 

signal.signal(signal.SIGINT, signal_handler)


# ABI do contrato (substitua pela ABI do seu contrato)
contract_abi = [
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
  ]  # ABI do contrato em formato JSON
contract_address = "0x0165878A594ca255338adfa4d48449f69242Eb8F"  # Endereço do contrato

# Criando uma instância do contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Função para tratar o evento ApostaCriada
def handle_aposta_criada(event):
    aposta_id = event.args.apostaId
    aposta_id = '0x' + aposta_id.hex()
    jogador1 = event.args.jogador1
    valor_aposta =  event.args.valorAposta
    escolha = event.args.escolha
    data = event.args.dataLimite

    # Converter para o fuso horário de Brasília usando pytz
    brasilia_tz = pytz.timezone("America/Sao_Paulo")
    data_hora_utc = datetime.utcfromtimestamp(data)
    data_hora_brasilia = data_hora_utc.astimezone(brasilia_tz)
    data_hora_utc = pytz.utc.localize(data_hora_utc)
    data_hora_brasilia = data_hora_utc - timedelta(hours=3)

# Formatando a data para exibição
    data_formatada = data_hora_brasilia.strftime('%d/%m/%Y %H:%M')
    
    dic_historico_aposta_criada.setdefault(aposta_id, "")
    
    if dic_historico_aposta_criada[aposta_id] == "":
      dic_historico_aposta_criada[aposta_id] = f"Aposta Criada! ID da aposta: {aposta_id}, Jogador 1: {jogador1}, Valor da aposta: {valor_aposta}, Escolha: {escolha}, Data limite: {data_formatada}"
      
    if (aposta_id not in list_finalizados) and (type == 0 or type == 1 or type == -1):
      print(f"Aposta Criada! ID da aposta: {aposta_id}, Jogador 1: {jogador1}, Valor da aposta: {valor_aposta}, Escolha: {escolha}, Data limite: {data_formatada}")

# Função para tratar o evento ApostaParticipante
def handle_aposta_participante(event):
    aposta_id = event.args.apostaId
    aposta_id = '0x' + aposta_id.hex()
    jogador = event.args.jogador
    escolha = event.args.escolha
    
    dic_historico_aposta_participantes.setdefault(aposta_id, [])
    verificacao = False
    
    if dic_historico_aposta_participantes[aposta_id] != []:
      
      for i in dic_historico_aposta_participantes[aposta_id][0]:
        
        if i == jogador: 
          verificacao = True
          break
    
    if not verificacao:
      dic_historico_aposta_participantes[aposta_id].append((jogador,f"Aposta Participante! ID da aposta: {aposta_id}, Jogador: {jogador}, Escolha: {escolha}"))

    
    if type == 0 or type == 2:
      
      print(f"Aposta Participante! ID da aposta: {aposta_id}, Jogador: {jogador}, Escolha: {escolha}")

# Função para tratar o evento JogoFinalizado
def handle_jogo_finalizado(event):
    aposta_id = event.args.apostaId
    aposta_id = '0x' + aposta_id.hex()
    valor_premio = event.args.valorPremio
    vencedores = event.args.vencedores
    resultado = event.args.resultado
    
    if aposta_id not in list_finalizados:

      list_finalizados.append(aposta_id)
    
    dic_historico_aposta_finalizada.setdefault(aposta_id, "")
    
    if dic_historico_aposta_finalizada[aposta_id] == "":
      dic_historico_aposta_finalizada[aposta_id] = f"Jogo Finalizado! ID da aposta: {aposta_id}, Valor do prêmio: {valor_premio}, Vencedores: {vencedores}, Resultado: {resultado}"
    
    
    if type == 0 or type == 3:
      
      print(f"Jogo Finalizado! ID da aposta: {aposta_id}, Valor do prêmio: {valor_premio}, Vencedores: {vencedores}, Resultado: {resultado}")

# Função para tratar o evento ApostaEncerrada
def handle_aposta_encerrada(event):
    aposta_id = event.args.apostaId
    aposta_id = '0x' + aposta_id.hex()
    dic_historico_aposta_encerrada.setdefault(aposta_id, "")
    
    if dic_historico_aposta_encerrada[aposta_id] == "":
      dic_historico_aposta_encerrada[aposta_id] =f"O administrador da aposta de ID {aposta_id} encerrou o evento"
      

    
    if aposta_id not in list_finalizados:

      list_finalizados.append(aposta_id)
    
    if type == 0 or type == 4:
    
      print(f"Aposta Encerrada! ID da aposta: {aposta_id}")
    
def getHistorico(apostaID):
    
    lista = [] 
    
    if apostaID in dic_historico_aposta_criada:
      lista.append(dic_historico_aposta_criada[apostaID])
      
    if apostaID in dic_historico_aposta_participantes:
      lista.append(dic_historico_aposta_participantes[apostaID])
    
    if apostaID in dic_historico_aposta_encerrada:
      lista.append(dic_historico_aposta_encerrada[apostaID])
      
    if apostaID in dic_historico_aposta_finalizada:
      lista.append(dic_historico_aposta_finalizada[apostaID])
      
      
    return lista
      
    
    

# Função para ouvir eventos
def listen_to_events(event_type=None):
   

    # Criar filtros para os eventos
    event_filter_aposta_criada = contract.events.ApostaCriada.create_filter(from_block=0)
    event_filter_aposta_participante = contract.events.ApostaParticipante.create_filter(from_block=0)
    event_filter_jogo_finalizado = contract.events.JogoFinalizado.create_filter(from_block=0)
    event_filter_aposta_encerrada = contract.events.ApostaEncerrada.create_filter(from_block=0)

    while not sair.is_set():
        
        
        if event_type in ['JogoFinalizado',None]:
            for event in event_filter_jogo_finalizado.get_new_entries():
                handle_jogo_finalizado(event)
        
        # Verifica os novos eventos e chama a função correspondente
        if event_type in ['ApostaCriada',None]:
            
            for event in event_filter_aposta_criada.get_new_entries():
                handle_aposta_criada(event)
        
        if event_type in ['ApostaParticipante',None]:
            for event in event_filter_aposta_participante.get_new_entries():
                handle_aposta_participante(event)


        if event_type in ['ApostaEncerrada',None]:
            for event in event_filter_aposta_encerrada.get_new_entries():
                handle_aposta_encerrada(event)

        # Aguardar para não sobrecarregar o loop
        time.sleep(5)

# Função para escutar um tipo específico de evento
def listen_for_event(event_name):
    listen_to_events(event_type=event_name)


def sair_func():
    global sair
    
    input("Pressione enter para volta para o menu \n\n\n")
    sair.set()

    
# Manter o script rodando indefinidamente

def ouvir_eventos(type_t):
    global sair
    global type 
    type = type_t
   
   
    
    event_sair = threading.Thread(target=sair_func, args=())
    event_sair.daemon = True  # Para que a thread termine quando o programa principal terminar
    event_sair.start()
    # Criar e iniciar a thread para escutar eventos
    
    
    try:
        
          while not sair.is_set():

              # Aqui você pode chamar as funções para escutar eventos específicos:
              # Exemplo: para escutar apenas o evento "ApostaCriada":
              # listen_for_event("ApostaCriada")

              # Ou para escutar todos os eventos:
              if type_t == 0 or type_t == -1 or type_t == -2:
                listen_for_event(None)# Altere para outro evento conforme necessário
              elif type_t == 1:
                listen_for_event('ApostaCriada')
              elif type_t == 2:
                listen_for_event('ApostaParticipante')
              elif type_t == 3:
                listen_for_event('JogoFinalizado')
              elif type_t == 4:
                listen_for_event('ApostaEncerrada')
              
              
              
                
              time.sleep(3)
             
          
          
          
          event_sair.join()
          sair.clear()
          
          
          
          
            
            
            
          
              
    except KeyboardInterrupt:
        print("Encerrando...")
