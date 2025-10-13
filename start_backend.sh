#!/bin/bash

# Script para iniciar o backend Flask do e-lib
# Uso: ./start_backend.sh

echo "🚀 Iniciando Backend Flask do e-lib..."
echo ""

# Ir para diretório do backend
cd "$(dirname "$0")/e-lib/backend" || exit 1

# Verificar se requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: requirements.txt não encontrado!"
    exit 1
fi

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python3 não está instalado!"
    exit 1
fi

# Verificar se MongoDB está rodando
echo "🔍 Verificando MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB não está rodando. Tentando iniciar..."
    sudo systemctl start mongod
    sleep 2
    if ! pgrep -x "mongod" > /dev/null; then
        echo "❌ Erro: Não foi possível iniciar MongoDB!"
        echo "   Execute manualmente: sudo systemctl start mongod"
        exit 1
    fi
fi
echo "✅ MongoDB está rodando"
echo ""

# Verificar se venv existe, se não, criar
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar/atualizar dependências
echo "📥 Instalando dependências..."
pip install -q -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# Verificar se banco está populado
echo "🗄️  Verificando banco de dados..."
ARTICLE_COUNT=$(mongosh --quiet --eval "db.getSiblingDB('simple-lib').artigos.countDocuments()" 2>/dev/null || echo "0")

if [ "$ARTICLE_COUNT" = "0" ]; then
    echo "⚠️  Banco de dados vazio!"
    echo "📚 Deseja popular com dados de teste? (s/n)"
    read -r resposta
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        if [ -f "seed_data.bib" ]; then
            echo "🌱 Populando banco com seed_data.bib..."
            python seed_bibtex.py seed_data.bib
            echo "✅ Banco de dados populado!"
        else
            echo "⚠️  Arquivo seed_data.bib não encontrado!"
        fi
    fi
fi
echo ""

# Iniciar servidor Flask
echo "🚀 Iniciando servidor Flask..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Backend estará disponível em:"
echo "  📡 http://localhost:5000"
echo "  📡 http://127.0.0.1:5000"
echo ""
echo "Para parar o servidor: Ctrl+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python run.py
