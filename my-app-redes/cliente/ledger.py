import hashlib
import json

class Ledger:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
        self.salvar_ledger()

    def salvar_ledger(self):
        with open("ledger.json", "w") as file:
            json.dump([t.to_dict() for t in self.transacoes], file, indent=4)

    def exibir_apostas(self):
        return [str(t) for t in self.transacoes]

    def carregar_ledger(self):
        try:
            with open("ledger.json", "r") as file:
                data = json.load(file)
                self.transacoes = [Transacao(**t) for t in data]
        except FileNotFoundError:
            self.transacoes = []

class Transacao:
    def __init__(self, client_id, valor, tipo_aposta):
        self.client_id = client_id
        self.valor = valor
        self.tipo_aposta = tipo_aposta
        self.hash = self.gerar_hash()
    
    def gerar_hash(self):
        return hashlib.sha256(f"{self.client_id}{self.valor}{self.tipo_aposta}".encode()).hexdigest()
    
    def to_dict(self):
        return {"client_id": self.client_id, "valor": self.valor, "tipo_aposta": self.tipo_aposta, "hash": self.hash}

    def __str__(self):
        return f"Aposta de {self.client_id}: {self.valor} em {self.tipo_aposta}, Hash: {self.hash}"
