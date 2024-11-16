import os
import sys 
import random
import flask 
from ledger import Ledger
from transacao import Transacao
from comunicacao import enviar_transacao


class Cliente:
    
    def __init__(self, client_id):
        self.client_id = client_id
        self.ledger = Ledger()
    
    def realizar_aposta(self, valor, tipo_aposta):
        transacao = Transacao(self.client_id, valor, tipo_aposta)
        self.ledger.adicionar_transacao(transacao)
        enviar_transacao(transacao)

    def ver_apostas(self):
        return self.ledger.exibir_apostas()

def limpar_tela():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')


def cara_ou_coroa_game():

    options = ['cara','coroa']
    result = random.randint(0, 1)

    return options[result]

def main():
    
    while True: 

        print("="*23)
        print("|  BET - distribuída  |               saldo atual: liso" )
        print("="*23)

        print("\n1. Participar de jogos")
        print("2. Cadastrar eventos")
        print("3. Verificar resultados")
        print("4. Consultar saldo")
        print("5. Adicionar créditos")
        print("6. Ver histórico")
        print("7. Sair\n")
        
        opcao = input("Escolha uma das opções: ")

        if opcao == "1": 
            ''
        elif opcao == "2": 
            ''
        elif opcao == "3":
            ''
        elif opcao == "7":
            limpar_tela()
            sys.exit()
        

        else:
            limpar_tela()
            print("\nOpção inválida! Tente novamente.\n")
            


if __name__ == "__main__":

    main()


    