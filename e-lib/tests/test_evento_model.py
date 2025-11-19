"""
Testes unitários para o modelo Evento
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

from app.models.evento import Evento


class TestEventoModel(unittest.TestCase):
    """Suite de testes unitários para o modelo Evento"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.test_nome = "Simpósio Brasileiro de Engenharia de Software"
        self.test_sigla = "SBES"
        self.test_descricao = "Principal evento de Engenharia de Software do Brasil"
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_creates_evento_with_required_fields(self):
        """Testa se o construtor cria um evento com campos obrigatórios"""
        # Arrange & Act
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        # Assert
        self.assertEqual(evento.nome, self.test_nome)
        self.assertEqual(evento.sigla, self.test_sigla)
    
    def test_init_creates_evento_with_all_fields(self):
        """Testa se o construtor cria um evento com todos os campos"""
        # Arrange & Act
        evento = Evento(
            nome=self.test_nome,
            sigla=self.test_sigla,
            descricao=self.test_descricao
        )
        
        # Assert
        self.assertEqual(evento.nome, self.test_nome)
        self.assertEqual(evento.sigla, self.test_sigla)
        self.assertEqual(evento.descricao, self.test_descricao)
    
    def test_init_sets_descricao_to_none_by_default(self):
        """Testa se descricao é None por padrão"""
        # Arrange & Act
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        # Assert
        self.assertIsNone(evento.descricao)
    
    def test_init_sets_data_criacao_automatically(self):
        """Testa se data_criacao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(evento.data_criacao)
        self.assertIsInstance(evento.data_criacao, datetime)
        self.assertGreaterEqual(evento.data_criacao, before)
        self.assertLessEqual(evento.data_criacao, after)
    
    # ==================== TESTES DE to_dict ====================
    
    def test_to_dict_returns_dictionary(self):
        """Testa se to_dict retorna um dicionário"""
        # Arrange
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        # Act
        evento_dict = evento.to_dict()
        
        # Assert
        self.assertIsInstance(evento_dict, dict)
    
    def test_to_dict_contains_all_fields(self):
        """Testa se to_dict contém todos os campos"""
        # Arrange
        evento = Evento(
            nome=self.test_nome,
            sigla=self.test_sigla,
            descricao=self.test_descricao
        )
        
        # Act
        evento_dict = evento.to_dict()
        
        # Assert
        self.assertIn('nome', evento_dict)
        self.assertIn('sigla', evento_dict)
        self.assertIn('descricao', evento_dict)
        self.assertIn('data_criacao', evento_dict)
    
    def test_to_dict_converts_data_criacao_to_isoformat(self):
        """Testa se to_dict converte data_criacao para formato ISO"""
        # Arrange
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        # Act
        evento_dict = evento.to_dict()
        
        # Assert
        self.assertIsInstance(evento_dict['data_criacao'], str)
        self.assertIn('T', evento_dict['data_criacao'])
    
    # ==================== TESTES COM MOCKS - save() ====================
    
    @patch('app.models.evento.mongo.get_collection')
    @patch('builtins.print')
    def test_save_inserts_evento_successfully(self, mock_print, mock_get_collection):
        """Testa se save() insere o evento com sucesso"""
        # Arrange
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = evento.save()
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.inserted_id, mock_result.inserted_id)
        mock_get_collection.assert_called_once_with('eventos')
    
    @patch('app.models.evento.mongo.get_collection')
    def test_save_returns_none_on_exception(self, mock_get_collection):
        """Testa se save() retorna None quando ocorre exceção"""
        # Arrange
        evento = Evento(nome=self.test_nome, sigla=self.test_sigla)
        
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = evento.save()
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES COM MOCKS - find_all() ====================
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_all_returns_list_of_eventos(self, mock_get_collection):
        """Testa se find_all retorna lista de eventos"""
        # Arrange
        mock_collection = MagicMock()
        mock_eventos = [
            {'_id': ObjectId(), 'nome': 'Evento 1', 'sigla': 'EV1'},
            {'_id': ObjectId(), 'nome': 'Evento 2', 'sigla': 'EV2'}
        ]
        mock_collection.find.return_value = mock_eventos
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_all()
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_all_converts_objectid_to_string(self, mock_get_collection):
        """Testa se find_all converte ObjectId para string"""
        # Arrange
        mock_collection = MagicMock()
        evento_id = ObjectId()
        mock_eventos = [{'_id': evento_id, 'nome': 'Teste', 'sigla': 'TST'}]
        mock_collection.find.return_value = mock_eventos
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_all()
        
        # Assert
        self.assertIsInstance(result[0]['_id'], str)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_all_returns_empty_list_on_exception(self, mock_get_collection):
        """Testa se find_all retorna lista vazia quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.side_effect = Exception("Erro")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_all()
        
        # Assert
        self.assertEqual(result, [])
    
    # ==================== TESTES COM MOCKS - find_by_id() ====================
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_by_id_returns_evento_when_found(self, mock_get_collection):
        """Testa se find_by_id retorna evento quando encontrado"""
        # Arrange
        mock_collection = MagicMock()
        evento_id = ObjectId()
        mock_evento = {
            '_id': evento_id,
            'nome': self.test_nome,
            'sigla': self.test_sigla
        }
        mock_collection.find_one.return_value = mock_evento
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_by_id(str(evento_id))
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result['_id'], str)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_by_id_returns_none_when_not_found(self, mock_get_collection):
        """Testa se find_by_id retorna None quando não encontrado"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_by_id(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_by_id_returns_none_on_exception(self, mock_get_collection):
        """Testa se find_by_id retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.side_effect = Exception("Erro")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_by_id(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES COM MOCKS - find_by_sigla() ====================
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_by_sigla_returns_evento_when_found(self, mock_get_collection):
        """Testa se find_by_sigla retorna evento quando encontrado"""
        # Arrange
        mock_collection = MagicMock()
        evento_id = ObjectId()
        mock_evento = {
            '_id': evento_id,
            'nome': self.test_nome,
            'sigla': self.test_sigla
        }
        mock_collection.find_one.return_value = mock_evento
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_by_sigla(self.test_sigla)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result['sigla'], self.test_sigla)
        self.assertIsInstance(result['_id'], str)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_by_sigla_returns_none_when_not_found(self, mock_get_collection):
        """Testa se find_by_sigla retorna None quando não encontrado"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_by_sigla("INEXISTENTE")
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_find_by_sigla_returns_none_on_exception(self, mock_get_collection):
        """Testa se find_by_sigla retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.side_effect = Exception("Erro")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.find_by_sigla(self.test_sigla)
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES COM MOCKS - update() ====================
    
    @patch('app.models.evento.mongo.get_collection')
    def test_update_updates_evento_successfully(self, mock_get_collection):
        """Testa se update() atualiza o evento com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.update(str(ObjectId()), {'nome': 'Novo Nome'})
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.modified_count, 1)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_update_returns_none_on_exception(self, mock_get_collection):
        """Testa se update() retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.update_one.side_effect = Exception("Erro")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.update(str(ObjectId()), {'nome': 'Teste'})
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES COM MOCKS - delete() ====================
    
    @patch('app.models.evento.mongo.get_collection')
    def test_delete_deletes_evento_successfully(self, mock_get_collection):
        """Testa se delete() deleta o evento com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.delete(str(ObjectId()))
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.deleted_count, 1)
    
    @patch('app.models.evento.mongo.get_collection')
    def test_delete_returns_none_on_exception(self, mock_get_collection):
        """Testa se delete() retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.delete_one.side_effect = Exception("Erro")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Evento.delete(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
