# 🚀 Guia Completo: Executar Testes E2E com Cobertura

## 📋 Pré-requisitos

✅ Cypress instalado
✅ Dependências de cobertura instaladas
✅ Configuração completa

---

## 🎯 Passo a Passo para Ver os Testes Rodando

### **Passo 1: Iniciar o Backend (Terminal 1)**

```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source ../../venv/bin/activate
python run.py
```

**Aguarde ver:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

---

### **Passo 2: Iniciar o Frontend (Terminal 2)**

```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm start
```

**Aguarde ver:**
```
** Angular Live Development Server is listening on localhost:4200 **
✔ Compiled successfully.
```

---

### **Passo 3: Executar Testes E2E (Terminal 3)**

Você tem 3 opções:

#### **Opção A: Modo Interativo (Recomendado para primeira vez)** 👁️
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:open
```

- Interface gráfica do Cypress abre
- Clique em "E2E Testing"
- Escolha navegador (Chrome recomendado)
- Clique em um teste para ver executando em tempo real
- **VISUAL**: Você vê cada ação acontecendo! 🎬

#### **Opção B: Modo Headless com Cobertura** 📊
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:coverage
```

- Roda todos os testes no terminal
- **Gera relatório de cobertura**
- Mostra resumo de cobertura no terminal
- Cria pasta `coverage-e2e/` com relatório HTML

#### **Opção C: Modo Headless Simples** 🏃
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e
```

- Roda todos os testes
- Não gera relatório de cobertura
- Mais rápido

---

## 📊 Como Ver a Cobertura dos Testes E2E

### **Método 1: Executar e Abrir Relatório**

```bash
# 1. Executar testes com cobertura
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:coverage

# 2. Abrir relatório no navegador
xdg-open coverage-e2e/index.html
# OU
firefox coverage-e2e/index.html
# OU
google-chrome coverage-e2e/index.html
```

### **Método 2: Visualizar no Terminal**

```bash
npm run e2e:coverage
```

Vai mostrar algo assim:
```
=============================== Coverage summary ===============================
Statements   : 75.32% ( 234/311 )
Branches     : 68.15% ( 92/135 )
Functions    : 71.43% ( 50/70 )
Lines        : 76.89% ( 230/299 )
================================================================================
```

---

## 📁 Estrutura de Relatórios

Após executar os testes, você terá:

```
frontend/
├── coverage-e2e/              # 📊 Cobertura dos testes E2E
│   ├── index.html             # ← ABRA ESTE ARQUIVO!
│   ├── lcov-report/
│   │   └── index.html
│   └── lcov.info
│
├── coverage/                  # 📊 Cobertura dos testes unitários
│   └── frontend/
│       └── index.html         # ← Cobertura unit tests
│
├── cypress/
│   ├── videos/                # 🎥 Vídeos dos testes
│   │   ├── auth.cy.ts.mp4
│   │   ├── eventos.cy.ts.mp4
│   │   └── ...
│   │
│   └── screenshots/           # 📸 Screenshots (quando falham)
│       └── (quando há falhas)
```

---

## 🎬 O Que Você Vai Ver

### **No Modo Interativo (e2e:open)**

1. **Interface do Cypress** abre
2. **Lista de testes** aparece:
   - auth.cy.ts (9 testes)
   - eventos.cy.ts (15 testes)
   - edicoes.cy.ts (12 testes)
   - artigos.cy.ts (18 testes)
   - inscricoes.cy.ts (20 testes)

3. **Clique em um teste** para ver:
   - Navegador abre ao lado
   - Cada comando executando
   - Elementos sendo clicados
   - Formulários sendo preenchidos
   - Validações acontecendo
   - ✅ ou ❌ para cada asserção

### **No Modo Headless (e2e:coverage)**

```
  Running:  auth.cy.ts                                               (1 of 5)

  Testes de Autenticação
    ✓ deve exibir página de login (543ms)
    ✓ deve fazer login com credenciais válidas (892ms)
    ✓ deve mostrar erro com credenciais inválidas (234ms)
    ...
    
  9 passing (4s)

  Running:  eventos.cy.ts                                            (2 of 5)
  
  Gerenciamento de Eventos
    ✓ deve listar eventos existentes (342ms)
    ✓ deve criar novo evento (1234ms)
    ...
    
  15 passing (8s)
  
  ...
  
  ====================================
  
    (Run Finished)
  
       Spec                    Tests  Passing  Failing  Pending  Skipped
  ┌────────────────────────────────────────────────────────────────────┐
  │ ✔  auth.cy.ts              9        9        -        -        -    │
  │ ✔  eventos.cy.ts          15       15        -        -        -    │
  │ ✔  edicoes.cy.ts          12       12        -        -        -    │
  │ ✔  artigos.cy.ts          18       18        -        -        -    │
  │ ✔  inscricoes.cy.ts       20       20        -        -        -    │
  └────────────────────────────────────────────────────────────────────┘
    ✔  All specs passed!       74       74        -        -        -
  
  
  =============================== Coverage summary ===============================
  Statements   : 75.32% ( 234/311 )
  Branches     : 68.15% ( 92/135 )
  Functions    : 71.43% ( 50/70 )
  Lines        : 76.89% ( 230/299 )
  ================================================================================
