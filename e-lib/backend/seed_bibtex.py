#!/usr/bin/env python3
"""
Script para popular o banco de dados MongoDB a partir de um arquivo BibTeX
Uso: python seed_bibtex.py [arquivo.bib]
"""

import sys
import os
from datetime import datetime
import bibtexparser
from pymongo import MongoClient
from bson import ObjectId

# Configuração do MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/simple-lib')
client = MongoClient(MONGODB_URI)
db = client.get_database()

def parse_bibtex_file(filepath):
    """Parse arquivo BibTeX e retorna lista de artigos"""
    print(f"📖 Parseando arquivo: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    
    print(f"✅ {len(bib_database.entries)} artigos encontrados no BibTeX")
    return bib_database.entries

def get_or_create_evento(sigla, nome, descricao=""):
    """Busca ou cria um evento no banco de dados"""
    evento = db.eventos.find_one({"sigla": sigla})
    
    if evento:
        print(f"  ↪ Evento '{sigla}' já existe (ID: {evento['_id']})")
        return evento['_id']
    
    evento_data = {
        "nome": nome,
        "sigla": sigla,
        "descricao": descricao,
        "criado_em": datetime.utcnow()
    }
    
    result = db.eventos.insert_one(evento_data)
    print(f"  ✅ Evento '{sigla}' criado (ID: {result.inserted_id})")
    return result.inserted_id

def get_or_create_edicao(evento_id, ano, local=""):
    """Busca ou cria uma edição no banco de dados"""
    edicao = db.edicoes.find_one({"evento_id": str(evento_id), "ano": ano})
    
    if edicao:
        print(f"    ↪ Edição {ano} já existe (ID: {edicao['_id']})")
        return edicao['_id']
    
    edicao_data = {
        "evento_id": str(evento_id),
        "ano": ano,
        "local": local,
        "data_inicio": f"{ano}-01-01",
        "data_fim": f"{ano}-12-31",
        "criado_em": datetime.utcnow()
    }
    
    result = db.edicoes.insert_one(edicao_data)
    print(f"    ✅ Edição {ano} criada (ID: {result.inserted_id})")
    return result.inserted_id

def parse_authors(author_string):
    """Converte string de autores do BibTeX em lista de objetos"""
    if not author_string:
        return []
    
    # BibTeX usa 'and' como separador
    authors = author_string.split(' and ')
    
    author_list = []
    for author in authors:
        author = author.strip()
        if author:
            # Formato: "Sobrenome, Nome" ou "Nome Sobrenome"
            author_list.append({
                "nome": author,
                "email": f"{author.split()[-1].lower()}@email.com"  # Email fictício
            })
    
    return author_list

def parse_keywords(keywords_string):
    """Converte string de keywords em lista"""
    if not keywords_string:
        return []
    
    # Keywords podem estar separadas por vírgula ou ponto-e-vírgula
    keywords = keywords_string.replace(';', ',').split(',')
    return [k.strip() for k in keywords if k.strip()]

def extract_event_info_from_booktitle(booktitle):
    """Extrai informações de evento do campo booktitle"""
    booktitle_lower = booktitle.lower()
    
    # Mapeamento de eventos conhecidos
    if 'simpósio brasileiro' in booktitle_lower or 'sbes' in booktitle_lower:
        return {
            'sigla': 'SBES',
            'nome': 'Simpósio Brasileiro de Engenharia de Software',
            'descricao': 'Principal evento brasileiro dedicado à engenharia de software'
        }
    elif 'icse' in booktitle_lower or 'international conference on software engineering' in booktitle_lower:
        return {
            'sigla': 'ICSE',
            'nome': 'International Conference on Software Engineering',
            'descricao': 'Premier international conference on software engineering'
        }
    else:
        # Evento genérico
        # Tentar extrair sigla do booktitle (ex: "Proceedings of XYZ 2024")
        words = booktitle.split()
        sigla = ''.join([w[0].upper() for w in words[:3] if w[0].isupper()])
        
        return {
            'sigla': sigla or 'CONF',
            'nome': booktitle,
            'descricao': f'Conferência: {booktitle}'
        }

def create_artigo(entry, edicao_id):
    """Cria um artigo no banco de dados a partir de uma entrada BibTeX"""
    titulo = entry.get('title', 'Sem Título')
    autores = parse_authors(entry.get('author', ''))
    resumo = entry.get('abstract', '')
    keywords = parse_keywords(entry.get('keywords', ''))
    
    # Verificar se artigo já existe (por título)
    existing = db.artigos.find_one({"titulo": titulo})
    if existing:
        print(f"      ⚠ Artigo '{titulo[:50]}...' já existe, pulando")
        return None
    
    artigo_data = {
        "titulo": titulo,
        "autores": autores,
        "edicao_id": str(edicao_id),
        "resumo": resumo,
        "keywords": keywords,
        "pdf_path": "",  # PDF será adicionado depois
        "criado_em": datetime.utcnow()
    }
    
    result = db.artigos.insert_one(artigo_data)
    print(f"      ✅ Artigo '{titulo[:50]}...' criado")
    return result.inserted_id

def seed_from_bibtex(filepath):
    """Função principal para popular o banco a partir do BibTeX"""
    print("\n" + "="*70)
    print("🌱 SEED DO BANCO DE DADOS A PARTIR DE BIBTEX")
    print("="*70 + "\n")
    
    # Parse do arquivo BibTeX
    entries = parse_bibtex_file(filepath)
    
    if not entries:
        print("❌ Nenhum artigo encontrado no arquivo BibTeX")
        return
    
    # Estatísticas
    stats = {
        'eventos_criados': 0,
        'edicoes_criadas': 0,
        'artigos_criados': 0,
        'artigos_duplicados': 0
    }
    
    # Processar cada entrada
    print("\n📝 Processando artigos...\n")
    
    for idx, entry in enumerate(entries, 1):
        print(f"[{idx}/{len(entries)}] Processando: {entry.get('title', 'Sem título')[:60]}...")
        
        # Extrair informações do evento
        booktitle = entry.get('booktitle', '')
        year = int(entry.get('year', datetime.now().year))
        
        event_info = extract_event_info_from_booktitle(booktitle)
        
        # Criar/buscar evento
        evento_id = get_or_create_evento(
            event_info['sigla'],
            event_info['nome'],
            event_info['descricao']
        )
        if db.eventos.find_one({"_id": evento_id, "criado_em": {"$gte": datetime.utcnow().replace(second=0, microsecond=0)}}):
            stats['eventos_criados'] += 1
        
        # Criar/buscar edição
        edicao_id = get_or_create_edicao(evento_id, year, entry.get('address', ''))
        if db.edicoes.find_one({"_id": edicao_id, "criado_em": {"$gte": datetime.utcnow().replace(second=0, microsecond=0)}}):
            stats['edicoes_criadas'] += 1
        
        # Criar artigo
        artigo_id = create_artigo(entry, edicao_id)
        if artigo_id:
            stats['artigos_criados'] += 1
        else:
            stats['artigos_duplicados'] += 1
        
        print()  # Linha em branco
    
    # Relatório final
    print("\n" + "="*70)
    print("✅ SEED COMPLETO!")
    print("="*70)
    print(f"\n📊 Estatísticas:")
    print(f"  • Eventos criados: {stats['eventos_criados']}")
    print(f"  • Edições criadas: {stats['edicoes_criadas']}")
    print(f"  • Artigos criados: {stats['artigos_criados']}")
    print(f"  • Artigos duplicados (pulados): {stats['artigos_duplicados']}")
    print(f"\n  Total de artigos no banco: {db.artigos.count_documents({})}")
    print(f"  Total de eventos no banco: {db.eventos.count_documents({})}")
    print(f"  Total de edições no banco: {db.edicoes.count_documents({})}")
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Uso: python seed_bibtex.py <arquivo.bib>")
        print(f"Exemplo: python seed_bibtex.py seed_data.bib")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"❌ Arquivo não encontrado: {filepath}")
        sys.exit(1)
    
    try:
        seed_from_bibtex(filepath)
    except Exception as e:
        print(f"\n❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
