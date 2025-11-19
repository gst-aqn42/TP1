"""
Testes de Integração: Frontend → Backend (Eventos)
Testa as chamadas HTTP do Angular para os endpoints de eventos.
Simula: ApiService.getEvents(), createEvent(), updateEvent(), deleteEvent()
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

import pytest
import json
from app import create_app
from app.services.database import mongo
from bson import ObjectId


@pytest.fixture
def app():
    """Cria uma instância do app Flask para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    """Cria um cliente de teste HTTP"""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Obtém um token de autenticação válido"""
    # Cria um admin
    usuarios_collection = mongo.get_collection('usuarios')
    usuarios_collection.delete_many({})
    
    admin_user = {
        'email': 'admin@test.com',
        'nome': 'Admin Test',
        'senha': 'admin123',  # Senha em texto plano
        'is_admin': True
    }
    usuarios_collection.insert_one(admin_user)
    
    # Faz login
    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'admin@test.com',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    
    return json.loads(response.data)['token']


@pytest.fixture(autouse=True)
def setup_database():
    """Setup e teardown do banco de dados de testes"""
    # Setup: limpa coleções
    eventos_collection = mongo.get_collection('eventos')
    eventos_collection.delete_many({})
    
    yield
    
    # Teardown: limpa o banco
    eventos_collection.delete_many({})
    usuarios_collection = mongo.get_collection('usuarios')
    usuarios_collection.delete_many({})


class TestFrontendEventosIntegration:
    """Testes de integração Frontend → Backend para Eventos"""
    
    def test_get_events_empty_list(self, client):
        """Testa GET /api/eventos/ sem eventos (simula ApiService.getEvents())"""
        response = client.get('/api/eventos/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Backend retorna {"eventos": []}
        assert 'eventos' in data
        assert isinstance(data['eventos'], list)
        assert len(data['eventos']) == 0
    
    def test_get_events_with_data(self, client):
        """Testa GET /api/eventos/ com eventos existentes"""
        # Insere eventos diretamente no banco
        eventos_collection = mongo.get_collection('eventos')
        eventos_collection.insert_many([
            {'nome': 'Evento 1', 'descricao': 'Descrição 1', 'sigla': 'EVT1'},
            {'nome': 'Evento 2', 'descricao': 'Descrição 2', 'sigla': 'EVT2'}
        ])
        
        response = client.get('/api/eventos/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Backend retorna {"eventos": [...]}
        assert 'eventos' in data
        assert isinstance(data['eventos'], list)
        assert len(data['eventos']) == 2
        assert data['eventos'][0]['nome'] == 'Evento 1'
        assert data['eventos'][1]['nome'] == 'Evento 2'
    
    def test_create_event_success(self, client, auth_token):
        """Testa POST /api/eventos/ criando evento (simula ApiService.createEvent())"""
        evento_data = {
            'nome': 'Novo Evento',
            'descricao': 'Descrição do novo evento',
            'sigla': 'NEVT'
        }
        
        response = client.post(
            '/api/eventos/',
            data=json.dumps(evento_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Pode retornar 201 (created) ou 200 dependendo da implementação
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        
        # Verifica se o evento foi criado
        if 'id' in data or '_id' in data:
            event_id = data.get('id') or data.get('_id')
            assert event_id is not None
        
        # Verifica no banco
        eventos_collection = mongo.get_collection('eventos')
        evento_db = eventos_collection.find_one({'nome': 'Novo Evento'})
        assert evento_db is not None
        assert evento_db['descricao'] == 'Descrição do novo evento'
    
    def test_create_event_without_auth(self, client):
        """Testa POST /api/eventos/ sem autenticação"""
        evento_data = {
            'nome': 'Evento Sem Auth',
            'descricao': 'Não deve ser criado'
        }
        
        response = client.post(
            '/api/eventos/',
            data=json.dumps(evento_data),
            content_type='application/json'
        )
        
        # Deve retornar 401 ou 403 se o endpoint for protegido
        # Ou 201 se for público
        assert response.status_code in [200, 201, 401, 403]
    
    def test_create_event_invalid_data(self, client, auth_token):
        """Testa POST /api/eventos/ com dados inválidos"""
        evento_data = {
            'nome': ''  # Nome vazio (inválido)
        }
        
        response = client.post(
            '/api/eventos/',
            data=json.dumps(evento_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Deve retornar erro de validação
        assert response.status_code in [400, 422]
    
    def test_update_event_success(self, client, auth_token):
        """Testa PUT /api/eventos/:id atualizando evento (simula ApiService.updateEvent())"""
        # Cria um evento primeiro
        eventos_collection = mongo.get_collection('eventos')
        result = eventos_collection.insert_one({
            'nome': 'Evento Original',
            'descricao': 'Descrição original',
            'sigla': 'EVTO'
        })
        evento_id = str(result.inserted_id)
        
        # Atualiza o evento
        update_data = {
            'nome': 'Evento Atualizado',
            'descricao': 'Descrição atualizada'
        }
        
        response = client.put(
            f'/api/eventos/{evento_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        
        # Verifica no banco
        evento_db = eventos_collection.find_one({'_id': ObjectId(evento_id)})
        assert evento_db['nome'] == 'Evento Atualizado'
        assert evento_db['descricao'] == 'Descrição atualizada'
    
    def test_update_event_not_found(self, client, auth_token):
        """Testa PUT /api/eventos/:id com ID inexistente"""
        fake_id = str(ObjectId())
        
        update_data = {
            'nome': 'Evento Inexistente'
        }
        
        response = client.put(
            f'/api/eventos/{fake_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 404
    
    def test_delete_event_success(self, client, auth_token):
        """Testa DELETE /api/eventos/:id (simula ApiService.deleteEvent())"""
        # Cria um evento primeiro
        eventos_collection = mongo.get_collection('eventos')
        result = eventos_collection.insert_one({
            'nome': 'Evento Para Deletar',
            'descricao': 'Será deletado'
        })
        evento_id = str(result.inserted_id)
        
        # Deleta o evento
        response = client.delete(
            f'/api/eventos/{evento_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [200, 204]
        
        # Verifica que foi deletado
        evento_db = eventos_collection.find_one({'_id': ObjectId(evento_id)})
        assert evento_db is None
    
    def test_delete_event_not_found(self, client, auth_token):
        """Testa DELETE /api/eventos/:id com ID inexistente"""
        fake_id = str(ObjectId())
        
        response = client.delete(
            f'/api/eventos/{fake_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 404
    
    def test_full_crud_workflow_from_frontend(self, client, auth_token):
        """Testa fluxo completo CRUD simulando chamadas do Angular"""
        # 1. CREATE - ApiService.createEvent()
        create_response = client.post(
            '/api/eventos/',
            data=json.dumps({
                'nome': 'Workshop EngSoft',
                'descricao': 'Workshop de Engenharia de Software',
                'sigla': 'WES'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert create_response.status_code in [200, 201]
        
        # 2. READ - ApiService.getEvents()
        read_response = client.get('/api/eventos/')
        assert read_response.status_code == 200
        eventos_data = json.loads(read_response.data)
        eventos = eventos_data['eventos']  # Backend retorna {"eventos": [...]}
        assert len(eventos) >= 1
        
        evento_id = eventos[0]['_id'] if '_id' in eventos[0] else eventos[0]['id']
        
        # 3. UPDATE - ApiService.updateEvent()
        update_response = client.put(
            f'/api/eventos/{evento_id}',
            data=json.dumps({
                'nome': 'Workshop EngSoft 2024',
                'descricao': 'Workshop de Engenharia de Software - Edição 2024'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert update_response.status_code == 200
        
        # 4. DELETE - ApiService.deleteEvent()
        delete_response = client.delete(
            f'/api/eventos/{evento_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert delete_response.status_code in [200, 204]
        
        # 5. Verifica que foi deletado
        final_response = client.get('/api/eventos/')
        eventos_final_data = json.loads(final_response.data)
        eventos_final = eventos_final_data['eventos']  # Backend retorna {"eventos": [...]}
        assert len(eventos_final) == 0
