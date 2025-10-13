# 🚀 GUIA RÁPIDO - e-lib

## Como Usar as Novas Funcionalidades

### 📦 1. POPULAR O BANCO DE DADOS

#### **Opção A: Via Linha de Comando (Recomendado para primeira vez)**

```bash
# 1. Certifique-se de que o backend está rodando
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python run.py

# 2. Em outro terminal, execute o parser
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python seed_bibtex.py seed_data.bib
```

**Resultado:** 22 artigos, 2 eventos, 4 edições criados instantaneamente!

---

#### **Opção B: Via Interface Web**

```bash
# 1. Certifique-se de que backend e frontend estão rodando
# Backend:
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python run.py

# Frontend (outro terminal):
cd /home/mostqi/EngSoft/TP1/frontend
npm start
```

1. Acesse: `http://localhost:4200/admin`
2. Faça login como admin
3. Vá para **"Batch Upload"** no menu
4. Clique em **"Selecionar Arquivo"**
5. Escolha `seed_data.bib` (está em `/e-lib/backend/`)
6. Clique em **"Processar Arquivo"**
7. Veja as estatísticas na notificação!

---

### ✏️ 2. GERENCIAR ARTIGOS

#### **Criar Novo Artigo**
1. Ir para `/admin/artigos`
2. Clicar em **"Novo Artigo"** (botão azul no topo)
3. Preencher formulário:
   - Selecionar edição
   - Título, autores (separados por vírgula)
   - Resumo, palavras-chave
4. Salvar

#### **Editar Artigo Existente**
1. Ir para `/admin/artigos`
2. Na linha do artigo, clicar no **botão de editar** (ícone de lápis)
3. Modificar campos desejados
4. Salvar

#### **Excluir Artigo**
1. Ir para `/admin/artigos`
2. Na linha do artigo, clicar no **botão de excluir** (ícone de lixeira)
3. Confirmar exclusão

---

### 📄 3. FAZER UPLOAD DE PDF

#### **Para Artigo Existente**
1. Ir para `/admin/artigos`
2. Na coluna "PDF", clicar no **botão de upload** (ícone de nuvem)
3. Selecionar arquivo PDF do computador
4. Aguardar confirmação de sucesso

#### **Ao Criar Novo Artigo** (futuro)
- No dialog de criação, usar o campo "PDF do Artigo"
- Anexar arquivo antes de salvar

---

### 🔍 4. BUSCAR ARTIGOS

#### **Página de Busca Pública**
1. Ir para: `http://localhost:4200/search`
2. Digitar termo de busca, por exemplo:
   - `agile` → encontra artigos sobre metodologias ágeis
   - `João Silva` → encontra artigos deste autor
   - `SBES` → encontra artigos do evento SBES
   - `inteligência artificial` → busca no título/resumo
3. (Opcional) Adicionar filtros:
   - **Filtro de Autor:** nome específico
   - **Filtro de Evento:** sigla ou nome do evento
4. Clicar em **"Buscar"**
5. Ver resultados com:
   - Título do artigo
   - Lista de autores
   - Evento e ano
   - Botão "Ver PDF" (se disponível)

---

## 🎯 CENÁRIOS DE USO

### **Cenário 1: Primeira Configuração**
```bash
# Passo 1: Popular banco com dados de teste
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python seed_bibtex.py seed_data.bib

# Passo 2: Acessar frontend
# http://localhost:4200

# Passo 3: Testar busca
# http://localhost:4200/search
# Buscar: "agile"
```

---

### **Cenário 2: Adicionar Novos Artigos de Conferência**

**Você tem um arquivo .bib da conferência ICSE 2024:**

1. Fazer login como admin: `/admin`
2. Ir para **Batch Upload**
3. Upload do arquivo `icse-2024.bib`
4. Ver estatísticas:
   ```
   ✅ Upload completo!
   📊 50 artigos criados
   📅 1 evento criado (ICSE)
   📖 1 edição criada (2024)
   ```
5. Ir para **Gerenciar Artigos**
6. Filtrar por evento "ICSE"
7. Verificar os 50 novos artigos

---

### **Cenário 3: Curadoria de Artigos**

**Você quer adicionar PDFs aos artigos importantes:**

1. Ir para `/admin/artigos`
2. Filtrar por evento (ex: SBES 2024)
3. Para cada artigo importante:
   - Clicar no botão de upload (nuvem)
   - Selecionar PDF correspondente
   - Ver confirmação
4. Testar download na página de busca pública

---

### **Cenário 4: Correção de Dados**

**Um artigo tem autores errados:**

1. Ir para `/admin/artigos`
2. Localizar o artigo (usar filtros)
3. Clicar no botão de editar (lápis)
4. Corrigir campo "Autores":
   ```
   Antes: João Silva, Maria Santos
   Depois: João Silva, Maria Santos, Pedro Oliveira
   ```
5. Salvar
6. Verificar atualização na tabela

---

## ⚡ DICAS PRO

### **Performance:**
- Upload em massa é ~10x mais rápido que criação individual
- Use CLI (`seed_bibtex.py`) para grandes volumes (>100 artigos)
- Use web para volumes pequenos (<50 artigos)

### **Organização:**
- Organize arquivos .bib por conferência/ano
- Mantenha `seed_data.bib` como backup
- Exporte periodicamente para .bib (quando implementado)

### **Busca:**
- Busque por palavras-chave amplas primeiro ("software")
- Refine com filtros de autor/evento
- Use aspas para termos exatos (quando implementado)

### **Manutenção:**
- Verifique duplicatas antes de upload em massa
- Use edição para corrigir dados em vez de deletar/recriar
- Anexe PDFs após verificar metadados

---

## 🐛 TROUBLESHOOTING

### **"Erro ao processar arquivo BibTeX"**
- Verifique se o arquivo é .bib válido
- Abra o arquivo e veja se tem entradas `@inproceedings{...}`
- Tente com arquivo menor primeiro

### **"Artigo não aparece após busca"**
- Aguarde alguns segundos (banco pode estar indexando)
- Atualize a página
- Verifique se o termo está no título/autores/resumo

### **"PDF não disponível"**
- Arquivo ainda não foi enviado
- Vá para `/admin/artigos` e faça upload
- Verifique formato do arquivo (deve ser .pdf)

### **"Artigos duplicados após upload"**
- Parser detecta duplicatas por título
- Duplicatas são puladas automaticamente
- Veja estatísticas: `artigos_duplicados: N`

---

## 📞 REFERÊNCIA RÁPIDA

| Funcionalidade | URL | Requer Admin |
|----------------|-----|--------------|
| **Busca pública** | `/search` | ❌ |
| **Login** | `/admin` | ❌ |
| **Batch Upload** | `/admin/batch-upload` | ✅ |
| **Gerenciar Eventos** | `/admin/eventos` | ✅ |
| **Gerenciar Edições** | `/admin/edicoes` | ✅ |
| **Gerenciar Artigos** | `/admin/artigos` | ✅ |

---

**Dúvidas?** Consulte `IMPLEMENTACOES.md` para detalhes técnicos completos.
