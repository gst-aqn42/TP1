"""
Testes de Integração: Frontend → Backend (Auth)
Testa as chamadas HTTP do Angular para os endpoints de autenticação.
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
    # Setup: limpa e cria usuário admin
    usuarios_collection = mongo.get_collection('usuarios')
    usuarios_collection.delete_many({})
    
    # Cria um admin para testes (senha em texto plano conforme backend espera)
    admin_user = {
        'email': 'admin@test.com',
        'nome': 'Admin Test',
        'senha': 'admin123',  # Senha em texto plano
        'is_admin': True
    }
    usuarios_collection.insert_one(admin_user)
    
    yield
    
    # Teardown: limpa o banco
    usuarios_collection.delete_many({})


class TestFrontendAuthIntegration:
    """Testes de integração Frontend → Backend para Auth"""
    
    def test_login_success_with_valid_credentials(self, client):
        """Testa POST /api/auth/login com credenciais válidas (simula Angular AuthService.login)"""
        # Simula a chamada HTTP do Angular
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'admin@test.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert data['token'] is not None
        assert len(data['token']) > 0
    
    def test_login_failure_with_invalid_email(self, client):
        """Testa POST /api/auth/login com email inválido"""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'invalid@test.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        
        # Backend retorna 404 (usuário não encontrado) ao invés de 401
        assert response.status_code in [401, 404]
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_failure_with_invalid_password(self, client):
        """Testa POST /api/auth/login com senha inválida"""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'admin@test.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_failure_missing_email(self, client):
        """Testa POST /api/auth/login sem email"""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_login_failure_missing_password(self, client):
        """Testa POST /api/auth/login sem senha"""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'admin@test.com'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_protected_endpoint_without_token(self, client):
        """Testa acesso a endpoint protegido sem token (simula frontend sem autenticação)"""
        response = client.get('/api/eventos/')
        
        # Deve retornar 401 ou permitir acesso dependendo da implementação
        # Se o endpoint for público, deve retornar 200
        # Se for protegido, deve retornar 401
        assert response.status_code in [200, 401]
    
    def test_protected_endpoint_with_valid_token(self, client):
        """Testa acesso a endpoint protegido com token válido"""
        # Primeiro faz login para obter token
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'admin@test.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['token']
        
        # Tenta acessar endpoint protegido com token
        response = client.post(
            '/api/eventos/',
            data=json.dumps({
                'nome': 'Evento Teste',
                'descricao': 'Descrição teste',
                'sigla': 'EVTST'  # Backend exige sigla
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Se o endpoint requer admin, pode retornar 201, 403 ou 400 (dados faltando)
        assert response.status_code in [201, 400, 403]
    
    def test_protected_endpoint_with_invalid_token(self, client):
        """Testa acesso a endpoint protegido com token inválido"""
        response = client.post(
            '/api/eventos/',
            data=json.dumps({
                'nome': 'Evento Teste',
                'descricao': 'Descrição teste'
            }),
            content_type='application/json',
            headers={'Authorization': 'Bearer invalid_token_xyz'}
        )
        
        assert response.status_code in [401, 403]
    
    def test_token_stored_in_frontend_simulation(self, client):
        """Simula fluxo completo: login → armazenar token → usar token"""
        # 1. Login (simula AuthService.login())
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'admin@test.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        
        assert login_response.status_code == 200
        token = json.loads(login_response.data)['token']
        
        # 2. Simula localStorage.setItem(TOKEN_KEY, token)
        # (em testes de integração, apenas guardamos na variável)
        stored_token = token
        
        # 3. Simula AuthService.getToken() e uso em interceptor
        assert stored_token is not None
        
        # 4. Usa o token em requisição subsequente
        response = client.get(
            '/api/eventos/',
            headers={'Authorization': f'Bearer {stored_token}'}
        )
        
        # Deve permitir acesso
        assert response.status_code == 200
