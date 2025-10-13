from flask import Blueprint, request, jsonify
from app.services.database import mongo
from app.services.email_service import enviar_email_confirmacao_inscricao
from datetime import datetime
import re

inscricoes_bp = Blueprint('inscricoes', __name__)

def validar_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@inscricoes_bp.route('', methods=['POST'])
@inscricoes_bp.route('/', methods=['POST'])
def criar_inscricao():
    """Cria uma nova inscrição para receber notificações"""
    try:
        data = request.get_json()
        print(f"📧 Inscrição recebida: {data}")
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        email = data['email'].strip().lower()
        
        # Validar formato do email
        if not validar_email(email):
            return jsonify({'error': 'Email inválido'}), 400
        
        # Verificar se já existe
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricao_existente = inscricoes_collection.find_one({'email': email})
        
        if inscricao_existente:
            # Se já existe mas está inativo, reativar
            if not inscricao_existente.get('ativo', True):
                inscricoes_collection.update_one(
                    {'email': email},
                    {'$set': {'ativo': True, 'data_reativacao': datetime.utcnow()}}
                )
                print(f"✅ Inscrição reativada: {email}")
                return jsonify({
                    'message': 'Inscrição reativada com sucesso!',
                    'email': email
                }), 200
            else:
                print(f"ℹ️  Email já inscrito: {email}")
                return jsonify({
                    'message': 'Este email já está inscrito',
                    'email': email
                }), 200
        
        # Criar nova inscrição
        inscricao_data = {
            'email': email,
            'ativo': True,
            'data_inscricao': datetime.utcnow(),
            'notificacoes_enviadas': 0
        }
        
        result = inscricoes_collection.insert_one(inscricao_data)
        print(f"✅ Nova inscrição criada: {email} (ID: {result.inserted_id})")
        
        # Tentar enviar email de confirmação
        try:
            enviar_email_confirmacao_inscricao(email)
            print(f"📧 Email de confirmação enviado para: {email}")
        except Exception as e:
            print(f"⚠️  Erro ao enviar email de confirmação: {e}")
            # Não falha a inscrição se o email não puder ser enviado
        
        return jsonify({
            'message': 'Inscrição realizada com sucesso!',
            'email': email,
            'inscricao_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        print(f"❌ Erro ao criar inscrição: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@inscricoes_bp.route('', methods=['GET'])
@inscricoes_bp.route('/', methods=['GET'])
def listar_inscricoes():
    """Lista todas as inscrições ativas"""
    try:
        inscricoes_collection = mongo.get_collection('inscricoes')
        inscricoes = list(inscricoes_collection.find({'ativo': True}))
        
        # Converter ObjectId para string
        for inscricao in inscricoes:
            inscricao['_id'] = str(inscricao['_id'])
        
        print(f"📋 Listando {len(inscricoes)} inscrições ativas")
        return jsonify(inscricoes)
        
    except Exception as e:
        print(f"❌ Erro ao listar inscrições: {e}")
        return jsonify({'error': str(e)}), 500

@inscricoes_bp.route('/<email>', methods=['DELETE'])
def cancelar_inscricao(email):
    """Cancela uma inscrição (marca como inativo)"""
    try:
        email = email.strip().lower()
        print(f"🗑️  Cancelando inscrição: {email}")
        
        inscricoes_collection = mongo.get_collection('inscricoes')
        result = inscricoes_collection.update_one(
            {'email': email},
            {'$set': {'ativo': False, 'data_cancelamento': datetime.utcnow()}}
        )
        
        if result.modified_count > 0:
            print(f"✅ Inscrição cancelada: {email}")
            return jsonify({'message': 'Inscrição cancelada com sucesso'})
        else:
            print(f"⚠️  Inscrição não encontrada: {email}")
            return jsonify({'error': 'Inscrição não encontrada'}), 404
            
    except Exception as e:
        print(f"❌ Erro ao cancelar inscrição: {e}")
        return jsonify({'error': str(e)}), 500

@inscricoes_bp.route('/total', methods=['GET'])
def total_inscricoes():
    """Retorna o total de inscrições ativas"""
    try:
        inscricoes_collection = mongo.get_collection('inscricoes')
        total = inscricoes_collection.count_documents({'ativo': True})
        
        return jsonify({'total': total})
        
    except Exception as e:
        print(f"❌ Erro ao contar inscrições: {e}")
        return jsonify({'error': str(e)}), 500
