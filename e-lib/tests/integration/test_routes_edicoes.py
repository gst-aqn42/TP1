"""
Testes de Integração: Rotas de Edições → Backend → MongoDB
Testa o fluxo completo de HTTP requests através das rotas de edições.
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
    edicoes_collection = mongo.get_collection('edicoes')
    eventos_collection.delete_many({})
    edicoes_collection.delete_many({})
    yield
    eventos_collection.delete_many({})
    edicoes_collection.delete_many({})


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
def sample_evento():
    """Cria um evento de exemplo no banco"""
    eventos_collection = mongo.get_collection('eventos')
    result = eventos_collection.insert_one({
        'nome': 'SBES',
        'sigla': 'SBES',
        'descricao': 'Simpósio Brasileiro'
    })
    evento_id = str(result.inserted_id)
    yield evento_id
    eventos_collection.delete_one({'_id': result.inserted_id})


@pytest.fixture
def sample_edicao(sample_evento):
    """Cria uma edição de exemplo no banco"""
    edicoes_collection = mongo.get_collection('edicoes')
    result = edicoes_collection.insert_one({
        'evento_id': sample_evento,
        'ano': 2024,
        'local': 'Brasília',
        'data_inicio': '2024-09-01',
        'data_fim': '2024-09-05'
    })
    edicao_id = str(result.inserted_id)
    yield edicao_id
    edicoes_collection.delete_one({'_id': result.inserted_id})


class TestEdicoesRoutes:
    """Testes de integração para rotas de edições"""
    
    def test_listar_edicoes_evento_vazio(self, client, clean_db, sample_evento):
        """Testa listagem de edições quando não há edições"""
        response = client.get(f'/api/edicoes/evento/{sample_evento}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_listar_edicoes_evento_com_dados(self, client, clean_db, sample_evento):
        """Testa listagem de edições com dados"""
        # Criar edições diretamente no banco
        edicoes_collection = mongo.get_collection('edicoes')
        edicoes_collection.insert_many([
            {
                'evento_id': sample_evento,
                'ano': 2023,
                'local': 'São Paulo',
                'data_inicio': '2023-09-01',
                'data_fim': '2023-09-05'
            },
            {
                'evento_id': sample_evento,
                'ano': 2024,
                'local': 'Rio de Janeiro',
                'data_inicio': '2024-09-01',
                'data_fim': '2024-09-05'
            }
        ])
        
        response = client.get(f'/api/edicoes/evento/{sample_evento}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['ano'] == 2023
        assert data[1]['ano'] == 2024
    
    def test_criar_edicao_success(self, client, clean_db, sample_evento, admin_token):
        """Testa criação de edição com sucesso"""
        response = client.post('/api/edicoes/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'evento_id': sample_evento,
                'ano': 2025,
                'local': 'Curitiba',
                'data_inicio': '2025-09-10',
                'data_fim': '2025-09-15'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Edição criada com sucesso'
        assert 'edicao_id' in data
        
        # Verificar que foi salvo no banco
        edicoes_collection = mongo.get_collection('edicoes')
        edicao_db = edicoes_collection.find_one({'_id': ObjectId(data['edicao_id'])})
        assert edicao_db is not None
        assert edicao_db['ano'] == 2025
        assert edicao_db['local'] == 'Curitiba'
        assert edicao_db['evento_id'] == sample_evento
    
    def test_criar_edicao_sem_campos_opcionais(self, client, clean_db, sample_evento, admin_token):
        """Testa criação de edição apenas com campos obrigatórios"""
        response = client.post('/api/edicoes/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'evento_id': sample_evento,
                'ano': 2025
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Verificar no banco
        edicoes_collection = mongo.get_collection('edicoes')
        edicao_db = edicoes_collection.find_one({'_id': ObjectId(data['edicao_id'])})
        assert edicao_db['local'] is None
        assert edicao_db['data_inicio'] is None
        assert edicao_db['data_fim'] is None
    
    def test_criar_edicao_sem_evento_id(self, client, clean_db, admin_token):
        """Testa criação de edição sem evento_id"""
        response = client.post('/api/edicoes/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'ano': 2025
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'evento_id e ano são obrigatórios' in data['error']
    
    def test_criar_edicao_sem_ano(self, client, clean_db, sample_evento, admin_token):
        """Testa criação de edição sem ano"""
        response = client.post('/api/edicoes/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'evento_id': sample_evento
            }
        )
        
        assert response.status_code == 400
    
    def test_criar_edicao_sem_autorizacao(self, client, clean_db, sample_evento):
        """Testa criação de edição sem token"""
        response = client.post('/api/edicoes/', json={
            'evento_id': sample_evento,
            'ano': 2025
        })
        
        assert response.status_code == 401
    
    def test_obter_edicao_success(self, client, sample_edicao):
        """Testa obter uma edição específica"""
        response = client.get(f'/api/edicoes/{sample_edicao}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['_id'] == sample_edicao
        assert data['ano'] == 2024
        assert data['local'] == 'Brasília'
    
    def test_obter_edicao_nao_encontrada(self, client, clean_db):
        """Testa obter edição inexistente"""
        fake_id = str(ObjectId())
        response = client.get(f'/api/edicoes/{fake_id}')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Edição não encontrada' in data['error']
    
    def test_atualizar_edicao_success(self, client, sample_edicao, admin_token):
        """Testa atualização de edição com sucesso"""
        response = client.put(f'/api/edicoes/{sample_edicao}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'local': 'Salvador',
                'data_inicio': '2024-10-01'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Edição atualizada com sucesso'
        
        # Verificar atualização no banco
        edicoes_collection = mongo.get_collection('edicoes')
        edicao_db = edicoes_collection.find_one({'_id': ObjectId(sample_edicao)})
        assert edicao_db['local'] == 'Salvador'
        assert edicao_db['data_inicio'] == '2024-10-01'
        assert edicao_db['ano'] == 2024  # Não alterado
    
    def test_atualizar_edicao_ano(self, client, sample_edicao, admin_token):
        """Testa atualização do ano da edição"""
        response = client.put(f'/api/edicoes/{sample_edicao}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'ano': 2025
            }
        )
        
        assert response.status_code == 200
        
        # Verificar no banco
        edicoes_collection = mongo.get_collection('edicoes')
        edicao_db = edicoes_collection.find_one({'_id': ObjectId(sample_edicao)})
        assert edicao_db['ano'] == 2025
    
    def test_atualizar_edicao_nao_encontrada(self, client, clean_db, admin_token):
        """Testa atualização de edição inexistente"""
        fake_id = str(ObjectId())
        response = client.put(f'/api/edicoes/{fake_id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'ano': 2026}
        )
        
        assert response.status_code == 404
    
    def test_atualizar_edicao_sem_dados(self, client, sample_edicao, admin_token):
        """Testa atualização sem dados"""
        response = client.put(f'/api/edicoes/{sample_edicao}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={}
        )
        
        assert response.status_code == 400
    
    def test_atualizar_edicao_sem_autorizacao(self, client, sample_edicao):
        """Testa atualização sem token"""
        response = client.put(f'/api/edicoes/{sample_edicao}',
            json={'ano': 2026}
        )
        
        assert response.status_code == 401
    
    def test_deletar_edicao_success(self, client, sample_edicao, admin_token):
        """Testa deleção de edição com sucesso"""
        response = client.delete(f'/api/edicoes/{sample_edicao}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'deletada com sucesso' in data['message']
        
        # Verificar que foi removido do banco
        edicoes_collection = mongo.get_collection('edicoes')
        edicao_db = edicoes_collection.find_one({'_id': ObjectId(sample_edicao)})
        assert edicao_db is None
    
    def test_deletar_edicao_nao_encontrada(self, client, clean_db, admin_token):
        """Testa deleção de edição inexistente"""
        fake_id = str(ObjectId())
        response = client.delete(f'/api/edicoes/{fake_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 404
    
    def test_deletar_edicao_sem_autorizacao(self, client, sample_edicao):
        """Testa deleção sem token"""
        response = client.delete(f'/api/edicoes/{sample_edicao}')
        
        assert response.status_code == 401
