import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

class AuthService:
    @staticmethod
    def generate_token(user_id, is_admin=False):
        """Gera um token JWT para o usuário"""
        payload = {
            'user_id': user_id,
            'is_admin': is_admin,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """Verifica e decodifica um token JWT"""
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def admin_required(f):
        """Decorator para rotas que requerem autenticação admin"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'error': 'Token de autorização necessário'}), 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = AuthService.verify_token(token)
            
            if not payload:
                return jsonify({'error': 'Token inválido ou expirado'}), 401
            
            if not payload.get('is_admin'):
                return jsonify({'error': 'Acesso restrito a administradores'}), 403
            
            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def auth_required(f):
        """Decorator para rotas que requerem autenticação"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'error': 'Token de autorização necessário'}), 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = AuthService.verify_token(token)
            
            if not payload:
                return jsonify({'error': 'Token inválido ou expirado'}), 401
            
            return f(*args, **kwargs)
        return decorated

auth_service = AuthService()
