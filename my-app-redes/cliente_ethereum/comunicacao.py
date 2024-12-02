from iota_sdk import Client,MnemonicSecretManager,SecretManager,CoinType,AddressAndAmount,NodeIndexerAPI,hex_to_utf8, utf8_to_hex
from mnemonic import Mnemonic
import requests
from time import sleep
import json
import hashlib
import datetime
from web3 import Web3







def get_eth_to_brl():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=brl"
    response = requests.get(url)
    data = response.json()
    return data['ethereum']['brl']


def postar_evento_aposta(evento):
    ''
    

def participar_evento_aposta(carteira_participante, valor_apostado, aposta):
    '' 



def encerrar_evento(quantidade_participantes, lista_carteira_ganhadores, lista_carteira_perdedores, id_evento): #postar uma nova mensagem na rede informando que o evento fechou
    ''


def gerar_evento_id(infos):
    # Concatenar os dados que compõem o evento para formar uma string única
    time_stamp = datetime.datetime.now()
    dados_evento = f"{infos}"
    
    # Gerar o hash SHA-256
    evento_id = hashlib.sha256(dados_evento.encode('utf-8')).hexdigest()
    
    return evento_id

