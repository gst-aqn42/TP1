"""
Testes de Integração: Rotas de Artigos → Backend → MongoDB
Testa o fluxo completo de HTTP requests através das rotas de artigos.
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
    artigos_collection = mongo.get_collection('artigos')
    eventos_collection = mongo.get_collection('eventos')
    edicoes_collection = mongo.get_collection('edicoes')
    artigos_collection.delete_many({})
    eventos_collection.delete_many({})
    edicoes_collection.delete_many({})
    yield
    artigos_collection.delete_many({})
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
def sample_edicao():
    """Cria uma edição de exemplo no banco"""
    eventos_collection = mongo.get_collection('eventos')
    edicoes_collection = mongo.get_collection('edicoes')
    
    # Criar evento
    evento_result = eventos_collection.insert_one({
        'nome': 'SBES',
        'sigla': 'SBES',
        'descricao': 'Simpósio Brasileiro'
    })
    
    # Criar edição
    edicao_result = edicoes_collection.insert_one({
        'evento_id': str(evento_result.inserted_id),
        'ano': 2024,
        'local': 'Brasília',
        'data_inicio': '2024-09-01',
        'data_fim': '2024-09-05'
    })
    
    edicao_id = str(edicao_result.inserted_id)
    yield edicao_id
    
    eventos_collection.delete_one({'_id': evento_result.inserted_id})
    edicoes_collection.delete_one({'_id': edicao_result.inserted_id})


@pytest.fixture
def sample_artigo(sample_edicao):
    """Cria um artigo de exemplo no banco"""
    artigos_collection = mongo.get_collection('artigos')
    result = artigos_collection.insert_one({
        'titulo': 'Artigo de Teste',
        'autores': [
            {'nome': 'João Silva', 'email': 'joao@exemplo.com'},
            {'nome': 'Maria Santos', 'email': 'maria@exemplo.com'}
        ],
        'edicao_id': sample_edicao,
        'resumo': 'Este é um resumo de teste',
        'keywords': ['teste', 'integração', 'software']
    })
    artigo_id = str(result.inserted_id)
    yield artigo_id
    artigos_collection.delete_one({'_id': result.inserted_id})


class TestArtigosRoutes:
    """Testes de integração para rotas de artigos"""
    
    def test_listar_artigos_edicao_vazio(self, client, clean_db, sample_edicao):
        """Testa listagem de artigos quando não há artigos na edição"""
        response = client.get(f'/api/artigos/edicao/{sample_edicao}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_listar_artigos_edicao_com_dados(self, client, clean_db, sample_edicao):
        """Testa listagem de artigos com dados"""
        # Criar artigos diretamente no banco
        artigos_collection = mongo.get_collection('artigos')
        artigos_collection.insert_many([
            {
                'titulo': 'Artigo 1',
                'autores': [{'nome': 'Autor 1', 'email': 'autor1@exemplo.com'}],
                'edicao_id': sample_edicao,
                'resumo': 'Resumo 1',
                'keywords': ['keyword1']
            },
            {
                'titulo': 'Artigo 2',
                'autores': [{'nome': 'Autor 2', 'email': 'autor2@exemplo.com'}],
                'edicao_id': sample_edicao,
                'resumo': 'Resumo 2',
                'keywords': ['keyword2']
            }
        ])
        
        response = client.get(f'/api/artigos/edicao/{sample_edicao}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['titulo'] == 'Artigo 1'
        assert data[1]['titulo'] == 'Artigo 2'
    
    def test_criar_artigo_success(self, client, clean_db, sample_edicao, admin_token):
        """Testa criação de artigo com sucesso"""
        response = client.post('/api/artigos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'titulo': 'Novo Artigo de Teste',
                'autores': [
                    {'nome': 'Autor Teste', 'email': 'autor@exemplo.com'}
                ],
                'edicao_id': sample_edicao,
                'resumo': 'Este é um resumo completo do artigo',
                'keywords': ['teste', 'tdd', 'python']
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Artigo criado com sucesso'
        assert 'artigo_id' in data
        
        # Verificar que foi salvo no banco
        artigos_collection = mongo.get_collection('artigos')
        artigo_db = artigos_collection.find_one({'_id': ObjectId(data['artigo_id'])})
        assert artigo_db is not None
        assert artigo_db['titulo'] == 'Novo Artigo de Teste'
        assert len(artigo_db['autores']) == 1
        assert artigo_db['autores'][0]['nome'] == 'Autor Teste'
    
    def test_criar_artigo_sem_titulo(self, client, clean_db, sample_edicao, admin_token):
        """Testa criação de artigo sem título"""
        response = client.post('/api/artigos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'autores': [{'nome': 'Autor', 'email': 'autor@exemplo.com'}],
                'edicao_id': sample_edicao
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'titulo e edicao_id são obrigatórios' in data['error']
    
    def test_criar_artigo_sem_edicao_id(self, client, clean_db, admin_token):
        """Testa criação de artigo sem edicao_id"""
        response = client.post('/api/artigos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'titulo': 'Artigo Sem Edição',
                'autores': [{'nome': 'Autor', 'email': 'autor@exemplo.com'}]
            }
        )
        
        assert response.status_code == 400
    
    def test_criar_artigo_sem_autorizacao(self, client, clean_db, sample_edicao):
        """Testa criação de artigo sem token"""
        response = client.post('/api/artigos/', json={
            'titulo': 'Artigo Teste',
            'edicao_id': sample_edicao
        })
        
        assert response.status_code == 401
    
    def test_criar_artigo_com_autores_vazios(self, client, clean_db, sample_edicao, admin_token):
        """Testa criação de artigo com lista de autores vazia"""
        response = client.post('/api/artigos/', 
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'titulo': 'Artigo Sem Autores',
                'autores': [],
                'edicao_id': sample_edicao,
                'resumo': 'Resumo',
                'keywords': ['teste']
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Verificar no banco
        artigos_collection = mongo.get_collection('artigos')
        artigo_db = artigos_collection.find_one({'_id': ObjectId(data['artigo_id'])})
        assert len(artigo_db['autores']) == 0
    
    def test_obter_artigo_success(self, client, sample_artigo):
        """Testa obter um artigo específico"""
        response = client.get(f'/api/artigos/{sample_artigo}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['_id'] == sample_artigo
        assert data['titulo'] == 'Artigo de Teste'
        assert len(data['autores']) == 2
        assert data['resumo'] == 'Este é um resumo de teste'
    
    def test_obter_artigo_nao_encontrado(self, client, clean_db):
        """Testa obter artigo inexistente"""
        fake_id = str(ObjectId())
        response = client.get(f'/api/artigos/{fake_id}')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Artigo não encontrado' in data['error']
    
    def test_atualizar_artigo_success(self, client, sample_artigo, admin_token):
        """Testa atualização de artigo com sucesso"""
        response = client.put(f'/api/artigos/{sample_artigo}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'titulo': 'Título Atualizado',
                'resumo': 'Resumo atualizado'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Artigo atualizado com sucesso'
        
        # Verificar atualização no banco
        artigos_collection = mongo.get_collection('artigos')
        artigo_db = artigos_collection.find_one({'_id': ObjectId(sample_artigo)})
        assert artigo_db['titulo'] == 'Título Atualizado'
        assert artigo_db['resumo'] == 'Resumo atualizado'
    
    def test_atualizar_artigo_keywords(self, client, sample_artigo, admin_token):
        """Testa atualização de keywords do artigo"""
        response = client.put(f'/api/artigos/{sample_artigo}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'keywords': ['nova', 'keywords', 'atualizadas']
            }
        )
        
        assert response.status_code == 200
        
        # Verificar no banco
        artigos_collection = mongo.get_collection('artigos')
        artigo_db = artigos_collection.find_one({'_id': ObjectId(sample_artigo)})
        assert artigo_db['keywords'] == ['nova', 'keywords', 'atualizadas']
    
    def test_atualizar_artigo_nao_encontrado(self, client, clean_db, admin_token):
        """Testa atualização de artigo inexistente"""
        fake_id = str(ObjectId())
        response = client.put(f'/api/artigos/{fake_id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'titulo': 'Novo Título'}
        )
        
        assert response.status_code == 404
    
    def test_atualizar_artigo_sem_dados(self, client, sample_artigo, admin_token):
        """Testa atualização sem dados"""
        response = client.put(f'/api/artigos/{sample_artigo}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={}
        )
        
        assert response.status_code == 400
    
    def test_atualizar_artigo_sem_autorizacao(self, client, sample_artigo):
        """Testa atualização sem token"""
        response = client.put(f'/api/artigos/{sample_artigo}',
            json={'titulo': 'Novo Título'}
        )
        
        assert response.status_code == 401
    
    def test_deletar_artigo_success(self, client, sample_artigo, admin_token):
        """Testa deleção de artigo com sucesso"""
        response = client.delete(f'/api/artigos/{sample_artigo}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'deletado com sucesso' in data['message']
        
        # Verificar que foi removido do banco
        artigos_collection = mongo.get_collection('artigos')
        artigo_db = artigos_collection.find_one({'_id': ObjectId(sample_artigo)})
        assert artigo_db is None
    
    def test_deletar_artigo_nao_encontrado(self, client, clean_db, admin_token):
        """Testa deleção de artigo inexistente"""
        fake_id = str(ObjectId())
        response = client.delete(f'/api/artigos/{fake_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 404
    
    def test_deletar_artigo_sem_autorizacao(self, client, sample_artigo):
        """Testa deleção sem token"""
        response = client.delete(f'/api/artigos/{sample_artigo}')
        
        assert response.status_code == 401
    
    def test_buscar_artigos_por_titulo(self, client, clean_db, sample_artigo):
        """Testa busca de artigos por título"""
        response = client.get('/api/artigos/busca?q=Teste&tipo=titulo')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'resultados' in data
        assert data['total'] >= 1
        assert any('Teste' in r['titulo'] for r in data['resultados'])
    
    def test_buscar_artigos_por_autor(self, client, clean_db, sample_artigo):
        """Testa busca de artigos por autor"""
        response = client.get('/api/artigos/busca?q=Silva&tipo=autor')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'resultados' in data
        assert data['total'] >= 1
    
    def test_buscar_artigos_sem_parametro(self, client):
        """Testa busca sem parâmetro de busca"""
        response = client.get('/api/artigos/busca')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Parâmetro de busca (q) é obrigatório' in data['error']
    
    def test_buscar_artigos_tipo_tudo(self, client, clean_db, sample_artigo):
        """Testa busca de artigos com tipo 'tudo'"""
        response = client.get('/api/artigos/busca?q=Teste&tipo=tudo')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'resultados' in data
        assert 'query' in data
        assert data['query'] == 'Teste'
        assert data['tipo'] == 'tudo'
    
    def test_buscar_artigos_nenhum_resultado(self, client, clean_db):
        """Testa busca de artigos sem resultados"""
        response = client.get('/api/artigos/busca?q=PalavraQueNaoExiste123&tipo=titulo')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total'] == 0
        assert len(data['resultados']) == 0
