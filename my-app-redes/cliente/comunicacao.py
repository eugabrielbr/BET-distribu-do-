import socket
import json

def enviar_transacao(transacao):
    # Enviar transação para outros nós
    dados = json.dumps(transacao.to_dict())
    
    # Envio simples via socket (pode ser aprimorado para múltiplos nós)
    for cliente in get_outros_clientes():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((cliente[0], cliente[1]))  # Exemplo de porta
            s.sendall(dados.encode())   
            resposta = s.recv(1024).decode()
            print(f"Resposta de {cliente}: {resposta}")

def get_outros_clientes():
    # Retornar lista de IPs de outros clientes na rede
    return [("192.168.0.2",5000), ("192.168.0.3",6000)]
