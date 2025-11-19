"""
Testes de integração: Backend → MongoDB (Operações CRUD Reais)
Testa as operações reais com o banco de dados MongoDB
"""

import pytest
import sys
import os
from datetime import datetime
from bson import ObjectId

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.models.evento import Evento
from app.models.edicao import EdicaoEvento
from app.models.artigo import Artigo
from app.models.usuario import Usuario
from app.models.notificacao import Notificacao


class TestEventoIntegration:
    """Testes de integração para o modelo Evento com MongoDB real"""
    
    def test_save_evento_persists_to_database(self, setup_test_mongo, sample_evento_data):
        """Testa se save() persiste o evento no MongoDB"""
        # Arrange
        evento = Evento(**sample_evento_data)
        
        # Act
        result = evento.save()
        
        # Assert
        assert result is not None
        assert result.inserted_id is not None
        
        # Verificar se foi salvo no banco
        eventos = Evento.find_all()
        assert len(eventos) == 1
        assert eventos[0]['nome'] == sample_evento_data['nome']
        assert eventos[0]['sigla'] == sample_evento_data['sigla']
    
    def test_find_all_returns_all_eventos(self, setup_test_mongo):
        """Testa se find_all() retorna todos os eventos"""
        # Arrange
        evento1 = Evento('Evento 1', 'EV1', 'Descrição 1')
        evento2 = Evento('Evento 2', 'EV2', 'Descrição 2')
        evento1.save()
        evento2.save()
        
        # Act
        eventos = Evento.find_all()
        
        # Assert
        assert len(eventos) == 2
        siglas = [e['sigla'] for e in eventos]
        assert 'EV1' in siglas
        assert 'EV2' in siglas
    
    def test_find_by_id_returns_correct_evento(self, setup_test_mongo, sample_evento_data):
        """Testa se find_by_id() retorna o evento correto"""
        # Arrange
        evento = Evento(**sample_evento_data)
        result = evento.save()
        evento_id = str(result.inserted_id)
        
        # Act
        found_evento = Evento.find_by_id(evento_id)
        
        # Assert
        assert found_evento is not None
        assert found_evento['_id'] == evento_id
        assert found_evento['nome'] == sample_evento_data['nome']
    
    def test_find_by_sigla_returns_correct_evento(self, setup_test_mongo, sample_evento_data):
        """Testa se find_by_sigla() retorna o evento correto"""
        # Arrange
        evento = Evento(**sample_evento_data)
        evento.save()
        
        # Act
        found_evento = Evento.find_by_sigla(sample_evento_data['sigla'])
        
        # Assert
        assert found_evento is not None
        assert found_evento['sigla'] == sample_evento_data['sigla']
        assert found_evento['nome'] == sample_evento_data['nome']
    
    def test_update_evento_modifies_database(self, setup_test_mongo, sample_evento_data):
        """Testa se update() modifica o evento no banco"""
        # Arrange
        evento = Evento(**sample_evento_data)
        result = evento.save()
        evento_id = str(result.inserted_id)
        
        # Act
        update_result = Evento.update(evento_id, {'descricao': 'Nova descrição'})
        
        # Assert
        assert update_result.modified_count == 1
        
        # Verificar se foi atualizado
        updated_evento = Evento.find_by_id(evento_id)
        assert updated_evento['descricao'] == 'Nova descrição'
    
    def test_delete_evento_removes_from_database(self, setup_test_mongo, sample_evento_data):
        """Testa se delete() remove o evento do banco"""
        # Arrange
        evento = Evento(**sample_evento_data)
        result = evento.save()
        evento_id = str(result.inserted_id)
        
        # Act
        delete_result = Evento.delete(evento_id)
        
        # Assert
        assert delete_result.deleted_count == 1
        
        # Verificar se foi removido
        deleted_evento = Evento.find_by_id(evento_id)
        assert deleted_evento is None


