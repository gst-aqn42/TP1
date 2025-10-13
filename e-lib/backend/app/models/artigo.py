from datetime import datetime
from app.services.database import mongo
from bson import ObjectId

class Artigo:
    def __init__(self, titulo, autores, edicao_id, resumo=None, keywords=None, pdf_path=None):
        self.titulo = titulo
        self.autores = autores  # Lista de dicionários com nome e email
        self.edicao_id = edicao_id
        self.resumo = resumo
        self.keywords = keywords or []
        self.pdf_path = pdf_path
        self.data_publicacao = datetime.utcnow()
        self.data_criacao = datetime.utcnow()
    
    def save(self):
        """Salva o artigo no MongoDB"""
        try:
            artigos_collection = mongo.get_collection('artigos')
            artigo_data = {
                'titulo': self.titulo,
                'autores': self.autores,
                'edicao_id': ObjectId(self.edicao_id),
                'resumo': self.resumo,
                'keywords': self.keywords,
                'pdf_path': self.pdf_path,
                'data_publicacao': self.data_publicacao,
                'data_criacao': self.data_criacao
            }
            print(f"Tentando salvar artigo: {self.titulo}")
            result = artigos_collection.insert_one(artigo_data)
            print(f"Artigo salvo no MongoDB com ID: {result.inserted_id}")
            return result
        except Exception as e:
            print(f"Erro ao salvar artigo no MongoDB: {e}")
            return None
    
    @staticmethod
    def find_by_edicao(edicao_id):
        """Encontra todos os artigos de uma edição"""
        try:
            artigos_collection = mongo.get_collection('artigos')
            artigos = list(artigos_collection.find({'edicao_id': ObjectId(edicao_id)}))
            # Converter ObjectId para string
            for artigo in artigos:
                artigo['_id'] = str(artigo['_id'])
                artigo['edicao_id'] = str(artigo['edicao_id'])
            return artigos
        except Exception as e:
            print(f"Erro ao buscar artigos por edição: {e}")
            return []
    
    @staticmethod
    def find_by_id(artigo_id):
        """Encontra artigo por ID"""
        try:
            artigos_collection = mongo.get_collection('artigos')
            artigo = artigos_collection.find_one({'_id': ObjectId(artigo_id)})
            if artigo:
                artigo['_id'] = str(artigo['_id'])
                artigo['edicao_id'] = str(artigo['edicao_id'])
            return artigo
        except Exception as e:
            print(f"Erro ao buscar artigo por ID: {e}")
            return None
    
    @staticmethod
    def update(artigo_id, update_data):
        """Atualiza um artigo"""
        try:
            artigos_collection = mongo.get_collection('artigos')
            return artigos_collection.update_one(
                {'_id': ObjectId(artigo_id)},
                {'$set': update_data}
            )
        except Exception as e:
            print(f"Erro ao atualizar artigo: {e}")
            return None
    
    @staticmethod
    def delete(artigo_id):
        """Deleta um artigo"""
        try:
            artigos_collection = mongo.get_collection('artigos')
            return artigos_collection.delete_one({'_id': ObjectId(artigo_id)})
        except Exception as e:
            print(f"Erro ao deletar artigo: {e}")
            return None
    
    def to_dict(self):
        return {
            'titulo': self.titulo,
            'autores': self.autores,
            'edicao_id': self.edicao_id,
            'resumo': self.resumo,
            'keywords': self.keywords,
            'pdf_path': self.pdf_path,
            'data_publicacao': self.data_publicacao.isoformat(),
            'data_criacao': self.data_criacao.isoformat()
        }
