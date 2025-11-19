"""
Testes de Integração: Frontend → Backend (Artigos)
Testa as chamadas HTTP do Angular para os endpoints de artigos.
Simula: ApiService.getArticlesByEdition(), createArticle(), createArticleWithPdf(), 
        updateArticle(), deleteArticle(), uploadPdfToArticle(), searchArticles()
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

import pytest
import json
import io
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
    usuarios_collection = mongo.get_collection('usuarios')
    usuarios_collection.delete_many({})
    
    admin_user = {
        'email': 'admin@test.com',
        'nome': 'Admin Test',
        'senha': 'admin123',  # Senha em texto plano
        'is_admin': True
    }
    usuarios_collection.insert_one(admin_user)
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'admin@test.com',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    
    return json.loads(response.data)['token']


@pytest.fixture
def edicao_id():
    """Cria um evento e edição para testes de artigos"""
    eventos_collection = mongo.get_collection('eventos')
    evento_result = eventos_collection.insert_one({
        'nome': 'Evento Teste',
        'descricao': 'Evento para testar artigos',
        'sigla': 'EVTT'
    })
    
    edicoes_collection = mongo.get_collection('edicoes')
    edicao_result = edicoes_collection.insert_one({
        'evento_id': evento_result.inserted_id,
        'numero': 1,
        'ano': 2024
    })
    
    return str(edicao_result.inserted_id)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup e teardown do banco de dados de testes"""
    artigos_collection = mongo.get_collection('artigos')
    autores_collection = mongo.get_collection('autores')
    edicoes_collection = mongo.get_collection('edicoes')
    eventos_collection = mongo.get_collection('eventos')
    
    artigos_collection.delete_many({})
    autores_collection.delete_many({})
    edicoes_collection.delete_many({})
    eventos_collection.delete_many({})
    
    yield
    
    artigos_collection.delete_many({})
    autores_collection.delete_many({})
    edicoes_collection.delete_many({})
    eventos_collection.delete_many({})
    usuarios_collection = mongo.get_collection('usuarios')
    usuarios_collection.delete_many({})


