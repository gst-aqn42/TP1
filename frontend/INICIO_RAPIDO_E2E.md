# 🎯 GUIA RÁPIDO: Ver Testes E2E Rodando

## ⚡ Método Mais Simples (Recomendado)

Execute o script automatizado:

```bash
cd /home/mostqi/EngSoft/TP1/frontend
./executar_testes_e2e.sh
```

Escolha uma opção:
- **1** → Ver testes rodando (interface gráfica) 👁️
- **2** → Rodar no terminal
- **3** → Rodar + gerar cobertura 📊

---

## 🔧 Método Manual

### 1️⃣ Iniciar Backend (Terminal 1)
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source ../../venv/bin/activate
python run.py
```

### 2️⃣ Iniciar Frontend (Terminal 2)
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm start
```

### 3️⃣ Executar Testes (Terminal 3)

**VER RODANDO:**
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:open
```

**COM COBERTURA:**
```bash
cd /home/mostqi/EngSoft/TP1/frontend
npm run e2e:coverage
```

---

## 📊 Ver Relatório de Cobertura

Após executar com cobertura:

```bash
cd /home/mostqi/EngSoft/TP1/frontend
xdg-open coverage-e2e/index.html
```

---

## 🎬 O Que Acontece

### Modo Interativo (e2e:open)
1. Interface do Cypress abre
2. Você vê lista de 5 arquivos de teste
3. Clica em um teste
4. Navegador abre
5. **VÊ CADA AÇÃO ACONTECENDO EM TEMPO REAL** 🎬
   - Formulários sendo preenchidos
   - Botões sendo clicados
   - Páginas navegando
   - Validações passando

### Modo Cobertura (e2e:coverage)
1. Todos os 74 testes rodam
2. Vídeos são gravados
3. Relatório de cobertura é gerado
4. Mostra % de código testado:
   ```
   Statements   : 75.32%
   Branches     : 68.15%
   Functions    : 71.43%
   Lines        : 76.89%
   ```

---

## 📈 Comparação com Outros Testes

| Tipo | Comando | Cobertura |
|------|---------|-----------|
| **Unit** (Karma) | `npm test` | `coverage/frontend/index.html` |
| **E2E** (Cypress) | `npm run e2e:coverage` | `coverage-e2e/index.html` |
| **Integration** (Pytest) | `cd e-lib/tests && pytest --cov` | Terminal |

---

## 📁 Arquivos Gerados

```
frontend/
├── coverage-e2e/           # 📊 Cobertura E2E
│   └── index.html          # ← ABRA ESTE!
├── coverage/               # 📊 Cobertura Unit
│   └── frontend/index.html
└── cypress/
    ├── videos/             # 🎥 Vídeo de cada teste
    └── screenshots/        # 📸 Screenshots de falhas
```

---

## ✅ Checklist Rápido

- [ ] Backend rodando em `http://localhost:5000`
- [ ] Frontend rodando em `http://localhost:4200`
- [ ] Cypress instalado (`npx cypress --version`)
- [ ] Execute: `./executar_testes_e2e.sh`
- [ ] Escolha opção 1 para ver rodando
- [ ] Escolha opção 3 para gerar cobertura
- [ ] Abra `coverage-e2e/index.html` no navegador

---

## 🆘 Problemas?

Veja: `COMO_EXECUTAR_TESTES_E2E.md` (guia detalhado)

---

**Dica**: Use opção 1 (interativo) na primeira vez para ver a mágica acontecer! ✨
