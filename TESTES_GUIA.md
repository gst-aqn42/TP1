# 🔧 CORREÇÕES E RESPOSTAS - e-lib

---

## 📋 PROBLEMAS REPORTADOS E SOLUÇÕES

### ✅ **1. Botão "Explorar Todos os Eventos" não funciona**

**Problema:** Botão não navegava para página de eventos.

**Solução Implementada:**
- ✅ Atualizado `/frontend/src/app/pages/events/events.ts` com integração ao backend
- ✅ Criado template HTML completo com lista de eventos
- ✅ Adicionado navegação ao clicar em eventos
- ✅ Spinner de loading enquanto carrega dados

**Arquivos Modificados:**
- `frontend/src/app/pages/events/events.ts` - Integrado com ApiService
- `frontend/src/app/pages/events/events.html` - Template completo
- `frontend/src/app/pages/home/home.ts` - Método `navigateToEvent()`

---

### ✅ **2. Clicar em Evento não faz nada**

**Problema:** Cards de eventos na home não tinham ação de clique.

**Solução Implementada:**
- ✅ Adicionado `(click)="navigateToEvent(event.id!, event.sigla!)"` nos cards
- ✅ Adicionado `cursor: pointer` para indicar interatividade
- ✅ Método navega para `/event/{sigla}`

**Código Aplicado em `home.html`:**
```html
<mat-card *ngFor="let event of topEvents; let i = index" 
          class="event-card"
          (click)="navigateToEvent(event.id!, event.sigla!)"
          style="cursor: pointer;">
```

---

### ⚠️ **3. "Ver PDF" redireciona para Example Domain**

**Problema:** Links de PDF apontam para `http://example.com` (dados mock).

**Causa:** Páginas home, search, author, edition ainda usam URLs fictícias.

**Solução Necessária:**

#### **A. Adicionar rota de download de PDF no backend**

Criar em `/e-lib/backend/app/routes/artigos.py`:

```python
@artigos_bp.route('/<artigo_id>/pdf', methods=['GET'])
def download_pdf(artigo_id):
    """Download do PDF do artigo"""
    try:
        artigo = Artigo.find_by_id(artigo_id)
        if not artigo or not artigo.get('pdf_path'):
            return jsonify({'error': 'PDF não encontrado'}), 404
        
        pdf_path = artigo['pdf_path']
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'Arquivo PDF não existe no servidor'}), 404
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=False,  # Abre no navegador
            download_name=f"{artigo['titulo']}.pdf"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

**Adicionar import:**
```python
from flask import send_file
```

#### **B. Páginas que precisam ser corrigidas:**

1. **`frontend/src/app/pages/home/home.ts`** ✅ **JÁ CORRIGIDO**
   ```typescript
   openPdf(articleId: string): void {
     if (articleId) {
       window.open(`http://localhost:5000/api/artigos/${articleId}/pdf`, '_blank');
     }
   }
   ```

2. **`frontend/src/app/pages/search-page/search-page.ts`** - Precisa correção
3. **`frontend/src/app/pages/author-page/author-page.ts`** - Precisa correção  
4. **`frontend/src/app/pages/edition-page/edition-page.ts`** - Precisa correção

**Correção a aplicar em todas:**
```typescript
openPdf(articleId: string): void {
  if (articleId) {
    window.open(`http://localhost:5000/api/artigos/${articleId}/pdf`, '_blank');
  } else {
    this.snackBar.open('PDF não disponível para este artigo', 'Fechar', {
      duration: 3000
    });
  }
}
```

---

### ✅ **4. Cadastro de artigo único não funciona mais**

**Problema:** Interface de cadastro manual ficou confusa com duas páginas separadas.

**Solução Recomendada:** Unificar em UMA única página de Artigos.

#### **Proposta de Interface Unificada:**

```
┌─────────────────────────────────────────────────────────┐
│  GERENCIAMENTO DE ARTIGOS                               │
├─────────────────────────────────────────────────────────┤
│  [Artigo Individual] [Upload em Massa]   <-- Abas      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ABA 1: Artigo Individual                               │
│  ┌────────────────────────────────────────────┐        │
│  │ [+ Novo Artigo]                            │        │
│  │                                             │        │
│  │ Tabela de Artigos (com filtros)            │        │
│  │ - Editar, Excluir, Upload PDF              │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│  ABA 2: Upload em Massa                                │
│  ┌────────────────────────────────────────────┐        │
│  │ Arraste arquivo .bib aqui                  │        │
│  │ ou clique para selecionar                  │        │
│  │                                             │        │
│  │ [Processar Arquivo BibTeX]                 │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 **LOCALIZAÇÃO DO ARQUIVO BIBTEX**