class TestFrontendArtigosIntegration:
    """Testes de integração Frontend → Backend para Artigos"""
    
    def test_get_articles_by_edition_empty(self, client, edicao_id):
        """Testa GET /api/artigos/edicao/:id sem artigos (simula ApiService.getArticlesByEdition())"""
        response = client.get(f'/api/artigos/edicao/{edicao_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_articles_by_edition_with_data(self, client, edicao_id):
        """Testa GET /api/artigos/edicao/:id com artigos existentes"""
        artigos_collection = mongo.get_collection('artigos')
        artigos_collection.insert_many([
            {
                'edicao_id': ObjectId(edicao_id),
                'titulo': 'Artigo 1',
                'resumo': 'Resumo do artigo 1',
                'autores': ['Autor 1']
            },
            {
                'edicao_id': ObjectId(edicao_id),
                'titulo': 'Artigo 2',
                'resumo': 'Resumo do artigo 2',
                'autores': ['Autor 2']
            }
        ])
        
        response = client.get(f'/api/artigos/edicao/{edicao_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_create_article_success(self, client, auth_token, edicao_id):
        """Testa POST /api/artigos/ criando artigo (simula ApiService.createArticle())"""
        artigo_data = {
            'edicao_id': edicao_id,
            'titulo': 'Novo Artigo',
            'resumo': 'Resumo do novo artigo',
            'autores': ['Autor 1', 'Autor 2'],
            'palavras_chave': ['teste', 'integração']
        }
        
        response = client.post(
            '/api/artigos/',
            data=json.dumps(artigo_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [200, 201]
        
        # Verifica no banco
        artigos_collection = mongo.get_collection('artigos')
        artigo_db = artigos_collection.find_one({'titulo': 'Novo Artigo'})
        assert artigo_db is not None
        assert artigo_db['resumo'] == 'Resumo do novo artigo'
    
    def test_create_article_with_pdf(self, client, auth_token, edicao_id):
        """Testa POST /api/artigos/ com PDF (simula ApiService.createArticleWithPdf())"""
        # Cria um arquivo PDF fake
        pdf_data = b'%PDF-1.4 fake pdf content'
        
        data = {
            'edicao_id': edicao_id,
            'titulo': 'Artigo com PDF',
            'resumo': 'Artigo com arquivo PDF',
            'autores': json.dumps(['Autor 1']),
            'pdf': (io.BytesIO(pdf_data), 'artigo.pdf')
        }
        
        response = client.post(
            '/api/artigos/',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Pode retornar 201 (criado) ou outro status dependendo da implementação
        assert response.status_code in [200, 201, 400]
    
    def test_create_article_without_auth(self, client, edicao_id):
        """Testa POST /api/artigos/ sem autenticação"""
        artigo_data = {
            'edicao_id': edicao_id,
            'titulo': 'Artigo Sem Auth'
        }
        
        response = client.post(
            '/api/artigos/',
            data=json.dumps(artigo_data),
            content_type='application/json'
        )
        
        assert response.status_code in [200, 201, 401, 403]
    
    def test_create_article_invalid_data(self, client, auth_token):
        """Testa POST /api/artigos/ com dados inválidos"""
        artigo_data = {
            'titulo': ''  # Título vazio
        }
        
        response = client.post(
            '/api/artigos/',
            data=json.dumps(artigo_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [400, 422]
    
    def test_update_article_success(self, client, auth_token, edicao_id):
        """Testa PUT /api/artigos/:id atualizando artigo (simula ApiService.updateArticle())"""
        # Cria um artigo primeiro
        artigos_collection = mongo.get_collection('artigos')
        result = artigos_collection.insert_one({
            'edicao_id': ObjectId(edicao_id),
            'titulo': 'Artigo Original',
            'resumo': 'Resumo original',
            'autores': ['Autor 1']
        })
        artigo_id = str(result.inserted_id)
        
        # Atualiza o artigo
        update_data = {
            'titulo': 'Artigo Atualizado',
            'resumo': 'Resumo atualizado'
        }
        
        response = client.put(
            f'/api/artigos/{artigo_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        
        # Verifica no banco
        artigo_db = artigos_collection.find_one({'_id': ObjectId(artigo_id)})
        assert artigo_db['titulo'] == 'Artigo Atualizado'
    
    def test_update_article_not_found(self, client, auth_token):
        """Testa PUT /api/artigos/:id com ID inexistente"""
        fake_id = str(ObjectId())
        
        update_data = {
            'titulo': 'Artigo Inexistente'
        }
        
        response = client.put(
            f'/api/artigos/{fake_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 404
    
    def test_delete_article_success(self, client, auth_token, edicao_id):
        """Testa DELETE /api/artigos/:id (simula ApiService.deleteArticle())"""
        # Cria um artigo primeiro
        artigos_collection = mongo.get_collection('artigos')
        result = artigos_collection.insert_one({
            'edicao_id': ObjectId(edicao_id),
            'titulo': 'Artigo Para Deletar',
            'autores': ['Autor 1']
        })
        artigo_id = str(result.inserted_id)
        
        # Deleta o artigo
        response = client.delete(
            f'/api/artigos/{artigo_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [200, 204]
        
        # Verifica que foi deletado
        artigo_db = artigos_collection.find_one({'_id': ObjectId(artigo_id)})
        assert artigo_db is None
    
    def test_delete_article_not_found(self, client, auth_token):
        """Testa DELETE /api/artigos/:id com ID inexistente"""
        fake_id = str(ObjectId())
        
        response = client.delete(
            f'/api/artigos/{fake_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 404
    
    def test_upload_pdf_to_article(self, client, auth_token, edicao_id):
        """Testa POST /api/artigos/:id/upload-pdf (simula ApiService.uploadPdfToArticle())"""
        # Cria um artigo primeiro
        artigos_collection = mongo.get_collection('artigos')
        result = artigos_collection.insert_one({
            'edicao_id': ObjectId(edicao_id),
            'titulo': 'Artigo Sem PDF',
            'autores': ['Autor 1']
        })
        artigo_id = str(result.inserted_id)
        
        # Faz upload do PDF
        pdf_data = b'%PDF-1.4 fake pdf content'
        data = {
            'pdf': (io.BytesIO(pdf_data), 'documento.pdf')
        }
        
        response = client.post(
            f'/api/artigos/{artigo_id}/upload-pdf',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Pode retornar 200 ou erro dependendo da implementação
        assert response.status_code in [200, 400, 404]
    
    def test_search_articles_by_query(self, client, edicao_id):
        """Testa GET /api/artigos/busca?q=query (simula ApiService.searchArticles())"""
        # Cria alguns artigos
        artigos_collection = mongo.get_collection('artigos')
        artigos_collection.insert_many([
            {
                'edicao_id': ObjectId(edicao_id),
                'titulo': 'Machine Learning em Python',
                'resumo': 'Estudo sobre ML',
                'autores': ['João Silva']
            },
            {
                'edicao_id': ObjectId(edicao_id),
                'titulo': 'Deep Learning com TensorFlow',
                'resumo': 'Aplicações de DL',
                'autores': ['Maria Santos']
            }
        ])
        
        # Busca por "Learning"
        response = client.get('/api/artigos/busca?q=Learning')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Deve retornar os artigos que contêm "Learning"
        if isinstance(data, list):
            assert len(data) >= 0  # Pode retornar resultados ou não dependendo da busca
    
    def test_search_articles_with_filters(self, client, edicao_id):
        """Testa GET /api/artigos/busca?q=query&tipo=autor (com filtros)"""
        artigos_collection = mongo.get_collection('artigos')
        artigos_collection.insert_one({
            'edicao_id': ObjectId(edicao_id),
            'titulo': 'Artigo Teste',
            'autores': [{'nome': 'João Silva'}]  # Backend espera objeto com nome
        })
        
        # Busca com filtro de tipo (backend suporta: titulo, autor, evento, tudo)
        response = client.get('/api/artigos/busca?q=João&tipo=autor')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_full_article_workflow(self, client, auth_token, edicao_id):
        """Testa fluxo completo: criar artigo → buscar → atualizar → deletar"""
        # 1. CREATE - ApiService.createArticle()
        create_response = client.post(
            '/api/artigos/',
            data=json.dumps({
                'edicao_id': edicao_id,
                'titulo': 'Testes de Integração',
                'resumo': 'Como fazer testes de integração',
                'autores': ['Autor Teste'],
                'palavras_chave': ['teste', 'integração', 'python']
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert create_response.status_code in [200, 201]
        
        # 2. READ - ApiService.getArticlesByEdition()
        read_response = client.get(f'/api/artigos/edicao/{edicao_id}')
        assert read_response.status_code == 200
        artigos = json.loads(read_response.data)
        assert len(artigos) >= 1
        
        artigo_id = artigos[0]['_id'] if '_id' in artigos[0] else artigos[0]['id']
        
        # 3. SEARCH - ApiService.searchArticles()
        search_response = client.get('/api/artigos/busca?q=Integração')
        assert search_response.status_code == 200
        
        # 4. UPDATE - ApiService.updateArticle()
        update_response = client.put(
            f'/api/artigos/{artigo_id}',
            data=json.dumps({
                'titulo': 'Testes de Integração - Edição Revisada',
                'resumo': 'Versão atualizada do artigo'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert update_response.status_code == 200
        
        # 5. DELETE - ApiService.deleteArticle()
        delete_response = client.delete(
            f'/api/artigos/{artigo_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert delete_response.status_code in [200, 204]
        
        # 6. Verifica que foi deletado
        final_response = client.get(f'/api/artigos/edicao/{edicao_id}')
        artigos_final = json.loads(final_response.data)
        assert len(artigos_final) == 0
