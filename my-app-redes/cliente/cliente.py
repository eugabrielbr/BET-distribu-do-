import os
import sys 
import random
import hashlib
import flask 
import jogos
from ledger import Ledger,Transacao
from comunicacao import enviar_transacao


def limpar_tela():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_evento():
    
    print("EVENTOS DISPONÍVEIS")

    print("\n1. Cara ou coroa")
    print("2. Número da sorte\n")

    game = input("Insira o tipo de evento:")

def gerar_hash(cpf: str) -> str:
    # Criando um hash SHA-256 do CPF
    hash_object = hashlib.sha256(cpf.encode())
    return hash_object.hexdigest()

def calcular_saldo(hash):
    saldo = Ledger.retornar_saldo(hash)
    return saldo


def login():

    cpf = input("insira seu cpf para acessar a plataforma: ")
    hash = gerar_hash(cpf)
    senha = input("insira sua senha:")


    #fazer mais coisas?

    return (hash,senha)
    

def main():
    '''
    O ledge so armazena transacoes, logo o cliente nao é registrado diretamente; todos os seus dados sao coletados a partir das
    transacoes


    tem que haver uma forma do cliente inserir uma senha, mas ela nao pode ser guardada no ledge, entao, onde guardar?
    '''

    cliente_hash = login()
    
    limpar_tela()

    while True: 

        print("="*23)
        print("|  BET - distribuída  |               saldo atual: liso" )
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

            cadastrar_evento()
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


    