### **Arquivo para Upload:**

```
/home/mostqi/EngSoft/TP1/e-lib/backend/seed_data.bib
```

**Conteúdo:** 22 artigos de teste prontos para importação

**Como usar:**

#### **Opção 1: Via Interface Web (Recomendado)**
1. Fazer login como admin: `http://localhost:4200/admin`
2. Ir para **"Batch Upload"** ou **"Artigos"** (aba Upload em Massa)
3. Clicar em **"Selecionar Arquivo"**
4. Navegar até: `/home/mostqi/EngSoft/TP1/e-lib/backend/seed_data.bib`
5. Clicar em **"Processar Arquivo"**
6. Aguardar processamento (5-10 segundos)
7. Ver estatísticas na notificação

#### **Opção 2: Via Linha de Comando**
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python seed_bibtex.py seed_data.bib
```

**Resultado Esperado:**
```
✅ SEED COMPLETO!
📊 Estatísticas:
  • Eventos criados: 2
  • Edições criadas: 4
  • Artigos criados: 22
  • Artigos duplicados: 0
```

---

## 🧪 TESTES UNITÁRIOS E FUNCIONAIS

### **GUIA COMPLETO DE TESTES DO SISTEMA e-lib**

---

## **1. TESTES FUNCIONAIS - FRONTEND**

### **Teste 1.1: Navegação na Home Page**

**Objetivo:** Verificar se a home carrega artigos e eventos do backend

**Pré-requisitos:**
- Backend rodando em `localhost:5000`
- Frontend rodando em `localhost:4200`
- Banco de dados populado (executar `seed_bibtex.py`)

**Passos:**
1. Abrir navegador em `http://localhost:4200`
2. Aguardar carregamento da página

**Resultado Esperado:**
- ✅ Aparecem 5 artigos na seção "Artigos em Destaque"
- ✅ Aparecem 5 eventos na seção "Eventos em Destaque"
- ✅ Cada artigo mostra: título, autores, resumo, ano
- ✅ Cada evento mostra: nome, sigla, descrição

**Critérios de Falha:**
- ❌ Nenhum artigo aparece
- ❌ Nenhum evento aparece
- ❌ Erro 404 no console do navegador
- ❌ Loading infinito

---

### **Teste 1.2: Clique em Evento**

**Objetivo:** Verificar navegação ao clicar em um evento

**Passos:**
1. Na home page, localizar um evento (ex: "SBES")
2. Clicar no card do evento

**Resultado Esperado:**
- ✅ URL muda para `/event/SBES`
- ✅ Página de detalhes do evento abre
- ✅ Mostra informações do evento
- ✅ Lista edições do evento

**Critérios de Falha:**
- ❌ Nada acontece ao clicar
- ❌ Erro 404
- ❌ Página em branco

---

### **Teste 1.3: Botão "Explorar Todos os Eventos"**

**Objetivo:** Verificar navegação para lista completa de eventos

**Passos:**
1. Na home page, rolar até seção "Eventos em Destaque"
2. Clicar no botão **"Explorar Todos os Eventos"**

**Resultado Esperado:**
- ✅ URL muda para `/events`
- ✅ Página lista TODOS os eventos do banco
- ✅ Cada evento é clicável
- ✅ Spinner aparece durante carregamento

**Critérios de Falha:**
- ❌ Botão não responde
- ❌ Página vazia
- ❌ Erro no console

---

### **Teste 1.4: Download de PDF**

**Objetivo:** Verificar download de PDF de artigo

**Pré-requisitos:**
- Pelo menos 1 artigo com PDF anexado

**Passos:**
1. Na home page, localizar artigo com botão "Ver PDF"
2. Clicar no botão **"Ver PDF"**

**Resultado Esperado:**
- ✅ Nova aba abre no navegador
- ✅ PDF é exibido (se backend tiver rota implementada)
- ✅ OU mensagem "PDF não disponível" (se artigo não tiver PDF)

