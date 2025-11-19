# Testes E2E com Cypress

## Visão Geral

Este projeto utiliza **Cypress** para testes End-to-End (E2E) da aplicação Angular. Os testes simulam interações reais de usuários no navegador, testando o fluxo completo da aplicação.

## 📁 Estrutura dos Testes

```
frontend/
├── cypress/
│   ├── e2e/                    # Testes E2E
│   │   ├── auth.cy.ts         # Testes de autenticação
│   │   ├── eventos.cy.ts      # Testes de eventos
│   │   ├── edicoes.cy.ts      # Testes de edições
│   │   ├── artigos.cy.ts      # Testes de artigos
│   │   └── inscricoes.cy.ts   # Testes de inscrições
│   ├── support/                # Arquivos de suporte
│   │   ├── commands.ts        # Comandos customizados
│   │   └── e2e.ts            # Configurações globais
│   ├── screenshots/           # Screenshots de falhas
│   └── videos/                # Vídeos dos testes
├── cypress.config.ts          # Configuração do Cypress
└── package.json
```

## 🚀 Instalação

### 1. Instalar dependências

```bash
cd frontend
npm install
```

Isso instalará o Cypress e todas as dependências necessárias (já configuradas no `package.json`).

### 2. Verificar instalação

```bash
npx cypress --version
```

## ▶️ Executando os Testes

### Modo Interativo (Desenvolvimento)

Abre a interface gráfica do Cypress onde você pode selecionar e executar testes individualmente:

```bash
npm run e2e:open
# ou
npm run cypress:open
```

### Modo Headless (CI/CD)

Executa todos os testes em modo headless (sem interface gráfica):

```bash
npm run e2e
# ou
npm run cypress:run
```

### Executar teste específico

```bash
# Apenas testes de autenticação
npx cypress run --spec "cypress/e2e/auth.cy.ts"

# Apenas testes de eventos
npx cypress run --spec "cypress/e2e/eventos.cy.ts"
```

### Executar em navegador específico

```bash
# Chrome
npx cypress run --browser chrome

# Firefox
npx cypress run --browser firefox

# Edge
npx cypress run --browser edge
```

## 📋 Arquivos de Teste

### 1. **auth.cy.ts** - Autenticação (9 testes)
- ✅ Exibir formulário de login
- ✅ Login com credenciais válidas
- ✅ Login com credenciais inválidas
- ✅ Validação de campos obrigatórios
- ✅ Logout
- ✅ Proteção de rotas
- ✅ Persistência de sessão
- ✅ Navegação na área admin

### 2. **eventos.cy.ts** - Eventos (15 testes)
- ✅ Listar eventos
- ✅ Criar novo evento
- ✅ Validar campos obrigatórios
- ✅ Editar evento
- ✅ Deletar evento com confirmação
- ✅ Cancelar deleção
- ✅ Fluxo CRUD completo
- ✅ Busca/filtro de eventos

### 3. **edicoes.cy.ts** - Edições (12 testes)
- ✅ Listar edições
- ✅ Criar nova edição vinculada a evento
- ✅ Criar múltiplas edições para mesmo evento
- ✅ Validar campos obrigatórios
- ✅ Editar edição
- ✅ Deletar edição
- ✅ Filtrar edições por evento
- ✅ Fluxo completo

### 4. **artigos.cy.ts** - Artigos (18 testes)
- ✅ Listar artigos
- ✅ Criar artigo sem PDF
- ✅ Criar artigo com upload de PDF
- ✅ Adicionar múltiplos autores
- ✅ Editar artigo
- ✅ Upload de PDF em artigo existente
- ✅ Buscar artigos por título
- ✅ Buscar artigos por autor
- ✅ Filtrar por edição
- ✅ Deletar artigo
- ✅ Fluxo CRUD completo

### 5. **inscricoes.cy.ts** - Inscrições (20 testes)
- ✅ Exibir formulário de inscrição
- ✅ Validar formato de email
- ✅ Inscrever email válido
- ✅ Tratar emails duplicados
- ✅ Responsividade (mobile, tablet, desktop)
- ✅ Acessibilidade (navegação por teclado, labels, etc)
- ✅ Integração com backend (interceptação de requisições)
- ✅ Tratamento de erros de rede

