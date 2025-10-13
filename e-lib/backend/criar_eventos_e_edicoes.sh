#!/bin/bash

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjhlYmYwODc5NTM2MjBlMDQwYTcxZjFiIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTc2MDM3OTcxMSwiaWF0IjoxNzYwMjkzMzExfQ.DfulG99H4ZfRzWaWK5RMPglXtWzrvIyUAs0hqIpU78U"

echo "=== Criando eventos SBES e ICSE ==="

# Criar evento SBES
echo "Criando SBES..."
RESPONSE_SBES=$(curl -s -X POST http://127.0.0.1:5000/api/eventos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nome": "Simpósio Brasileiro de Engenharia de Software",
    "sigla": "SBES",
    "descricao": "Principal evento brasileiro de engenharia de software"
  }')
echo $RESPONSE_SBES

# Criar evento ICSE
echo "Criando ICSE..."
RESPONSE_ICSE=$(curl -s -X POST http://127.0.0.1:5000/api/eventos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nome": "International Conference on Software Engineering",
    "sigla": "ICSE",
    "descricao": "Conferência internacional de engenharia de software"
  }')
echo $RESPONSE_ICSE

# Extrair IDs dos eventos
ID_SBES=$(echo $RESPONSE_SBES | grep -o '"evento_id":"[^"]*' | cut -d'"' -f4)
ID_ICSE=$(echo $RESPONSE_ICSE | grep -o '"evento_id":"[^"]*' | cut -d'"' -f4)

echo "ID_SBES: $ID_SBES"
echo "ID_ICSE: $ID_ICSE"

# Aguardar um pouco para garantir que os eventos foram criados
sleep 2

echo -e "\n=== Criando edições para SBES e ICSE ==="

# Criar edição para SBES
if [ -n "$ID_SBES" ]; then
    echo "Criando edição para SBES 2025..."
    curl -X POST http://127.0.0.1:5000/api/edicoes/ \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d "{
        \"evento_id\": \"$ID_SBES\",
        \"ano\": 2025,
        \"local\": \"Belo Horizonte, MG\",
        \"data_inicio\": \"2025-09-15\",
        \"data_fim\": \"2025-09-18\"
      }"
    echo -e "\n"
fi

# Criar edição para ICSE
if [ -n "$ID_ICSE" ]; then
    echo "Criando edição para ICSE 2024..."
    curl -X POST http://127.0.0.1:5000/api/edicoes/ \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d "{
        \"evento_id\": \"$ID_ICSE\",
        \"ano\": 2024,
        \"local\": \"Lisboa, Portugal\",
        \"data_inicio\": \"2024-04-14\",
        \"data_fim\": \"2024-04-20\"
      }"
    echo -e "\n"
fi

echo -e "\n=== Listando todos os eventos ==="
curl -s http://127.0.0.1:5000/api/eventos/ | python3 -m json.tool

echo -e "\n=== Listando edições de cada evento ==="

if [ -n "$ID_SBES" ]; then
    echo "Edições do SBES:"
    curl -s http://127.0.0.1:5000/api/edicoes/evento/$ID_SBES | python3 -m json.tool
fi

if [ -n "$ID_ICSE" ]; then
    echo "Edições do ICSE:"
    curl -s http://127.0.0.1:5000/api/edicoes/evento/$ID_ICSE | python3 -m json.tool
fi

echo -e "\n=== Verificando todas as edições no MongoDB ==="
mongosh simple-lib --eval "db.edicoes.find().pretty()" --quiet
