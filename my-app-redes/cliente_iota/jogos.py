import random

def cara_ou_coroa() -> str:

    options = ['cara','coroa']
    result = random.randint(0, 1)

    return options[result]
    
def numero_da_sorte(apostas: list[tuple[int, str]]) -> str:
    if not apostas:
        return "Nenhuma aposta foi fornecida."
    
    numero_sorteado = random.randint(1, 50)
    
    # Determina o vencedor com base na menor diferença
    vencedor = min(apostas, key=lambda aposta: abs(aposta[0] - numero_sorteado))
    numero_vencedor, id_vencedor = vencedor
    diferenca = abs(numero_vencedor - numero_sorteado)
    
    return (f"O número sorteado foi {numero_sorteado}. "
            f"Vencedor: ID {id_vencedor}, número escolhido {numero_vencedor}, "
            f"com diferença de {diferenca}.")



class Aposta:
    
    def __init__(self, jogador, valor, evento):
        self.jogador = jogador
        self.valor = valor
        self.evento = evento
        self.estado = 'pendente'

    def registrar_aposta(self):
        # Registra a aposta no contrato inteligente
        print(f"Aposta de {self.valor} tokens registrada para o evento {self.evento}")
        self.estado = 'registrada'

    def verificar_resultado(self, resultado):
        # Verifica o resultado de um evento, obtido de um oráculo
        if self.evento == resultado['evento'] and resultado['vencedor'] == self.jogador:
            self.estado = 'ganhou'
            print(f"{self.jogador} venceu! Prêmio transferido.")
        else:
            self.estado = 'perdeu'
            print(f"{self.jogador} perdeu a aposta.")

    def distribuir_premio(self, vencedor):
        if self.estado == 'ganhou':
            # Distribui o prêmio (se for o vencedor)
            print(f"Distribuindo prêmio de {self.valor} tokens para {vencedor}")
            return True
        else:
            print("Não há prêmio a ser distribuído.")
            return False