class TestEdicaoEventoIntegration:
    """Testes de integração para o modelo EdicaoEvento com MongoDB real"""
    
    def test_save_edicao_persists_to_database(self, setup_test_mongo, sample_edicao_data):
        """Testa se save() persiste a edição no MongoDB"""
        # Arrange
        edicao = EdicaoEvento(**sample_edicao_data)
        
        # Act
        result = edicao.save()
        
        # Assert
        assert result is not None
        assert result.inserted_id is not None
    
    def test_find_by_evento_returns_edicoes(self, setup_test_mongo, sample_evento_data):
        """Testa se find_by_evento() retorna edições do evento"""
        # Arrange
        evento = Evento(**sample_evento_data)
        evento_result = evento.save()
        evento_id = str(evento_result.inserted_id)
        
        edicao1 = EdicaoEvento(evento_id, 2023, 'Rio de Janeiro')
        edicao2 = EdicaoEvento(evento_id, 2024, 'São Paulo')
        edicao1.save()
        edicao2.save()
        
        # Act
        edicoes = EdicaoEvento.find_by_evento(evento_id)
        
        # Assert
        assert len(edicoes) == 2
        anos = [e['ano'] for e in edicoes]
        assert 2023 in anos
        assert 2024 in anos
    
    def test_find_by_id_returns_correct_edicao(self, setup_test_mongo, sample_edicao_data):
        """Testa se find_by_id() retorna a edição correta"""
        # Arrange
        edicao = EdicaoEvento(**sample_edicao_data)
        result = edicao.save()
        edicao_id = str(result.inserted_id)
        
        # Act
        found_edicao = EdicaoEvento.find_by_id(edicao_id)
        
        # Assert
        assert found_edicao is not None
        assert found_edicao['_id'] == edicao_id
        assert found_edicao['ano'] == sample_edicao_data['ano']
    
    def test_update_edicao_modifies_database(self, setup_test_mongo, sample_edicao_data):
        """Testa se update() modifica a edição no banco"""
        # Arrange
        edicao = EdicaoEvento(**sample_edicao_data)
        result = edicao.save()
        edicao_id = str(result.inserted_id)
        
        # Act
        update_result = EdicaoEvento.update(edicao_id, {'local': 'Brasília, DF'})
        
        # Assert
        assert update_result.modified_count == 1
        
        updated_edicao = EdicaoEvento.find_by_id(edicao_id)
        assert updated_edicao['local'] == 'Brasília, DF'
    
    def test_delete_edicao_removes_from_database(self, setup_test_mongo, sample_edicao_data):
        """Testa se delete() remove a edição do banco"""
        # Arrange
        edicao = EdicaoEvento(**sample_edicao_data)
        result = edicao.save()
        edicao_id = str(result.inserted_id)
        
        # Act
        delete_result = EdicaoEvento.delete(edicao_id)
        
        # Assert
        assert delete_result.deleted_count == 1
        
        deleted_edicao = EdicaoEvento.find_by_id(edicao_id)
        assert deleted_edicao is None


class TestArtigoIntegration:
    """Testes de integração para o modelo Artigo com MongoDB real"""
    
    def test_save_artigo_persists_to_database(self, setup_test_mongo, sample_artigo_data):
        """Testa se save() persiste o artigo no MongoDB"""
        # Arrange
        artigo = Artigo(**sample_artigo_data)
        
        # Act
        result = artigo.save()
        
        # Assert
        assert result is not None
        assert result.inserted_id is not None
    
    def test_find_by_edicao_returns_artigos(self, setup_test_mongo, sample_artigo_data):
        """Testa se find_by_edicao() retorna artigos da edição"""
        # Arrange
        edicao_id = sample_artigo_data['edicao_id']
        
        artigo1 = Artigo(
            titulo='Artigo 1',
            autores=[{'nome': 'Autor 1', 'email': 'autor1@test.com'}],
            edicao_id=edicao_id
        )
        artigo2 = Artigo(
            titulo='Artigo 2',
            autores=[{'nome': 'Autor 2', 'email': 'autor2@test.com'}],
            edicao_id=edicao_id
        )
        artigo1.save()
        artigo2.save()
        
        # Act
        artigos = Artigo.find_by_edicao(edicao_id)
        
        # Assert
        assert len(artigos) == 2
        titulos = [a['titulo'] for a in artigos]
        assert 'Artigo 1' in titulos
        assert 'Artigo 2' in titulos
    
    def test_find_by_id_returns_correct_artigo(self, setup_test_mongo, sample_artigo_data):
        """Testa se find_by_id() retorna o artigo correto"""
        # Arrange
        artigo = Artigo(**sample_artigo_data)
        result = artigo.save()
        artigo_id = str(result.inserted_id)
        
        # Act
        found_artigo = Artigo.find_by_id(artigo_id)
        
        # Assert
        assert found_artigo is not None
        assert found_artigo['_id'] == artigo_id
        assert found_artigo['titulo'] == sample_artigo_data['titulo']
    
    def test_update_artigo_modifies_database(self, setup_test_mongo, sample_artigo_data):
        """Testa se update() modifica o artigo no banco"""
        # Arrange
        artigo = Artigo(**sample_artigo_data)
        result = artigo.save()
        artigo_id = str(result.inserted_id)
        
        # Act
        update_result = Artigo.update(artigo_id, {'titulo': 'Título Atualizado'})
        
        # Assert
        assert update_result.modified_count == 1
        
        updated_artigo = Artigo.find_by_id(artigo_id)
        assert updated_artigo['titulo'] == 'Título Atualizado'
    
    def test_delete_artigo_removes_from_database(self, setup_test_mongo, sample_artigo_data):
        """Testa se delete() remove o artigo do banco"""
        # Arrange
        artigo = Artigo(**sample_artigo_data)
        result = artigo.save()
        artigo_id = str(result.inserted_id)
        
        # Act
        delete_result = Artigo.delete(artigo_id)
        
        # Assert
        assert delete_result.deleted_count == 1
        
        deleted_artigo = Artigo.find_by_id(artigo_id)
        assert deleted_artigo is None
    
    def test_artigo_preserves_autores_array(self, setup_test_mongo, sample_artigo_data):
        """Testa se o array de autores é preservado corretamente"""
        # Arrange
        artigo = Artigo(**sample_artigo_data)
        result = artigo.save()
        artigo_id = str(result.inserted_id)
        
        # Act
        found_artigo = Artigo.find_by_id(artigo_id)
        
        # Assert
        assert len(found_artigo['autores']) == 2
        assert found_artigo['autores'][0]['nome'] == 'Dr. João Silva'
        assert found_artigo['autores'][1]['email'] == 'maria@univ.edu'


