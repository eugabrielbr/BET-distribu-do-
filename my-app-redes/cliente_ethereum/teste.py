from web3 import Web3


#PRIVATE_KEY = b'\xea\xc4d\xd7Z\xe3%&\xa8\x97\xd4b\xb1(+\xb9\xac`\x1d\x1f\x1e\xad\xb1\xabT+\x0c\x02\xce\x1c\xb8\xad'
ENDERECO = '0x8072b8d4598b213901BfEeF097aB64918436C2A2'


# Gerar nova conta Ethereum

infura_url = 'https://sepolia.infura.io/v3/6211b6cc406f48de8c3cce2a6a27f264'

w3 = Web3(Web3.HTTPProvider(infura_url))

# Verificar a conexão
if w3.is_connected():
    print("Conectado à rede Sepolia!")
else:
    print("Falha ao conectar à rede Sepolia.")


balance = w3.eth.get_balance(ENDERECO)
eth_balance = w3.from_wei(balance, 'ether')  # Converter de wei para ether

print(f"Saldo de {ENDERECO}: {eth_balance} ETH")



