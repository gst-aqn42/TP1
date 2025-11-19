"""
Testes de Integração: Rotas de Eventos → Backend → MongoDB
Testa o fluxo completo de HTTP requests através das rotas de eventos.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app import create_app
from app.services.database import mongo
from bson import ObjectId
import jwt


@pytest.fixture
def app():
    """Cria a aplicação Flask para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key-123'
    yield app


@pytest.fixture
def client(app):
    """Cliente de teste Flask"""
    return app.test_client()


@pytest.fixture
def clean_db():
    """Limpa o banco de dados antes de cada teste"""
    eventos_collection = mongo.get_collection('eventos')
    eventos_collection.delete_many({})
    yield
    eventos_collection.delete_many({})


@pytest.fixture
def admin_token(app):
    """Gera um token de admin para testes"""
    with app.app_context():
        token = jwt.encode(
            {'user_id': str(ObjectId()), 'is_admin': True},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    return token


@pytest.fixture
def user_token(app):
    """Gera um token de usuário comum para testes"""
    with app.app_context():
        token = jwt.encode(
            {'user_id': str(ObjectId()), 'is_admin': False},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    return token


@pytest.fixture
def sample_evento():
    """Cria um evento de exemplo no banco"""
    eventos_collection = mongo.get_collection('eventos')
    result = eventos_collection.insert_one({
        'nome': 'Simpósio Brasileiro de Engenharia de Software',
        'sigla': 'SBES',
        'descricao': 'Evento anual de engenharia de software'
    })
    evento_id = str(result.inserted_id)
    yield evento_id
    eventos_collection.delete_one({'_id': result.inserted_id})


class TestEventosRoutes:
    """Testes de integração para rotas de eventos"""
    
    def test_listar_eventos_vazio(self, client, clean_db):
        """Testa listagem de eventos quando não há eventos"""
        response = client.get('/api/eventos/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'eventos' in data
        assert len(data['eventos']) == 0
    
    def test_listar_eventos_com_dados(self, client, clean_db):
        """Testa listagem de eventos com dados"""
        # Criar eventos diretamente no banco
        eventos_collection = mongo.get_collection('eventos')
        eventos_collection.insert_many([
            {'nome': 'Evento 1', 'sigla': 'EV1', 'descricao': 'Descrição 1'},
            {'nome': 'Evento 2', 'sigla': 'EV2', 'descricao': 'Descrição 2'}
        ])
        
        response = client.get('/api/eventos/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['eventos']) == 2
        assert data['eventos'][0]['nome'] == 'Evento 1'
        assert data['eventos'][1]['sigla'] == 'EV2'
    
    def test_criar_evento_success(self, client, clean_db, admin_token):
        """Testa criação de evento com sucesso"""
        response = client.post('/api/eventos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'nome': 'Conferência Internacional de IA',
                'sigla': 'ICAI',
                'descricao': 'Conferência sobre inteligência artificial'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Evento criado com sucesso'
        assert 'evento_id' in data
        
        # Verificar que foi salvo no banco
        eventos_collection = mongo.get_collection('eventos')
        evento_db = eventos_collection.find_one({'_id': ObjectId(data['evento_id'])})
        assert evento_db is not None
        assert evento_db['nome'] == 'Conferência Internacional de IA'
        assert evento_db['sigla'] == 'ICAI'
    
    def test_criar_evento_sem_descricao(self, client, clean_db, admin_token):
        """Testa criação de evento sem descrição (opcional)"""
        response = client.post('/api/eventos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'nome': 'Workshop de Testes',
                'sigla': 'WT'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Verificar no banco
        eventos_collection = mongo.get_collection('eventos')
        evento_db = eventos_collection.find_one({'_id': ObjectId(data['evento_id'])})
        assert evento_db['descricao'] is None
    
    def test_criar_evento_sem_nome(self, client, clean_db, admin_token):
        """Testa criação de evento sem nome"""
        response = client.post('/api/eventos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'sigla': 'TEST'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Nome e sigla são obrigatórios' in data['error']
    
    def test_criar_evento_sem_sigla(self, client, clean_db, admin_token):
        """Testa criação de evento sem sigla"""
        response = client.post('/api/eventos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'nome': 'Evento Teste'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Nome e sigla são obrigatórios' in data['error']
    
    def test_criar_evento_sem_autorizacao(self, client, clean_db):
        """Testa criação de evento sem token de autenticação"""
        response = client.post('/api/eventos/', json={
            'nome': 'Evento Teste',
            'sigla': 'ET'
        })
        
        assert response.status_code == 401
    
    def test_criar_evento_usuario_comum(self, client, clean_db, user_token):
        """Testa criação de evento com usuário não-admin"""
        response = client.post('/api/eventos/', 
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'nome': 'Evento Teste',
                'sigla': 'ET'
            }
        )
        
        assert response.status_code == 403
    
    def test_obter_evento_success(self, client, sample_evento):
        """Testa obter um evento específico"""
        response = client.get(f'/api/eventos/{sample_evento}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['_id'] == sample_evento
        assert data['nome'] == 'Simpósio Brasileiro de Engenharia de Software'
        assert data['sigla'] == 'SBES'
    
    def test_obter_evento_nao_encontrado(self, client, clean_db):
        """Testa obter evento inexistente"""
        fake_id = str(ObjectId())
        response = client.get(f'/api/eventos/{fake_id}')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Evento não encontrado' in data['error']
    
    def test_obter_evento_id_invalido(self, client):
        """Testa obter evento com ID inválido"""
        response = client.get('/api/eventos/id-invalido')
        
        assert response.status_code == 500
    
    def test_atualizar_evento_success(self, client, sample_evento, admin_token):
        """Testa atualização de evento com sucesso"""
        response = client.put(f'/api/eventos/{sample_evento}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'nome': 'SBES - Atualizado',
                'descricao': 'Nova descrição'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Evento atualizado com sucesso'
        
        # Verificar atualização no banco
        eventos_collection = mongo.get_collection('eventos')
        evento_db = eventos_collection.find_one({'_id': ObjectId(sample_evento)})
        assert evento_db['nome'] == 'SBES - Atualizado'
        assert evento_db['descricao'] == 'Nova descrição'
    
    def test_atualizar_evento_parcial(self, client, sample_evento, admin_token):
        """Testa atualização parcial de evento"""
        response = client.put(f'/api/eventos/{sample_evento}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'sigla': 'SBES2024'
            }
        )
        
        assert response.status_code == 200
        
        # Verificar que apenas sigla foi atualizada
        eventos_collection = mongo.get_collection('eventos')
        evento_db = eventos_collection.find_one({'_id': ObjectId(sample_evento)})
        assert evento_db['sigla'] == 'SBES2024'
        assert evento_db['nome'] == 'Simpósio Brasileiro de Engenharia de Software'
    
    def test_atualizar_evento_nao_encontrado(self, client, clean_db, admin_token):
        """Testa atualização de evento inexistente"""
        fake_id = str(ObjectId())
        response = client.put(f'/api/eventos/{fake_id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'nome': 'Novo Nome'}
        )
        
        assert response.status_code == 404
    
    def test_atualizar_evento_sem_dados(self, client, sample_evento, admin_token):
        """Testa atualização sem dados"""
        response = client.put(f'/api/eventos/{sample_evento}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={}
        )
        
        assert response.status_code == 400
    
    def test_atualizar_evento_sem_autorizacao(self, client, sample_evento):
        """Testa atualização sem token"""
        response = client.put(f'/api/eventos/{sample_evento}',
            json={'nome': 'Novo Nome'}
        )
        
        assert response.status_code == 401
    
    def test_atualizar_evento_usuario_comum(self, client, sample_evento, user_token):
        """Testa atualização com usuário não-admin"""
        response = client.put(f'/api/eventos/{sample_evento}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'nome': 'Novo Nome'}
        )
        
        assert response.status_code == 403
    
    def test_deletar_evento_success(self, client, sample_evento, admin_token):
        """Testa deleção de evento com sucesso"""
        response = client.delete(f'/api/eventos/{sample_evento}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'deletado com sucesso' in data['message']
        
        # Verificar que foi removido do banco
        eventos_collection = mongo.get_collection('eventos')
        evento_db = eventos_collection.find_one({'_id': ObjectId(sample_evento)})
        assert evento_db is None
    
    def test_deletar_evento_nao_encontrado(self, client, clean_db, admin_token):
        """Testa deleção de evento inexistente"""
        fake_id = str(ObjectId())
        response = client.delete(f'/api/eventos/{fake_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 404
    
    def test_deletar_evento_sem_autorizacao(self, client, sample_evento):
        """Testa deleção sem token"""
        response = client.delete(f'/api/eventos/{sample_evento}')
        
        assert response.status_code == 401
    
    def test_deletar_evento_usuario_comum(self, client, sample_evento, user_token):
        """Testa deleção com usuário não-admin"""
        response = client.delete(f'/api/eventos/{sample_evento}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        
        assert response.status_code == 403