class TestUsuarioIntegration:
    """Testes de integração para o modelo Usuario com MongoDB real"""
    
    def test_save_usuario_persists_to_database(self, setup_test_mongo, sample_usuario_data):
        """Testa se save() persiste o usuário no MongoDB"""
        # Arrange
        usuario = Usuario(**sample_usuario_data)
        
        # Act
        result = usuario.save()
        
        # Assert
        assert result is not None
        assert result.inserted_id is not None
    
    def test_find_by_email_returns_correct_usuario(self, setup_test_mongo, sample_usuario_data):
        """Testa se find_by_email() retorna o usuário correto"""
        # Arrange
        usuario = Usuario(**sample_usuario_data)
        usuario.save()
        
        # Act
        found_usuario = Usuario.find_by_email(sample_usuario_data['email'])
        
        # Assert
        assert found_usuario is not None
        assert found_usuario['email'] == sample_usuario_data['email']
        assert found_usuario['nome'] == sample_usuario_data['nome']
    
    def test_find_by_email_returns_none_when_not_found(self, setup_test_mongo):
        """Testa se find_by_email() retorna None quando não encontrado"""
        # Act
        found_usuario = Usuario.find_by_email('naoexiste@test.com')
        
        # Assert
        assert found_usuario is None
    
    def test_create_admin_user_creates_default_admin(self, setup_test_mongo):
        """Testa se create_admin_user() cria o admin padrão"""
        # Act
        Usuario.create_admin_user()
        
        # Assert
        admin = Usuario.find_by_email('admin@simple-lib.com')
        assert admin is not None
        assert admin['nome'] == 'Administrador'
        assert admin['is_admin'] is True
    
    def test_create_admin_user_does_not_duplicate(self, setup_test_mongo):
        """Testa se create_admin_user() não cria duplicados"""
        # Arrange
        Usuario.create_admin_user()
        
        # Act
        Usuario.create_admin_user()
        
        # Assert
        from app.services.database import mongo
        usuarios = list(mongo.get_collection('usuarios').find({'email': 'admin@simple-lib.com'}))
        assert len(usuarios) == 1


class TestNotificacaoIntegration:
    """Testes de integração para o modelo Notificacao com MongoDB real"""
    
    def test_save_notificacao_persists_to_database(self, setup_test_mongo, sample_notificacao_data):
        """Testa se save() persiste a notificação no MongoDB"""
        # Arrange
        notificacao = Notificacao(**sample_notificacao_data)
        
        # Act
        result = notificacao.save()
        
        # Assert
        assert result is not None
        assert result.inserted_id is not None
    
    def test_find_by_autor_returns_notificacoes(self, setup_test_mongo):
        """Testa se find_by_autor() retorna notificações do autor"""
        # Arrange
        notif1 = Notificacao('user1@test.com', 'Dr. João Silva')
        notif2 = Notificacao('user2@test.com', 'Dr. João Silva')
        notif1.save()
        notif2.save()
        
        # Act
        notificacoes = Notificacao.find_by_autor('Dr. João Silva')
        
        # Assert
        assert len(notificacoes) == 2
    
    def test_find_by_autor_is_case_insensitive(self, setup_test_mongo):
        """Testa se find_by_autor() é case-insensitive"""
        # Arrange
        notif = Notificacao('user@test.com', 'Dr. João Silva')
        notif.save()
        
        # Act
        notificacoes = Notificacao.find_by_autor('joão silva')
        
        # Assert
        assert len(notificacoes) == 1
    
    def test_desativar_inscricao_sets_ativo_to_false(self, setup_test_mongo, sample_notificacao_data):
        """Testa se desativar_inscricao() define ativo como False"""
        # Arrange
        notificacao = Notificacao(**sample_notificacao_data)
        result = notificacao.save()
        notificacao_id = str(result.inserted_id)
        
        # Act
        update_result = Notificacao.desativar_inscricao(notificacao_id)
        
        # Assert
        assert update_result.modified_count == 1
        
        # Verificar no banco
        from app.services.database import mongo
        notif_data = mongo.get_collection('notificacoes').find_one({'_id': ObjectId(notificacao_id)})
        assert notif_data['ativo'] is False
    
    def test_find_by_autor_only_returns_active(self, setup_test_mongo):
        """Testa se find_by_autor() retorna apenas notificações ativas"""
        # Arrange
        notif1 = Notificacao('user1@test.com', 'Dr. João Silva')
        notif2 = Notificacao('user2@test.com', 'Dr. João Silva')
        result1 = notif1.save()
        notif2.save()
        
        # Desativar uma
        Notificacao.desativar_inscricao(str(result1.inserted_id))
        
        # Act
        notificacoes = Notificacao.find_by_autor('Dr. João Silva')
        
        # Assert
        assert len(notificacoes) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
