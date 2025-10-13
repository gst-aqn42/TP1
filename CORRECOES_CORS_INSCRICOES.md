# Correções de CORS e Inscrições

**Data:** 13 de outubro de 2025

## 🚨 Problemas Identificados

### 1. Erro CORS nas requisições
```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading 
the remote resource at http://localhost:5000/api/inscricoes. 
(Reason: CORS request did not succeed). Status code: (null).
```

### 2. Rota de inscrições inexistente
- Frontend chamava `/api/inscricoes` mas a rota não existia no backend
- Funcionalidade de envio de e-mail de confirmação não implementada

## ✅ Correções Aplicadas

### 1. Configuração CORS Melhorada

**Arquivo:** `/e-lib/backend/app/__init__.py`

**Antes:**
```python
CORS(app)  # Configuração genérica
```

**Depois:**
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:4200", "http://127.0.0.1:4200"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})
```

**Benefícios:**
- ✅ Permite requisições do frontend Angular (localhost:4200)
- ✅ Suporta todos os métodos HTTP necessários
- ✅ Permite headers de autorização para rotas protegidas
- ✅ Habilita credentials para cookies/sessões
- ✅ Cache de preflight por 1 hora (performance)

### 2. Criação da Rota de Inscrições

**Novo arquivo:** `/e-lib/backend/app/routes/inscricoes.py`

**Endpoints implementados:**

#### POST `/api/inscricoes`
- Cria nova inscrição para receber notificações
- Valida formato do email
- Verifica duplicatas
- Reativa inscrições canceladas
- Envia email de confirmação
- Retorna 201 Created

#### GET `/api/inscricoes`
- Lista todas as inscrições ativas
- Útil para administração

#### DELETE `/api/inscricoes/<email>`
- Cancela inscrição (marca como inativa)
- Não remove do banco (mantém histórico)

#### GET `/api/inscricoes/total`
- Retorna total de inscrições ativas
- Para estatísticas

**Exemplo de resposta bem-sucedida:**
```json
{
  "message": "Inscrição realizada com sucesso!",
  "email": "usuario@example.com",
  "inscricao_id": "507f1f77bcf86cd799439011"
}
```

### 3. Serviço de Email de Confirmação

**Arquivo:** `/e-lib/backend/app/services/email_service.py`

**Nova função:** `enviar_email_confirmacao_inscricao(email)`

- Envia email de boas-vindas ao novo inscrito
- Atualmente simula envio (logs no console)
- Código preparado para SMTP real quando configurado

**Para ativar envio real de emails:**
```python
# Configurar variáveis de ambiente:
export EMAIL_USER="seu-email@gmail.com"
export EMAIL_PASSWORD="sua-senha-app"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

### 4. Registro do Blueprint

**Arquivo:** `/e-lib/backend/app/__init__.py`

```python
from app.routes.inscricoes import inscricoes_bp
app.register_blueprint(inscricoes_bp, url_prefix='/api/inscricoes')
```

## 📊 Estrutura do Banco de Dados

### Collection: `inscricoes`

```json
{
  "_id": ObjectId("..."),
  "email": "usuario@example.com",
  "ativo": true,
  "data_inscricao": ISODate("2025-10-13T..."),
  "notificacoes_enviadas": 0,
  "data_reativacao": ISODate("..."),  // Se reativado
  "data_cancelamento": ISODate("...")  // Se cancelado
}
```

## 🧪 Como Testar

### 1. Reiniciar o Backend
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
./start_backend.sh
```

O backend deve mostrar no console:
```
Database configurado com sucesso!
 * Running on http://127.0.0.1:5000
```

### 2. Testar Inscrição via Frontend

1. Acesse a página inicial (http://localhost:4200)
2. Encontre o formulário de inscrição
3. Digite um email válido
4. Clique em "Inscrever"
5. Aguarde a mensagem de sucesso

**Console do Backend deve mostrar:**
```
📧 Inscrição recebida: {'email': 'teste@example.com'}
✅ Nova inscrição criada: teste@example.com (ID: ...)
📧 Simulando envio de email de confirmação para: teste@example.com
```

**Console do Frontend (F12) deve mostrar:**
```
POST http://localhost:5000/api/inscricoes 201 (Created)
```

### 3. Testar via cURL

#### Criar inscrição:
```bash
curl -X POST http://localhost:5000/api/inscricoes \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@example.com"}'
```

#### Listar inscrições:
```bash
curl http://localhost:5000/api/inscricoes
```

#### Total de inscrições:
```bash
curl http://localhost:5000/api/inscricoes/total
```

#### Cancelar inscrição:
```bash
curl -X DELETE http://localhost:5000/api/inscricoes/teste@example.com
```

### 4. Verificar no MongoDB

```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source venv/bin/activate
python3 -c "
from app.services.database import mongo

inscricoes = mongo.get_collection('inscricoes')
total = inscricoes.count_documents({'ativo': True})
print(f'Total de inscrições ativas: {total}')

for insc in inscricoes.find({'ativo': True}):
    print(f\"  - {insc['email']} (inscrito em {insc['data_inscricao']})\")
"
```

## 🔍 Logs de Debug

### Backend - Inscrições
- `📧 Inscrição recebida` - Dados recebidos
- `✅ Nova inscrição criada` - Sucesso
- `ℹ️  Email já inscrito` - Duplicata
- `✅ Inscrição reativada` - Reativação
- `⚠️  Erro ao enviar email` - Falha no email (não bloqueia inscrição)
- `❌ Erro ao criar inscrição` - Erro crítico

### Frontend - Subscribe Form
- Mensagem de sucesso: "Inscrição realizada com sucesso! Você receberá notificações sobre novos artigos."
- Mensagem de erro: "Erro ao realizar inscrição. Tente novamente."

## ⚙️ Validações Implementadas

1. **Email obrigatório** - Retorna 400 se ausente
2. **Formato de email** - Regex validation
3. **Duplicatas** - Verifica antes de inserir
4. **Normalização** - Email sempre lowercase e trimmed
5. **Soft delete** - Marca como inativo em vez de deletar

## 🚀 Próximos Passos Sugeridos

1. **Configurar SMTP real** para envio de emails
2. **Criar página de gerenciamento** de inscrições no admin
3. **Implementar unsubscribe link** nos emails
4. **Adicionar CAPTCHA** para prevenir spam
5. **Criar sistema de templates** para emails HTML
6. **Implementar rate limiting** para inscrições
7. **Adicionar métricas** de abertura de emails
8. **Criar confirmação dupla** (double opt-in)

## 📝 Notas Importantes

- ⚠️ **Emails estão simulados** - Configure SMTP para produção
- 🔒 **CORS em desenvolvimento** - Ajustar origins para produção
- 📊 **Soft deletes** - Inscrições canceladas ficam no banco
- 🔄 **Reativação automática** - Reinscrição reativa email anterior