**TOTAL: ~74 testes E2E**

## 🛠️ Comandos Customizados

Os comandos abaixo estão definidos em `cypress/support/commands.ts`:

### `cy.loginAsAdmin()`
Faz login como administrador automaticamente.

```typescript
cy.loginAsAdmin();
cy.visit('/admin/eventos');
```

### `cy.clearDatabase()`
Limpa o localStorage para resetar a sessão.

```typescript
cy.clearDatabase();
```

## ⚙️ Configuração

### cypress.config.ts

```typescript
{
  baseUrl: 'http://localhost:4200',  // URL do frontend Angular
  env: {
    apiUrl: 'http://localhost:5000/api'  // URL do backend Flask
  }
}
```

### Timeouts

- **defaultCommandTimeout**: 10000ms (10s)
- **requestTimeout**: 10000ms (10s)
- **responseTimeout**: 10000ms (10s)

## 📊 Relatórios e Screenshots

### Screenshots

Falhas de teste geram screenshots automáticos em:
```
frontend/cypress/screenshots/
```

### Vídeos

Execuções em modo headless gravam vídeos em:
```
frontend/cypress/videos/
```

Para desabilitar vídeos (mais rápido):
```bash
npx cypress run --config video=false
```

## 🔧 Pré-requisitos para Executar

### 1. Backend Flask rodando
```bash
cd e-lib/backend
source ../../venv/bin/activate
python run.py
```

### 2. Frontend Angular rodando
```bash
cd frontend
npm start
```

### 3. Banco MongoDB rodando
```bash
# Geralmente já está rodando como serviço
mongod
```

## 💡 Boas Práticas

### 1. Isolar Testes
Cada teste deve ser independente. Use `beforeEach` para setup:

```typescript
beforeEach(() => {
  cy.clearDatabase();
  cy.loginAsAdmin();
});
```

### 2. Seletores Robustos
Prefira:
- `data-testid` attributes
- `aria-label` attributes
- IDs específicos

Evite:
- Classes CSS que podem mudar
- Textos que podem ser traduzidos

### 3. Aguardar Elementos
```typescript
cy.get('button').should('be.visible'); // ✅ Bom
cy.get('button').click();

cy.get('button').click(); // ❌ Pode falhar se elemento não carregou
```

### 4. Assertions Claras
```typescript
cy.url().should('include', '/admin');
cy.contains('Evento criado').should('be.visible');
cy.get('.lista').should('have.length', 3);
```

## 🐛 Debugging

### Modo Interativo
Use `cypress:open` e observe cada passo visualmente.

### Console Logs
```typescript
cy.get('.elemento').then(($el) => {
  console.log('Elemento:', $el);
});
```

### Pausar Execução
```typescript
cy.pause(); // Pausa a execução
```

### Time Travel
No modo interativo, clique em qualquer comando para ver o estado da aplicação naquele momento.

## 🚨 Troubleshooting

### Teste falha com "element not found"
- Aumente o timeout: `cy.get('button', { timeout: 15000 })`
- Verifique se a aplicação está rodando
- Verifique seletores

### Backend não responde
- Confirme que Flask está rodando em `http://localhost:5000`
- Verifique logs do backend
- Teste endpoint manualmente: `curl http://localhost:5000/api/eventos/`

### Frontend não carrega
- Confirme que Angular está rodando em `http://localhost:4200`
- Verifique erros no console do navegador
- Teste: `curl http://localhost:4200`

## 📚 Recursos

- [Documentação Cypress](https://docs.cypress.io/)
- [Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [API Reference](https://docs.cypress.io/api/table-of-contents)

## 🎯 Próximos Passos

1. **Instalar Cypress**:
   ```bash
   cd frontend
   npm install
   ```

2. **Iniciar aplicação**:
   ```bash
   # Terminal 1 - Backend
   cd e-lib/backend && python run.py
   
   # Terminal 2 - Frontend
   cd frontend && npm start
   ```

3. **Executar testes**:
   ```bash
   cd frontend
   npm run e2e:open  # Modo interativo
   # ou
   npm run e2e       # Modo headless
   ```

---

**Nota**: Os erros de lint nos arquivos `.cy.ts` são normais antes de instalar o Cypress. Eles desaparecerão após `npm install`.
