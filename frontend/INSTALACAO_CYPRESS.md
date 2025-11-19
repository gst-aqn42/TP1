# Guia de Instalação do Cypress

## 🎯 Instalação do Cypress no Projeto

### Passo 1: Navegar para o diretório do frontend
```bash
cd /home/mostqi/EngSoft/TP1/frontend
```

### Passo 2: Instalar Cypress (já está no package.json)
```bash
npm install
```

Isso instalará:
- `cypress@^13.7.0`
- Todas as dependências do Cypress

### Passo 3: Verificar instalação
```bash
npx cypress --version
```

Deve mostrar algo como:
```
Cypress package version: 13.7.0
Cypress binary version: 13.7.0
```

---

## 🚀 Primeiro Teste

### 1. Iniciar o backend
```bash
# Terminal 1
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source ../../venv/bin/activate
python run.py
```

Deve mostrar:
```
* Running on http://localhost:5000
```

### 2. Iniciar o frontend
```bash
# Terminal 2
cd /home/mostqi/EngSoft/TP1/frontend
npm start
```

Aguarde até ver:
```
** Angular Live Development Server is listening on localhost:4200 **
✔ Compiled successfully.
```

### 3. Abrir Cypress
```bash
# Terminal 3
cd /home/mostqi/EngSoft/TP1/frontend
npm run cypress:open
```

### 4. Executar um teste
1. Na interface do Cypress, clique em "E2E Testing"
2. Escolha um navegador (Chrome recomendado)
3. Clique em "Start E2E Testing"
4. Selecione um teste (ex: `auth.cy.ts`)
5. Observe o teste executar!

---

## 📋 Comandos Úteis

### Modo Interativo (Recomendado para desenvolvimento)
```bash
npm run cypress:open
# ou
npm run e2e:open
```

### Modo Headless (Para CI/CD)
```bash
npm run cypress:run
# ou
npm run e2e
```

### Executar teste específico
```bash
npx cypress run --spec "cypress/e2e/auth.cy.ts"
```

### Executar em navegador específico
```bash
npx cypress run --browser chrome
npx cypress run --browser firefox
npx cypress run --browser edge
```

---

## 🐛 Troubleshooting

### Erro: "Cannot find module 'cypress'"
**Solução**:
```bash
cd frontend
npm install
```

### Erro: "Failed to connect to http://localhost:4200"
**Solução**: Certifique-se que o Angular está rodando:
```bash
cd frontend
npm start
```

### Erro: "ECONNREFUSED 127.0.0.1:5000"
**Solução**: Certifique-se que o Flask está rodando:
```bash
cd e-lib/backend
source ../../venv/bin/activate
python run.py
```

### Testes falham com "Timed out"
**Soluções**:
1. Aumente o timeout no `cypress.config.ts`
2. Verifique se backend e frontend estão respondendo
3. Verifique console do navegador para erros

### MongoDB não está rodando
**Solução**:
```bash
sudo systemctl start mongod
# ou
sudo service mongod start
```

---

## 📁 Estrutura Criada

Após instalação, você terá:

```
frontend/
├── node_modules/
│   └── cypress/               # Binários do Cypress
├── cypress/
│   ├── e2e/                   # ✅ Testes já criados
│   │   ├── auth.cy.ts
│   │   ├── eventos.cy.ts
│   │   ├── edicoes.cy.ts
│   │   ├── artigos.cy.ts
│   │   └── inscricoes.cy.ts
│   ├── support/               # ✅ Comandos já criados
│   │   ├── commands.ts
│   │   └── e2e.ts
│   ├── screenshots/           # 📸 Gerado automaticamente
│   ├── videos/                # 🎥 Gerado automaticamente
│   └── downloads/             # 📥 Para testes de download
├── cypress.config.ts          # ✅ Já configurado
├── package.json               # ✅ Já atualizado
└── TESTES_E2E.md             # ✅ Documentação
```

---

## ✅ Checklist de Instalação

- [ ] `npm install` executado
- [ ] `npx cypress --version` mostra versão
- [ ] Backend rodando em `http://localhost:5000`
- [ ] Frontend rodando em `http://localhost:4200`
- [ ] MongoDB rodando
- [ ] `npm run cypress:open` abre interface
- [ ] Consegue executar teste `auth.cy.ts`

---

## 🎓 Próximos Passos

1. **Execute os testes em modo interativo** para se familiarizar:
   ```bash
   npm run cypress:open
   ```

2. **Ajuste os testes** conforme necessário para sua implementação

3. **Execute em headless** para validar:
   ```bash
   npm run e2e
   ```

4. **Verifique relatórios**:
   - Screenshots: `cypress/screenshots/`
   - Vídeos: `cypress/videos/`

---

## 📚 Recursos

- [Cypress Documentation](https://docs.cypress.io/)
- [Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [API Commands](https://docs.cypress.io/api/table-of-contents)
- [Assertions](https://docs.cypress.io/guides/references/assertions)

---

**Pronto!** Agora você tem uma suíte completa de testes E2E com Cypress! 🎉
