"""
Testes unitários para o serviço de conexão com MongoDB
Testa as funcionalidades com mocks para isolar dependências do MongoDB
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.services.connection import MongoDB


class TestMongoDB(unittest.TestCase):
    """Suite de testes unitários para a classe MongoDB"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.mongodb = MongoDB()
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_sets_default_uri(self):
        """Testa se __init__ define URI padrão quando não especificado"""
        # Arrange & Act
        with patch.dict(os.environ, {}, clear=True):
            db = MongoDB()
        
        # Assert
        self.assertEqual(db.uri, 'mongodb://localhost:27017/simple-lib')
    
    def test_init_reads_uri_from_env(self):
        """Testa se __init__ lê URI de variável de ambiente"""
        # Arrange
        custom_uri = 'mongodb://custom:27017/testdb'
        
        # Act
        with patch.dict(os.environ, {'MONGODB_URI': custom_uri}):
            db = MongoDB()
        
        # Assert
        self.assertEqual(db.uri, custom_uri)
    
    def test_init_sets_client_to_none(self):
        """Testa se __init__ define client como None"""
        # Arrange & Act
        db = MongoDB()
        
        # Assert
        self.assertIsNone(db.client)
    
    def test_init_sets_db_to_none(self):
        """Testa se __init__ define db como None"""
        # Arrange & Act
        db = MongoDB()
        
        # Assert
        self.assertIsNone(db.db)
    
    # ==================== TESTES DE connect() ====================
    
    @patch('app.services.connection.MongoClient')
    @patch('builtins.print')
    def test_connect_creates_mongo_client(self, mock_print, mock_mongo_client):
        """Testa se connect() cria um MongoClient"""
        # Arrange
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_client.get_database.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        db = MongoDB()
        
        # Act
        result = db.connect()
        
        # Assert
        mock_mongo_client.assert_called_once_with(db.uri)
        self.assertEqual(db.client, mock_client)
    
    @patch('app.services.connection.MongoClient')
    @patch('builtins.print')
    def test_connect_gets_database(self, mock_print, mock_mongo_client):
        """Testa se connect() obtém o banco de dados"""
        # Arrange
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_client.get_database.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        db = MongoDB()
        
        # Act
        result = db.connect()
        
        # Assert
        mock_client.get_database.assert_called_once()
        self.assertEqual(db.db, mock_db)
        self.assertEqual(result, mock_db)
    
    @patch('app.services.connection.MongoClient')
    @patch('builtins.print')
    def test_connect_prints_success_message(self, mock_print, mock_mongo_client):
        """Testa se connect() imprime mensagem de sucesso"""
        # Arrange
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_client.get_database.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        db = MongoDB()
        
        # Act
        db.connect()
        
        # Assert
        self.assertTrue(any("Conectado ao MongoDB com sucesso" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('app.services.connection.MongoClient')
    @patch('builtins.print')
    def test_connect_returns_none_on_exception(self, mock_print, mock_mongo_client):
        """Testa se connect() retorna None quando ocorre exceção"""
        # Arrange
        mock_mongo_client.side_effect = Exception("Erro de conexão")
        db = MongoDB()
        
        # Act
        result = db.connect()
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.services.connection.MongoClient')
    @patch('builtins.print')
    def test_connect_prints_error_message_on_exception(self, mock_print, mock_mongo_client):
        """Testa se connect() imprime mensagem de erro quando ocorre exceção"""
        # Arrange
        mock_mongo_client.side_effect = Exception("Erro de conexão")
        db = MongoDB()
        
        # Act
        db.connect()
        
        # Assert
        self.assertTrue(any("Erro ao conectar com MongoDB" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES DE get_collection() ====================
    
    @patch('app.services.connection.MongoClient')
    def test_get_collection_returns_collection(self, mock_mongo_client):
        """Testa se get_collection() retorna uma coleção"""
        # Arrange
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client.get_database.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        db = MongoDB()
        db.db = mock_db
        
        # Act
        result = db.get_collection('test_collection')
        
        # Assert
        mock_db.__getitem__.assert_called_once_with('test_collection')
        self.assertEqual(result, mock_collection)
    
    @patch('app.services.connection.MongoClient')
    @patch('builtins.print')
    def test_get_collection_connects_if_db_is_none(self, mock_print, mock_mongo_client):
        """Testa se get_collection() conecta se db for None"""
        # Arrange
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client.get_database.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        db = MongoDB()
        db.db = None  # Garante que db é None
        
        # Act
        result = db.get_collection('test_collection')
        
        # Assert
        # Verifica se connect foi chamado (MongoClient foi instanciado)
        mock_mongo_client.assert_called_once()
        self.assertIsNotNone(db.db)
    
    @patch('app.services.connection.MongoClient')
    def test_get_collection_with_different_collection_names(self, mock_mongo_client):
        """Testa se get_collection() funciona com diferentes nomes de coleções"""
        # Arrange
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_client.get_database.return_value = mock_db
        mock_mongo_client.return_value = mock_client
        
        db = MongoDB()
        db.db = mock_db
        
        collection_names = ['artigos', 'eventos', 'edicoes', 'usuarios', 'notificacoes']
        
        # Act & Assert
        for collection_name in collection_names:
            db.get_collection(collection_name)
            mock_db.__getitem__.assert_called_with(collection_name)
    
    # ==================== TESTES DE INTEGRAÇÃO DA INSTÂNCIA ====================
    
    def test_mongo_instance_exists(self):
        """Testa se a instância global 'mongo' foi criada"""
        # Arrange & Act
        from app.services.connection import mongo
        
        # Assert
        self.assertIsInstance(mongo, MongoDB)
    
    def test_mongo_instance_has_default_uri(self):
        """Testa se a instância global tem URI padrão ou de ambiente"""
        # Arrange & Act
        from app.services.connection import mongo
        
        # Assert
        self.assertIsNotNone(mongo.uri)
        self.assertIsInstance(mongo.uri, str)
        self.assertIn('mongodb://', mongo.uri)


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
