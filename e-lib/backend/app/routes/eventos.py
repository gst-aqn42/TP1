from flask import Blueprint, request, jsonify
from app.models.evento import Evento
from app.services.auth import auth_service
from bson import ObjectId

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/', methods=['GET'])
@eventos_bp.route('', methods=['GET'])
def listar_eventos():
    """Lista todos os eventos"""
    try:
        eventos = Evento.find_all()
        return jsonify({"eventos": eventos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@eventos_bp.route('/', methods=['POST'])
@eventos_bp.route('', methods=['POST'])
@auth_service.admin_required
def criar_evento():
    """Cria um novo evento (apenas admin)"""
    try:
        data = request.get_json()
        print(f"Evento recebido para criação: {data}")
        
        if not data or not data.get('nome') or not data.get('sigla'):
            return jsonify({'error': 'Nome e sigla são obrigatórios'}), 400
        
        evento = Evento(
            nome=data['nome'],
            sigla=data['sigla'],
            descricao=data.get('descricao')
        )
        
        result = evento.save()
        
        if result is None:
            return jsonify({'error': 'Falha ao salvar evento no banco de dados'}), 500
        
        return jsonify({
            'message': 'Evento criado com sucesso',
            'evento_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        print(f"Erro na rota criar_evento: {e}")
        return jsonify({'error': str(e)}), 500

@eventos_bp.route('/<evento_id>', methods=['GET'])
def obter_evento(evento_id):
    """Obtém um evento específico"""
    try:
        evento = Evento.find_by_id(evento_id)
        if evento:
            return jsonify(evento)
        else:
            return jsonify({'error': 'Evento não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@eventos_bp.route('/<evento_id>', methods=['PUT'])
@auth_service.admin_required
def atualizar_evento(evento_id):
    """Atualiza um evento (apenas admin)"""
    try:
        data = request.get_json()
        print(f"📝 Atualizando evento {evento_id} com dados: {data}")
        
        if not data:
            return jsonify({'error': 'Dados de atualização necessários'}), 400
        
        update_data = {}
        if 'nome' in data:
            update_data['nome'] = data['nome']
        if 'sigla' in data:
            update_data['sigla'] = data['sigla']
        if 'descricao' in data:
            update_data['descricao'] = data['descricao']
        
        print(f"✅ Dados a atualizar: {update_data}")
        result = Evento.update(evento_id, update_data)
        print(f"💾 Resultado: modified_count={result.modified_count}")
        
        if result.modified_count > 0:
            return jsonify({'message': 'Evento atualizado com sucesso'})
        else:
            return jsonify({'error': 'Evento não encontrado ou nenhuma alteração feita'}), 404
    except Exception as e:
        print(f"❌ Erro ao atualizar evento: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@eventos_bp.route('/<evento_id>', methods=['DELETE'])
@auth_service.admin_required
def deletar_evento(evento_id):
    """Deleta um evento (apenas admin)"""
    try:
        print(f"🗑️  Tentando deletar evento: {evento_id}")
        result = Evento.delete(evento_id)
        print(f"💾 Resultado: deleted_count={result.deleted_count}")
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Evento deletado com sucesso'})
        else:
            return jsonify({'error': 'Evento não encontrado'}), 404
    except Exception as e:
        print(f"❌ Erro ao deletar evento: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Rota de teste
@eventos_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Rota de eventos funcionando!"})