```

---

## 📊 Visualizando Relatório de Cobertura

### **Abrir Relatório HTML**

```bash
cd /home/mostqi/EngSoft/TP1/frontend
xdg-open coverage-e2e/index.html
```

### **O que você verá:**

1. **Dashboard Principal**
   - % de Statements cobertos
   - % de Branches cobertos
   - % de Functions cobertos
   - % de Lines cobertos

2. **Lista de Arquivos**
   - Cada arquivo .ts do seu projeto
   - Cores indicando cobertura:
     - 🟢 Verde: Alta cobertura (>80%)
     - 🟡 Amarelo: Média cobertura (50-80%)
     - 🔴 Vermelho: Baixa cobertura (<50%)

3. **Clique em um arquivo** para ver:
   - Código-fonte com highlights
   - Linhas verdes: executadas pelos testes
   - Linhas vermelhas: NÃO executadas
   - Linhas amarelas: parcialmente executadas

---

## 🔄 Comparando Coberturas

Você tem 3 níveis de testes:

### **1. Testes Unitários (Karma/Jasmine)**
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm test
# Cobertura em: coverage/frontend/index.html
```

### **2. Testes de Integração (Backend + Frontend)**
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/tests
pytest --cov
# Cobertura do backend
```

### **3. Testes E2E (Cypress)**
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:coverage
# Cobertura em: coverage-e2e/index.html
```

---

## 🎯 Resumo dos Comandos

### **Sequência Completa (Primeira Execução)**

```bash
# Terminal 1: Backend
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source ../../venv/bin/activate
python run.py

# Terminal 2: Frontend
cd /home/mostqi/EngSoft/TP1/frontend
npm start

# Terminal 3: Testes E2E (Modo Interativo)
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:open
```

### **Sequência para CI/CD (Automatizado)**

```bash
# Terminal 1: Backend
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source ../../venv/bin/activate
python run.py &

# Terminal 2: Frontend
cd /home/mostqi/EngSoft/TP1/frontend
npm start &

# Aguardar serviços iniciarem (30s)
sleep 30

# Terminal 3: Testes E2E com Cobertura
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:coverage

# Abrir relatório
xdg-open coverage-e2e/index.html
```

---

## 🐛 Troubleshooting

### **Problema: "Error: connect ECONNREFUSED 127.0.0.1:4200"**
**Solução**: Frontend não está rodando
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm start
```

### **Problema: "Error: connect ECONNREFUSED 127.0.0.1:5000"**
**Solução**: Backend não está rodando
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source ../../venv/bin/activate
python run.py
```

### **Problema: "No tests found"**
**Solução**: Verificar caminho dos testes
```bash
cd /home/mostqi/EngSoft/TP1/frontend
ls cypress/e2e/
# Deve listar: auth.cy.ts, eventos.cy.ts, etc.
```

### **Problema: "Cobertura 0%"**
**Solução**: Código não está instrumentado. Cypress code coverage precisa que a aplicação seja servida com instrumentação. Para Angular, pode ser necessário configuração adicional.

---

## 📈 Próximos Passos

1. ✅ **Execute no modo interativo** primeiro para ver os testes rodando
2. ✅ **Execute com cobertura** para gerar relatórios
3. ✅ **Abra o relatório HTML** para analisar cobertura
4. ✅ **Compare com cobertura dos unit tests**
5. ✅ **Identifique áreas sem cobertura**
6. ✅ **Adicione mais testes** se necessário

---

## 🎉 Pronto!

Agora você pode:
- ✅ Ver testes E2E rodando em tempo real
- ✅ Executar testes em modo headless
- ✅ Visualizar cobertura de código
- ✅ Comparar com outros níveis de teste
- ✅ Gerar relatórios para análise

---

**Dica**: Sempre execute no modo interativo primeiro para debugar e entender o que os testes fazem! 👁️
