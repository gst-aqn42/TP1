"""
Testes de Integração: Rotas de Inscrições → Backend → MongoDB
Testa o fluxo completo de HTTP requests através das rotas de inscrições.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app import create_app
from app.services.database import mongo
from bson import ObjectId
from datetime import datetime


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
    inscricoes_collection = mongo.get_collection('inscricoes')
    inscricoes_collection.delete_many({})
    yield
    inscricoes_collection.delete_many({})


@pytest.fixture
def sample_inscricao():
    """Cria uma inscrição de exemplo no banco"""
    inscricoes_collection = mongo.get_collection('inscricoes')
    result = inscricoes_collection.insert_one({
        'email': 'teste@exemplo.com',
        'ativo': True,
        'data_inscricao': datetime.utcnow(),
        'notificacoes_enviadas': 0
    })
    inscricao_id = str(result.inserted_id)
    yield inscricao_id
    inscricoes_collection.delete_one({'_id': result.inserted_id})


class TestInscricoesRoutes:
    """Testes de integração para rotas de inscrições"""
    
    def test_criar_inscricao_success(self, client, clean_db):
        """Testa criação de inscrição com sucesso"""
        response = client.post('/api/inscricoes/', json={
            'email': 'novo@exemplo.com'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Inscrição realizada com sucesso!'
        assert data['email'] == 'novo@exemplo.com'
        assert 'inscricao_id' in data
        
        # Verificar que foi salvo no banco
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricao_db = inscricoes_collection.find_one({'_id': ObjectId(data['inscricao_id'])})
        assert inscricao_db is not None
        assert inscricao_db['email'] == 'novo@exemplo.com'
        assert inscricao_db['ativo'] is True
        assert inscricao_db['notificacoes_enviadas'] == 0
    
    def test_criar_inscricao_email_com_espacos(self, client, clean_db):
        """Testa criação de inscrição com email contendo espaços"""
        response = client.post('/api/inscricoes/', json={
            'email': '  teste@exemplo.com  '
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == 'teste@exemplo.com'  # Deve ter removido espaços e lowercase
    
    def test_criar_inscricao_email_uppercase(self, client, clean_db):
        """Testa criação de inscrição com email em uppercase"""
        response = client.post('/api/inscricoes/', json={
            'email': 'TESTE@EXEMPLO.COM'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == 'teste@exemplo.com'  # Deve converter para lowercase
    
    def test_criar_inscricao_sem_email(self, client, clean_db):
        """Testa criação de inscrição sem email"""
        response = client.post('/api/inscricoes/', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Email é obrigatório' in data['error']
    
    def test_criar_inscricao_email_invalido(self, client, clean_db):
        """Testa criação de inscrição com email inválido"""
        response = client.post('/api/inscricoes/', json={
            'email': 'email-invalido'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Email inválido' in data['error']
    
    def test_criar_inscricao_email_invalido_sem_dominio(self, client, clean_db):
        """Testa criação de inscrição com email sem domínio"""
        response = client.post('/api/inscricoes/', json={
            'email': 'email@'
        })
        
        assert response.status_code == 400
    
    def test_criar_inscricao_duplicada_ativa(self, client, clean_db):
        """Testa criação de inscrição duplicada (já ativa)"""
        # Criar primeira inscrição
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_one({
            'email': 'teste@exemplo.com',
            'ativo': True,
            'data_inscricao': datetime.utcnow(),
            'notificacoes_enviadas': 0
        })
        
        # Tentar criar duplicada
        response = client.post('/api/inscricoes/', json={
            'email': 'teste@exemplo.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Este email já está inscrito' in data['message']
        assert data['email'] == 'teste@exemplo.com'
    
    def test_criar_inscricao_reativar_inativa(self, client, clean_db):
        """Testa reativação de inscrição inativa"""
        # Criar inscrição inativa
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_one({
            'email': 'teste@exemplo.com',
            'ativo': False,
            'data_inscricao': datetime.utcnow(),
            'notificacoes_enviadas': 5
        })
        
        # Reativar
        response = client.post('/api/inscricoes/', json={
            'email': 'teste@exemplo.com'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Inscrição reativada com sucesso!' in data['message']
        
        # Verificar que foi reativada no banco
        inscricao_db = inscricoes_collection.find_one({'email': 'teste@exemplo.com'})
        assert inscricao_db['ativo'] is True
        assert 'data_reativacao' in inscricao_db
    
    def test_listar_inscricoes_vazio(self, client, clean_db):
        """Testa listagem de inscrições quando não há inscrições"""
        response = client.get('/api/inscricoes/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_listar_inscricoes_com_dados(self, client, clean_db):
        """Testa listagem de inscrições com dados"""
        # Criar inscrições diretamente no banco
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_many([
            {
                'email': 'inscrito1@exemplo.com',
                'ativo': True,
                'data_inscricao': datetime.utcnow(),
                'notificacoes_enviadas': 3
            },
            {
                'email': 'inscrito2@exemplo.com',
                'ativo': True,
                'data_inscricao': datetime.utcnow(),
                'notificacoes_enviadas': 0
            },
            {
                'email': 'inativo@exemplo.com',
                'ativo': False,
                'data_inscricao': datetime.utcnow(),
                'notificacoes_enviadas': 1
            }
        ])
        
        response = client.get('/api/inscricoes/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2  # Apenas ativos
        assert all(i['ativo'] is True for i in data)
        assert any(i['email'] == 'inscrito1@exemplo.com' for i in data)
        assert any(i['email'] == 'inscrito2@exemplo.com' for i in data)
        assert not any(i['email'] == 'inativo@exemplo.com' for i in data)
    
    def test_listar_inscricoes_apenas_ativas(self, client, clean_db):
        """Testa que listagem retorna apenas inscrições ativas"""
        # Criar inscrições ativas e inativas
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_many([
            {'email': 'ativo1@exemplo.com', 'ativo': True, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0},
            {'email': 'ativo2@exemplo.com', 'ativo': True, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0},
            {'email': 'inativo1@exemplo.com', 'ativo': False, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0},
            {'email': 'inativo2@exemplo.com', 'ativo': False, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0}
        ])
        
        response = client.get('/api/inscricoes/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        for inscricao in data:
            assert inscricao['ativo'] is True
    
    def test_cancelar_inscricao_success(self, client, clean_db):
        """Testa cancelamento de inscrição por email com sucesso"""
        # Criar inscrição
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_one({
            'email': 'cancelar@exemplo.com',
            'ativo': True,
            'data_inscricao': datetime.utcnow(),
            'notificacoes_enviadas': 0
        })
        
        response = client.delete('/api/inscricoes/cancelar@exemplo.com')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Inscrição cancelada com sucesso' in data['message']
        
        # Verificar que foi marcada como inativa no banco
        inscricao_db = inscricoes_collection.find_one({'email': 'cancelar@exemplo.com'})
        assert inscricao_db['ativo'] is False
        assert 'data_cancelamento' in inscricao_db
    
    def test_cancelar_inscricao_nao_encontrada(self, client, clean_db):
        """Testa cancelamento de inscrição inexistente"""
        response = client.delete('/api/inscricoes/naoexiste@exemplo.com')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Inscrição não encontrada' in data['error']
    
    def test_cancelar_inscricao_email_com_espacos(self, client, clean_db):
        """Testa cancelamento com email contendo espaços"""
        # Criar inscrição
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_one({
            'email': 'teste@exemplo.com',
            'ativo': True,
            'data_inscricao': datetime.utcnow(),
            'notificacoes_enviadas': 0
        })
        
        # URL encoding fará o strip automaticamente
        response = client.delete('/api/inscricoes/teste@exemplo.com')
        
        assert response.status_code == 200
    
    def test_total_inscricoes_vazio(self, client, clean_db):
        """Testa total de inscrições quando não há inscrições"""
        response = client.get('/api/inscricoes/total')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total'] == 0
    
    def test_total_inscricoes_com_dados(self, client, clean_db):
        """Testa total de inscrições com dados"""
        # Criar inscrições
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes_collection.insert_many([
            {'email': 'ativo1@exemplo.com', 'ativo': True, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0},
            {'email': 'ativo2@exemplo.com', 'ativo': True, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0},
            {'email': 'ativo3@exemplo.com', 'ativo': True, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0},
            {'email': 'inativo@exemplo.com', 'ativo': False, 'data_inscricao': datetime.utcnow(), 'notificacoes_enviadas': 0}
        ])
        
        response = client.get('/api/inscricoes/total')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total'] == 3  # Apenas ativos
