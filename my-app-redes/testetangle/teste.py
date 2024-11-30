from iota_sdk import Client,MnemonicSecretManager,SecretManager,CoinType,AddressAndAmount,NodeIndexerAPI
from mnemonic import Mnemonic
import secrets
import os
import json

EXPLORER_URL = 'https://explorer.shimmer.network/testnet'
FRASE_M = 'build hat fantasy circle already renew elder night print prepare quit bulk'

mnemo = Mnemonic("english")
frase = mnemo.generate(strength=128) #frase para gerar seeds (carteira e endereço de transferencia)

# Create a Client instance
client = Client(nodes=['https://api.testnet.shimmer.network'])


# Get the node info
node_info = client.get_info()
print(f'{node_info}')

#gerando uma seed

# Gerar uma chave aleatória de 32 bytes
def generate_random_key():
    seed_bytes = secrets.token_bytes(81)  # 32 bytes (256 bits) de chave aleatória

    seed = seed_bytes.hex()[:81]
    return seed # Converter para formato hexadecimal (mais legível)

# Exemplo de uso
random_key = generate_random_key()
print(f"\nChave aleatória gerada: {random_key}")

#gerando endereços de transacao com MNEMOIC

secret_manager_frase = MnemonicSecretManager(FRASE_M)

secret_manager_object = SecretManager(MnemonicSecretManager(FRASE_M))

addresses = secret_manager_object.generate_ed25519_addresses() #endereços para transacao com range aleatorio

#aparentemente gera enderecos de acordo com dados do cliente e transacao
addresses = secret_manager_object.generate_ed25519_addresses(
    coin_type=CoinType.SHIMMER,
    account_index=0,
    start=0,
    end=1, #aqui pode-se gerar vários endereços de transação 
    internal=False,
    bech32_hrp='rms')

print(f"\nFrase gerada: {frase}") 
print(f"\n{addresses}")

#consultar saldo
#obs: para adicionar dinheiro na carteira deve-se solicitar a um shimmer faucet

ADDRESS = addresses[0]

query_parameters = NodeIndexerAPI.QueryParameters(
    ADDRESS,
    has_expiration=False,
    has_timelock=False,
    has_storage_deposit_return=False
)

output_ids_response = client.basic_output_ids(query_parameters)
#print(f'{output_ids_response.items}') 

# Get the outputs by their id
outputs = client.get_outputs(output_ids_response.items)
#print(f'{outputs}') #possivel historico do cliente?


# Calculate the total amount and native tokens
total_amount = 0
native_tokens = []
for output_with_metadata in outputs:
    output = output_with_metadata.output
    total_amount += int(output.amount)
    if output.nativeTokens:
        native_tokens.append(output.nativeTokens)

print(
    f'Outputs controlled by {ADDRESS} have {total_amount} glow and native tokens: {native_tokens}')


# efetuar uma trasação (falta ainda)

'''
address_and_amount = AddressAndAmount(
    1000000,
    addresses[0], #deve-se colocar o endereço da carteira de destino
                  #secretet manager teoricamente seria a carteira de origem
)


# Create and post a block with a transaction
#
block = client.build_and_post_block(secret_manager_frase,output=address_and_amount)
print(f'Block sent: {EXPLORER_URL}/block/{block[0]}')
'''











