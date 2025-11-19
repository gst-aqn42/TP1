"""
Testes unitários para o serviço de Email (EmailService)
Testa as funcionalidades com mocks para isolar dependências externas (SMTP)
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.services.email_service import EmailService, enviar_email_confirmacao_inscricao


class TestEmailService(unittest.TestCase):
    """Suite de testes unitários para o serviço de Email"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.email_service = EmailService()
        self.test_destinatario = "leitor@example.com"
        self.test_nome_autor = "Dr. João Silva"
        self.test_artigo = {
            'titulo': 'Análise de Sistemas Distribuídos',
            'autores': [
                {'nome': 'Dr. João Silva', 'email': 'joao@univ.edu'},
                {'nome': 'Dra. Maria Santos', 'email': 'maria@univ.edu'}
            ],
            'resumo': 'Este artigo apresenta uma análise detalhada...'
        }
    
    # ==================== TESTES DE __init__ (Construtor) ====================
    
    def test_init_sets_default_smtp_server(self):
        """Testa se __init__ define servidor SMTP padrão"""
        # Arrange & Act
        with patch.dict(os.environ, {}, clear=True):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.smtp_server, 'smtp.gmail.com')
    
    def test_init_sets_default_smtp_port(self):
        """Testa se __init__ define porta SMTP padrão"""
        # Arrange & Act
        with patch.dict(os.environ, {}, clear=True):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.smtp_port, 587)
    
    def test_init_sets_empty_email_user_by_default(self):
        """Testa se __init__ define email_user vazio por padrão"""
        # Arrange & Act
        with patch.dict(os.environ, {}, clear=True):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.email_user, '')
    
    def test_init_sets_empty_email_password_by_default(self):
        """Testa se __init__ define email_password vazio por padrão"""
        # Arrange & Act
        with patch.dict(os.environ, {}, clear=True):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.email_password, '')
    
    def test_init_reads_smtp_server_from_env(self):
        """Testa se __init__ lê servidor SMTP de variável de ambiente"""
        # Arrange & Act
        with patch.dict(os.environ, {'SMTP_SERVER': 'smtp.custom.com'}):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.smtp_server, 'smtp.custom.com')
    
    def test_init_reads_smtp_port_from_env(self):
        """Testa se __init__ lê porta SMTP de variável de ambiente"""
        # Arrange & Act
        with patch.dict(os.environ, {'SMTP_PORT': '465'}):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.smtp_port, 465)
    
    def test_init_reads_email_credentials_from_env(self):
        """Testa se __init__ lê credenciais de email de variáveis de ambiente"""
        # Arrange & Act
        with patch.dict(os.environ, {
            'EMAIL_USER': 'test@example.com',
            'EMAIL_PASSWORD': 'secret123'
        }):
            service = EmailService()
        
        # Assert
        self.assertEqual(service.email_user, 'test@example.com')
        self.assertEqual(service.email_password, 'secret123')
    
    # ==================== TESTES DE enviar_notificacao() ====================
    
    @patch('builtins.print')
    def test_enviar_notificacao_prints_simulation_message(self, mock_print):
        """Testa se enviar_notificacao imprime mensagem de simulação"""
        # Arrange
        service = EmailService()
        
        # Act
        result = service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            self.test_artigo
        )
        
        # Assert
        self.assertTrue(any("Simulando envio de email" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_notificacao_includes_correct_subject(self, mock_print):
        """Testa se enviar_notificacao inclui assunto correto"""
        # Arrange
        service = EmailService()
        
        # Act
        service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            self.test_artigo
        )
        
        # Assert
        self.assertTrue(any(f"Novo artigo publicado de {self.test_nome_autor}" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_notificacao_includes_article_title(self, mock_print):
        """Testa se enviar_notificacao inclui título do artigo"""
        # Arrange
        service = EmailService()
        
        # Act
        service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            self.test_artigo
        )
        
        # Assert
        self.assertTrue(any(self.test_artigo['titulo'] in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_notificacao_includes_authors_list(self, mock_print):
        """Testa se enviar_notificacao inclui lista de autores"""
        # Arrange
        service = EmailService()
        
        # Act
        service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            self.test_artigo
        )
        
        # Assert
        # Verifica se pelo menos um dos nomes de autores aparece
        print_calls_str = str(mock_print.call_args_list)
        self.assertTrue(
            'Dr. João Silva' in print_calls_str or 
            'Dra. Maria Santos' in print_calls_str
        )
    
    @patch('builtins.print')
    def test_enviar_notificacao_returns_true_on_success(self, mock_print):
        """Testa se enviar_notificacao retorna True em caso de sucesso"""
        # Arrange
        service = EmailService()
        
        # Act
        result = service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            self.test_artigo
        )
        
        # Assert
        self.assertTrue(result)
    
    @patch('builtins.print')
    def test_enviar_notificacao_handles_article_without_resumo(self, mock_print):
        """Testa se enviar_notificacao lida com artigo sem resumo"""
        # Arrange
        service = EmailService()
        artigo_sem_resumo = {
            'titulo': 'Teste',
            'autores': [{'nome': 'Autor', 'email': 'autor@test.com'}]
        }
        
        # Act
        result = service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            artigo_sem_resumo
        )
        
        # Assert
        self.assertTrue(result)
        self.assertTrue(any("Sem resumo" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_notificacao_returns_false_on_exception(self, mock_print):
        """Testa se enviar_notificacao retorna False quando ocorre exceção"""
        # Arrange
        service = EmailService()
        
        # Simula exceção ao acessar título do artigo
        artigo_invalido = None
        
        # Act
        result = service.enviar_notificacao(
            self.test_destinatario,
            self.test_nome_autor,
            artigo_invalido
        )
        
        # Assert
        self.assertFalse(result)
        self.assertTrue(any("Erro ao enviar email" in str(call) 
                           for call in mock_print.call_args_list))
    
    # ==================== TESTES DE enviar_email_confirmacao_inscricao() ====================
    
    @patch('builtins.print')
    def test_enviar_email_confirmacao_prints_simulation_message(self, mock_print):
        """Testa se enviar_email_confirmacao_inscricao imprime mensagem de simulação"""
        # Arrange
        email = "test@example.com"
        
        # Act
        result = enviar_email_confirmacao_inscricao(email)
        
        # Assert
        self.assertTrue(any("Simulando envio de email de confirmação" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_email_confirmacao_includes_correct_subject(self, mock_print):
        """Testa se enviar_email_confirmacao_inscricao inclui assunto correto"""
        # Arrange
        email = "test@example.com"
        
        # Act
        enviar_email_confirmacao_inscricao(email)
        
        # Assert
        self.assertTrue(any("Confirmação de Inscrição" in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_email_confirmacao_prints_recipient_email(self, mock_print):
        """Testa se enviar_email_confirmacao_inscricao imprime email do destinatário"""
        # Arrange
        email = "test@example.com"
        
        # Act
        enviar_email_confirmacao_inscricao(email)
        
        # Assert
        self.assertTrue(any(email in str(call) 
                           for call in mock_print.call_args_list))
    
    @patch('builtins.print')
    def test_enviar_email_confirmacao_returns_true_on_success(self, mock_print):
        """Testa se enviar_email_confirmacao_inscricao retorna True em caso de sucesso"""
        # Arrange
        email = "test@example.com"
        
        # Act
        result = enviar_email_confirmacao_inscricao(email)
        
        # Assert
        self.assertTrue(result)
    
    @patch('builtins.print')
    def test_enviar_email_confirmacao_returns_false_on_exception(self, mock_print):
        """Testa se enviar_email_confirmacao_inscricao retorna False quando ocorre exceção"""
        # Arrange
        # Simula exceção mockando print para lançar erro
        mock_print.side_effect = Exception("Erro simulado")
        
        # Act
        result = enviar_email_confirmacao_inscricao("test@example.com")
        
        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
