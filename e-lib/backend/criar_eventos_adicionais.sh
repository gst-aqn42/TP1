#!/bin/bash

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjhlYmYwODc5NTM2MjBlMDQwYTcxZjFiIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTc2MDM3OTcxMSwiaWF0IjoxNzYwMjkzMzExfQ.DfulG99H4ZfRzWaWK5RMPglXtWzrvIyUAs0hqIpU78U"

echo "=== Criando eventos SBES e ICSE ==="

# Criar SBES
echo "Criando SBES..."
curl -X POST http://127.0.0.1:5000/api/eventos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nome": "Simpósio Brasileiro de Engenharia de Software",
    "sigla": "SBES",
    "descricao": "Principal evento brasileiro de engenharia de software"
  }'

echo -e "\n"

# Criar ICSE
echo "Criando ICSE..."
curl -X POST http://127.0.0.1:5000/api/eventos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nome": "International Conference on Software Engineering",
    "sigla": "ICSE", 
    "descricao": "Conferência internacional de engenharia de software"
  }'

echo -e "\n=== Listando todos os eventos ==="
curl -s http://127.0.0.1:5000/api/eventos/ | python3 -m json.tool