**Resultado Atual (Bug Conhecido):**
- ❌ Abre `example.com` (dados mock)
- **Correção:** Implementar rota `/api/artigos/:id/pdf` no backend

---

### **Teste 1.5: Busca de Artigos**

**Objetivo:** Verificar funcionalidade de busca

**Passos:**
1. Clicar em **"Buscar Todos os Artigos"** ou ir para `/search`
2. Digitar termo de busca: "software"
3. Clicar em **"Buscar"**

**Resultado Esperado:**
- ✅ Lista de artigos matching aparece
- ✅ Contador mostra "X resultado(s) encontrado(s)"
- ✅ Cada resultado mostra: título, autores, ano, evento
- ✅ Botão "Ver PDF" funciona (se PDF disponível)

**Critérios de Falha:**
- ❌ Nenhum resultado
- ❌ Erro 500
- ❌ Resultados vazios

---

## **2. TESTES FUNCIONAIS - ADMIN**

### **Teste 2.1: Login Admin**

**Objetivo:** Verificar autenticação de administrador

**Passos:**
1. Ir para `http://localhost:4200/admin`
2. Inserir email: `admin@e-lib.com`
3. Clicar em **"Entrar"**

**Resultado Esperado:**
- ✅ Redirect para dashboard admin
- ✅ Menu lateral aparece com opções: Eventos, Edições, Artigos, Batch Upload
- ✅ Token JWT salvo no localStorage

**Critérios de Falha:**
- ❌ Erro de autenticação
- ❌ Página não redireciona

---

### **Teste 2.2: CRUD de Eventos**

#### **2.2.1: Criar Evento**

**Passos:**
1. Login como admin
2. Ir para **"Gerenciar Eventos"** (`/admin/eventos`)
3. Clicar em **"Novo Evento"**
4. Preencher:
   - Nome: "Workshop de Testes"
   - Sigla: "WT"
   - Descrição: "Workshop sobre testes de software"
5. Clicar em **"Salvar"**

**Resultado Esperado:**
- ✅ Mensagem "Evento criado com sucesso!"
- ✅ Evento aparece na tabela
- ✅ Banco de dados contém novo evento

#### **2.2.2: Editar Evento**

**Passos:**
1. Na tabela de eventos, clicar no botão **editar** (ícone de lápis)
2. Alterar descrição
3. Salvar

**Resultado Esperado:**
- ✅ Mensagem "Evento atualizado com sucesso!"
- ✅ Alteração refletida na tabela

#### **2.2.3: Deletar Evento**

**Passos:**
1. Clicar no botão **deletar** (ícone de lixeira)
2. Confirmar exclusão

**Resultado Esperado:**
- ✅ Mensagem "Evento excluído com sucesso!"
- ✅ Evento removido da tabela

---

### **Teste 2.3: CRUD de Artigos**

#### **2.3.1: Criar Artigo Individual**

**Passos:**
1. Ir para **"Gerenciar Artigos"** (`/admin/artigos`)
2. Clicar em **"Novo Artigo"**
3. Preencher:
   - Evento: SBES
   - Edição: 2024
   - Título: "Teste de Software com IA"
   - Autores: "Maria Silva, João Santos"
   - Resumo: "Aplicação de IA em testes"
   - Palavras-chave: "IA, Testes"
4. Salvar

**Resultado Esperado:**
- ✅ Mensagem "Artigo criado com sucesso!"
- ✅ Artigo aparece na tabela filtrada

#### **2.3.2: Upload de PDF em Artigo Existente**

**Passos:**
1. Na tabela de artigos, localizar artigo
2. Clicar no botão **Upload PDF** (ícone de nuvem)
3. Selecionar arquivo PDF de teste
4. Aguardar upload

**Resultado Esperado:**
- ✅ Mensagem "PDF enviado com sucesso!"
- ✅ Artigo agora tem PDF associado
- ✅ Botão "Ver PDF" funciona em páginas públicas

#### **2.3.3: Editar Artigo**

**Passos:**
1. Clicar no botão **editar** do artigo
2. Alterar título ou autores
3. Salvar

**Resultado Esperado:**
- ✅ Mensagem "Artigo atualizado com sucesso!"
- ✅ Alterações refletidas

---

### **Teste 2.4: Upload em Massa (BibTeX)**

