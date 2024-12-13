import time
import json
from web3 import Web3
import threading

# Conectando-se ao nó local (ajuste a URL, se necessário)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Verifique se a conexão foi bem-sucedida
if w3.isConnected():
    print("Conectado à rede local.")
else:
    print("Falha na conexão.")
    exit()

# ABI do contrato (substitua pela ABI do seu contrato)
contract_abi = json.loads('[...]')  # ABI do contrato em formato JSON
contract_address = "0xSeuEnderecoDeContrato"  # Endereço do contrato

# Criando uma instância do contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Função para ouvir eventos
def listen_to_events():
    print("Escutando eventos...")

    # Criar filtros para os eventos
    event_filter_aposta_criada = contract.events.ApostaCriada.createFilter(fromBlock='latest')
    event_filter_aposta_aceita = contract.events.ApostaAceita.createFilter(fromBlock='latest')
    event_filter_jogo_finalizado = contract.events.JogoFinalizado.createFilter(fromBlock='latest')

    while True:
        # Verifica os novos eventos
        for event in event_filter_aposta_criada.get_new_entries():
            print("Evento ApostaCriada disparado!")
            aposta_id, jogador1, valor_aposta, escolha = event.args
            print(f"Aposta Criada! ID da aposta: {aposta_id}, Jogador 1: {jogador1}, Valor da aposta: {valor_aposta}, Escolha: {escolha}")
        
        for event in event_filter_aposta_aceita.get_new_entries():
            print("Evento ApostaAceita disparado!")
            aposta_id, jogador2 = event.args
            print(f"Aposta Aceita! ID da aposta: {aposta_id}, Jogador 2: {jogador2}")
        
        for event in event_filter_jogo_finalizado.get_new_entries():
            print("Evento JogoFinalizado disparado!")
            aposta_id, vencedor, valor_premio = event.args
            print(f"Jogo Finalizado! ID da aposta: {aposta_id}, Vencedor: {vencedor}, Valor do prêmio: {valor_premio}")
        
        # Aguardar para não sobrecarregar o loop
        time.sleep(10)

# Criar e iniciar a thread para escutar eventos
event_listener_thread = threading.Thread(target=listen_to_events)
event_listener_thread.daemon = True  # Para que a thread termine quando o programa principal terminar
event_listener_thread.start()

# Manter o script rodando indefinidamente
print("Ouvindo eventos... Pressione Ctrl+C para sair.")
try:
    while True:
        # Este loop mantém o programa ativo
        time.sleep(10)
except KeyboardInterrupt:
    print("Encerrando...")

