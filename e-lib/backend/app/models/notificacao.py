from datetime import datetime
from app.services.database import mongo
from bson import ObjectId

class Notificacao:
    def __init__(self, email, nome_autor):
        self.email = email
        self.nome_autor = nome_autor
        self.data_inscricao = datetime.utcnow()
        self.ativo = True
    
    def save(self):
        """Salva a inscrição de notificação"""
        try:
            notificacoes_collection = mongo.get_collection('notificacoes')
            notificacao_data = {
                'email': self.email,
                'nome_autor': self.nome_autor,
                'data_inscricao': self.data_inscricao,
                'ativo': self.ativo
            }
            result = notificacoes_collection.insert_one(notificacao_data)
            print(f"Inscrição de notificação salva: {self.email} para {self.nome_autor}")
            return result
        except Exception as e:
            print(f"Erro ao salvar notificação: {e}")
            return None
    
    @staticmethod
    def find_by_autor(nome_autor):
        """Encontra notificações por nome do autor"""
        try:
            notificacoes_collection = mongo.get_collection('notificacoes')
            notificacoes = list(notificacoes_collection.find({
                'nome_autor': {'$regex': nome_autor, '$options': 'i'},
                'ativo': True
            }))
            return notificacoes
        except Exception as e:
            print(f"Erro ao buscar notificações: {e}")
            return []
    
    @staticmethod
    def desativar_inscricao(notificacao_id):
        """Desativa uma inscrição"""
        try:
            notificacoes_collection = mongo.get_collection('notificacoes')
            result = notificacoes_collection.update_one(
                {'_id': ObjectId(notificacao_id)},
                {'$set': {'ativo': False}}
            )
            return result
        except Exception as e:
            print(f"Erro ao desativar notificação: {e}")
            return None
