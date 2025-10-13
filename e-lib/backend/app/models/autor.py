from datetime import datetime

class Autor:
    def __init__(self, nome, email, instituicao=None, orcid=None):
        self.nome = nome
        self.email = email
        self.instituicao = instituicao
        self.orcid = orcid
        self.artigos = []  # Lista de IDs de artigos
        self.data_criacao = datetime.utcnow()
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'instituicao': self.instituicao,
            'orcid': self.orcid,
            'artigos': self.artigos,
            'data_criacao': self.data_criacao.isoformat()
        }
