"""
Testes unitários para o serviço de autenticação (AuthService)
Testa as funcionalidades de geração e verificação de tokens JWT
"""
import os
import sys
import unittest
import jwt
import datetime
from unittest.mock import Mock, patch, MagicMock
from flask import Flask, jsonify
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/app')))
from services.auth import AuthService


class TestAuthService(unittest.TestCase):
    """Suite de testes para AuthService"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret-key-12345'
        self.app.config['TESTING'] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        self.test_user_id = 'user123'
        self.test_admin_id = 'admin456'
    
    def tearDown(self):
        """Limpeza após cada teste"""
        self.ctx.pop()
    
    # ==================== TESTES DE generate_token ====================
    
    def test_generate_token_returns_valid_jwt(self):
        """Testa se generate_token retorna um token JWT válido"""
        # Arrange
        user_id = self.test_user_id
        is_admin = False
        
        # Act
        token = AuthService.generate_token(user_id, is_admin)
        
        # Assert
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        # Verifica se o token tem 3 partes separadas por '.'
        self.assertEqual(len(token.split('.')), 3)
    
    def test_generate_token_contains_correct_user_id(self):
        """Testa se o token contém o user_id correto no payload"""
        # Arrange
        user_id = self.test_user_id
        is_admin = False
        
        # Act
        token = AuthService.generate_token(user_id, is_admin)
        payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Assert
        self.assertEqual(payload['user_id'], user_id)
    
    def test_generate_token_contains_correct_is_admin_flag(self):
        """Testa se o token contém a flag is_admin correta"""
        # Arrange & Act
        admin_token = AuthService.generate_token(self.test_admin_id, True)
        user_token = AuthService.generate_token(self.test_user_id, False)
        
        admin_payload = jwt.decode(admin_token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        user_payload = jwt.decode(user_token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Assert
        self.assertTrue(admin_payload['is_admin'])
        self.assertFalse(user_payload['is_admin'])
    
    def test_generate_token_has_expiration_time(self):
        """Testa se o token tem tempo de expiração (exp)"""
        # Arrange
        user_id = self.test_user_id
        
        # Act
        token = AuthService.generate_token(user_id, False)
        payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Assert
        self.assertIn('exp', payload)
        self.assertIsInstance(payload['exp'], int)
    
    def test_generate_token_expires_in_one_day(self):
        """Testa se o token expira em aproximadamente 1 dia"""
        # Arrange
        user_id = self.test_user_id
        now = datetime.datetime.utcnow()
        
        # Act
        token = AuthService.generate_token(user_id, False)
        payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Assert
        exp_time = datetime.datetime.fromtimestamp(payload['exp'])
        time_diff = exp_time - now
        # Verifica se está entre 23h59min e 24h01min
        self.assertGreater(time_diff.total_seconds(), 23 * 3600 + 59 * 60)
        self.assertLess(time_diff.total_seconds(), 24 * 3600 + 60)
    
    def test_generate_token_has_issued_at_time(self):
        """Testa se o token tem tempo de emissão (iat)"""
        # Arrange
        user_id = self.test_user_id
        
        # Act
        token = AuthService.generate_token(user_id, False)
        payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Assert
        self.assertIn('iat', payload)
        self.assertIsInstance(payload['iat'], int)
    
    def test_generate_token_default_is_admin_is_false(self):
        """Testa se is_admin é False por padrão quando não especificado"""
        # Arrange
        user_id = self.test_user_id
        
        # Act
        token = AuthService.generate_token(user_id)
        payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Assert
        self.assertFalse(payload['is_admin'])
    
    # ==================== TESTES DE verify_token ====================
    
    def test_verify_token_returns_payload_for_valid_token(self):
        """Testa se verify_token retorna o payload para um token válido"""
        # Arrange
        user_id = self.test_user_id
        is_admin = True
        token = AuthService.generate_token(user_id, is_admin)
        
        # Act
        payload = AuthService.verify_token(token)
        
        # Assert
        self.assertIsNotNone(payload)
        self.assertEqual(payload['user_id'], user_id)
        self.assertEqual(payload['is_admin'], is_admin)
    
    def test_verify_token_returns_none_for_expired_token(self):
        """Testa se verify_token retorna None para token expirado"""
        # Arrange
        expired_payload = {
            'user_id': self.test_user_id,
            'is_admin': False,
            'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow() - datetime.timedelta(days=2)
        }
        expired_token = jwt.encode(expired_payload, self.app.config['SECRET_KEY'], algorithm='HS256')
        
        # Act
        result = AuthService.verify_token(expired_token)
        
        # Assert
        self.assertIsNone(result)
    
    def test_verify_token_returns_none_for_invalid_signature(self):
        """Testa se verify_token retorna None para token com assinatura inválida"""
        # Arrange
        payload = {
            'user_id': self.test_user_id,
            'is_admin': False,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        # Token assinado com chave diferente
        invalid_token = jwt.encode(payload, 'wrong-secret-key', algorithm='HS256')
        
        # Act
        result = AuthService.verify_token(invalid_token)
        
        # Assert
        self.assertIsNone(result)
    
    def test_verify_token_returns_none_for_malformed_token(self):
        """Testa se verify_token retorna None para token malformado"""
        # Arrange
        malformed_token = 'this.is.not.a.valid.jwt.token'
        
        # Act
        result = AuthService.verify_token(malformed_token)
        
        # Assert
        self.assertIsNone(result)
    
    def test_verify_token_returns_none_for_empty_token(self):
        """Testa se verify_token retorna None para token vazio"""
        # Arrange
        empty_token = ''
        
        # Act
        result = AuthService.verify_token(empty_token)
        
        # Assert
        self.assertIsNone(result)
    
    # ==================== TESTES DE admin_required ====================
    
    def test_admin_required_allows_valid_admin_token(self):
        """Testa se admin_required permite acesso com token admin válido"""
        # Arrange
        admin_token = AuthService.generate_token(self.test_admin_id, is_admin=True)
        
        @AuthService.admin_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {admin_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 200)
    
    def test_admin_required_rejects_non_admin_token(self):
        """Testa se admin_required rejeita token de usuário não-admin"""
        # Arrange
        user_token = AuthService.generate_token(self.test_user_id, is_admin=False)
        
        @AuthService.admin_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {user_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 403)
            self.assertIn('Acesso restrito a administradores', response[0].get_json()['error'])
    
    def test_admin_required_rejects_missing_token(self):
        """Testa se admin_required rejeita requisição sem token"""
        # Arrange
        @AuthService.admin_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context():
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 401)
            self.assertIn('Token de autorização necessário', response[0].get_json()['error'])
    
    def test_admin_required_rejects_expired_token(self):
        """Testa se admin_required rejeita token expirado"""
        # Arrange
        expired_payload = {
            'user_id': self.test_admin_id,
            'is_admin': True,
            'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1)
        }
        expired_token = jwt.encode(expired_payload, self.app.config['SECRET_KEY'], algorithm='HS256')
        
        @AuthService.admin_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {expired_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 401)
            self.assertIn('Token inválido ou expirado', response[0].get_json()['error'])
    
    def test_admin_required_handles_bearer_prefix(self):
        """Testa se admin_required remove corretamente o prefixo 'Bearer '"""
        # Arrange
        admin_token = AuthService.generate_token(self.test_admin_id, is_admin=True)
        
        @AuthService.admin_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {admin_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 200)
    
    def test_admin_required_handles_token_without_bearer(self):
        """Testa se admin_required funciona com token sem prefixo Bearer"""
        # Arrange
        admin_token = AuthService.generate_token(self.test_admin_id, is_admin=True)
        
        @AuthService.admin_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': admin_token}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 200)
    
    # ==================== TESTES DE auth_required ====================
    
    def test_auth_required_allows_valid_user_token(self):
        """Testa se auth_required permite acesso com token de usuário válido"""
        # Arrange
        user_token = AuthService.generate_token(self.test_user_id, is_admin=False)
        
        @AuthService.auth_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {user_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 200)
    
    def test_auth_required_allows_admin_token(self):
        """Testa se auth_required permite acesso com token admin"""
        # Arrange
        admin_token = AuthService.generate_token(self.test_admin_id, is_admin=True)
        
        @AuthService.auth_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {admin_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 200)
    
    def test_auth_required_rejects_missing_token(self):
        """Testa se auth_required rejeita requisição sem token"""
        # Arrange
        @AuthService.auth_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context():
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 401)
            self.assertIn('Token de autorização necessário', response[0].get_json()['error'])
    
    def test_auth_required_rejects_expired_token(self):
        """Testa se auth_required rejeita token expirado"""
        # Arrange
        expired_payload = {
            'user_id': self.test_user_id,
            'is_admin': False,
            'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1)
        }
        expired_token = jwt.encode(expired_payload, self.app.config['SECRET_KEY'], algorithm='HS256')
        
        @AuthService.auth_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {expired_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 401)
            self.assertIn('Token inválido ou expirado', response[0].get_json()['error'])
    
    def test_auth_required_rejects_invalid_token(self):
        """Testa se auth_required rejeita token inválido"""
        # Arrange
        invalid_token = 'invalid.token.here'
        
        @AuthService.auth_required
        def protected_route():
            return jsonify({'message': 'success'}), 200
        
        with self.app.test_request_context(
            headers={'Authorization': f'Bearer {invalid_token}'}
        ):
            # Act
            response = protected_route()
            
            # Assert
            self.assertEqual(response[1], 401)
            self.assertIn('Token inválido ou expirado', response[0].get_json()['error'])


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)
