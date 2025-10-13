#!/bin/bash

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjhlYmYwODc5NTM2MjBlMDQwYTcxZjFiIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTc2MDM3OTcxMSwiaWF0IjoxNzYwMjkzMzExfQ.DfulG99H4ZfRzWaWK5RMPglXtWzrvIyUAs0hqIpU78U"

echo "=== 1. Buscando eventos ==="
EVENTOS_JSON=$(curl -s http://127.0.0.1:5000/api/eventos/)
echo "$EVENTOS_JSON"

echo -e "\n=== 2. Extraindo IDs manualmente (copie e cole abaixo) ==="
echo "IDs disponíveis:"
curl -s http://127.0.0.1:5000/api/eventos/ | python3 -c "
import json, sys
data = json.load(sys.stdin)
for evento in data['eventos']:
    print(f\"Sigla: {evento['sigla']} -> ID: {evento['_id']}\")
"

echo -e "\n=== 3. Use um dos IDs acima para testar edições ==="
echo "Vou usar o primeiro evento da lista:"

# Pegar o primeiro ID automaticamente
FIRST_ID=$(curl -s http://127.0.0.1:5000/api/eventos/ | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data['eventos']:
    print(data['eventos'][0]['_id'])
")

echo "Usando ID: $FIRST_ID"

if [ -z "$FIRST_ID" ]; then
    echo "❌ Nenhum evento encontrado. Crie eventos primeiro."
    exit 1
fi

echo -e "\n=== 4. Criando edições ==="

# Criar edição 2023
echo "Criando edição 2023..."
curl -X POST http://127.0.0.1:5000/api/edicoes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"evento_id\": \"$FIRST_ID\",
    \"ano\": 2023,
    \"local\": \"São Paulo, SP\",
    \"data_inicio\": \"2023-08-10\",
    \"data_fim\": \"2023-08-12\"
  }"
echo -e "\n"

# Criar edição 2024
echo "Criando edição 2024..."
curl -X POST http://127.0.0.1:5000/api/edicoes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"evento_id\": \"$FIRST_ID\",
    \"ano\": 2024, 
    \"local\": \"Rio de Janeiro, RJ\",
    \"data_inicio\": \"2024-09-05\",
    \"data_fim\": \"2024-09-08\"
  }"
echo -e "\n"

echo -e "\n=== 5. Listando edições criadas ==="
curl -s http://127.0.0.1:5000/api/edicoes/evento/$FIRST_ID | python3 -m json.tool

echo -e "\n=== 6. Verificando no MongoDB ==="
mongosh simple-lib --eval "db.edicoes.find().pretty()" --quiet
