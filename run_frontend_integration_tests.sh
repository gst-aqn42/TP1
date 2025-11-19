#!/bin/bash

# Script para executar testes de integração Frontend → Backend
# Localização: /home/mostqi/EngSoft/TP1/

echo "========================================="
echo "Testes de Integração Frontend → Backend"
echo "========================================="
echo ""

# Ativa o ambiente virtual
source venv/bin/activate

# Opção 1: Executar todos os testes de integração frontend
echo "Opção 1: Executar todos os testes"
echo "Comando: pytest e-lib/tests/integration/test_frontend_*.py -v"
echo ""

# Opção 2: Executar com coverage
echo "Opção 2: Executar com coverage"
echo "Comando: pytest e-lib/tests/integration/test_frontend_*.py --cov=e-lib/backend/app/routes --cov-report=html -v"
echo ""

# Opção 3: Executar teste específico
echo "Opção 3: Executar teste específico"
echo "Auth:        pytest e-lib/tests/integration/test_frontend_auth.py -v"
echo "Eventos:     pytest e-lib/tests/integration/test_frontend_eventos.py -v"
echo "Edições:     pytest e-lib/tests/integration/test_frontend_edicoes.py -v"
echo "Artigos:     pytest e-lib/tests/integration/test_frontend_artigos.py -v"
echo "Batch:       pytest e-lib/tests/integration/test_frontend_batch.py -v"
echo "Inscrições:  pytest e-lib/tests/integration/test_frontend_inscricoes.py -v"
echo ""

# Pergunta ao usuário qual opção executar
echo "Escolha uma opção (1, 2, 3) ou 'q' para sair:"
read opcao

case $opcao in
    1)
        echo "Executando todos os testes..."
        pytest e-lib/tests/integration/test_frontend_*.py -v
        ;;
    2)
        echo "Executando com coverage..."
        pytest e-lib/tests/integration/test_frontend_*.py --cov=e-lib/backend/app/routes --cov-report=html -v
        echo ""
        echo "Relatório HTML gerado em: htmlcov/index.html"
        ;;
    3)
        echo "Qual teste específico?"
        echo "1) Auth"
        echo "2) Eventos"
        echo "3) Edições"
        echo "4) Artigos"
        echo "5) Batch Upload"
        echo "6) Inscrições"
        read teste
        
        case $teste in
            1) pytest e-lib/tests/integration/test_frontend_auth.py -v ;;
            2) pytest e-lib/tests/integration/test_frontend_eventos.py -v ;;
            3) pytest e-lib/tests/integration/test_frontend_edicoes.py -v ;;
            4) pytest e-lib/tests/integration/test_frontend_artigos.py -v ;;
            5) pytest e-lib/tests/integration/test_frontend_batch.py -v ;;
            6) pytest e-lib/tests/integration/test_frontend_inscricoes.py -v ;;
            *) echo "Opção inválida" ;;
        esac
        ;;
    q)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida"
        ;;
esac
