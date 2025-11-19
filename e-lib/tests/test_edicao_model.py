"""
Testes unitários para o modelo EdicaoEvento
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

from app.models.edicao import EdicaoEvento


class TestEdicaoEventoModel(unittest.TestCase):
    """Suite de testes unitários para o modelo EdicaoEvento"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.test_evento_id = "507f1f77bcf86cd799439011"
        self.test_ano = 2024
        self.test_local = "São Paulo, SP"
        self.test_data_inicio = datetime(2024, 10, 15)
        self.test_data_fim = datetime(2024, 10, 18)
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_creates_edicao_with_required_fields(self):
        """Testa se o construtor cria uma edição com campos obrigatórios"""
        # Arrange & Act
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Assert
        self.assertEqual(edicao.evento_id, self.test_evento_id)
        self.assertEqual(edicao.ano, self.test_ano)
        self.assertEqual(edicao.local, self.test_local)
    
    def test_init_creates_edicao_with_all_fields(self):
        """Testa se o construtor cria uma edição com todos os campos"""
        # Arrange & Act
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local,
            data_inicio=self.test_data_inicio,
            data_fim=self.test_data_fim
        )
        
        # Assert
        self.assertEqual(edicao.evento_id, self.test_evento_id)
        self.assertEqual(edicao.ano, self.test_ano)
        self.assertEqual(edicao.local, self.test_local)
        self.assertEqual(edicao.data_inicio, self.test_data_inicio)
        self.assertEqual(edicao.data_fim, self.test_data_fim)
    
    def test_init_sets_data_inicio_to_none_by_default(self):
        """Testa se data_inicio é None por padrão"""
        # Arrange & Act
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Assert
        self.assertIsNone(edicao.data_inicio)
    
    def test_init_sets_data_fim_to_none_by_default(self):
        """Testa se data_fim é None por padrão"""
        # Arrange & Act
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Assert
        self.assertIsNone(edicao.data_fim)
    
    def test_init_creates_empty_artigos_list(self):
        """Testa se artigos é uma lista vazia por padrão"""
        # Arrange & Act
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Assert
        self.assertEqual(edicao.artigos, [])
        self.assertIsInstance(edicao.artigos, list)
    
    def test_init_sets_data_criacao_automatically(self):
        """Testa se data_criacao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(edicao.data_criacao)
        self.assertIsInstance(edicao.data_criacao, datetime)
        self.assertGreaterEqual(edicao.data_criacao, before)
        self.assertLessEqual(edicao.data_criacao, after)
    
    # ==================== TESTES DE to_dict ====================
    
    def test_to_dict_returns_dictionary(self):
        """Testa se to_dict retorna um dicionário"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Act
        edicao_dict = edicao.to_dict()
        
        # Assert
        self.assertIsInstance(edicao_dict, dict)
    
    def test_to_dict_contains_all_fields(self):
        """Testa se to_dict contém todos os campos"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local,
            data_inicio=self.test_data_inicio,
            data_fim=self.test_data_fim
        )
        
        # Act
        edicao_dict = edicao.to_dict()
        
        # Assert
        self.assertIn('evento_id', edicao_dict)
        self.assertIn('ano', edicao_dict)
        self.assertIn('local', edicao_dict)
        self.assertIn('data_inicio', edicao_dict)
        self.assertIn('data_fim', edicao_dict)
        self.assertIn('artigos', edicao_dict)
        self.assertIn('data_criacao', edicao_dict)
    
    def test_to_dict_converts_data_inicio_to_isoformat(self):
        """Testa se to_dict converte data_inicio para formato ISO"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local,
            data_inicio=self.test_data_inicio
        )
        
        # Act
        edicao_dict = edicao.to_dict()
        
        # Assert
        self.assertIsInstance(edicao_dict['data_inicio'], str)
        self.assertIn('T', edicao_dict['data_inicio'])
    
    def test_to_dict_converts_data_fim_to_isoformat(self):
        """Testa se to_dict converte data_fim para formato ISO"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local,
            data_fim=self.test_data_fim
        )
        
        # Act
        edicao_dict = edicao.to_dict()
        
        # Assert
        self.assertIsInstance(edicao_dict['data_fim'], str)
        self.assertIn('T', edicao_dict['data_fim'])
    
    def test_to_dict_handles_none_data_inicio(self):
        """Testa se to_dict lida com data_inicio None"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Act
        edicao_dict = edicao.to_dict()
        
        # Assert
        self.assertIsNone(edicao_dict['data_inicio'])
    
    def test_to_dict_handles_none_data_fim(self):
        """Testa se to_dict lida com data_fim None"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        # Act
        edicao_dict = edicao.to_dict()
        
        # Assert
        self.assertIsNone(edicao_dict['data_fim'])
    
    # ==================== TESTES COM MOCKS - save() ====================
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_save_inserts_edicao_successfully(self, mock_get_collection):
        """Testa se save() insere a edição com sucesso"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = edicao.save()
        
        # Assert
        self.assertIsNotNone(result)
        mock_get_collection.assert_called_once_with('edicoes')
        mock_collection.insert_one.assert_called_once()
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_save_converts_evento_id_to_objectid(self, mock_get_collection):
        """Testa se save() converte evento_id para ObjectId"""
        # Arrange
        edicao = EdicaoEvento(
            evento_id=self.test_evento_id,
            ano=self.test_ano,
            local=self.test_local
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        edicao.save()
        
        # Assert
        call_args = mock_collection.insert_one.call_args[0][0]
        self.assertIsInstance(call_args['evento_id'], ObjectId)
    
    # ==================== TESTES COM MOCKS - find_by_evento() ====================
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_find_by_evento_returns_list_of_edicoes(self, mock_get_collection):
        """Testa se find_by_evento retorna lista de edições"""
        # Arrange
        mock_collection = MagicMock()
        mock_edicoes = [
            {'_id': ObjectId(), 'evento_id': ObjectId(self.test_evento_id), 'ano': 2024},
            {'_id': ObjectId(), 'evento_id': ObjectId(self.test_evento_id), 'ano': 2023}
        ]
        mock_collection.find.return_value = mock_edicoes
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.find_by_evento(self.test_evento_id)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_find_by_evento_converts_objectid_to_string(self, mock_get_collection):
        """Testa se find_by_evento converte ObjectId para string"""
        # Arrange
        mock_collection = MagicMock()
        mock_edicoes = [
            {'_id': ObjectId(), 'evento_id': ObjectId(self.test_evento_id), 'ano': 2024}
        ]
        mock_collection.find.return_value = mock_edicoes
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.find_by_evento(self.test_evento_id)
        
        # Assert
        self.assertIsInstance(result[0]['_id'], str)
        self.assertIsInstance(result[0]['evento_id'], str)
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_find_by_evento_handles_string_evento_id(self, mock_get_collection):
        """Testa se find_by_evento lida com evento_id como string"""
        # Arrange
        mock_collection = MagicMock()
        mock_edicoes = [
            {'_id': ObjectId(), 'evento_id': self.test_evento_id, 'ano': 2024}
        ]
        mock_collection.find.return_value = mock_edicoes
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.find_by_evento(self.test_evento_id)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
    
    # ==================== TESTES COM MOCKS - find_by_id() ====================
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_find_by_id_returns_edicao_when_found(self, mock_get_collection):
        """Testa se find_by_id retorna edição quando encontrada"""
        # Arrange
        mock_collection = MagicMock()
        edicao_id = ObjectId()
        mock_edicao = {
            '_id': edicao_id,
            'evento_id': ObjectId(self.test_evento_id),
            'ano': self.test_ano
        }
        mock_collection.find_one.return_value = mock_edicao
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.find_by_id(str(edicao_id))
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result['_id'], str)
        self.assertIsInstance(result['evento_id'], str)
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_find_by_id_returns_none_when_not_found(self, mock_get_collection):
        """Testa se find_by_id retorna None quando não encontrada"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.find_by_id(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES COM MOCKS - update() ====================
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_update_updates_edicao_successfully(self, mock_get_collection):
        """Testa se update() atualiza a edição com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.update(str(ObjectId()), {'local': 'Novo Local'})
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.modified_count, 1)
    
    # ==================== TESTES COM MOCKS - delete() ====================
    
    @patch('app.models.edicao.mongo.get_collection')
    def test_delete_deletes_edicao_successfully(self, mock_get_collection):
        """Testa se delete() deleta a edição com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = EdicaoEvento.delete(str(ObjectId()))
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.deleted_count, 1)


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
