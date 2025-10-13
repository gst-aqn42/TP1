from flask import Blueprint, request, jsonify
from app.models.artigo import Artigo
from app.services.auth import auth_service
from app.services.database import mongo # Importação adicionada para a busca
from bson import ObjectId
import os
import json
from werkzeug.utils import secure_filename
from app.routes.notificacoes import notificar_novo_artigo

artigos_bp = Blueprint('artigos', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROTAS CRUD BÁSICAS ---

@artigos_bp.route('/edicao/<edicao_id>', methods=['GET'])
def listar_artigos_edicao(edicao_id):
    """Lista todos os artigos de uma edição"""
    try:
        artigos = Artigo.find_by_edicao(edicao_id)
        return jsonify(artigos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artigos_bp.route('/', methods=['POST'])
@auth_service.admin_required
def criar_artigo():
    """Cria um novo artigo (apenas admin)"""
    try:
        # Lógica para criar artigo com ou sem upload de PDF
        if 'pdf' in request.files:
            file = request.files['pdf']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                autores_str = request.form.get('autores', '[]')
                keywords_str = request.form.get('keywords', '[]')
                
                artigo = Artigo(
                    titulo=request.form.get('titulo'),
                    autores=json.loads(autores_str),
                    edicao_id=request.form.get('edicao_id'),
                    resumo=request.form.get('resumo'),
                    keywords=json.loads(keywords_str),
                    pdf_path=file_path
                )
            else:
                return jsonify({'error': 'Arquivo inválido ou ausente'}), 400
        else:
            data = request.get_json()
            if not data or not data.get('titulo') or not data.get('edicao_id'):
                return jsonify({'error': 'titulo e edicao_id são obrigatórios'}), 400
            
            artigo = Artigo(
                titulo=data['titulo'],
                autores=data.get('autores', []),
                edicao_id=data['edicao_id'],
                resumo=data.get('resumo'),
                keywords=data.get('keywords', [])
            )
        
        result = artigo.save()
        if result is None:
            return jsonify({'error': 'Falha ao salvar artigo no banco de dados'}), 500
        
        # ADICIONE AQUI A NOTIFICAÇÃO DO NOVO ARTIGO
        if result is not None:
            # Buscar o artigo salvo para notificar
            artigo_salvo = Artigo.find_by_id(str(result.inserted_id))
            if artigo_salvo:
                notificar_novo_artigo(artigo_salvo)
        
        return jsonify({
            'message': 'Artigo criado com sucesso',
            'artigo_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        print(f"Erro na rota criar_artigo: {e}")
        return jsonify({'error': str(e)}), 500

@artigos_bp.route('/<artigo_id>', methods=['GET'])
def obter_artigo(artigo_id):
    """Obtém um artigo específico"""
    try:
        artigo = Artigo.find_by_id(artigo_id)
        if artigo:
            return jsonify(artigo)
        return jsonify({'error': 'Artigo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artigos_bp.route('/<artigo_id>', methods=['PUT'])
@auth_service.admin_required
def atualizar_artigo(artigo_id):
    """Atualiza um artigo (apenas admin)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados de atualização necessários'}), 400
        
        result = Artigo.update(artigo_id, data)
        if result and result.modified_count > 0:
            return jsonify({'message': 'Artigo atualizado com sucesso'})
        return jsonify({'error': 'Artigo não encontrado ou nenhuma alteração feita'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artigos_bp.route('/<artigo_id>', methods=['DELETE'])
@auth_service.admin_required
def deletar_artigo(artigo_id):
    """Deleta um artigo (apenas admin)"""
    try:
        artigo = Artigo.find_by_id(artigo_id)
        if artigo and artigo.get('pdf_path') and os.path.exists(artigo['pdf_path']):
            os.remove(artigo['pdf_path'])
        
        result = Artigo.delete(artigo_id)
        if result and result.deleted_count > 0:
            return jsonify({'message': 'Artigo deletado com sucesso'})
        return jsonify({'error': 'Artigo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- ROTA DE UPLOAD DE PDF SEPARADA ---

@artigos_bp.route('/<artigo_id>/upload-pdf', methods=['POST'])
@auth_service.admin_required
def upload_pdf_artigo(artigo_id):
    """Faz upload de PDF para um artigo existente"""
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, f"{artigo_id}_{filename}")
            file.save(file_path)
            
            result = Artigo.update(artigo_id, {'pdf_path': file_path})
            
            if result and result.modified_count > 0:
                return jsonify({'message': 'PDF enviado com sucesso', 'pdf_path': file_path})
            return jsonify({'error': 'Artigo não encontrado'}), 404
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido. Apenas PDF é aceito.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- ROTA DE BUSCA ---

@artigos_bp.route('/busca', methods=['GET'])
def buscar_artigos():
    """Busca artigos por título, autor ou evento"""
    try:
        query = request.args.get('q', '')
        tipo = request.args.get('tipo', 'tudo')  # 'titulo', 'autor', 'evento', 'tudo'

        if not query:
            return jsonify({'error': 'Parâmetro de busca (q) é obrigatório'}), 400

        artigos_collection = mongo.get_collection('artigos')
        eventos_collection = mongo.get_collection('eventos')
        edicoes_collection = mongo.get_collection('edicoes')
        
        artigos = []

        if tipo == 'titulo':
            artigos = list(artigos_collection.find({'titulo': {'$regex': query, '$options': 'i'}}))
        elif tipo == 'autor':
            artigos = list(artigos_collection.find({'autores.nome': {'$regex': query, '$options': 'i'}}))
        elif tipo == 'evento':
            eventos = eventos_collection.find({'$or': [{'nome': {'$regex': query, '$options': 'i'}}, {'sigla': {'$regex': query, '$options': 'i'}}]})
            eventos_ids = [evento['_id'] for evento in eventos]
            edicoes = edicoes_collection.find({'evento_id': {'$in': eventos_ids}})
            edicoes_ids = [edicao['_id'] for edicao in edicoes]
            artigos = list(artigos_collection.find({'edicao_id': {'$in': edicoes_ids}}))
        else:  # tipo 'tudo'
            artigos_titulo = list(artigos_collection.find({'titulo': {'$regex': query, '$options': 'i'}}))
            artigos_autor = list(artigos_collection.find({'autores.nome': {'$regex': query, '$options': 'i'}}))
            
            eventos = eventos_collection.find({'$or': [{'nome': {'$regex': query, '$options': 'i'}}, {'sigla': {'$regex': query, '$options': 'i'}}]})
            eventos_ids = [evento['_id'] for evento in eventos]
            edicoes = edicoes_collection.find({'evento_id': {'$in': eventos_ids}})
            edicoes_ids = [edicao['_id'] for edicao in edicoes]
            artigos_evento = list(artigos_collection.find({'edicao_id': {'$in': edicoes_ids}}))

            # Combinar resultados, evitando duplicatas
            artigos_dict = {}
            for artigo in artigos_titulo + artigos_autor + artigos_evento:
                artigos_dict[str(artigo['_id'])] = artigo
            artigos = list(artigos_dict.values())

        # Enriquecer resultados com informações de edição e evento
        resultados = []
        for artigo in artigos:
            edicao_id_obj = ObjectId(artigo['edicao_id'])
            edicao = edicoes_collection.find_one({'_id': edicao_id_obj})
            if edicao:
                artigo['edicao_ano'] = edicao.get('ano')
                evento_id_obj = ObjectId(edicao['evento_id'])
                evento = eventos_collection.find_one({'_id': evento_id_obj})
                if evento:
                    artigo['evento_nome'] = evento.get('nome')
                    artigo['evento_sigla'] = evento.get('sigla')
            
            artigo['_id'] = str(artigo['_id'])
            artigo['edicao_id'] = str(artigo['edicao_id'])
            resultados.append(artigo)

        return jsonify({
            'resultados': resultados,
            'total': len(resultados),
            'query': query,
            'tipo': tipo
        })

    except Exception as e:
        print(f"Erro na busca: {e}")
        return jsonify({'error': str(e)}), 500

# --- ROTA DE TESTE ---

@artigos_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Rota de artigos funcionando!"})