**Objetivo:** Importar múltiplos artigos via arquivo .bib

**Arquivo de Teste:** `/home/mostqi/EngSoft/TP1/e-lib/backend/seed_data.bib`

**Passos:**
1. Ir para **"Batch Upload"** (`/admin/batch-upload`)
2. Clicar em **"Selecionar Arquivo"**
3. Escolher `seed_data.bib`
4. Clicar em **"Processar Arquivo"**
5. Aguardar processamento (5-15 segundos)

**Resultado Esperado:**
- ✅ Barra de progresso aparece
- ✅ Mensagem com estatísticas:
  ```
  ✅ Upload completo!
  📊 22 artigos criados
  📅 2 eventos criados
  📖 4 edições criadas
  ⚠️ 0 duplicados ignorados
  ```
- ✅ Artigos aparecem em "Gerenciar Artigos"
- ✅ Eventos aparecem em página pública

**Critérios de Falha:**
- ❌ Erro "Arquivo inválido"
- ❌ Timeout
- ❌ 0 artigos criados

---

## **3. TESTES DE INTEGRAÇÃO**

### **Teste 3.1: Fluxo Completo de Artigo**

**Cenário:** Criar evento → edição → artigo → upload PDF → visualizar

**Passos:**
1. **Criar Evento**
   - Admin → Eventos → Novo
   - Nome: "Conferência de IA"
   - Sigla: "CIA"

2. **Criar Edição**
   - Admin → Edições → Nova
   - Evento: CIA
   - Ano: 2025
   - Local: "São Paulo"

3. **Criar Artigo**
   - Admin → Artigos → Novo
   - Edição: CIA 2025
   - Título: "Deep Learning em Produção"
   - Autores: "Ana Costa"

4. **Upload PDF**
   - Botão upload na linha do artigo
   - Selecionar PDF de teste

5. **Visualizar Publicamente**
   - Sair do admin
   - Ir para `/search`
   - Buscar "Deep Learning"
   - Clicar em "Ver PDF"

**Resultado Esperado:**
- ✅ Todas as etapas funcionam
- ✅ Artigo encontrado na busca
- ✅ PDF abre em nova aba

---

### **Teste 3.2: Cascata de Filtros**

**Objetivo:** Verificar dependência Evento → Edição → Artigos

**Passos:**
1. Admin → Artigos
2. Selecionar **Evento**: SBES
3. Observar dropdown de **Edições**
4. Selecionar **Edição**: 2024
5. Observar tabela de artigos

**Resultado Esperado:**
- ✅ Dropdown de edições mostra apenas edições do SBES
- ✅ Tabela mostra apenas artigos da edição selecionada
- ✅ Alterar evento limpa seleção de edição

---

## **4. TESTES DE API (Backend)**

### **Teste 4.1: GET /api/eventos/**

**Comando:**
```bash
curl http://localhost:5000/api/eventos/
```

**Resultado Esperado:**
```json
{
  "eventos": [
    {
      "_id": "67...",
      "nome": "Simpósio Brasileiro de Engenharia de Software",
      "sigla": "SBES",
      "descricao": "...",
      "criado_em": "2025-10-13T..."
    }
  ]
}
```

---

### **Teste 4.2: POST /api/artigos/ (Criar Artigo)**

**Comando:**
```bash
curl -X POST http://localhost:5000/api/artigos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "titulo": "Teste de API",
    "autores": [{"nome": "Teste"}],
    "edicao_id": "67...",
    "resumo": "Teste"
  }'
```

**Resultado Esperado:**
```json
{
  "message": "Artigo criado com sucesso",
  "artigo_id": "67..."
}
```

---

### **Teste 4.3: GET /api/artigos/busca?q=software**

**Comando:**
```bash
curl "http://localhost:5000/api/artigos/busca?q=software"
```

**Resultado Esperado:**
```json
{
  "resultados": [...],
  "total": 15,
  "query": "software"
}
```

---

### **Teste 4.4: POST /api/batch/upload-bibtex**

**Comando:**
```bash
curl -X POST http://localhost:5000/api/batch/upload-bibtex \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@seed_data.bib"
```

**Resultado Esperado:**
```json
{
  "message": "Upload processado com sucesso",
  "stats": {
    "total_entries": 22,
    "artigos_criados": 22,
    "eventos_criados": 2,
    "edicoes_criadas": 4
  }
}
```

