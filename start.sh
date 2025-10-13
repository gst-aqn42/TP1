#!/bin/bash

echo "🚀 Iniciando e-lib (Backend + Frontend)"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar se MongoDB está rodando
echo -e "${BLUE}📦 Verificando MongoDB...${NC}"
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB não está rodando. Iniciando..."
    sudo systemctl start mongod || echo "Execute: sudo systemctl start mongod"
fi

# Iniciar Backend
echo -e "${GREEN}🐍 Iniciando Backend (Flask)...${NC}"
cd "$(dirname "$0")/e-lib/backend"

# Verificar se existe venv
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativar venv e instalar dependências
source venv/bin/activate
pip install -q -r requirements.txt

# Iniciar backend em background
export FLASK_APP=run.py
export FLASK_ENV=development
python run.py &
BACKEND_PID=$!
echo "Backend rodando no PID: $BACKEND_PID"

# Aguardar backend iniciar
sleep 3

# Criar usuário admin inicial
echo -e "${BLUE}👤 Criando usuário admin...${NC}"
curl -s -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@simple-lib.com", "nome": "Administrador", "is_admin": true}' \
  > /dev/null 2>&1

# Iniciar Frontend
echo -e "${GREEN}🅰️  Iniciando Frontend (Angular)...${NC}"
cd ../../frontend

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências npm..."
    npm install
fi

# Iniciar frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Aplicação iniciada!"
echo "📍 Backend:  http://localhost:5000"
echo "📍 Frontend: http://localhost:4200"
echo ""
echo "🔐 Para fazer login use: admin@simple-lib.com"
echo ""
echo "Para parar os servidores: kill $BACKEND_PID $FRONTEND_PID"
echo "Ou pressione Ctrl+C"

# Manter script rodando
wait
