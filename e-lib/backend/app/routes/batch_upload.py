from flask import Blueprint, request, jsonify
from app.services.auth import auth_service
from werkzeug.utils import secure_filename
import os
import tempfile
import bibtexparser
from datetime import datetime
from app.services.database import mongo
from bson import ObjectId

batch_upload_bp = Blueprint('batch_upload', __name__)

ALLOWED_EXTENSIONS = {'bib'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_authors(author_string):
    """Converte string de autores do BibTeX em lista de objetos"""
    if not author_string:
        return []
    
    authors = author_string.split(' and ')
    author_list = []
    for author in authors:
        author = author.strip()
        if author:
            author_list.append({
                "nome": author,
                "email": f"{author.split()[-1].lower()}@email.com"
            })
    return author_list

def parse_keywords(keywords_string):
    """Converte string de keywords em lista"""
    if not keywords_string:
        return []
    
    keywords = keywords_string.replace(';', ',').split(',')
    return [k.strip() for k in keywords if k.strip()]

def extract_event_info(booktitle):
    """Extrai informações de evento do booktitle"""
    booktitle_lower = booktitle.lower()
    
    if 'simpósio brasileiro' in booktitle_lower or 'sbes' in booktitle_lower:
        return {
            'sigla': 'SBES',
            'nome': 'Simpósio Brasileiro de Engenharia de Software',
            'descricao': 'Principal evento brasileiro dedicado à engenharia de software'
        }
    elif 'icse' in booktitle_lower:
        return {
            'sigla': 'ICSE',
            'nome': 'International Conference on Software Engineering',
            'descricao': 'Premier international conference on software engineering'
        }
    else:
        words = booktitle.split()
        sigla = ''.join([w[0].upper() for w in words[:3] if w[0].isupper()])
        return {
            'sigla': sigla or 'CONF',
            'nome': booktitle,
            'descricao': f'Conferência: {booktitle}'
        }

@batch_upload_bp.route('/upload-bibtex', methods=['POST'])
@auth_service.admin_required
def upload_bibtex():
    """Upload e processamento de arquivo BibTeX para cadastro em massa"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nome de arquivo vazio'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Apenas arquivos .bib são permitidos'}), 400
        
        # Salvar arquivo temporariamente
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)
        
        # Parse do BibTeX
        with open(temp_path, 'r', encoding='utf-8') as bibfile:
            bib_database = bibtexparser.load(bibfile)
        
        # Remover arquivo temporário
        os.remove(temp_path)
        
        if not bib_database.entries:
            return jsonify({'error': 'Nenhum artigo encontrado no arquivo BibTeX'}), 400
        
        # Estatísticas
        stats = {
            'total_entries': len(bib_database.entries),
            'eventos_criados': 0,
            'edicoes_criadas': 0,
            'artigos_criados': 0,
            'artigos_duplicados': 0,
            'erros': []
        }
        
        # Processar cada entrada
        for entry in bib_database.entries:
            try:
                titulo = entry.get('title', '')
                if not titulo:
                    stats['erros'].append({'entry': entry.get('ID', 'unknown'), 'error': 'Título vazio'})
                    continue
                
                # Verificar duplicatas
                existing = mongo.db.artigos.find_one({"titulo": titulo})
                if existing:
                    stats['artigos_duplicados'] += 1
                    continue
                
                # Extrair informações do evento
                booktitle = entry.get('booktitle', 'Conferência Desconhecida')
                year = int(entry.get('year', datetime.now().year))
                event_info = extract_event_info(booktitle)
                
                # Criar/buscar evento
                evento = mongo.db.eventos.find_one({"sigla": event_info['sigla']})
                if not evento:
                    evento_data = {
                        "nome": event_info['nome'],
                        "sigla": event_info['sigla'],
                        "descricao": event_info['descricao'],
                        "criado_em": datetime.utcnow()
                    }
                    evento_result = mongo.db.eventos.insert_one(evento_data)
                    evento_id = str(evento_result.inserted_id)
                    stats['eventos_criados'] += 1
                else:
                    evento_id = str(evento['_id'])
                
                # Criar/buscar edição
                edicao = mongo.db.edicoes.find_one({
                    "evento_id": evento_id,
                    "ano": year
                })
                if not edicao:
                    edicao_data = {
                        "evento_id": evento_id,
                        "ano": year,
                        "local": entry.get('address', ''),
                        "data_inicio": f"{year}-01-01",
                        "data_fim": f"{year}-12-31",
                        "criado_em": datetime.utcnow()
                    }
                    edicao_result = mongo.db.edicoes.insert_one(edicao_data)
                    edicao_id = str(edicao_result.inserted_id)
                    stats['edicoes_criadas'] += 1
                else:
                    edicao_id = str(edicao['_id'])
                
                # Criar artigo
                artigo_data = {
                    "titulo": titulo,
                    "autores": parse_authors(entry.get('author', '')),
                    "edicao_id": edicao_id,
                    "resumo": entry.get('abstract', ''),
                    "keywords": parse_keywords(entry.get('keywords', '')),
                    "pdf_path": "",
                    "criado_em": datetime.utcnow()
                }
                
                mongo.db.artigos.insert_one(artigo_data)
                stats['artigos_criados'] += 1
                
            except Exception as e:
                stats['erros'].append({
                    'entry': entry.get('ID', 'unknown'),
                    'error': str(e)
                })
        
        return jsonify({
            'message': 'Upload processado com sucesso',
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500
