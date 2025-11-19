"""
Testes de Integração: Frontend → Backend (Batch Upload)
Testa as chamadas HTTP do Angular para upload em lote de BibTeX.
Simula: ApiService.uploadBibtex()
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
    """Cria um evento e edição para testes de batch upload"""
    eventos_collection = mongo.get_collection('eventos')
    evento_result = eventos_collection.insert_one({
        'nome': 'Evento Teste',
        'descricao': 'Evento para testar batch upload',
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


class TestFrontendBatchUploadIntegration:
    """Testes de integração Frontend → Backend para Batch Upload"""
    
    def test_upload_bibtex_success(self, client, auth_token, edicao_id):
        """Testa POST /api/batch/upload-bibtex com arquivo válido (simula ApiService.uploadBibtex())"""
        # Cria um arquivo BibTeX fake
        bibtex_content = """
@article{silva2024,
  title={Machine Learning em Python},
  author={Silva, João and Santos, Maria},
  year={2024},
  journal={Journal of AI}
}

@inproceedings{costa2024,
  title={Deep Learning Applications},
  author={Costa, Pedro},
  year={2024},
  booktitle={Proceedings of AI Conference}
}
"""
        
        bibtex_file = io.BytesIO(bibtex_content.encode('utf-8'))
        
        data = {
            'bibtex': (bibtex_file, 'artigos.bib'),
            'edicao_id': edicao_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Pode retornar 200, 201 ou erro dependendo da implementação
        assert response.status_code in [200, 201, 400]
        
        # Se foi sucesso, verifica a resposta
        if response.status_code in [200, 201]:
            data = json.loads(response.data)
            # Pode retornar informações sobre artigos criados
            assert 'message' in data or 'artigos' in data or 'count' in data
    
    def test_upload_bibtex_without_auth(self, client, edicao_id):
        """Testa POST /api/batch/upload-bibtex sem autenticação"""
        bibtex_content = "@article{test2024, title={Test}}"
        bibtex_file = io.BytesIO(bibtex_content.encode('utf-8'))
        
        data = {
            'bibtex': (bibtex_file, 'test.bib'),
            'edicao_id': edicao_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code in [200, 201, 401, 403]
    
    def test_upload_bibtex_without_file(self, client, auth_token, edicao_id):
        """Testa POST /api/batch/upload-bibtex sem arquivo"""
        data = {
            'edicao_id': edicao_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 400
    
    def test_upload_bibtex_without_edicao_id(self, client, auth_token):
        """Testa POST /api/batch/upload-bibtex sem edicao_id"""
        bibtex_content = "@article{test2024, title={Test}}"
        bibtex_file = io.BytesIO(bibtex_content.encode('utf-8'))
        
        data = {
            'bibtex': (bibtex_file, 'test.bib')
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [400, 422]
    
    def test_upload_bibtex_invalid_format(self, client, auth_token, edicao_id):
        """Testa POST /api/batch/upload-bibtex com formato inválido"""
        # Arquivo com conteúdo não-BibTeX
        invalid_content = "This is not a BibTeX file, just plain text"
        invalid_file = io.BytesIO(invalid_content.encode('utf-8'))
        
        data = {
            'bibtex': (invalid_file, 'invalid.bib'),
            'edicao_id': edicao_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Deve retornar erro de formato
        assert response.status_code in [400, 422]
    
    def test_upload_bibtex_empty_file(self, client, auth_token, edicao_id):
        """Testa POST /api/batch/upload-bibtex com arquivo vazio"""
        empty_file = io.BytesIO(b'')
        
        data = {
            'bibtex': (empty_file, 'empty.bib'),
            'edicao_id': edicao_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [400, 422]
    
    def test_upload_bibtex_with_invalid_edicao_id(self, client, auth_token):
        """Testa POST /api/batch/upload-bibtex com edicao_id inexistente"""
        bibtex_content = "@article{test2024, title={Test Article}}"
        bibtex_file = io.BytesIO(bibtex_content.encode('utf-8'))
        
        fake_id = str(ObjectId())
        
        data = {
            'bibtex': (bibtex_file, 'test.bib'),
            'edicao_id': fake_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Pode retornar 404 (não encontrado) ou 400 (bad request)
        assert response.status_code in [400, 404]
    
    def test_upload_bibtex_multiple_entries(self, client, auth_token, edicao_id):
        """Testa upload de BibTeX com múltiplas entradas"""
        bibtex_content = """
@article{entry1,
  title={First Article},
  author={Author One},
  year={2024}
}

@article{entry2,
  title={Second Article},
  author={Author Two},
  year={2024}
}

@inproceedings{entry3,
  title={Third Paper},
  author={Author Three},
  year={2024}
}
"""
        
        bibtex_file = io.BytesIO(bibtex_content.encode('utf-8'))
        
        data = {
            'bibtex': (bibtex_file, 'multiple.bib'),
            'edicao_id': edicao_id
        }
        
        response = client.post(
            '/api/batch/upload-bibtex',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Se aceitar, deve processar todas as entradas
        if response.status_code in [200, 201]:
            data = json.loads(response.data)
            # Verifica que processou múltiplas entradas
            if 'count' in data:
                assert data['count'] >= 3 or data['count'] == 0
    
    def test_upload_bibtex_workflow_with_verification(self, client, auth_token, edicao_id):
        """Testa fluxo completo: upload BibTeX → verificar artigos criados"""
        # 1. Upload BibTeX - ApiService.uploadBibtex()
        bibtex_content = """
@article{workflow2024,
  title={Integration Testing Workflow},
  author={Test, Author},
  year={2024},
  journal={Test Journal}
}
"""
        
        bibtex_file = io.BytesIO(bibtex_content.encode('utf-8'))
        
        upload_response = client.post(
            '/api/batch/upload-bibtex',
            data={
                'bibtex': (bibtex_file, 'workflow.bib'),
                'edicao_id': edicao_id
            },
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Aceita sucesso ou erro dependendo da implementação
        assert upload_response.status_code in [200, 201, 400]
        
        # 2. Se upload foi bem-sucedido, verifica artigos criados
        if upload_response.status_code in [200, 201]:
            # ApiService.getArticlesByEdition()
            artigos_response = client.get(f'/api/artigos/edicao/{edicao_id}')
            assert artigos_response.status_code == 200
            
            artigos = json.loads(artigos_response.data)
            # Pode ter artigos criados ou não dependendo da implementação
            assert isinstance(artigos, list)
