from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.services.auth import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('nome'):
        return jsonify({'error': 'Email e nome são obrigatórios'}), 400
    
    # Verificar se usuário já existe
    if Usuario.find_by_email(data['email']):
        return jsonify({'error': 'Usuário já existe'}), 409
    
    # Criar novo usuário (não-admin por padrão)
    usuario = Usuario(
        email=data['email'],
        nome=data['nome'],
        is_admin=data.get('is_admin', False)
    )
    
    result = usuario.save()
    
    # Gerar token JWT
    token = auth_service.generate_token(str(result.inserted_id), usuario.is_admin)
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'token': token,
        'user': usuario.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de usuário com username/password"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    username = data.get('username') or data.get('email')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username e senha são obrigatórios'}), 400
    
    # Buscar usuário - aceitar tanto 'admin' quanto 'admin@admin.com'
    usuario_data = None
    if username == 'admin':
        usuario_data = Usuario.find_by_email('admin@admin.com')
    else:
        usuario_data = Usuario.find_by_email(username)
    
    if not usuario_data:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # Verificar senha (simplificado para teste)
    senha_db = usuario_data.get('senha', '')
    if senha_db != password:
        return jsonify({'error': 'Senha incorreta'}), 401
    
    # Gerar token JWT
    token = auth_service.generate_token(str(usuario_data['_id']), usuario_data.get('is_admin', False))
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': {
            'email': usuario_data['email'],
            'nome': usuario_data['nome'],
            'is_admin': usuario_data.get('is_admin', False)
        }
    })

@auth_bp.route('/me', methods=['GET'])
@auth_service.auth_required
def get_me():
    """Retorna informações do usuário atual"""
    token = request.headers.get('Authorization')[7:]  # Remove 'Bearer '
    payload = auth_service.verify_token(token)
    
    # Em uma implementação real, buscaríamos o usuário do banco
    return jsonify({
        'user_id': payload['user_id'],
        'is_admin': payload['is_admin']
    })

# Rota protegida de exemplo para admin
@auth_bp.route('/admin-test', methods=['GET'])
@auth_service.admin_required
def admin_test():
    return jsonify({'message': 'Acesso admin autorizado!'})
