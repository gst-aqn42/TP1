#!/bin/bash

# Script para popular o banco de dados com dados de teste
# Execute este script após iniciar o backend

echo "================================================"
echo "🌱 SEED DO BANCO DE DADOS - e-lib"
echo "================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:5000/api"

# Função para fazer requisições
function api_post() {
    local endpoint=$1
    local data=$2
    local description=$3
    
    echo -e "${BLUE}📤 ${description}...${NC}"
    response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}${endpoint}" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "$data")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ Sucesso!${NC}"
        echo "$body"
        return 0
    else
        echo -e "${RED}❌ Erro (HTTP $http_code)${NC}"
        echo "$body"
        return 1
    fi
}

echo -e "${YELLOW}⚠️  Certifique-se de que o backend está rodando em $BASE_URL${NC}"
echo ""

# 1. Criar usuário admin e obter token
echo "========================================="
echo -e "${BLUE}👤 Passo 1: Criar usuário admin${NC}"
echo "========================================="
ADMIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@e-lib.com",
        "nome": "Administrador",
        "is_admin": true
    }')

TOKEN=$(echo $ADMIN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "${YELLOW}⚠️  Tentando fazer login...${NC}"
    LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"email": "admin@e-lib.com"}')
    TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
fi

if [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ Erro ao obter token de autenticação${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Token obtido com sucesso!${NC}"
echo "Token: ${TOKEN:0:50}..."
echo ""

# 2. Criar Eventos
echo "========================================="
echo -e "${BLUE}📅 Passo 2: Criar Eventos${NC}"
echo "========================================="

SBES_RESPONSE=$(api_post "/eventos/" '{
    "nome": "Simpósio Brasileiro de Engenharia de Software",
    "sigla": "SBES",
    "descricao": "O principal evento brasileiro dedicado à engenharia de software, promovendo a troca de experiências entre pesquisadores e profissionais."
}' "Criando evento SBES")

SBES_ID=$(echo $SBES_RESPONSE | grep -o '"evento_id":"[^"]*' | cut -d'"' -f4)
echo "SBES ID: $SBES_ID"
echo ""

ICSE_RESPONSE=$(api_post "/eventos/" '{
    "nome": "International Conference on Software Engineering",
    "sigla": "ICSE",
    "descricao": "Premier international conference on software engineering research and practice."
}' "Criando evento ICSE")

ICSE_ID=$(echo $ICSE_RESPONSE | grep -o '"evento_id":"[^"]*' | cut -d'"' -f4)
echo "ICSE ID: $ICSE_ID"
echo ""

# 3. Criar Edições
echo "========================================="
echo -e "${BLUE}📖 Passo 3: Criar Edições${NC}"
echo "========================================="

if [ ! -z "$SBES_ID" ]; then
    SBES_2024_RESPONSE=$(api_post "/edicoes/" "{
        \"evento_id\": \"$SBES_ID\",
        \"ano\": 2024,
        \"local\": \"Curitiba, PR\",
        \"data_inicio\": \"2024-09-23\",
        \"data_fim\": \"2024-09-27\"
    }" "Criando SBES 2024")
    
    SBES_2024_ID=$(echo $SBES_2024_RESPONSE | grep -o '"edicao_id":"[^"]*' | cut -d'"' -f4)
    echo "SBES 2024 ID: $SBES_2024_ID"
    echo ""
    
    SBES_2023_RESPONSE=$(api_post "/edicoes/" "{
        \"evento_id\": \"$SBES_ID\",
        \"ano\": 2023,
        \"local\": \"Campo Grande, MS\",
        \"data_inicio\": \"2023-09-25\",
        \"data_fim\": \"2023-09-29\"
    }" "Criando SBES 2023")
    
    SBES_2023_ID=$(echo $SBES_2023_RESPONSE | grep -o '"edicao_id":"[^"]*' | cut -d'"' -f4)
    echo "SBES 2023 ID: $SBES_2023_ID"
    echo ""
fi

if [ ! -z "$ICSE_ID" ]; then
    ICSE_2024_RESPONSE=$(api_post "/edicoes/" "{
        \"evento_id\": \"$ICSE_ID\",
        \"ano\": 2024,
        \"local\": \"Lisbon, Portugal\",
        \"data_inicio\": \"2024-04-14\",
        \"data_fim\": \"2024-04-20\"
    }" "Criando ICSE 2024")
    
    ICSE_2024_ID=$(echo $ICSE_2024_RESPONSE | grep -o '"edicao_id":"[^"]*' | cut -d'"' -f4)
    echo "ICSE 2024 ID: $ICSE_2024_ID"
    echo ""
fi

# 4. Criar Artigos
echo "========================================="
echo -e "${BLUE}📄 Passo 4: Criar Artigos${NC}"
echo "========================================="

if [ ! -z "$SBES_2024_ID" ]; then
    api_post "/artigos/" "{
        \"titulo\": \"Metodologias Ágeis na Engenharia de Software Moderna\",
        \"autores\": [
            {\"nome\": \"João Silva\", \"email\": \"joao.silva@email.com\"},
            {\"nome\": \"Maria Santos\", \"email\": \"maria.santos@email.com\"}
        ],
        \"edicao_id\": \"$SBES_2024_ID\",
        \"resumo\": \"Este artigo apresenta uma análise abrangente das metodologias ágeis aplicadas no contexto moderno de engenharia de software, com foco em Scrum, Kanban e XP.\",
        \"keywords\": [\"Metodologias Ágeis\", \"Scrum\", \"Kanban\", \"XP\"]
    }" "Artigo 1: Metodologias Ágeis"
    echo ""
    
    api_post "/artigos/" "{
        \"titulo\": \"Inteligência Artificial no Desenvolvimento de Software\",
        \"autores\": [
            {\"nome\": \"Ana Costa\", \"email\": \"ana.costa@email.com\"},
            {\"nome\": \"Carlos Mendes\", \"email\": \"carlos.mendes@email.com\"}
        ],
        \"edicao_id\": \"$SBES_2024_ID\",
        \"resumo\": \"Revisão sistemática sobre aplicações de IA no ciclo de desenvolvimento de software, incluindo code completion, bug detection e test generation.\",
        \"keywords\": [\"Inteligência Artificial\", \"Machine Learning\", \"Desenvolvimento\"]
    }" "Artigo 2: IA no Desenvolvimento"
    echo ""
    
    api_post "/artigos/" "{
        \"titulo\": \"Arquiteturas de Microserviços: Padrões e Anti-padrões\",
        \"autores\": [
            {\"nome\": \"Carlos Mendes\", \"email\": \"carlos.mendes@email.com\"},
            {\"nome\": \"Paula Souza\", \"email\": \"paula.souza@email.com\"}
        ],
        \"edicao_id\": \"$SBES_2024_ID\",
        \"resumo\": \"Identificação e documentação de padrões e anti-padrões em arquiteturas de microserviços, baseado em estudos empíricos.\",
        \"keywords\": [\"Microserviços\", \"Arquitetura\", \"Padrões\"]
    }" "Artigo 3: Microserviços"
    echo ""
fi

if [ ! -z "$SBES_2023_ID" ]; then
    api_post "/artigos/" "{
        \"titulo\": \"Qualidade de Software em Equipes Distribuídas\",
        \"autores\": [
            {\"nome\": \"Pedro Oliveira\", \"email\": \"pedro.oliveira@email.com\"},
            {\"nome\": \"Ana Silva\", \"email\": \"ana.silva@email.com\"}
        ],
        \"edicao_id\": \"$SBES_2023_ID\",
        \"resumo\": \"Estudo sobre garantia de qualidade em projetos com equipes geograficamente distribuídas.\",
        \"keywords\": [\"Qualidade\", \"Equipes Distribuídas\", \"DevOps\"]
    }" "Artigo 4: Qualidade Distribuída"
    echo ""
    
    api_post "/artigos/" "{
        \"titulo\": \"Test-Driven Development na Prática\",
        \"autores\": [
            {\"nome\": \"Lucas Ferreira\", \"email\": \"lucas.ferreira@email.com\"},
            {\"nome\": \"Maria Santos\", \"email\": \"maria.santos@email.com\"}
        ],
        \"edicao_id\": \"$SBES_2023_ID\",
        \"resumo\": \"Experimento controlado comparando TDD com abordagens tradicionais.\",
        \"keywords\": [\"TDD\", \"Testes\", \"Qualidade\"]
    }" "Artigo 5: TDD"
    echo ""
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ SEED COMPLETO!${NC}"
echo "================================================"
echo ""
echo -e "${BLUE}📊 Resumo:${NC}"
echo "  • 2 Eventos criados"
echo "  • 3 Edições criadas"
echo "  • 5 Artigos criados"
echo ""
echo -e "${YELLOW}🚀 Acesse o frontend para visualizar os dados:${NC}"
echo "   http://localhost:4200"
echo ""
echo -e "${BLUE}👤 Login admin:${NC}"
echo "   Email: admin@e-lib.com"
echo ""