---

## **5. TESTES DE PERFORMANCE**

### **Teste 5.1: Tempo de Carregamento da Home**

**Métrica:** Tempo para carregar 5 artigos + 5 eventos

**Como medir:**
1. Abrir DevTools (F12)
2. Ir para aba **Network**
3. Recarregar página (`Ctrl+R`)
4. Observar tempo de resposta das APIs

**Resultado Aceitável:**
- ✅ `/api/eventos/` < 200ms
- ✅ `/api/artigos/busca` < 500ms
- ✅ Página totalmente carregada < 2s

---

### **Teste 5.2: Upload de BibTeX Grande**

**Cenário:** Arquivo com 100+ artigos

**Métrica:** Tempo de processamento

**Resultado Aceitável:**
- ✅ 100 artigos < 30 segundos
- ✅ Sem timeout
- ✅ Memória < 512MB

---

## **6. TESTES DE SEGURANÇA**

### **Teste 6.1: Acesso sem Autenticação**

**Objetivo:** Verificar proteção de rotas admin

**Comando:**
```bash
curl -X POST http://localhost:5000/api/eventos/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Hack"}'
```

**Resultado Esperado:**
```json
{
  "error": "Token de autorização necessário"
}
```
**Status Code:** `401 Unauthorized`

---

### **Teste 6.2: Token Expirado**

**Objetivo:** Verificar expiração de JWT

**Passos:**
1. Fazer login
2. Aguardar 24 horas (ou modificar token manualmente)
3. Tentar criar evento

**Resultado Esperado:**
- ✅ Erro "Token inválido ou expirado"
- ✅ Redirect para login

---

### **Teste 6.3: SQL Injection / NoSQL Injection**

**Objetivo:** Testar sanitização de inputs

**Comando:**
```bash
curl "http://localhost:5000/api/artigos/busca?q=\$ne"
```

**Resultado Esperado:**
- ✅ Busca retorna vazia ou erro, não expõe dados

---

## **7. CHECKLIST RESUMIDO**

### **Frontend**
- [ ] Home carrega artigos reais
- [ ] Home carrega eventos reais
- [ ] Clique em evento navega corretamente
- [ ] Botão "Explorar Eventos" funciona
- [ ] Busca retorna resultados do banco
- [ ] Filtros funcionam (evento, edição)

### **Admin**
- [ ] Login funciona
- [ ] CRUD de eventos completo
- [ ] CRUD de edições completo
- [ ] CRUD de artigos completo
- [ ] Upload de PDF funciona
- [ ] Upload em massa (BibTeX) funciona

### **Backend**
- [ ] Todas as rotas retornam 200 OK
- [ ] Autenticação JWT funciona
- [ ] Parser BibTeX processa corretamente
- [ ] Busca retorna resultados relevantes

### **Integração**
- [ ] Frontend comunica com backend
- [ ] Dados salvos no banco aparecem no frontend
- [ ] PDFs podem ser baixados
- [ ] Notificações aparecem corretamente

---

## **8. COMANDOS ÚTEIS PARA TESTE**

### **Iniciar Sistema**
```bash
# Backend
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python run.py

# Frontend (outro terminal)
cd /home/mostqi/EngSoft/TP1/frontend
npm start
```

### **Popular Banco**
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python seed_bibtex.py seed_data.bib
```

### **Limpar Banco**
```bash
mongosh
> use simple-lib
> db.artigos.deleteMany({})
> db.eventos.deleteMany({})
> db.edicoes.deleteMany({})
```

### **Ver Logs do Backend**
```bash
tail -f /home/mostqi/EngSoft/TP1/e-lib/backend/app.log
```

---

## **9. RELATÓRIO DE BUGS CONHECIDOS**

| # | Bug | Severidade | Status |
|---|-----|------------|--------|
| 1 | PDF abre example.com | Alta | 🔧 Em correção |
| 2 | Rota /api/artigos/:id/pdf não existe | Alta | ⏳ Pendente |
| 3 | Interface de artigos confusa (2 páginas) | Média | ⏳ Pendente |
| 4 | Busca não funciona sem termo | Baixa | ⏳ Pendente |

---

**Documento criado em:** 13 de outubro de 2025  
**Versão:** 1.0  
**Status:** ✅ GUIA COMPLETO DE TESTES
