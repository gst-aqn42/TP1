from datetime import datetime
from app.services.database import mongo
from bson import ObjectId

class Evento:
    def __init__(self, nome, sigla, descricao=None):
        self.nome = nome
        self.sigla = sigla
        self.descricao = descricao
        self.data_criacao = datetime.utcnow()
    
    def save(self):
        """Salva o evento no MongoDB"""
        try:
            eventos_collection = mongo.get_collection('eventos')
            evento_data = {
                'nome': self.nome,
                'sigla': self.sigla,
                'descricao': self.descricao,
                'data_criacao': self.data_criacao
            }
            print(f" Tentando salvar evento: {evento_data}")
            result = eventos_collection.insert_one(evento_data)
            print(f"Evento salvo no MongoDB com ID: {result.inserted_id}")
            return result
        except Exception as e:
            print(f"Erro ao salvar evento no MongoDB: {e}")
            return None
    
    @staticmethod
    def find_all():
        """Encontra todos os eventos"""
        try:
            eventos_collection = mongo.get_collection('eventos')
            print("Buscando eventos no MongoDB...")
            eventos = list(eventos_collection.find())
            print(f"Encontrados {len(eventos)} eventos")
            # Converter ObjectId para string
            for evento in eventos:
                evento['_id'] = str(evento['_id'])
            return eventos
        except Exception as e:
            print(f"Erro ao buscar eventos: {e}")
            return []
    
    @staticmethod
    def find_by_id(evento_id):
        """Encontra evento por ID"""
        try:
            eventos_collection = mongo.get_collection('eventos')
            evento = eventos_collection.find_one({'_id': ObjectId(evento_id)})
            if evento:
                evento['_id'] = str(evento['_id'])
            return evento
        except Exception as e:
            print(f"Erro ao buscar evento por ID: {e}")
            return None
    
    @staticmethod
    def update(evento_id, update_data):
        """Atualiza um evento"""
        try:
            eventos_collection = mongo.get_collection('eventos')
            return eventos_collection.update_one(
                {'_id': ObjectId(evento_id)},
                {'$set': update_data}
            )
        except Exception as e:
            print(f"Erro ao atualizar evento: {e}")
            return None
    
    @staticmethod
    def delete(evento_id):
        """Deleta um evento"""
        try:
            eventos_collection = mongo.get_collection('eventos')
            return eventos_collection.delete_one({'_id': ObjectId(evento_id)})
        except Exception as e:
            print(f"Erro ao deletar evento: {e}")
            return None
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'sigla': self.sigla,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat()
        }

    @staticmethod
    def find_by_sigla(sigla):
        """Encontra evento por sigla"""
        try:
            eventos_collection = mongo.get_collection('eventos')
            evento = eventos_collection.find_one({'sigla': sigla})
            if evento:
                evento['_id'] = str(evento['_id'])
            return evento
        except Exception as e:
            print(f"Erro ao buscar evento por sigla: {e}")
            return None
