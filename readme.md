# TP1: e-lib - Biblioteca Digital de Artigos

## 1. Equipe
- **Back-end:** Gustavo Rodrigues de Aquino
- **Front-end:** Maria Eduarda Rodrigues Pasquel

## 2. Detalhamento do Projeto
Deseja-se disponibilizar acesso de forma fácil aos artigos publicados em determinados eventos científicos. Para isso, foi proposto o desenvolvimento da **e-lib** - uma `Biblioteca Digital de Artigos` moderna e intuitiva. O sistema deve atender aos requerimentos passados pelas histórias de usuário, mas sua implementação é livre e deve ser definida pelo time. Entretanto, **é obrigatório o uso do GitHub** e recomendado a utilização de uma IA de 2ª geração.

## 3. Tecnologias
### Tecnologias utilizadas
- **Linguagem Back-end:** Python
- **Frameworks Front-end:** Angular 19 + Angular Material
- **Banco de dados:** MongoDB
- **Repositório do GitHub:** `git@github.com:gst-aqn42/TP1.git`
- **Ferramenta de IA:** GitHub Copilot

### Dependências do Front-end
- Angular CLI: 19.0.7
- Angular Material: 20.2.8
- TypeScript: ~5.6.0
- RxJS: ~7.8.0

## 4. Histórias de Usuário

#### 4.1 Funcionalidades para Administradores
- **Cadastrar, editar e deletar eventos**
  - Exemplo: *Simpósio Brasileiro de Engenharia de Software (SBES)*
- **Cadastrar, editar e deletar edições de eventos**
  - Exemplo: *Edição de 2025 do SBES*
- **Cadastrar, editar e deletar artigos manualmente**
  - Incluindo o upload do arquivo PDF de cada artigo
- **Cadastrar artigos em massa**
  - A partir de um arquivo BibTeX contendo os dados de vários artigos
- **Home page para cada evento**
  - Cada evento deve ter uma página principal com suas edições listadas
  - Exemplo de URL: `simple-lib/sbes`
- **Home page para cada edição de evento**
  - Cada edição deve ter sua própria página com os artigos publicados
  - Exemplo de URL: `simple-lib/sbes/2025`

#### 4.2 Funcionalidades para Usuários
- **Pesquisar por artigos**
  - Filtros disponíveis: título, autor e nome do evento
- **Visualizar home page pessoal**
  - Página com todos os artigos do usuário, organizados por ano
  - Exemplo de URL: `simple-lib/nome-autor`
- **Receber notificações por e-mail**
  - Cadastro para receber alertas sempre que um novo artigo for disponibilizado com o nome do usuário

## 5. CRC's


## 6. Diagrama UML


## 7. Relatório sobre o uso de IA

[A ser preenchido após o desenvolvimento]

## 8. Backlog da Sprint

[A ser preenchido com as tarefas da sprint]

## 9. Critérios de Avaliação

**Total:** 20 pontos

- **Backlog da sprint (1pt)**

- **Implementação das histórias (10pts)**

- **Qualidade da UI (3pts)**

- **Diagramas UML (2pts)**

- **Relatório sobre o uso de IA (3pts)**

- **Retrospectiva (1pt)**

## 10. Contatos

Gustavo de Aquino | gst.aqn@gmail.com |

## 11. Estrutura do Projeto

### Estrutura Atual do Front-end (Angular)

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout/
│   │   │   └── header/          # Componente de cabeçalho com navegação
│   │   ├── pages/
│   │   │   ├── home/            # Página inicial
│   │   │   ├── events/          # Gerenciamento de eventos
│   │   │   ├── articles/        # Gerenciamento de artigos
│   │   │   ├── search/          # Busca de artigos
│   │   │   ├── authors/         # Páginas de autores
│   │   │   └── notifications/   # Sistema de notificações
│   │   ├── services/
│   │   │   ├── event.ts         # Serviço para eventos
│   │   │   ├── article.ts       # Serviço para artigos
│   │   │   └── notification.ts  # Serviço para notificações
│   │   ├── models/
│   │   │   ├── event.model.ts   # Interface Event, EventEdition, Article
│   │   │   └── user.model.ts    # Interface User, NotificationPreference
│   │   ├── app.routes.ts        # Configuração de rotas
│   │   ├── app.config.ts        # Configuração da aplicação
│   │   └── app.ts               # Componente raiz
│   ├── styles.scss              # Estilos globais com Angular Material
│   └── index.html
├── package.json                 # Dependências do projeto
└── angular.json                 # Configuração do Angular CLI
```

### Funcionalidades Implementadas (Passo 0)

✅ **Configuração Inicial Completa:**
- Projeto Angular 19 criado com roteamento e SCSS
- Angular Material instalado e configurado
- HttpClient configurado para requisições HTTP
- Estrutura de componentes criada para todas as user stories
- Sistema de roteamento configurado
- Layout responsivo com header de navegação
- Estilos globais configurados

### Como Executar o Projeto

```bash
# 1. Navegar para o diretório do projeto
cd frontend

