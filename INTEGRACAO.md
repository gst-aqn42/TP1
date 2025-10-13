# 🔗 Guia de Integração Backend ↔ Frontend

## ✅ O que foi corrigido?

### 1. **URL Base da API**
- ✅ Corrigido de `http://localhost:5000` para `http://localhost:5000/api`
- **Arquivo:** `frontend/src/app/services/api.ts`

### 2. **HTTP Interceptor para Autenticação**
- ✅ Criado interceptor que adiciona token JWT automaticamente em todas as requisições
- **Arquivo:** `frontend/src/app/interceptors/auth.interceptor.ts`
- **Registrado em:** `frontend/src/app/app.config.ts`

### 3. **AuthService Integrado**
- ✅ Removida autenticação fake
- ✅ Conectado ao endpoint `/api/auth/login` do backend
- **Arquivo:** `frontend/src/app/services/auth.ts`

### 4. **Componente ManageEvents**
- ✅ Removidos dados mockados
- ✅ Integrado com API real (GET, POST, PUT, DELETE)
- ✅ Mapeamento de campos backend ↔ frontend
- **Arquivo:** `frontend/src/app/pages/admin/manage-events/manage-events.ts`

### 5. **Bug Crítico do Backend**
- ✅ Criado arquivo `database.py` que estava faltando
- **Arquivo:** `e-lib/backend/app/services/database.py`

---

## 🚀 Como testar a integração

### Opção 1: Script Automático (Recomendado)
```bash
chmod +x start.sh
./start.sh
```

### Opção 2: Manual

#### Terminal 1 - Backend:
```bash
cd e-lib/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm install
npm start
```

#### Terminal 3 - Criar Admin:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@simple-lib.com",
    "nome": "Administrador",
    "is_admin": true
  }'
```

---

## 🔑 Como fazer login

1. Acesse: `http://localhost:4200/admin/login`
2. Use o email: `admin@simple-lib.com`
3. Clique em "Entrar"

> ⚠️ **Nota:** Sistema simplificado para trabalho acadêmico - login apenas com email, sem senha.

---

## 📊 Mapeamento de Campos

O backend usa nomes em português, o frontend em inglês. O mapeamento é feito automaticamente:

| Backend (Python) | Frontend (TypeScript) |
|------------------|----------------------|
| `_id` | `id` |
| `nome` | `name` |
| `descricao` | `description` |
| `sigla` | `sigla` ✅ |

---

## 🧪 Testar Endpoints Manualmente

### 1. Fazer Login e Pegar Token:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@simple-lib.com"}'
```

### 2. Usar Token para Criar Evento:
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:5000/api/eventos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nome": "Simpósio Teste",
    "sigla": "ST",
    "descricao": "Evento de teste"
  }'
```

### 3. Listar Eventos (público):
```bash
curl http://localhost:5000/api/eventos/
```

---

## 🔄 Fluxo de Autenticação

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│  Frontend   │         │   Backend    │         │   MongoDB    │
│  (Angular)  │         │   (Flask)    │         │              │
└──────┬──────┘         └──────┬───────┘         └──────┬───────┘
       │                       │                        │
       │  POST /auth/login     │                        │
       ├──────────────────────►│                        │
       │  {email}              │  Buscar usuário        │
       │                       ├───────────────────────►│
       │                       │◄───────────────────────┤
       │                       │  Gerar JWT             │
       │  {token, user}        │                        │
       │◄──────────────────────┤                        │
       │                       │                        │
       │  Salva token em       │                        │
       │  localStorage         │                        │
       │                       │                        │
       │  GET /eventos         │                        │
       │  Header: Bearer token │                        │
       ├──────────────────────►│                        │
       │                       │  Valida JWT            │
       │                       │  Buscar eventos        │
       │                       ├───────────────────────►│
       │                       │◄───────────────────────┤
       │  {eventos: [...]}     │                        │
       │◄──────────────────────┤                        │
```

---

## ⚠️ Problemas Conhecidos e Soluções

### Problema: CORS Error
**Solução:** Backend já tem `CORS(app)` habilitado em `app/__init__.py`

### Problema: "Token inválido"
**Solução:** Faça logout e login novamente. Token expira em 24h.

### Problema: MongoDB Connection Error
**Solução:** 
```bash
sudo systemctl start mongod
# ou
mongod --dbpath ~/data/db
```

### Problema: "404 Not Found" nas rotas
**Solução:** Verifique se está usando `/api/` no início das URLs

---

## 📝 Próximos Passos (Para Trabalho Completo)

### Já Implementado ✅
- [x] Integração básica de eventos (CRUD)
- [x] Autenticação JWT
- [x] HTTP Interceptor
- [x] Mapeamento de campos

### Falta Implementar ❌
- [ ] Integração de edições (manage-editions)
- [ ] Integração de artigos (manage-articles)
- [ ] Upload de PDF
- [ ] Sistema de busca
- [ ] Notificações por email
- [ ] Upload em massa (BibTeX)

---

## 🎯 Recomendações para o Trabalho

Para um **trabalho simples e funcional**, foque em:

1. ✅ **Manter as funcionalidades básicas integradas** (eventos, edições, artigos)
2. ✅ **Login simplificado** (apenas email, sem senha - como está agora)
3. ✅ **CRUD completo de pelo menos 2 entidades** (Eventos + Artigos)
4. ⚠️ **Não precisa implementar tudo!** Funcionalidades core são suficientes
5. ✅ **Documentar o que funciona** (este README é um bom exemplo)

### O que NÃO é crítico:
- ❌ Upload de arquivos (pode simplificar)
- ❌ Sistema de notificações (pode deixar apenas no backend)
- ❌ BibTeX (funcionalidade avançada)
- ❌ Autenticação completa com senha hash (simplificado é OK para acadêmico)

---

## 📚 Documentação de Referência

- **Backend API:** `http://localhost:5000/` (retorna info da API)
- **Frontend:** `http://localhost:4200/`
- **MongoDB:** `mongodb://localhost:27017/simple-lib`

---

Criado em: 13 de outubro de 2025  
Última atualização: Integração básica completa
