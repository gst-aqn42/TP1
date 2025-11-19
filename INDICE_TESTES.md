# 📚 Índice Completo de Testes - E-Lib

## 🎯 Início Rápido

### Para ver testes E2E rodando AGORA:
```bash
cd /home/mostqi/EngSoft/TP1/frontend
./executar_testes_e2e.sh
```
Escolha opção **1** para ver testes rodando visualmente! 👁️

---

## 📖 Documentação por Tipo de Teste

### 🔬 Testes Unitários (Unit Tests)
- **Quantidade**: 136 testes
- **Framework**: Karma + Jasmine
- **Executar**: `cd frontend && npm test`
- **Cobertura**: `coverage/frontend/index.html`
- **Documentação**: `frontend/src/app/README.md`

### 🔗 Testes de Integração (Integration Tests)
- **Quantidade**: 66 testes
- **Framework**: Pytest
- **Executar**: `cd e-lib/tests && pytest`
- **Cobertura**: `pytest --cov`
- **Documentação**: `e-lib/tests/README.md`

### 🌐 Testes E2E (End-to-End Tests)
- **Quantidade**: 74 testes
- **Framework**: Cypress
- **Executar**: `cd frontend && npm run e2e:open`
- **Cobertura**: `coverage-e2e/index.html`
- **Documentação**: ⬇️ Veja abaixo

---

## 📂 Documentação de Testes E2E

### 🚀 Guias de Execução

1. **INICIO_RAPIDO_E2E.md** ⭐
   - Comandos rápidos
   - Métodos automático e manual
   - Checklist
   - **USE ESTE PRIMEIRO!**

2. **COMO_EXECUTAR_TESTES_E2E.md**
   - Guia completo passo a passo
   - Explicação detalhada de cada modo
   - O que você vai ver em cada execução
   - Troubleshooting básico

3. **executar_testes_e2e.sh** 🤖
   - Script automatizado
   - Inicia backend e frontend automaticamente
   - Menu interativo
   - **RECOMENDADO PARA INICIANTES**

### 📚 Documentação Técnica

4. **TESTES_E2E.md**
   - Documentação completa dos testes
   - Estrutura de cada teste
   - Comandos customizados
   - Best practices
   - Debugging avançado

5. **INSTALACAO_CYPRESS.md**
   - Guia de instalação
   - Configuração inicial
   - Checklist de setup
   - Próximos passos

### 🐛 Troubleshooting

6. **TROUBLESHOOTING_COBERTURA.md**
   - Problemas comuns com cobertura
   - Diferenças entre cobertura Unit vs E2E
   - Como melhorar cobertura
   - Recomendações finais

### 📊 Relatórios

7. **RESUMO_TESTES.md** (na raiz do projeto)
   - Visão geral de TODOS os testes
   - 276 testes totais (Unit + Integration + E2E)
   - Comparação entre tipos
   - Estatísticas completas

---

## 🗂️ Estrutura de Arquivos de Teste

```
/home/mostqi/EngSoft/TP1/
│
├── frontend/                           # FRONTEND ANGULAR
│   │
│   ├── 📄 INICIO_RAPIDO_E2E.md        # ⭐ COMECE AQUI!
│   ├── 📄 COMO_EXECUTAR_TESTES_E2E.md # Guia completo
│   ├── 📄 INSTALACAO_CYPRESS.md       # Setup inicial
│   ├── 📄 TESTES_E2E.md               # Documentação técnica
│   ├── 📄 TROUBLESHOOTING_COBERTURA.md # Problemas e soluções
│   ├── 🤖 executar_testes_e2e.sh      # Script automatizado
│   │
│   ├── cypress/                        # TESTES E2E
│   │   ├── e2e/
│   │   │   ├── auth.cy.ts             # 9 testes de autenticação
│   │   │   ├── eventos.cy.ts          # 15 testes de eventos
│   │   │   ├── edicoes.cy.ts          # 12 testes de edições
│   │   │   ├── artigos.cy.ts          # 18 testes de artigos
│   │   │   └── inscricoes.cy.ts       # 20 testes de inscrições
│   │   │
│   │   ├── support/
│   │   │   ├── commands.ts            # Comandos customizados
│   │   │   └── e2e.ts                 # Configuração global
│   │   │
│   │   ├── videos/                    # 🎥 Vídeos dos testes
│   │   └── screenshots/               # 📸 Screenshots
│   │
│   ├── src/                            # CÓDIGO FONTE
│   │   └── app/
│   │       └── **/*.spec.ts           # 136 testes unitários
│   │
│   ├── coverage/                       # 📊 COBERTURA UNIT
│   │   └── frontend/index.html
│   │
│   ├── coverage-e2e/                   # 📊 COBERTURA E2E
│   │   └── index.html
│   │
│   ├── cypress.config.ts               # Configuração Cypress
│   ├── .nycrc.json                     # Configuração cobertura
│   └── package.json                    # Scripts npm
│
├── e-lib/                              # BACKEND FLASK
│   ├── backend/
│   │   ├── app/                        # Código fonte
│   │   └── run.py                      # Servidor Flask
│   │
│   └── tests/                          # TESTES DE INTEGRAÇÃO
│       ├── test_*.py                   # 66 testes
│       └── README.md                   # Documentação
│
└── 📄 RESUMO_TESTES.md                 # VISÃO GERAL COMPLETA
```

