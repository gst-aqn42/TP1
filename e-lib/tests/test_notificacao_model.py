"""
Testes unitários para o modelo Notificacao
Testa as funcionalidades com mocks para isolar dependências do banco de dados
"""

import unittest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from bson import ObjectId

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.models.notificacao import Notificacao


class TestNotificacaoModel(unittest.TestCase):
    """Suite de testes unitários para o modelo Notificacao"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.test_email = "leitor@example.com"
        self.test_nome_autor = "Dr. João Silva"
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_creates_notificacao_with_required_fields(self):
        """Testa se o construtor cria uma notificação com campos obrigatórios"""
        # Arrange & Act
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        # Assert
        self.assertEqual(notificacao.email, self.test_email)
        self.assertEqual(notificacao.nome_autor, self.test_nome_autor)
    
    def test_init_sets_ativo_to_true_by_default(self):
        """Testa se ativo é True por padrão"""
        # Arrange & Act
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        # Assert
        self.assertTrue(notificacao.ativo)
    
    def test_init_sets_data_inscricao_automatically(self):
        """Testa se data_inscricao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(notificacao.data_inscricao)
        self.assertIsInstance(notificacao.data_inscricao, datetime)
        self.assertGreaterEqual(notificacao.data_inscricao, before)
        self.assertLessEqual(notificacao.data_inscricao, after)
    
    # ==================== TESTES COM MOCKS - save() ====================
    
    @patch('app.models.notificacao.mongo.get_collection')
    @patch('builtins.print')
    def test_save_inserts_notificacao_successfully(self, mock_print, mock_get_collection):
        """Testa se save() insere a notificação com sucesso"""
        # Arrange
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = notificacao.save()
        
        # Assert
        self.assertIsNotNone(result)
        mock_get_collection.assert_called_once_with('notificacoes')
        mock_collection.insert_one.assert_called_once()
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_save_calls_insert_one_with_correct_data(self, mock_get_collection):
        """Testa se save() chama insert_one com os dados corretos"""
        # Arrange
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        notificacao.save()
        
        # Assert
        call_args = mock_collection.insert_one.call_args[0][0]
        self.assertEqual(call_args['email'], self.test_email)
        self.assertEqual(call_args['nome_autor'], self.test_nome_autor)
        self.assertTrue(call_args['ativo'])
        self.assertIsInstance(call_args['data_inscricao'], datetime)
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_save_returns_none_on_exception(self, mock_get_collection):
        """Testa se save() retorna None quando ocorre exceção"""
        # Arrange
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = notificacao.save()
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.notificacao.mongo.get_collection')
    @patch('builtins.print')
    def test_save_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se save() imprime erro quando ocorre exceção"""
        # Arrange
        notificacao = Notificacao(
            email=self.test_email,
            nome_autor=self.test_nome_autor
        )
        
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        notificacao.save()
        
        # Assert
        self.assertTrue(any("Erro ao salvar notificação" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES COM MOCKS - find_by_autor() ====================
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_find_by_autor_returns_list_of_notificacoes(self, mock_get_collection):
        """Testa se find_by_autor retorna lista de notificações"""
        # Arrange
        mock_collection = MagicMock()
        mock_notificacoes = [
            {
                '_id': ObjectId(),
                'email': 'user1@test.com',
                'nome_autor': self.test_nome_autor,
                'ativo': True
            },
            {
                '_id': ObjectId(),
                'email': 'user2@test.com',
                'nome_autor': self.test_nome_autor,
                'ativo': True
            }
        ]
        mock_collection.find.return_value = mock_notificacoes
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Notificacao.find_by_autor(self.test_nome_autor)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        mock_get_collection.assert_called_once_with('notificacoes')
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_find_by_autor_uses_regex_for_case_insensitive_search(self, mock_get_collection):
        """Testa se find_by_autor usa regex para busca case-insensitive"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.return_value = []
        mock_get_collection.return_value = mock_collection
        
        # Act
        Notificacao.find_by_autor("joão")
        
        # Assert
        call_args = mock_collection.find.call_args[0][0]
        self.assertIn('nome_autor', call_args)
        self.assertIn('$regex', call_args['nome_autor'])
        self.assertEqual(call_args['nome_autor']['$options'], 'i')
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_find_by_autor_only_returns_active_notifications(self, mock_get_collection):
        """Testa se find_by_autor retorna apenas notificações ativas"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.return_value = []
        mock_get_collection.return_value = mock_collection
        
        # Act
        Notificacao.find_by_autor(self.test_nome_autor)
        
        # Assert
        call_args = mock_collection.find.call_args[0][0]
        self.assertTrue(call_args['ativo'])
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_find_by_autor_returns_empty_list_on_exception(self, mock_get_collection):
        """Testa se find_by_autor retorna lista vazia quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Notificacao.find_by_autor(self.test_nome_autor)
        
        # Assert
        self.assertEqual(result, [])
    
    @patch('app.models.notificacao.mongo.get_collection')
    @patch('builtins.print')
    def test_find_by_autor_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se find_by_autor imprime erro quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        Notificacao.find_by_autor(self.test_nome_autor)
        
        # Assert
        self.assertTrue(any("Erro ao buscar notificações" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES COM MOCKS - desativar_inscricao() ====================
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_desativar_inscricao_updates_successfully(self, mock_get_collection):
        """Testa se desativar_inscricao atualiza com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        notificacao_id = str(ObjectId())
        
        # Act
        result = Notificacao.desativar_inscricao(notificacao_id)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.modified_count, 1)
        mock_get_collection.assert_called_once_with('notificacoes')
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_desativar_inscricao_sets_ativo_to_false(self, mock_get_collection):
        """Testa se desativar_inscricao define ativo como False"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.update_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        notificacao_id = str(ObjectId())
        
        # Act
        Notificacao.desativar_inscricao(notificacao_id)
        
        # Assert
        call_args = mock_collection.update_one.call_args[0]
        self.assertEqual(call_args[1], {'$set': {'ativo': False}})
    
    @patch('app.models.notificacao.mongo.get_collection')
    def test_desativar_inscricao_returns_none_on_exception(self, mock_get_collection):
        """Testa se desativar_inscricao retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.update_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Notificacao.desativar_inscricao(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.notificacao.mongo.get_collection')
    @patch('builtins.print')
    def test_desativar_inscricao_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se desativar_inscricao imprime erro quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.update_one.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        Notificacao.desativar_inscricao(str(ObjectId()))
        
        # Assert
        self.assertTrue(any("Erro ao desativar notificação" in str(call) 
                           for call in mock_print.call_args_list))


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
