from flask import Blueprint, jsonify
from app.models.evento import Evento
from app.models.edicao import EdicaoEvento
from app.models.artigo import Artigo
from bson import ObjectId
from app.services.database import mongo

public_bp = Blueprint('public', __name__)

# Homepage para cada evento (ex: /api/public/eventos/SBES)
@public_bp.route('/eventos/<sigla>', methods=['GET'])
def homepage_evento(sigla):
    """Homepage de um evento específico com suas edições"""
    try:
        # Buscar evento pela sigla
        evento = Evento.find_by_sigla(sigla)
        if not evento:
            return jsonify({'error': 'Evento não encontrado'}), 404
        
        # Buscar edições do evento
        edicoes = EdicaoEvento.find_by_evento(evento['_id'])
        
        # Ordenar edições por ano (mais recente primeiro)
        edicoes.sort(key=lambda x: x['ano'], reverse=True)
        
        return jsonify({
            'evento': evento,
            'edicoes': edicoes,
            'total_edicoes': len(edicoes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Homepage para cada edição de evento (ex: /api/public/eventos/SBES/2025)
@public_bp.route('/eventos/<sigla>/<int:ano>', methods=['GET'])
def homepage_edicao(sigla, ano):
    """Homepage de uma edição específica com seus artigos"""
    try:
        # Buscar evento pela sigla
        evento = Evento.find_by_sigla(sigla)
        if not evento:
            return jsonify({'error': 'Evento não encontrado'}), 404
        
        # Buscar edição específica
        edicoes = EdicaoEvento.find_by_evento(evento['_id'])
        edicao = None
        for ed in edicoes:
            if ed['ano'] == ano:
                edicao = ed
                break
        
        if not edicao:
            return jsonify({'error': 'Edição não encontrada'}), 404
        
        # Buscar artigos da edição
        artigos = Artigo.find_by_edicao(edicao['_id'])
        
        return jsonify({
            'evento': evento,
            'edicao': edicao,
            'artigos': artigos,
            'total_artigos': len(artigos)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@public_bp.route('/autores/<nome>', methods=['GET'])
def homepage_autor(nome):
    """Homepage pessoal de um autor com todos os seus artigos organizados por ano"""
    try:
        # Usar a instância do MongoDB para acessar a coleção de artigos
        artigos_collection = mongo.get_collection('artigos')
        
        # Buscar artigos onde o autor está na lista de autores
        artigos = list(artigos_collection.find({
            'autores.nome': {'$regex': nome, '$options': 'i'}
        }))
        
        # Converter ObjectId para string
        for artigo in artigos:
            artigo['_id'] = str(artigo['_id'])
            artigo['edicao_id'] = str(artigo['edicao_id'])
        
        # Organizar artigos por ano
        artigos_por_ano = {}
        for artigo in artigos:
            # Buscar a edição para obter o ano
            edicao = EdicaoEvento.find_by_id(artigo['edicao_id'])
            if edicao:
                ano = edicao['ano']
                if ano not in artigos_por_ano:
                    artigos_por_ano[ano] = []
                artigos_por_ano[ano].append(artigo)
        
        # Ordenar anos em ordem decrescente
        anos_ordenados = sorted(artigos_por_ano.keys(), reverse=True)
        
        return jsonify({
            'autor': nome,
            'artigos_por_ano': artigos_por_ano,
            'anos_ordenados': anos_ordenados,
            'total_artigos': len(artigos)
        })
    except Exception as e:
        print(f"Erro na homepage_autor: {e}")
        return jsonify({'error': str(e)}), 500