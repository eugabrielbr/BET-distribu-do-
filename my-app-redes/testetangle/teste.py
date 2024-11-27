from iota_sdk import Client,MnemonicSecretManager
import secrets

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









