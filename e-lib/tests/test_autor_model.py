"""
Testes unitários para o modelo Autor
Testa as funcionalidades que podem ser isoladas sem depender do banco de dados
"""

import unittest
import sys
import os
from datetime import datetime

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.models.autor import Autor


class TestAutorModel(unittest.TestCase):
    """Suite de testes unitários para o modelo Autor"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.test_nome = "Dr. João Silva"
        self.test_email = "joao.silva@university.edu"
        self.test_instituicao = "Universidade Federal de Minas Gerais"
        self.test_orcid = "0000-0002-1825-0097"
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_creates_autor_with_required_fields(self):
        """Testa se o construtor cria um autor com campos obrigatórios"""
        # Arrange & Act
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Assert
        self.assertEqual(autor.nome, self.test_nome)
        self.assertEqual(autor.email, self.test_email)
    
    def test_init_creates_autor_with_all_fields(self):
        """Testa se o construtor cria um autor com todos os campos"""
        # Arrange & Act
        autor = Autor(
            nome=self.test_nome,
            email=self.test_email,
            instituicao=self.test_instituicao,
            orcid=self.test_orcid
        )
        
        # Assert
        self.assertEqual(autor.nome, self.test_nome)
        self.assertEqual(autor.email, self.test_email)
        self.assertEqual(autor.instituicao, self.test_instituicao)
        self.assertEqual(autor.orcid, self.test_orcid)
    
    def test_init_sets_instituicao_to_none_by_default(self):
        """Testa se instituicao é None por padrão"""
        # Arrange & Act
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Assert
        self.assertIsNone(autor.instituicao)
    
    def test_init_sets_orcid_to_none_by_default(self):
        """Testa se orcid é None por padrão"""
        # Arrange & Act
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Assert
        self.assertIsNone(autor.orcid)
    
    def test_init_creates_empty_artigos_list(self):
        """Testa se artigos é uma lista vazia por padrão"""
        # Arrange & Act
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Assert
        self.assertEqual(autor.artigos, [])
        self.assertIsInstance(autor.artigos, list)
    
    def test_init_sets_data_criacao_automatically(self):
        """Testa se data_criacao é definida automaticamente"""
        # Arrange
        before = datetime.utcnow()
        
        # Act
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        after = datetime.utcnow()
        
        # Assert
        self.assertIsNotNone(autor.data_criacao)
        self.assertIsInstance(autor.data_criacao, datetime)
        self.assertGreaterEqual(autor.data_criacao, before)
        self.assertLessEqual(autor.data_criacao, after)
    
    # ==================== TESTES DE to_dict ====================
    
    def test_to_dict_returns_dictionary(self):
        """Testa se to_dict retorna um dicionário"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertIsInstance(autor_dict, dict)
    
    def test_to_dict_contains_all_required_fields(self):
        """Testa se to_dict contém todos os campos obrigatórios"""
        # Arrange
        autor = Autor(
            nome=self.test_nome,
            email=self.test_email,
            instituicao=self.test_instituicao,
            orcid=self.test_orcid
        )
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertIn('nome', autor_dict)
        self.assertIn('email', autor_dict)
        self.assertIn('instituicao', autor_dict)
        self.assertIn('orcid', autor_dict)
        self.assertIn('artigos', autor_dict)
        self.assertIn('data_criacao', autor_dict)
    
    def test_to_dict_has_correct_nome(self):
        """Testa se to_dict retorna o nome correto"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertEqual(autor_dict['nome'], self.test_nome)
    
    def test_to_dict_has_correct_email(self):
        """Testa se to_dict retorna o email correto"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertEqual(autor_dict['email'], self.test_email)
    
    def test_to_dict_has_correct_instituicao(self):
        """Testa se to_dict retorna a instituição correta"""
        # Arrange
        autor = Autor(
            nome=self.test_nome,
            email=self.test_email,
            instituicao=self.test_instituicao
        )
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertEqual(autor_dict['instituicao'], self.test_instituicao)
    
    def test_to_dict_has_correct_orcid(self):
        """Testa se to_dict retorna o orcid correto"""
        # Arrange
        autor = Autor(
            nome=self.test_nome,
            email=self.test_email,
            orcid=self.test_orcid
        )
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertEqual(autor_dict['orcid'], self.test_orcid)
    
    def test_to_dict_has_empty_artigos_list(self):
        """Testa se to_dict retorna lista vazia de artigos"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertEqual(autor_dict['artigos'], [])
    
    def test_to_dict_converts_data_criacao_to_isoformat(self):
        """Testa se to_dict converte data_criacao para formato ISO"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertIsInstance(autor_dict['data_criacao'], str)
        self.assertIn('T', autor_dict['data_criacao'])
    
    def test_to_dict_with_none_instituicao(self):
        """Testa se to_dict lida corretamente com instituicao None"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email, instituicao=None)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertIsNone(autor_dict['instituicao'])
    
    def test_to_dict_with_none_orcid(self):
        """Testa se to_dict lida corretamente com orcid None"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email, orcid=None)
        
        # Act
        autor_dict = autor.to_dict()
        
        # Assert
        self.assertIsNone(autor_dict['orcid'])
    
    # ==================== TESTES DE VALIDAÇÃO DE DADOS ====================
    
    def test_autor_accepts_special_characters_in_nome(self):
        """Testa se autor aceita caracteres especiais no nome"""
        # Arrange
        nome_especial = "Dr. José Müller-López"
        
        # Act
        autor = Autor(nome=nome_especial, email=self.test_email)
        
        # Assert
        self.assertEqual(autor.nome, nome_especial)
        self.assertEqual(autor.to_dict()['nome'], nome_especial)
    
    def test_autor_accepts_long_instituicao_name(self):
        """Testa se autor aceita nome longo de instituição"""
        # Arrange
        instituicao_longa = "Instituto de Ciências Matemáticas e de Computação da Universidade de São Paulo"
        
        # Act
        autor = Autor(
            nome=self.test_nome,
            email=self.test_email,
            instituicao=instituicao_longa
        )
        
        # Assert
        self.assertEqual(autor.instituicao, instituicao_longa)
    
    def test_autor_artigos_list_is_mutable(self):
        """Testa se a lista de artigos pode ser modificada"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        artigo_id = "507f1f77bcf86cd799439011"
        
        # Act
        autor.artigos.append(artigo_id)
        
        # Assert
        self.assertEqual(len(autor.artigos), 1)
        self.assertIn(artigo_id, autor.artigos)
    
    def test_autor_preserves_multiple_artigo_ids(self):
        """Testa se autor preserva múltiplos IDs de artigos"""
        # Arrange
        autor = Autor(nome=self.test_nome, email=self.test_email)
        artigo_ids = ["id1", "id2", "id3"]
        
        # Act
        autor.artigos = artigo_ids.copy()
        
        # Assert
        self.assertEqual(len(autor.artigos), 3)
        self.assertEqual(autor.artigos, artigo_ids)
        self.assertEqual(autor.to_dict()['artigos'], artigo_ids)
    
    def test_autor_handles_valid_orcid_format(self):
        """Testa se autor aceita formato válido de ORCID"""
        # Arrange
        valid_orcid = "0000-0002-1825-0097"
        
        # Act
        autor = Autor(
            nome=self.test_nome,
            email=self.test_email,
            orcid=valid_orcid
        )
        
        # Assert
        self.assertEqual(autor.orcid, valid_orcid)
    
    def test_autor_preserves_email_format(self):
        """Testa se autor preserva o formato do email"""
        # Arrange
        emails = [
            "test@example.com",
            "user.name@university.edu.br",
            "test+tag@domain.co.uk"
        ]
        
        for email in emails:
            # Act
            autor = Autor(nome=self.test_nome, email=email)
            
            # Assert
            self.assertEqual(autor.email, email)
            self.assertEqual(autor.to_dict()['email'], email)


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
