"""
Configuração e fixtures para testes de integração
Fornece setup e teardown para testes que usam MongoDB real
"""

import pytest
import os
import sys
from pymongo import MongoClient

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.services.connection import mongo


@pytest.fixture(scope='session')
def mongodb_uri():
    """URI do MongoDB para testes (usa banco de teste)"""
    return os.environ.get('MONGODB_TEST_URI', 'mongodb://localhost:27017/simple-lib-test')


@pytest.fixture(scope='session')
def mongodb_client(mongodb_uri):
    """Cliente MongoDB para testes"""
    client = MongoClient(mongodb_uri)
    yield client
    client.close()


@pytest.fixture(scope='session')
def mongodb_database(mongodb_client):
    """Database do MongoDB para testes"""
    db = mongodb_client.get_database()
    yield db


@pytest.fixture(scope='function')
def clean_database(mongodb_database):
    """Limpa o banco de dados antes e depois de cada teste"""
    # Limpar antes do teste
    for collection_name in mongodb_database.list_collection_names():
        mongodb_database[collection_name].delete_many({})
    
    yield
    
    # Limpar depois do teste
    for collection_name in mongodb_database.list_collection_names():
        mongodb_database[collection_name].delete_many({})


@pytest.fixture(scope='function')
def setup_test_mongo(mongodb_uri, clean_database):
    """Configura o objeto mongo global para usar o banco de teste"""
    # Salvar URI original
    original_uri = mongo.uri
    
    # Configurar para usar banco de teste
    mongo.uri = mongodb_uri
    mongo.client = None
    mongo.db = None
    mongo.connect()
    
    yield mongo
    
    # Restaurar URI original
    mongo.uri = original_uri
    mongo.client = None
    mongo.db = None


@pytest.fixture
def sample_evento_data():
    """Dados de exemplo para criar um evento"""
    return {
        'nome': 'Simpósio Brasileiro de Engenharia de Software',
        'sigla': 'SBES',
        'descricao': 'Principal evento de Engenharia de Software do Brasil'
    }


@pytest.fixture
def sample_edicao_data(sample_evento_data, setup_test_mongo):
    """Dados de exemplo para criar uma edição (requer um evento)"""
    from app.models.evento import Evento
    from datetime import datetime
    
    evento = Evento(**sample_evento_data)
    result = evento.save()
    
    return {
        'evento_id': str(result.inserted_id),
        'ano': 2024,
        'local': 'São Paulo, SP',
        'data_inicio': datetime(2024, 10, 15),
        'data_fim': datetime(2024, 10, 18)
    }


@pytest.fixture
def sample_artigo_data(sample_edicao_data, setup_test_mongo):
    """Dados de exemplo para criar um artigo (requer uma edição)"""
    from app.models.edicao import EdicaoEvento
    
    edicao = EdicaoEvento(**sample_edicao_data)
    result = edicao.save()
    
    return {
        'titulo': 'Análise de Sistemas Distribuídos',
        'autores': [
            {'nome': 'Dr. João Silva', 'email': 'joao@univ.edu'},
            {'nome': 'Dra. Maria Santos', 'email': 'maria@univ.edu'}
        ],
        'edicao_id': str(result.inserted_id),
        'resumo': 'Este artigo apresenta uma análise detalhada de sistemas distribuídos.',
        'keywords': ['sistemas distribuídos', 'computação', 'arquitetura']
    }


@pytest.fixture
def sample_usuario_data():
    """Dados de exemplo para criar um usuário"""
    return {
        'email': 'usuario@test.com',
        'nome': 'Usuário Teste',
        'is_admin': False,
        'senha': 'senha123'
    }


@pytest.fixture
def sample_notificacao_data():
    """Dados de exemplo para criar uma notificação"""
    return {
        'email': 'leitor@test.com',
        'nome_autor': 'Dr. João Silva'
    }
