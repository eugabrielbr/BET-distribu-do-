import hashlib

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
