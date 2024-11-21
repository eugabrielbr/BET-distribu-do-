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
