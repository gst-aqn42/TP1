from datetime import datetime
from app.services.database import mongo

class Usuario:
    def __init__(self, email, nome, is_admin=False, senha=None):
        self.email = email
        self.nome = nome
        self.is_admin = is_admin
        self.senha = senha  # Em produção, use hash de senha
        self.data_criacao = datetime.utcnow()
        self.preferences = {
            'notificacoes_email': True,
            'artigos_por_pagina': 10
        }

    def save(self):
        """Salva o usuário no MongoDB"""
        usuarios_collection = mongo.get_collection('usuarios')
        usuario_data = {
            'email': self.email,
            'nome': self.nome,
            'is_admin': self.is_admin,
            'data_criacao': self.data_criacao,
            'preferences': self.preferences
        }
        if self.senha:
            usuario_data['senha'] = self.senha
        return usuarios_collection.insert_one(usuario_data)

    @staticmethod
    def find_by_email(email):
        """Encontra usuário por email"""
        usuarios_collection = mongo.get_collection('usuarios')
        return usuarios_collection.find_one({'email': email})

    @staticmethod
    def create_admin_user():
        """Cria usuário admin padrão se não existir"""
        admin_email = 'admin@simple-lib.com'
        if not Usuario.find_by_email(admin_email):
            admin = Usuario(admin_email, 'Administrador', True)
            admin.save()
            print("Usuário admin criado: admin@simple-lib.com")

    def to_dict(self):
        return {
            'email': self.email,
            'nome': self.nome,
            'is_admin': self.is_admin,
            'data_criacao': self.data_criacao.isoformat(),
            'preferences': self.preferences
        }
