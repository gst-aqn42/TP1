from flask import Blueprint, request, jsonify
from app.models.notificacao import Notificacao
from app.services.email_service import email_service

notificacoes_bp = Blueprint('notificacoes', __name__)

@notificacoes_bp.route('/inscrever', methods=['POST'])
def inscrever_notificacao():
    """Inscreve um email para receber notificações de um autor"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('nome_autor'):
            return jsonify({'error': 'Email e nome_autor são obrigatórios'}), 400
        
        # Verificar se já existe inscrição ativa
        notificacoes_existentes = Notificacao.find_by_autor(data['nome_autor'])
        for notif in notificacoes_existentes:
            if notif['email'] == data['email'] and notif.get('ativo', True):
                return jsonify({'error': 'Email já inscrito para este autor'}), 409
        
        notificacao = Notificacao(
            email=data['email'],
            nome_autor=data['nome_autor']
        )
        
        result = notificacao.save()
        
        if result is None:
            return jsonify({'error': 'Falha ao salvar inscrição'}), 500
        
        return jsonify({
            'message': 'Inscrição realizada com sucesso',
            'notificacao_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacoes_bp.route('/desinscrever/<notificacao_id>', methods=['POST'])
def desinscrever_notificacao(notificacao_id):
    """Desativa uma inscrição de notificação"""
    try:
        result = Notificacao.desativar_inscricao(notificacao_id)
        
        if result and result.modified_count > 0:
            return jsonify({'message': 'Inscrição desativada com sucesso'})
        else:
            return jsonify({'error': 'Inscrição não encontrada'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Função para notificar quando um artigo é criado
def notificar_novo_artigo(artigo):
    """Notifica todos os inscritos quando um novo artigo é publicado"""
    try:
        # Para cada autor do artigo, buscar inscrições
        for autor in artigo.get('autores', []):
            nome_autor = autor.get('nome', '')
            notificacoes = Notificacao.find_by_autor(nome_autor)
            
            for notificacao in notificacoes:
                print(f"Notificando {notificacao['email']} sobre novo artigo de {nome_autor}")
                email_service.enviar_notificacao(
                    notificacao['email'],
                    nome_autor,
                    artigo
                )
                
    except Exception as e:
        print(f"Erro ao notificar novo artigo: {e}")
