from flask import Blueprint, request, jsonify
from app.models.edicao import EdicaoEvento
from app.services.auth import auth_service
from bson import ObjectId

edicoes_bp = Blueprint('edicoes', __name__)

@edicoes_bp.route('/evento/<evento_id>', methods=['GET'])
def listar_edicoes_evento(evento_id):
    """Lista todas as edições de um evento"""
    try:
        edicoes = EdicaoEvento.find_by_evento(evento_id)
        return jsonify(edicoes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@edicoes_bp.route('/', methods=['POST'])
@auth_service.admin_required
def criar_edicao():
    """Cria uma nova edição (apenas admin)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('evento_id') or not data.get('ano'):
            return jsonify({'error': 'evento_id e ano são obrigatórios'}), 400
        
        edicao = EdicaoEvento(
            evento_id=data['evento_id'],
            ano=data['ano'],
            local=data.get('local'),
            data_inicio=data.get('data_inicio'),
            data_fim=data.get('data_fim')
        )
        
        result = edicao.save()
        return jsonify({
            'message': 'Edição criada com sucesso',
            'edicao_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@edicoes_bp.route('/<edicao_id>', methods=['GET'])
def obter_edicao(edicao_id):
    """Obtém uma edição específica"""
    try:
        edicao = EdicaoEvento.find_by_id(edicao_id)
        if edicao:
            return jsonify(edicao)
        else:
            return jsonify({'error': 'Edição não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@edicoes_bp.route('/<edicao_id>', methods=['PUT'])
@auth_service.admin_required
def atualizar_edicao(edicao_id):
    """Atualiza uma edição (apenas admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados de atualização necessários'}), 400
        
        update_data = {}
        if 'ano' in data:
            update_data['ano'] = data['ano']
        if 'local' in data:
            update_data['local'] = data['local']
        if 'data_inicio' in data:
            update_data['data_inicio'] = data['data_inicio']
        if 'data_fim' in data:
            update_data['data_fim'] = data['data_fim']
        
        result = EdicaoEvento.update(edicao_id, update_data)
        
        if result.modified_count > 0:
            return jsonify({'message': 'Edição atualizada com sucesso'})
        else:
            return jsonify({'error': 'Edição não encontrada ou nenhuma alteração feita'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@edicoes_bp.route('/<edicao_id>', methods=['DELETE'])
@auth_service.admin_required
def deletar_edicao(edicao_id):
    """Deleta uma edição (apenas admin)"""
    try:
        result = EdicaoEvento.delete(edicao_id)
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Edição deletada com sucesso'})
        else:
            return jsonify({'error': 'Edição não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota de teste mantida para compatibilidade
@edicoes_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Rota de edições funcionando!"})
