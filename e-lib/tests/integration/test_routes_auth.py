"""
Testes de Integração: Rotas de Autenticação → Backend → MongoDB
Testa o fluxo completo de HTTP requests através das rotas de autenticação.
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
    usuarios_collection = mongo.get_collection('usuarios')
    usuarios_collection.delete_many({})
    yield
    usuarios_collection.delete_many({})


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


class TestAuthRoutes:
    """Testes de integração para rotas de autenticação"""
    
    def test_register_success(self, client, clean_db):
        """Testa registro de novo usuário com sucesso"""
        response = client.post('/api/auth/register', json={
            'email': 'teste@exemplo.com',
            'nome': 'Usuário Teste'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Usuário criado com sucesso'
        assert 'token' in data
        assert data['user']['email'] == 'teste@exemplo.com'
        assert data['user']['nome'] == 'Usuário Teste'
        assert data['user']['is_admin'] is False
        
        # Verificar que foi salvo no banco
        usuarios_collection = mongo.get_collection('usuarios')
        usuario_db = usuarios_collection.find_one({'email': 'teste@exemplo.com'})
        assert usuario_db is not None
        assert usuario_db['nome'] == 'Usuário Teste'
    
    def test_register_admin(self, client, clean_db):
        """Testa registro de usuário admin"""
        response = client.post('/api/auth/register', json={
            'email': 'admin@exemplo.com',
            'nome': 'Admin Teste',
            'is_admin': True
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['is_admin'] is True
        
        # Verificar no banco
        usuarios_collection = mongo.get_collection('usuarios')
        usuario_db = usuarios_collection.find_one({'email': 'admin@exemplo.com'})
        assert usuario_db['is_admin'] is True
    
    def test_register_missing_email(self, client, clean_db):
        """Testa registro sem email"""
        response = client.post('/api/auth/register', json={
            'nome': 'Usuário Teste'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Email e nome são obrigatórios' in data['error']
    
    def test_register_missing_nome(self, client, clean_db):
        """Testa registro sem nome"""
        response = client.post('/api/auth/register', json={
            'email': 'teste@exemplo.com'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_duplicate_user(self, client, clean_db):
        """Testa registro de usuário duplicado"""
        # Primeiro registro
        client.post('/api/auth/register', json={
            'email': 'teste@exemplo.com',
            'nome': 'Usuário Teste'
        })
        
        # Segundo registro com mesmo email
        response = client.post('/api/auth/register', json={
            'email': 'teste@exemplo.com',
            'nome': 'Outro Usuário'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'Usuário já existe' in data['error']
    
    def test_login_success(self, client, clean_db):
        """Testa login com sucesso"""
        # Criar usuário diretamente no banco
        usuarios_collection = mongo.get_collection('usuarios')
        usuarios_collection.insert_one({
            'email': 'admin@admin.com',
            'nome': 'Admin',
            'senha': 'admin123',
            'is_admin': True
        })
        
        response = client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Login realizado com sucesso'
        assert 'token' in data
        assert data['user']['email'] == 'admin@admin.com'
        assert data['user']['is_admin'] is True
    
    def test_login_with_email(self, client, clean_db):
        """Testa login usando email completo"""
        usuarios_collection = mongo.get_collection('usuarios')
        usuarios_collection.insert_one({
            'email': 'teste@exemplo.com',
            'nome': 'Teste',
            'senha': 'senha123',
            'is_admin': False
        })
        
        response = client.post('/api/auth/login', json={
            'email': 'teste@exemplo.com',
            'password': 'senha123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
    
    def test_login_user_not_found(self, client, clean_db):
        """Testa login com usuário inexistente"""
        response = client.post('/api/auth/login', json={
            'username': 'naoexiste@exemplo.com',
            'password': 'senha123'
        })
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Usuário não encontrado' in data['error']
    
    def test_login_wrong_password(self, client, clean_db):
        """Testa login com senha incorreta"""
        usuarios_collection = mongo.get_collection('usuarios')
        usuarios_collection.insert_one({
            'email': 'teste@exemplo.com',
            'nome': 'Teste',
            'senha': 'senha123',
            'is_admin': False
        })
        
        response = client.post('/api/auth/login', json={
            'username': 'teste@exemplo.com',
            'password': 'senhaerrada'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Senha incorreta' in data['error']
    
    def test_login_missing_credentials(self, client, clean_db):
        """Testa login sem credenciais"""
        response = client.post('/api/auth/login', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_get_me_success(self, client, user_token):
        """Testa obter informações do usuário autenticado"""
        response = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {user_token}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'user_id' in data
        assert 'is_admin' in data
        assert data['is_admin'] is False
    
    def test_get_me_no_token(self, client):
        """Testa obter informações sem token"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
    
    def test_get_me_invalid_token(self, client):
        """Testa obter informações com token inválido"""
        response = client.get('/api/auth/me', headers={
            'Authorization': 'Bearer token-invalido'
        })
        
        assert response.status_code == 401
    
    def test_admin_test_with_admin_token(self, client, admin_token):
        """Testa rota admin com token de admin"""
        response = client.get('/api/auth/admin-test', headers={
            'Authorization': f'Bearer {admin_token}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Acesso admin autorizado!' in data['message']
    
    def test_admin_test_with_user_token(self, client, user_token):
        """Testa rota admin com token de usuário comum"""
        response = client.get('/api/auth/admin-test', headers={
            'Authorization': f'Bearer {user_token}'
        })
        
        assert response.status_code == 403
    
    def test_admin_test_no_token(self, client):
        """Testa rota admin sem token"""
        response = client.get('/api/auth/admin-test')
        
        assert response.status_code == 401
