#!/bin/bash

# Script para executar testes E2E com Cypress
# Localização: /home/mostqi/EngSoft/TP1/frontend/

echo "================================================="
echo "Testes E2E com Cypress"
echo "================================================="
echo ""

# Verifica se está no diretório correto
if [ ! -f "package.json" ]; then
    echo "❌ Erro: Execute este script no diretório frontend/"
    exit 1
fi

# Verifica se Cypress está instalado
if [ ! -d "node_modules/cypress" ]; then
    echo "⚠️  Cypress não encontrado. Instalando..."
    npm install
fi

echo "Escolha uma opção:"
echo "1) Abrir Cypress (Modo Interativo)"
echo "2) Executar todos os testes (Headless)"
echo "3) Executar teste de Autenticação"
echo "4) Executar teste de Eventos"
echo "5) Executar teste de Edições"
echo "6) Executar teste de Artigos"
echo "7) Executar teste de Inscrições"
echo "8) Executar testes com Chrome"
echo "9) Executar testes com Firefox"
echo "q) Sair"
echo ""
echo -n "Opção: "
read opcao

case $opcao in
    1)
        echo "🔧 Abrindo Cypress em modo interativo..."
        npm run cypress:open
        ;;
    2)
        echo "🚀 Executando todos os testes..."
        npm run cypress:run
        ;;
    3)
        echo "🔐 Executando testes de Autenticação..."
        npx cypress run --spec "cypress/e2e/auth.cy.ts"
        ;;
    4)
        echo "📅 Executando testes de Eventos..."
        npx cypress run --spec "cypress/e2e/eventos.cy.ts"
        ;;
    5)
        echo "📚 Executando testes de Edições..."
        npx cypress run --spec "cypress/e2e/edicoes.cy.ts"
        ;;
    6)
        echo "📝 Executando testes de Artigos..."
        npx cypress run --spec "cypress/e2e/artigos.cy.ts"
        ;;
    7)
        echo "✉️  Executando testes de Inscrições..."
        npx cypress run --spec "cypress/e2e/inscricoes.cy.ts"
        ;;
    8)
        echo "🌐 Executando testes no Chrome..."
        npm run cypress:run -- --browser chrome
        ;;
    9)
        echo "🦊 Executando testes no Firefox..."
        npm run cypress:run -- --browser firefox
        ;;
    q)
        echo "👋 Saindo..."
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "✅ Execução concluída!"
echo ""
echo "📊 Resultados:"
echo "   - Screenshots: cypress/screenshots/"
echo "   - Vídeos: cypress/videos/"
