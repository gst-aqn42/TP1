from datetime import datetime
from app.services.database import mongo
from bson import ObjectId

class EdicaoEvento:
    def __init__(self, evento_id, ano, local, data_inicio=None, data_fim=None):
        self.evento_id = evento_id
        self.ano = ano
        self.local = local
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.artigos = []
        self.data_criacao = datetime.utcnow()
    
    def save(self):
        """Salva a edição no MongoDB"""
        edicoes_collection = mongo.get_collection('edicoes')
        edicao_data = {
            'evento_id': ObjectId(self.evento_id),
            'ano': self.ano,
            'local': self.local,
            'data_inicio': self.data_inicio,
            'data_fim': self.data_fim,
            'artigos': self.artigos,
            'data_criacao': self.data_criacao
        }
        return edicoes_collection.insert_one(edicao_data)
    
    @staticmethod
    def find_by_evento(evento_id):
        """Encontra todas as edições de um evento"""
        edicoes_collection = mongo.get_collection('edicoes')
        
        # Tentar buscar com ObjectId e com string (compatibilidade com dados antigos)
        try:
            evento_obj_id = ObjectId(evento_id)
            edicoes = list(edicoes_collection.find({
                '$or': [
                    {'evento_id': evento_obj_id},
                    {'evento_id': str(evento_id)}
                ]
            }))
        except:
            # Se não conseguir converter para ObjectId, busca apenas como string
            edicoes = list(edicoes_collection.find({'evento_id': str(evento_id)}))
        
        # Converter ObjectId para string
        for edicao in edicoes:
            edicao['_id'] = str(edicao['_id'])
            # Normalizar evento_id para string
            if isinstance(edicao.get('evento_id'), ObjectId):
                edicao['evento_id'] = str(edicao['evento_id'])
        return edicoes
    
    @staticmethod
    def find_by_id(edicao_id):
        """Encontra edição por ID"""
        edicoes_collection = mongo.get_collection('edicoes')
        edicao = edicoes_collection.find_one({'_id': ObjectId(edicao_id)})
        if edicao:
            edicao['_id'] = str(edicao['_id'])
            edicao['evento_id'] = str(edicao['evento_id'])
        return edicao
    
    @staticmethod
    def update(edicao_id, update_data):
        """Atualiza uma edição"""
        edicoes_collection = mongo.get_collection('edicoes')
        return edicoes_collection.update_one(
            {'_id': ObjectId(edicao_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def delete(edicao_id):
        """Deleta uma edição"""
        edicoes_collection = mongo.get_collection('edicoes')
        return edicoes_collection.delete_one({'_id': ObjectId(edicao_id)})
    
    def to_dict(self):
        return {
            'evento_id': self.evento_id,
            'ano': self.ano,
            'local': self.local,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'artigos': self.artigos,
            'data_criacao': self.data_criacao.isoformat()
        }
