from iota_sdk import Client,MnemonicSecretManager,SecretManager,CoinType,AddressAndAmount,NodeIndexerAPI,hex_to_utf8, utf8_to_hex
from mnemonic import Mnemonic
import requests
from time import sleep
import json
import hashlib
import datetime

client = Client(nodes=['https://api.testnet.shimmer.network'])

def generate_private_key():

    mnemo = Mnemonic("english")
    frase = mnemo.generate(strength=128) #frase para gerar seeds (carteira e endereço de transferencia)
    secret_manager_frase = MnemonicSecretManager(frase)
    return secret_manager_frase

def generate_public_keys(phrase,start,end):

    secret_manager_object = SecretManager(MnemonicSecretManager(phrase))

    addresses = secret_manager_object.generate_ed25519_addresses(
    coin_type=CoinType.SHIMMER,
    account_index=0,
    start=start,
    end=end, #aqui pode-se gerar vários endereços de transação 
    internal=False,
    bech32_hrp='rms')

    return addresses

def generate_random_range_public_keys(phrase):

    secret_manager_object = SecretManager(MnemonicSecretManager(phrase))
    addresses = secret_manager_object.generate_ed25519_addresses()

    return addresses

def check_balance(key):

    query_parameters = NodeIndexerAPI.QueryParameters(
    key,
    has_expiration=False,
    has_timelock=False,
    has_storage_deposit_return=False
    )

    output_ids_response = client.basic_output_ids(query_parameters)
    outputs = client.get_outputs(output_ids_response.items)

    total_amount = 0
    total_amount = float(total_amount)
    native_tokens = []
    for output_with_metadata in outputs:
        output = output_with_metadata.output
        total_amount += int(output.amount)
        if output.nativeTokens:
            native_tokens.append(output.nativeTokens)

    return (total_amount,native_tokens)


def shimmer_para_reais(quantidade_smr):

  
    try:
        # URL da API de preços (CoinGecko neste caso)
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "shimmer",  # Nome do ativo na CoinGecko
            "vs_currencies": "brl"  # Converter para reais
        }
        
        # Fazendo a solicitação para obter o preço atual
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta uma exceção em caso de erro na requisição
        data = response.json()
        
        # Obtendo o preço do Shimmer em BRL
        preco_smr_brl = data["shimmer"]["brl"]
        preco_smr_brl = float(preco_smr_brl)
        quantidade_smr = float(quantidade_smr)
        
        # Calculando o valor em reais
        valor_em_reais = quantidade_smr * preco_smr_brl
        return valor_em_reais
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
    except KeyError:
        print("Erro ao obter os dados da API.")
        return None
    

def postar_evento_aposta(evento):
    # Estrutura do evento de aposta

    tag = "teste"
    tag_hex = utf8_to_hex(tag)
    evento = str(evento)
    evento_hex = utf8_to_hex(evento)
    blockIDandBlock = client.build_and_post_block(secret_manager=None,data=evento_hex,tag=tag_hex)
    blockid = blockIDandBlock[0]
    blockData = blockIDandBlock[1]

    # so para testar se foi postado

    # pegando bloco com seu ID
    '''
    block = client.get_block_data(blockid)
    block = cliente.get_block_tag()
    payload_out = block.payload
    payload_out_data = block.payload.data
    payload_out_data = str(hex_to_utf8(payload_out_data))
    json_string_corrected = payload_out_data.replace("'", '"')
    payload_out_data_json = json.loads(json_string_corrected)
    print(payload_out_data_json)
    '''

    return blockid
    

def participar_evento_aposta(carteira_participante, valor_apostado, aposta):
    '' 



def encerrar_evento(quantidade_participantes, lista_carteira_ganhadores, lista_carteira_perdedores, id_evento): #postar uma nova mensagem na rede informando que o evento fechou
    ''


def gerar_evento_id(infos):
    # Concatenar os dados que compõem o evento para formar uma string única
    time_stamp = datetime.datetime.now()
    dados_evento = f"{infos['status']}_{infos['valor_min_aposta']}_{infos['data_criacao']}_{infos['data_validade']}_{infos['tipo_evento']}_{time_stamp}"
    
    # Gerar o hash SHA-256
    evento_id = hashlib.sha256(dados_evento.encode('utf-8')).hexdigest()
    
    return evento_id

