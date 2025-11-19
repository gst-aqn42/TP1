"""
Testes unitários para o modelo Artigo
Testa as funcionalidades que podem ser isoladas sem depender do banco de dados
"""

import unittest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from bson import ObjectId

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.models.artigo import Artigo


class TestArtigoModel(unittest.TestCase):
    """Suite de testes unitários para o modelo Artigo"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.test_titulo = "Análise de Sistemas Distribuídos"
        self.test_autores = [
            {"nome": "João Silva", "email": "joao@example.com"},
            {"nome": "Maria Santos", "email": "maria@example.com"}
        ]
        self.test_edicao_id = "507f1f77bcf86cd799439011"
        self.test_resumo = "Este artigo apresenta uma análise detalhada de sistemas distribuídos."
        self.test_keywords = ["sistemas distribuídos", "computação", "arquitetura"]
        self.test_pdf_path = "/uploads/artigo123.pdf"
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_creates_artigo_with_required_fields(self):
        """Testa se o construtor cria um artigo com campos obrigatórios"""
        # Arrange & Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertEqual(artigo.titulo, self.test_titulo)
        self.assertEqual(artigo.autores, self.test_autores)
        self.assertEqual(artigo.edicao_id, self.test_edicao_id)
    
    def test_init_creates_artigo_with_all_fields(self):
        """Testa se o construtor cria um artigo com todos os campos"""
        # Arrange & Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=self.test_resumo,
            keywords=self.test_keywords,
            pdf_path=self.test_pdf_path
        )
        
        # Assert
        self.assertEqual(artigo.titulo, self.test_titulo)
        self.assertEqual(artigo.autores, self.test_autores)
        self.assertEqual(artigo.edicao_id, self.test_edicao_id)
        self.assertEqual(artigo.resumo, self.test_resumo)
        self.assertEqual(artigo.keywords, self.test_keywords)
        self.assertEqual(artigo.pdf_path, self.test_pdf_path)
    
    def test_init_sets_default_empty_keywords_list(self):
        """Testa se keywords é uma lista vazia por padrão quando não fornecida"""
        # Arrange & Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertEqual(artigo.keywords, [])
        self.assertIsInstance(artigo.keywords, list)
    
    def test_init_sets_resumo_to_none_by_default(self):
        """Testa se resumo é None por padrão quando não fornecido"""
        # Arrange & Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertIsNone(artigo.resumo)
    
    def test_init_sets_pdf_path_to_none_by_default(self):
        """Testa se pdf_path é None por padrão quando não fornecido"""
        # Arrange & Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertIsNone(artigo.pdf_path)
    
    def test_init_sets_data_publicacao_automatically(self):
        """Testa se data_publicacao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(artigo.data_publicacao)
        self.assertIsInstance(artigo.data_publicacao, datetime)
        self.assertGreaterEqual(artigo.data_publicacao, before)
        self.assertLessEqual(artigo.data_publicacao, after)
    
    def test_init_sets_data_criacao_automatically(self):
        """Testa se data_criacao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(artigo.data_criacao)
        self.assertIsInstance(artigo.data_criacao, datetime)
        self.assertGreaterEqual(artigo.data_criacao, before)
        self.assertLessEqual(artigo.data_criacao, after)
    
    def test_init_accepts_multiple_autores(self):
        """Testa se o construtor aceita múltiplos autores"""
        # Arrange
        autores = [
            {"nome": "Autor 1", "email": "autor1@example.com"},
            {"nome": "Autor 2", "email": "autor2@example.com"},
            {"nome": "Autor 3", "email": "autor3@example.com"}
        ]
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertEqual(len(artigo.autores), 3)
        self.assertEqual(artigo.autores, autores)
    
    def test_init_accepts_single_autor(self):
        """Testa se o construtor aceita um único autor"""
        # Arrange
        autores = [{"nome": "Único Autor", "email": "unico@example.com"}]
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertEqual(len(artigo.autores), 1)
        self.assertEqual(artigo.autores[0]["nome"], "Único Autor")
    
    def test_init_accepts_empty_keywords_list(self):
        """Testa se o construtor aceita lista vazia de keywords"""
        # Arrange & Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            keywords=[]
        )
        
        # Assert
        self.assertEqual(artigo.keywords, [])
    
    # ==================== TESTES DE to_dict ====================
    
    def test_to_dict_returns_dictionary(self):
        """Testa se to_dict retorna um dicionário"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertIsInstance(artigo_dict, dict)
    
    def test_to_dict_contains_all_required_fields(self):
        """Testa se to_dict contém todos os campos obrigatórios"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=self.test_resumo,
            keywords=self.test_keywords,
            pdf_path=self.test_pdf_path
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertIn('titulo', artigo_dict)
        self.assertIn('autores', artigo_dict)
        self.assertIn('edicao_id', artigo_dict)
        self.assertIn('resumo', artigo_dict)
        self.assertIn('keywords', artigo_dict)
        self.assertIn('pdf_path', artigo_dict)
        self.assertIn('data_publicacao', artigo_dict)
        self.assertIn('data_criacao', artigo_dict)
    
    def test_to_dict_has_correct_titulo(self):
        """Testa se to_dict retorna o título correto"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['titulo'], self.test_titulo)
    
    def test_to_dict_has_correct_autores(self):
        """Testa se to_dict retorna os autores corretos"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['autores'], self.test_autores)
    
    def test_to_dict_has_correct_edicao_id(self):
        """Testa se to_dict retorna o edicao_id correto"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['edicao_id'], self.test_edicao_id)
    
    def test_to_dict_has_correct_resumo(self):
        """Testa se to_dict retorna o resumo correto"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=self.test_resumo
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['resumo'], self.test_resumo)
    
    def test_to_dict_has_correct_keywords(self):
        """Testa se to_dict retorna as keywords corretas"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            keywords=self.test_keywords
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['keywords'], self.test_keywords)
    
    def test_to_dict_has_correct_pdf_path(self):
        """Testa se to_dict retorna o pdf_path correto"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            pdf_path=self.test_pdf_path
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['pdf_path'], self.test_pdf_path)
    
    def test_to_dict_converts_data_publicacao_to_isoformat(self):
        """Testa se to_dict converte data_publicacao para formato ISO"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertIsInstance(artigo_dict['data_publicacao'], str)
        # Verifica se está no formato ISO (contém 'T' e termina com 'Z' ou tem offset)
        self.assertIn('T', artigo_dict['data_publicacao'])
    
    def test_to_dict_converts_data_criacao_to_isoformat(self):
        """Testa se to_dict converte data_criacao para formato ISO"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertIsInstance(artigo_dict['data_criacao'], str)
        # Verifica se está no formato ISO
        self.assertIn('T', artigo_dict['data_criacao'])
    
    def test_to_dict_with_none_resumo(self):
        """Testa se to_dict lida corretamente com resumo None"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=None
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertIsNone(artigo_dict['resumo'])
    
    def test_to_dict_with_none_pdf_path(self):
        """Testa se to_dict lida corretamente com pdf_path None"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            pdf_path=None
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertIsNone(artigo_dict['pdf_path'])
    
    def test_to_dict_with_empty_keywords(self):
        """Testa se to_dict lida corretamente com keywords vazia"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            keywords=[]
        )
        
        # Act
        artigo_dict = artigo.to_dict()
        
        # Assert
        self.assertEqual(artigo_dict['keywords'], [])
    
    # ==================== TESTES DE VALIDAÇÃO DE DADOS ====================
    
    def test_artigo_preserves_autor_structure(self):
        """Testa se a estrutura dos autores é preservada"""
        # Arrange
        autores = [
            {"nome": "João", "email": "joao@test.com"},
            {"nome": "Maria", "email": "maria@test.com"}
        ]
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertEqual(len(artigo.autores), 2)
        self.assertEqual(artigo.autores[0]["nome"], "João")
        self.assertEqual(artigo.autores[0]["email"], "joao@test.com")
        self.assertEqual(artigo.autores[1]["nome"], "Maria")
        self.assertEqual(artigo.autores[1]["email"], "maria@test.com")
    
    def test_artigo_handles_special_characters_in_titulo(self):
        """Testa se o artigo lida com caracteres especiais no título"""
        # Arrange
        titulo_especial = "Análise de Código: C++, Java & Python (2024)"
        
        # Act
        artigo = Artigo(
            titulo=titulo_especial,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        # Assert
        self.assertEqual(artigo.titulo, titulo_especial)
        self.assertEqual(artigo.to_dict()['titulo'], titulo_especial)
    
    def test_artigo_handles_long_resumo(self):
        """Testa se o artigo lida com resumo longo"""
        # Arrange
        resumo_longo = "Este é um resumo muito longo. " * 100
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=resumo_longo
        )
        
        # Assert
        self.assertEqual(artigo.resumo, resumo_longo)
        self.assertEqual(len(artigo.resumo), len(resumo_longo))
    
    def test_artigo_handles_many_keywords(self):
        """Testa se o artigo lida com muitas keywords"""
        # Arrange
        many_keywords = [f"keyword{i}" for i in range(20)]
        
        # Act
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            keywords=many_keywords
        )
        
        # Assert
        self.assertEqual(len(artigo.keywords), 20)
        self.assertEqual(artigo.keywords, many_keywords)
    
    # ==================== TESTES COM MOCKS - save() ====================
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_save_inserts_artigo_successfully(self, mock_get_collection):
        """Testa se save() insere o artigo no MongoDB com sucesso"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=self.test_resumo,
            keywords=self.test_keywords,
            pdf_path=self.test_pdf_path
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = artigo.save()
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.inserted_id, mock_result.inserted_id)
        mock_get_collection.assert_called_once_with('artigos')
        mock_collection.insert_one.assert_called_once()
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_save_calls_insert_one_with_correct_data(self, mock_get_collection):
        """Testa se save() chama insert_one com os dados corretos"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id,
            resumo=self.test_resumo
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        artigo.save()
        
        # Assert
        call_args = mock_collection.insert_one.call_args[0][0]
        self.assertEqual(call_args['titulo'], self.test_titulo)
        self.assertEqual(call_args['autores'], self.test_autores)
        self.assertEqual(call_args['resumo'], self.test_resumo)
        self.assertIsInstance(call_args['edicao_id'], ObjectId)
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_save_handles_exception_and_returns_none(self, mock_get_collection):
        """Testa se save() retorna None quando ocorre uma exceção"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = artigo.save()
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.artigo.mongo.get_collection')
    @patch('builtins.print')
    def test_save_prints_success_message(self, mock_print, mock_get_collection):
        """Testa se save() imprime mensagens de sucesso"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        test_id = ObjectId()
        mock_result.inserted_id = test_id
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        artigo.save()
        
        # Assert
        # Verifica se print foi chamado com as mensagens esperadas
        self.assertTrue(any(f"Tentando salvar artigo: {self.test_titulo}" in str(call) 
                           for call in mock_print.call_args_list))
        self.assertTrue(any(f"Artigo salvo no MongoDB com ID: {test_id}" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('app.models.artigo.mongo.get_collection')
    @patch('builtins.print')
    def test_save_prints_error_message_on_exception(self, mock_print, mock_get_collection):
        """Testa se save() imprime mensagem de erro quando ocorre exceção"""
        # Arrange
        artigo = Artigo(
            titulo=self.test_titulo,
            autores=self.test_autores,
            edicao_id=self.test_edicao_id
        )
        
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        artigo.save()
        
        # Assert
        self.assertTrue(any("Erro ao salvar artigo no MongoDB" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES COM MOCKS - find_by_edicao() ====================
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_edicao_returns_list_of_artigos(self, mock_get_collection):
        """Testa se find_by_edicao retorna lista de artigos"""
        # Arrange
        mock_collection = MagicMock()
        mock_artigos = [
            {
                '_id': ObjectId(),
                'edicao_id': ObjectId(self.test_edicao_id),
                'titulo': 'Artigo 1',
                'autores': self.test_autores
            },
            {
                '_id': ObjectId(),
                'edicao_id': ObjectId(self.test_edicao_id),
                'titulo': 'Artigo 2',
                'autores': self.test_autores
            }
        ]
        mock_collection.find.return_value = mock_artigos
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_edicao(self.test_edicao_id)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        mock_get_collection.assert_called_once_with('artigos')
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_edicao_converts_objectid_to_string(self, mock_get_collection):
        """Testa se find_by_edicao converte ObjectId para string"""
        # Arrange
        mock_collection = MagicMock()
        artigo_id = ObjectId()
        edicao_id = ObjectId(self.test_edicao_id)
        mock_artigos = [
            {
                '_id': artigo_id,
                'edicao_id': edicao_id,
                'titulo': 'Artigo Teste'
            }
        ]
        mock_collection.find.return_value = mock_artigos
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_edicao(self.test_edicao_id)
        
        # Assert
        self.assertIsInstance(result[0]['_id'], str)
        self.assertIsInstance(result[0]['edicao_id'], str)
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_edicao_returns_empty_list_on_exception(self, mock_get_collection):
        """Testa se find_by_edicao retorna lista vazia quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_edicao(self.test_edicao_id)
        
        # Assert
        self.assertEqual(result, [])
    
    @patch('app.models.artigo.mongo.get_collection')
    @patch('builtins.print')
    def test_find_by_edicao_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se find_by_edicao imprime erro quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        Artigo.find_by_edicao(self.test_edicao_id)
        
        # Assert
        self.assertTrue(any("Erro ao buscar artigos por edição" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES COM MOCKS - find_by_id() ====================
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_id_returns_artigo_when_found(self, mock_get_collection):
        """Testa se find_by_id retorna artigo quando encontrado"""
        # Arrange
        mock_collection = MagicMock()
        artigo_id = ObjectId()
        mock_artigo = {
            '_id': artigo_id,
            'edicao_id': ObjectId(self.test_edicao_id),
            'titulo': self.test_titulo,
            'autores': self.test_autores
        }
        mock_collection.find_one.return_value = mock_artigo
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_id(str(artigo_id))
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result['titulo'], self.test_titulo)
        mock_get_collection.assert_called_once_with('artigos')
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_id_converts_objectid_to_string(self, mock_get_collection):
        """Testa se find_by_id converte ObjectId para string"""
        # Arrange
        mock_collection = MagicMock()
        artigo_id = ObjectId()
        edicao_id = ObjectId(self.test_edicao_id)
        mock_artigo = {
            '_id': artigo_id,
            'edicao_id': edicao_id,
            'titulo': self.test_titulo
        }
        mock_collection.find_one.return_value = mock_artigo
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_id(str(artigo_id))
        
        # Assert
        self.assertIsInstance(result['_id'], str)
        self.assertIsInstance(result['edicao_id'], str)
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_id_returns_none_when_not_found(self, mock_get_collection):
        """Testa se find_by_id retorna None quando artigo não existe"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_id(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_find_by_id_returns_none_on_exception(self, mock_get_collection):
        """Testa se find_by_id retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.find_by_id(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.artigo.mongo.get_collection')
    @patch('builtins.print')
    def test_find_by_id_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se find_by_id imprime erro quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        Artigo.find_by_id(str(ObjectId()))
        
        # Assert
        self.assertTrue(any("Erro ao buscar artigo por ID" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES COM MOCKS - update() ====================
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_update_updates_artigo_successfully(self, mock_get_collection):
        """Testa se update() atualiza o artigo com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        artigo_id = str(ObjectId())
        update_data = {'titulo': 'Novo Título'}
        
        # Act
        result = Artigo.update(artigo_id, update_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.modified_count, 1)
        mock_get_collection.assert_called_once_with('artigos')
        mock_collection.update_one.assert_called_once()
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_update_calls_update_one_with_correct_parameters(self, mock_get_collection):
        """Testa se update() chama update_one com parâmetros corretos"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.update_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        artigo_id = str(ObjectId())
        update_data = {'titulo': 'Novo Título', 'resumo': 'Novo Resumo'}
        
        # Act
        Artigo.update(artigo_id, update_data)
        
        # Assert
        call_args = mock_collection.update_one.call_args[0]
        self.assertIsInstance(call_args[0]['_id'], ObjectId)
        self.assertEqual(call_args[1], {'$set': update_data})
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_update_returns_none_on_exception(self, mock_get_collection):
        """Testa se update() retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.update_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.update(str(ObjectId()), {'titulo': 'Teste'})
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.artigo.mongo.get_collection')
    @patch('builtins.print')
    def test_update_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se update() imprime erro quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.update_one.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        Artigo.update(str(ObjectId()), {'titulo': 'Teste'})
        
        # Assert
        self.assertTrue(any("Erro ao atualizar artigo" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES COM MOCKS - delete() ====================
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_delete_deletes_artigo_successfully(self, mock_get_collection):
        """Testa se delete() deleta o artigo com sucesso"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        artigo_id = str(ObjectId())
        
        # Act
        result = Artigo.delete(artigo_id)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.deleted_count, 1)
        mock_get_collection.assert_called_once_with('artigos')
        mock_collection.delete_one.assert_called_once()
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_delete_calls_delete_one_with_correct_id(self, mock_get_collection):
        """Testa se delete() chama delete_one com ID correto"""
        # Arrange
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.delete_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        artigo_id = str(ObjectId())
        
        # Act
        Artigo.delete(artigo_id)
        
        # Assert
        call_args = mock_collection.delete_one.call_args[0][0]
        self.assertIsInstance(call_args['_id'], ObjectId)
    
    @patch('app.models.artigo.mongo.get_collection')
    def test_delete_returns_none_on_exception(self, mock_get_collection):
        """Testa se delete() retorna None quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.delete_one.side_effect = Exception("Erro de conexão")
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Artigo.delete(str(ObjectId()))
        
        # Assert
        self.assertIsNone(result)
    
    @patch('app.models.artigo.mongo.get_collection')
    @patch('builtins.print')
    def test_delete_prints_error_on_exception(self, mock_print, mock_get_collection):
        """Testa se delete() imprime erro quando ocorre exceção"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.delete_one.side_effect = Exception("Erro de teste")
        mock_get_collection.return_value = mock_collection
        
        # Act
        Artigo.delete(str(ObjectId()))
        
        # Assert
        self.assertTrue(any("Erro ao deletar artigo" in str(call) 
                           for call in mock_print.call_args_list))


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
