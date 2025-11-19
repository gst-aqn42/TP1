#!/bin/bash

# Script para executar testes E2E com cobertura
# Uso: ./executar_testes_e2e.sh [modo]
# Modos: interativo, headless, cobertura

set -e

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios
BACKEND_DIR="/home/mostqi/EngSoft/TP1/e-lib/backend"
FRONTEND_DIR="/home/mostqi/EngSoft/TP1/frontend"
VENV_DIR="/home/mostqi/EngSoft/TP1/venv"

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🧪 E-Lib - Executor de Testes E2E           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Função para verificar se serviço está rodando
check_service() {
    local url=$1
    local name=$2
    
    echo -e "${YELLOW}Verificando ${name}...${NC}"
    
    if curl -s "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ${name} está rodando${NC}"
        return 0
    else
        echo -e "${RED}✗ ${name} NÃO está rodando${NC}"
        return 1
    fi
}

# Função para iniciar backend
start_backend() {
    echo -e "${YELLOW}Iniciando Backend Flask...${NC}"
    
    cd "$BACKEND_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Matar processo Flask anterior se existir
    pkill -f "python run.py" 2>/dev/null || true
    
    # Iniciar Flask em background
    python run.py > /tmp/flask.log 2>&1 &
    BACKEND_PID=$!
    
    echo -e "${BLUE}Aguardando backend iniciar...${NC}"
    sleep 5
    
    if check_service "http://localhost:5000/api" "Backend"; then
        echo -e "${GREEN}✓ Backend iniciado (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${RED}✗ Falha ao iniciar backend${NC}"
        echo -e "${RED}Ver logs em: /tmp/flask.log${NC}"
        exit 1
    fi
}

# Função para iniciar frontend
start_frontend() {
    echo -e "${YELLOW}Iniciando Frontend Angular...${NC}"
    
    cd "$FRONTEND_DIR"
    
    # Matar processo Angular anterior se existir
    pkill -f "ng serve" 2>/dev/null || true
    
    # Iniciar Angular em background
    npm start > /tmp/angular.log 2>&1 &
    FRONTEND_PID=$!
    
    echo -e "${BLUE}Aguardando frontend compilar (pode demorar ~30s)...${NC}"
    
    # Aguardar até 60 segundos
    for i in {1..60}; do
        if check_service "http://localhost:4200" "Frontend" 2>/dev/null; then
            echo -e "${GREEN}✓ Frontend iniciado (PID: $FRONTEND_PID)${NC}"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    echo -e "\n${RED}✗ Timeout ao iniciar frontend${NC}"
    echo -e "${RED}Ver logs em: /tmp/angular.log${NC}"
    exit 1
}

# Função para parar serviços
stop_services() {
    echo -e "\n${YELLOW}Parando serviços...${NC}"
    
    pkill -f "python run.py" 2>/dev/null || true
    pkill -f "ng serve" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Serviços parados${NC}"
}

# Trap para garantir cleanup
trap stop_services EXIT

# Menu
echo "Escolha o modo de execução:"
echo "1) Interativo (abre interface gráfica do Cypress)"
echo "2) Headless (roda no terminal)"
echo "3) Headless com Cobertura (gera relatório)"
echo "4) Apenas iniciar serviços"
echo "5) Parar serviços"
echo ""
read -p "Opção [1-5]: " option

case $option in
    1)
        MODE="interativo"
        ;;
    2)
        MODE="headless"
        ;;
    3)
        MODE="cobertura"
        ;;
    4)
        MODE="servicos"
        ;;
    5)
        stop_services
        exit 0
        ;;
    *)
        echo -e "${RED}Opção inválida!${NC}"
        exit 1
        ;;
esac

# Verificar se serviços já estão rodando
BACKEND_RUNNING=false
FRONTEND_RUNNING=false

if check_service "http://localhost:5000/api" "Backend" 2>/dev/null; then
    BACKEND_RUNNING=true
fi

if check_service "http://localhost:4200" "Frontend" 2>/dev/null; then
    FRONTEND_RUNNING=true
fi

# Iniciar serviços se necessário
if [ "$BACKEND_RUNNING" = false ]; then
    start_backend
else
    echo -e "${GREEN}✓ Backend já está rodando${NC}"
fi

if [ "$FRONTEND_RUNNING" = false ]; then
    start_frontend
else
    echo -e "${GREEN}✓ Frontend já está rodando${NC}"
fi

# Apenas iniciar serviços
if [ "$MODE" = "servicos" ]; then
    echo -e "\n${GREEN}✓ Serviços iniciados com sucesso!${NC}"
    echo -e "${BLUE}Backend: http://localhost:5000${NC}"
    echo -e "${BLUE}Frontend: http://localhost:4200${NC}"
    echo ""
    echo "Para parar os serviços, execute:"
    echo "  ./executar_testes_e2e.sh (escolha opção 5)"
    exit 0
fi

echo -e "\n${GREEN}✓ Todos os serviços estão prontos!${NC}"
echo ""

# Executar testes
cd "$FRONTEND_DIR"

case $MODE in
    interativo)
        echo -e "${BLUE}Abrindo Cypress em modo interativo...${NC}"
        echo -e "${YELLOW}Pressione CTRL+C para encerrar${NC}"
        npm run e2e:open
        ;;
        
    headless)
        echo -e "${BLUE}Executando testes em modo headless...${NC}"
        npm run e2e
        
        echo -e "\n${GREEN}✓ Testes concluídos!${NC}"
        echo -e "${BLUE}Vídeos salvos em: cypress/videos/${NC}"
        ;;
        
    cobertura)
        echo -e "${BLUE}Executando testes com cobertura de código...${NC}"
        npm run e2e:coverage
        
        echo -e "\n${GREEN}✓ Testes concluídos!${NC}"
        echo -e "${BLUE}Relatório de cobertura: coverage-e2e/index.html${NC}"
        
        # Abrir relatório no navegador
        read -p "Deseja abrir o relatório de cobertura? [s/N]: " open_report
        if [[ $open_report =~ ^[Ss]$ ]]; then
            xdg-open coverage-e2e/index.html 2>/dev/null || \
            firefox coverage-e2e/index.html 2>/dev/null || \
            google-chrome coverage-e2e/index.html 2>/dev/null || \
            echo -e "${YELLOW}Não foi possível abrir automaticamente. Abra manualmente: coverage-e2e/index.html${NC}"
        fi
        ;;
esac

echo -e "\n${GREEN}✓ Concluído!${NC}"