---

## 🎮 Comandos Principais

### Executar Testes

```bash
# Unit Tests (Frontend)
cd /home/mostqi/EngSoft/TP1/frontend
npm test

# Integration Tests (Backend)
cd /home/mostqi/EngSoft/TP1/e-lib/tests
pytest

# E2E Tests (Modo Interativo) ⭐
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:open

# E2E Tests (Modo Headless)
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e

# E2E Tests (Com Cobertura)
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:coverage

# TUDO AUTOMATIZADO 🤖
cd /home/mostqi/EngSoft/TP1/frontend
./executar_testes_e2e.sh
```

### Visualizar Cobertura

```bash
# Cobertura Unit
xdg-open /home/mostqi/EngSoft/TP1/frontend/coverage/frontend/index.html

# Cobertura E2E
xdg-open /home/mostqi/EngSoft/TP1/frontend/coverage-e2e/index.html
```

---

## 📊 Estatísticas do Projeto

| Tipo | Quantidade | Framework | Cobertura |
|------|------------|-----------|-----------|
| **Unit** | 136 testes | Karma/Jasmine | ~80-90% |
| **Integration** | 66 testes | Pytest | ~75-85% |
| **E2E** | 74 testes | Cypress | ~60-70% |
| **TOTAL** | **276 testes** | - | - |

### Distribuição dos Testes E2E

| Arquivo | Testes | Funcionalidade |
|---------|--------|----------------|
| auth.cy.ts | 9 | Login, Logout, Sessão |
| eventos.cy.ts | 15 | CRUD de Eventos |
| edicoes.cy.ts | 12 | CRUD de Edições |
| artigos.cy.ts | 18 | CRUD de Artigos + Upload PDF |
| inscricoes.cy.ts | 20 | Formulário + Validação + Responsividade |
| **TOTAL** | **74** | - |

---

## 🎯 Fluxo de Trabalho Recomendado

### 1. Desenvolvimento de Nova Feature

```bash
# 1. Escrever código
# 2. Adicionar unit tests
npm test

# 3. Verificar cobertura
npm test -- --code-coverage

# 4. Adicionar integration tests
cd ../e-lib/tests
pytest

# 5. Adicionar E2E test
cd ../../frontend
# Editar cypress/e2e/[feature].cy.ts

# 6. Testar E2E visualmente
npm run e2e:open

# 7. Executar todos os testes
./executar_testes_e2e.sh
```

### 2. Antes de Commit

```bash
# Executar todos os testes
cd /home/mostqi/EngSoft/TP1/frontend
npm test && npm run e2e

cd ../e-lib/tests
pytest
```

### 3. CI/CD Pipeline

```bash
# Unit Tests
npm test -- --browsers=ChromeHeadless --watch=false

# Integration Tests
pytest --cov --cov-report=html

# E2E Tests
npm run e2e:coverage
```

---

## 🆘 Precisa de Ajuda?

### Problemas Comuns

1. **"Não consigo ver os testes rodando"**
   → Leia: `INICIO_RAPIDO_E2E.md`

2. **"Testes falham"**
   → Leia: `TESTES_E2E.md` (seção Troubleshooting)

3. **"Cobertura não funciona"**
   → Leia: `TROUBLESHOOTING_COBERTURA.md`

4. **"Como instalar Cypress?"**
   → Leia: `INSTALACAO_CYPRESS.md`

5. **"Quero entender os testes"**
   → Leia: `TESTES_E2E.md` (seção Estrutura dos Testes)

---

## 🌟 Melhores Práticas

### ✅ FAÇA

- Use `npm run e2e:open` para desenvolvimento
- Execute todos os testes antes de commit
- Mantenha cobertura acima de 80% (unit tests)
- Teste fluxos principais com E2E
- Use script automatizado (`executar_testes_e2e.sh`)

### ❌ NÃO FAÇA

- Commitar código sem testes
- Ignorar testes falhando
- Testar apenas com E2E (lento)
- Deletar testes antigos sem razão
- Executar E2E sem backend/frontend rodando

---

## 🚀 Próximos Passos

1. ✅ **Executar testes pela primeira vez**
   ```bash
   cd /home/mostqi/EngSoft/TP1/frontend
   ./executar_testes_e2e.sh
   ```

2. ✅ **Ver testes rodando visualmente**
   - Escolha opção 1 no menu

3. ✅ **Gerar relatório de cobertura**
   - Escolha opção 3 no menu

4. ✅ **Explorar documentação**
   - Leia `INICIO_RAPIDO_E2E.md`
   - Explore outros arquivos conforme necessidade

---

## 📞 Suporte

- **Documentação Cypress**: https://docs.cypress.io/
- **Angular Testing**: https://angular.io/guide/testing
- **Pytest**: https://docs.pytest.org/

---

**Última atualização**: 19 de novembro de 2025

**Desenvolvido para**: Projeto E-Lib - Engenharia de Software TP1
