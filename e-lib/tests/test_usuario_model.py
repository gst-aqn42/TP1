"""
Testes unitários para o modelo Usuario
Testa as funcionalidades com mocks para isolar dependências do banco de dados
"""

import unittest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.models.usuario import Usuario


class TestUsuarioModel(unittest.TestCase):
    """Suite de testes unitários para o modelo Usuario"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.test_email = "usuario@example.com"
        self.test_nome = "João da Silva"
        self.test_senha = "senha123"
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_creates_usuario_with_required_fields(self):
        """Testa se o construtor cria um usuário com campos obrigatórios"""
        # Arrange & Act
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Assert
        self.assertEqual(usuario.email, self.test_email)
        self.assertEqual(usuario.nome, self.test_nome)
    
    def test_init_creates_usuario_with_all_fields(self):
        """Testa se o construtor cria um usuário com todos os campos"""
        # Arrange & Act
        usuario = Usuario(
            email=self.test_email,
            nome=self.test_nome,
            is_admin=True,
            senha=self.test_senha
        )
        
        # Assert
        self.assertEqual(usuario.email, self.test_email)
        self.assertEqual(usuario.nome, self.test_nome)
        self.assertTrue(usuario.is_admin)
        self.assertEqual(usuario.senha, self.test_senha)
    
    def test_init_sets_is_admin_to_false_by_default(self):
        """Testa se is_admin é False por padrão"""
        # Arrange & Act
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Assert
        self.assertFalse(usuario.is_admin)
    
    def test_init_sets_senha_to_none_by_default(self):
        """Testa se senha é None por padrão"""
        # Arrange & Act
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Assert
        self.assertIsNone(usuario.senha)
    
    def test_init_sets_data_criacao_automatically(self):
        """Testa se data_criacao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(usuario.data_criacao)
        self.assertIsInstance(usuario.data_criacao, datetime)
        self.assertGreaterEqual(usuario.data_criacao, before)
        self.assertLessEqual(usuario.data_criacao, after)
    
    def test_init_creates_default_preferences(self):
        """Testa se preferences é criado com valores padrão"""
        # Arrange & Act
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Assert
        self.assertIsInstance(usuario.preferences, dict)
        self.assertTrue(usuario.preferences['notificacoes_email'])
        self.assertEqual(usuario.preferences['artigos_por_pagina'], 10)
    
    def test_init_admin_user(self):
        """Testa criação de usuário admin"""
        # Arrange & Act
        usuario = Usuario(
            email="admin@test.com",
            nome="Admin",
            is_admin=True,
            senha="admin123"
        )
        
        # Assert
        self.assertTrue(usuario.is_admin)
        self.assertEqual(usuario.senha, "admin123")
    
    # ==================== TESTES DE to_dict ====================
    
    def test_to_dict_returns_dictionary(self):
        """Testa se to_dict retorna um dicionário"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertIsInstance(usuario_dict, dict)
    
    def test_to_dict_contains_all_required_fields(self):
        """Testa se to_dict contém todos os campos obrigatórios"""
        # Arrange
        usuario = Usuario(
            email=self.test_email,
            nome=self.test_nome,
            is_admin=True
        )
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertIn('email', usuario_dict)
        self.assertIn('nome', usuario_dict)
        self.assertIn('is_admin', usuario_dict)
        self.assertIn('data_criacao', usuario_dict)
        self.assertIn('preferences', usuario_dict)
    
    def test_to_dict_has_correct_email(self):
        """Testa se to_dict retorna o email correto"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertEqual(usuario_dict['email'], self.test_email)
    
    def test_to_dict_has_correct_nome(self):
        """Testa se to_dict retorna o nome correto"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertEqual(usuario_dict['nome'], self.test_nome)
    
    def test_to_dict_has_correct_is_admin(self):
        """Testa se to_dict retorna o is_admin correto"""
        # Arrange
        usuario_admin = Usuario(email=self.test_email, nome=self.test_nome, is_admin=True)
        usuario_normal = Usuario(email=self.test_email, nome=self.test_nome, is_admin=False)
        
        # Act
        admin_dict = usuario_admin.to_dict()
        normal_dict = usuario_normal.to_dict()
        
        # Assert
        self.assertTrue(admin_dict['is_admin'])
        self.assertFalse(normal_dict['is_admin'])
    
    def test_to_dict_converts_data_criacao_to_isoformat(self):
        """Testa se to_dict converte data_criacao para formato ISO"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertIsInstance(usuario_dict['data_criacao'], str)
        self.assertIn('T', usuario_dict['data_criacao'])
    
    def test_to_dict_includes_preferences(self):
        """Testa se to_dict inclui preferences"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertIn('preferences', usuario_dict)
        self.assertIsInstance(usuario_dict['preferences'], dict)
    
    def test_to_dict_does_not_include_senha(self):
        """Testa se to_dict NÃO inclui a senha (segurança)"""
        # Arrange
        usuario = Usuario(
            email=self.test_email,
            nome=self.test_nome,
            senha=self.test_senha
        )
        
        # Act
        usuario_dict = usuario.to_dict()
        
        # Assert
        self.assertNotIn('senha', usuario_dict)
    
    # ==================== TESTES COM MOCKS - save() ====================
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_save_inserts_usuario_successfully(self, mock_get_collection):
        """Testa se save() insere o usuário com sucesso"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = "507f1f77bcf86cd799439011"
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = usuario.save()
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.inserted_id, mock_result.inserted_id)
        mock_get_collection.assert_called_once_with('usuarios')
        mock_collection.insert_one.assert_called_once()
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_save_calls_insert_one_with_correct_data(self, mock_get_collection):
        """Testa se save() chama insert_one com os dados corretos"""
        # Arrange
        usuario = Usuario(
            email=self.test_email,
            nome=self.test_nome,
            is_admin=True
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        usuario.save()
        
        # Assert
        call_args = mock_collection.insert_one.call_args[0][0]
        self.assertEqual(call_args['email'], self.test_email)
        self.assertEqual(call_args['nome'], self.test_nome)
        self.assertTrue(call_args['is_admin'])
        self.assertIn('preferences', call_args)
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_save_includes_senha_when_provided(self, mock_get_collection):
        """Testa se save() inclui senha quando fornecida"""
        # Arrange
        usuario = Usuario(
            email=self.test_email,
            nome=self.test_nome,
            senha=self.test_senha
        )
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        usuario.save()
        
        # Assert
        call_args = mock_collection.insert_one.call_args[0][0]
        self.assertIn('senha', call_args)
        self.assertEqual(call_args['senha'], self.test_senha)
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_save_does_not_include_senha_when_none(self, mock_get_collection):
        """Testa se save() não inclui senha quando None"""
        # Arrange
        usuario = Usuario(email=self.test_email, nome=self.test_nome)
        
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        usuario.save()
        
        # Assert
        call_args = mock_collection.insert_one.call_args[0][0]
        self.assertNotIn('senha', call_args)
    
    # ==================== TESTES COM MOCKS - find_by_email() ====================
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_find_by_email_returns_usuario_when_found(self, mock_get_collection):
        """Testa se find_by_email retorna usuário quando encontrado"""
        # Arrange
        mock_collection = MagicMock()
        mock_usuario = {
            'email': self.test_email,
            'nome': self.test_nome,
            'is_admin': False
        }
        mock_collection.find_one.return_value = mock_usuario
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Usuario.find_by_email(self.test_email)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result['email'], self.test_email)
        mock_get_collection.assert_called_once_with('usuarios')
        mock_collection.find_one.assert_called_once_with({'email': self.test_email})
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_find_by_email_returns_none_when_not_found(self, mock_get_collection):
        """Testa se find_by_email retorna None quando não encontrado"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_get_collection.return_value = mock_collection
        
        # Act
        result = Usuario.find_by_email("naoexiste@test.com")
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES COM MOCKS - create_admin_user() ====================
    
    @patch('app.models.usuario.mongo.get_collection')
    @patch('builtins.print')
    def test_create_admin_user_creates_when_not_exists(self, mock_print, mock_get_collection):
        """Testa se create_admin_user cria admin quando não existe"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None  # Admin não existe
        mock_result = MagicMock()
        mock_collection.insert_one.return_value = mock_result
        mock_get_collection.return_value = mock_collection
        
        # Act
        Usuario.create_admin_user()
        
        # Assert
        mock_collection.insert_one.assert_called_once()
        self.assertTrue(any("Usuário admin criado" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('app.models.usuario.mongo.get_collection')
    def test_create_admin_user_does_not_create_when_exists(self, mock_get_collection):
        """Testa se create_admin_user não cria admin quando já existe"""
        # Arrange
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {
            'email': 'admin@simple-lib.com',
            'nome': 'Administrador'
        }
        mock_get_collection.return_value = mock_collection
        
        # Act
        Usuario.create_admin_user()
        
        # Assert
        mock_collection.insert_one.assert_not_called()


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