# 2. Instalar dependências
npm install

# 3. Executar a aplicação
ng serve

# 4. Abrir no navegador
# http://localhost:4200
```

### 🎯 Guia de Teste das Funcionalidades

#### **Área Pública**
1. **Página Inicial**: Acesse `/pesquisa` para buscar artigos
2. **Busca de Artigos**: Teste busca por "metodologia" (título), "João Silva" (autor), "software" (evento)
3. **Páginas de Eventos**: Acesse `/eventos/sbes` para ver edições do SBES
4. **Páginas de Edições**: Acesse `/eventos/sbes/2024` para ver artigos da edição
5. **Página de Autor**: Acesse `/autores/joao-silva` para ver artigos organizados por ano
6. **Inscrição**: Use o formulário no footer para se inscrever para notificações

#### **Área Administrativa**
1. **Login**: Acesse `/admin/login` com usuário: `admin` / senha: `admin`
2. **Gerenciar Eventos**: Criar, editar e excluir eventos acadêmicos
3. **Gerenciar Edições**: Criar edições vinculadas a eventos específicos
4. **Gerenciar Artigos**: Cadastrar artigos individuais com upload de PDF
5. **Upload em Lote**: Simular importação de artigos via arquivo BibTeX

### 🔍 Recursos de Destaque

- **Interface Moderna**: Material Design 3 com tema personalizado
- **Design Elegante**: Fundo temático de biblioteca com efeitos de transparência
- **Navegação Intuitiva**: Breadcrumbs e links contextuais
- **Responsivo**: Totalmente adaptável para desktop e mobile
- **Estados Visuais**: Loading, sucesso, erro em todas as operações
- **Simulação Realista**: Backend mockado com dados consistentes
- **Validações Robustas**: Formulários com feedback em tempo real
- **Visual Premium**: Backdrop blur e transparências para melhor legibilidade

### Status do Desenvolvimento

- ✅ **Passo 0 - Configuração Inicial:** Completo
- ✅ **Passo 1 - Serviços Essenciais:** Completo
- ✅ **Passo 2 - Roteamento e Proteção:** Completo
- ✅ **Passo 3 - Geração de Componentes:** Completo
- ✅ **Passo 4 - Implementação dos Componentes:** Completo
- ✅ **Todas as Histórias de Usuário:** Implementadas

### Novas Funcionalidades Implementadas (Passos 1 e 2)

✅ **Serviços Essenciais:**
- `ApiService`: Centraliza todas as chamadas para a API REST
- `AuthService`: Gerencia autenticação com credenciais admin/admin
- Métodos implementados para eventos, edições, artigos e inscrições

✅ **Sistema de Roteamento:**
- Rotas organizadas com proteção por autenticação
- AuthGuard implementado para páginas administrativas
- Rota principal redirecionando para `/pesquisa`
- Rotas administrativas aninhadas em `/admin`

✅ **Componentes Criados:**
- `SearchPage`: Página principal de busca de artigos
- `LoginPage`: Autenticação administrativa
- `AdminLayout`: Layout para área administrativa
- Componentes para gerenciamento (eventos, edições, artigos)

✅ **Estrutura de Componentes (Passo 3):**
- **Layouts**: MainLayout e AdminLayout organizados
- **Componentes**: Header, Footer e SubscribeForm reutilizáveis
- **Páginas Públicas**: SearchPage, EventPage, EditionPage, AuthorPage
- **Páginas Admin**: LoginPage, ManageEvents, ManageEditions, ManageArticles, BatchUpload
- **Organização**: Separação clara entre componentes públicos e administrativos

✅ **Histórias de Usuário Implementadas:**

**📋 Área Administrativa (Histórias 1-4):**
- ✅ **História 1**: Cadastro completo de eventos (criar, editar, deletar)
- ✅ **História 2**: Gerenciamento de edições com filtros por evento
- ✅ **História 3**: Cadastro manual de artigos com upload de PDF
- ✅ **História 4**: Upload em massa via arquivo BibTeX

**🌐 Área Pública (Histórias 5-8):**
- ✅ **História 5**: Busca avançada por título, autor ou evento
- ✅ **História 6**: Páginas dinâmicas de eventos e edições
- ✅ **História 7**: Página personalizada do autor com accordion por ano
- ✅ **História 8**: Sistema de notificações por email

**🔧 Funcionalidades Técnicas:**
- Sistema de login funcional (admin/admin)
- Proteção de rotas administrativas
- Interface responsiva com Material Design
- Simulação completa de backend com dados mock
- Estados de loading, erro e sucesso
- Validações de formulário abrangentes
- Feedback visual com snackbars
- Upload de arquivos com validação


<!--

Estrutura do Repositório Proposta:

simple-lib/
├── 
│   ├── 
│   ├── 
│   ├── 
│   └── 
├── 
│   ├── 
│   ├── 
│   ├── 
│   └── 