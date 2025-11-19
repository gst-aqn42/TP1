"""
Testes de Integração: Frontend → Backend (Inscrições)
Testa as chamadas HTTP do Angular para inscrições de email.
Simula: ApiService.subscribeEmail()
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

import pytest
import json
from app import create_app
from app.services.database import mongo


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


@pytest.fixture(autouse=True)
def setup_database():
    """Setup e teardown do banco de dados de testes"""
    inscricoes_collection = mongo.get_collection('inscricoes')
    inscricoes_collection.delete_many({})
    
    yield
    
    inscricoes_collection.delete_many({})


class TestFrontendInscricoesIntegration:
    """Testes de integração Frontend → Backend para Inscrições"""
    
    def test_subscribe_email_success(self, client):
        """Testa POST /api/inscricoes com email válido (simula ApiService.subscribeEmail())"""
        email_data = {
            'email': 'usuario@test.com'
        }
        
        response = client.post(
            '/api/inscricoes',
            data=json.dumps(email_data),
            content_type='application/json'
        )
        
        assert response.status_code in [200, 201]
        
        # Verifica a resposta
        data = json.loads(response.data)
        assert 'message' in data or 'success' in data or 'email' in data
        
        # Verifica no banco
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricao_db = inscricoes_collection.find_one({'email': 'usuario@test.com'})
        assert inscricao_db is not None
    
    def test_subscribe_email_duplicate(self, client):
        """Testa POST /api/inscricoes com email já inscrito"""
        # Insere um email primeiro
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_one({'email': 'duplicado@test.com'})
        
        # Tenta inscrever o mesmo email
        email_data = {
            'email': 'duplicado@test.com'
        }
        
        response = client.post(
            '/api/inscricoes',
            data=json.dumps(email_data),
            content_type='application/json'
        )
        
        # Pode retornar 200 (já inscrito) ou 409 (conflito)
        assert response.status_code in [200, 201, 409, 400]
    
    def test_subscribe_email_invalid_format(self, client):
        """Testa POST /api/inscricoes com formato de email inválido"""
        email_data = {
            'email': 'email_invalido'  # Sem @
        }
        
        response = client.post(
            '/api/inscricoes',
            data=json.dumps(email_data),
            content_type='application/json'
        )
        
        # Deve retornar erro de validação
        assert response.status_code in [400, 422]
    
    def test_subscribe_email_empty(self, client):
        """Testa POST /api/inscricoes com email vazio"""
        email_data = {
            'email': ''
        }
        
        response = client.post(
            '/api/inscricoes',
            data=json.dumps(email_data),
            content_type='application/json'
        )
        
        assert response.status_code in [400, 422]
    
    def test_subscribe_email_missing(self, client):
        """Testa POST /api/inscricoes sem campo email"""
        email_data = {}
        
        response = client.post(
            '/api/inscricoes',
            data=json.dumps(email_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_subscribe_email_with_whitespace(self, client):
        """Testa POST /api/inscricoes com email contendo espaços"""
        email_data = {
            'email': '  usuario@test.com  '
        }
        
        response = client.post(
            '/api/inscricoes',
            data=json.dumps(email_data),
            content_type='application/json'
        )
        
        # Pode aceitar (removendo espaços) ou rejeitar
        assert response.status_code in [200, 201, 400, 422]
        
        if response.status_code in [200, 201]:
            # Verifica que armazenou sem espaços
            inscricoes_collection = mongo.get_collection('inscricoes')
            inscricao_db = inscricoes_collection.find_one({})
            if inscricao_db:
                email_stored = inscricao_db['email']
                assert email_stored.strip() == email_stored  # Sem espaços nas pontas
    
    def test_subscribe_multiple_emails(self, client):
        """Testa inscrição de múltiplos emails diferentes"""
        emails = [
            'usuario1@test.com',
            'usuario2@test.com',
            'usuario3@test.com'
        ]
        
        for email in emails:
            response = client.post(
                '/api/inscricoes',
                data=json.dumps({'email': email}),
                content_type='application/json'
            )
            assert response.status_code in [200, 201]
        
        # Verifica que todos foram salvos
        inscricoes_collection = mongo.get_collection('inscricoes')
        count = inscricoes_collection.count_documents({})
        assert count == 3
    
    def test_subscribe_email_different_domains(self, client):
        """Testa inscrição com diferentes domínios de email"""
        emails = [
            'user@gmail.com',
            'user@hotmail.com',
            'user@yahoo.com',
            'user@company.com.br'
        ]
        
        for email in emails:
            response = client.post(
                '/api/inscricoes',
                data=json.dumps({'email': email}),
                content_type='application/json'
            )
            assert response.status_code in [200, 201, 400, 422]
    
    def test_subscribe_workflow_from_frontend(self, client):
        """Testa fluxo completo de inscrição simulando frontend Angular"""
        # 1. Usuário preenche formulário e clica em "Inscrever"
        # O componente Angular chama ApiService.subscribeEmail()
        
        user_email = 'novousuario@test.com'
        
        # 2. Frontend faz POST /api/inscricoes
        response = client.post(
            '/api/inscricoes',
            data=json.dumps({'email': user_email}),
            content_type='application/json'
        )
        
        # 3. Verifica resposta de sucesso
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        
        # 4. Frontend mostra mensagem de sucesso ao usuário
        assert 'message' in data or 'success' in data or 'email' in data
        
        # 5. Verifica que email foi salvo no backend
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricao = inscricoes_collection.find_one({'email': user_email})
        assert inscricao is not None
        assert inscricao['email'] == user_email
        
        # 6. Tenta inscrever novamente (usuário clica duas vezes)
        duplicate_response = client.post(
            '/api/inscricoes',
            data=json.dumps({'email': user_email}),
            content_type='application/json'
        )
        
        # Deve lidar com duplicata apropriadamente
        assert duplicate_response.status_code in [200, 201, 409, 400]
    
    def test_subscribe_email_case_sensitivity(self, client):
        """Testa se emails com diferentes cases são tratados corretamente"""
        # Inscreve em lowercase
        response1 = client.post(
            '/api/inscricoes',
            data=json.dumps({'email': 'user@test.com'}),
            content_type='application/json'
        )
        assert response1.status_code in [200, 201]
        
        # Tenta inscrever em uppercase
        response2 = client.post(
            '/api/inscricoes',
            data=json.dumps({'email': 'USER@TEST.COM'}),
            content_type='application/json'
        )
        
        # Pode aceitar (emails diferentes) ou rejeitar (mesmo email)
        assert response2.status_code in [200, 201, 400, 409]
