#!/bin/bash

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjhlYmYwODc5NTM2MjBlMDQwYTcxZjFiIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTc2MDM3OTcxMSwiaWF0IjoxNzYwMjkzMzExfQ.DfulG99H4ZfRzWaWK5RMPglXtWzrvIyUAs0hqIpU78U"

echo "=== 1. Buscando ID do evento TESTE ==="
EVENTOS_JSON=$(curl -s http://127.0.0.1:5000/api/eventos/)
echo "$EVENTOS_JSON"

# Extrair ID do evento TESTE
ID_TESTE=$(echo "$EVENTOS_JSON" | grep -o '"TESTE"[^}]*"_id":"[^"]*' | cut -d'"' -f7)

echo "ID do evento TESTE: $ID_TESTE"

if [ -z "$ID_TESTE" ]; then
    echo "❌ Não foi possível encontrar o evento TESTE"
    exit 1
fi

echo -e "\n=== 2. Criando edições para o evento TESTE ==="

# Criar edição 2023
echo "Criando edição 2023..."
curl -X POST http://127.0.0.1:5000/api/edicoes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"evento_id\": \"$ID_TESTE\",
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
    \"evento_id\": \"$ID_TESTE\",
    \"ano\": 2024, 
    \"local\": \"Rio de Janeiro, RJ\",
    \"data_inicio\": \"2024-09-05\",
    \"data_fim\": \"2024-09-08\"
  }"
echo -e "\n"

echo -e "\n=== 3. Listando edições do evento TESTE ==="
curl -s http://127.0.0.1:5000/api/edicoes/evento/$ID_TESTE | python3 -m json.tool

echo -e "\n=== 4. Verificando edições no MongoDB ==="
mongosh simple-lib --eval "db.edicoes.find().pretty()" --quiet
