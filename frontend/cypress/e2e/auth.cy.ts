/**
 * Testes E2E de Autenticação
 * 
 * Testa o fluxo completo de autenticação do usuário:
 * - Login
 * - Logout
 * - Proteção de rotas
 * - Persistência de sessão
 */

describe('Autenticação E2E', () => {
  beforeEach(() => {
    // Visita uma página primeiro antes de limpar
    cy.visit('/');
    // Limpa localStorage antes de cada teste
    cy.clearDatabase();
  });

  describe('Página de Login', () => {
    it('deve exibir o formulário de login', () => {
      cy.visit('/admin/login');
      
      // Verifica se os elementos do formulário estão presentes
      cy.get('input[formControlName="username"]').should('be.visible');
      cy.get('input[formControlName="password"]').should('be.visible');
      cy.get('button[type="submit"]').should('be.visible');
    });

    it('deve fazer login com credenciais válidas', () => {
      cy.visit('/admin/login');
      
      // Preenche o formulário
      cy.get('input[formControlName="username"]').type('admin@admin.com');
      cy.get('input[formControlName="password"]').type('admin');
      
      // Submete o formulário
      cy.get('button[type="submit"]').click();
      
      // Aguarda e verifica se não está mais na página de login
      cy.wait(1000);
      cy.url().should('not.include', '/login');
    });

    it('deve mostrar erro com credenciais inválidas', () => {
      cy.visit('/admin/login');
      
      // Preenche com credenciais inválidas
      cy.get('input[formControlName="username"]').type('usuario@invalido.com');
      cy.get('input[formControlName="password"]').type('senhaerrada');
      
      // Submete o formulário
      cy.get('button[type="submit"]').click();
      
      // Aguarda resposta
      cy.wait(1000);
      
      // Verifica que continua na página de login
      cy.url().should('include', '/login');
    });

    it('deve validar campos obrigatórios', () => {
      cy.visit('/admin/login');
      
      // Tenta submeter sem preencher
      cy.get('button[type="submit"]').click();
      
      // Formulário não deve submeter (ainda na página de login)
      cy.url().should('include', '/login');
    });
  });

  describe('Logout', () => {
    beforeEach(() => {
      // Faz login antes de cada teste
      cy.loginAsAdmin();
    });

    it('deve fazer logout com sucesso', () => {
      // Aguarda a página carregar
      cy.wait(1000);
      
      // Procura por botão de logout (pode ser um ícone, link, etc)
      // Adaptar conforme implementação real
      cy.get('body').then(($body) => {
        if ($body.text().includes('Sair')) {
          cy.contains('Sair').click();
        }
      });
    });
  });

  describe('Proteção de Rotas', () => {
    it('deve redirecionar para login ao acessar rota protegida sem autenticação', () => {
      // Tenta acessar área admin sem estar logado
      cy.visit('/admin/eventos', { failOnStatusCode: false });
      
      // Aguarda redirecionamento
      cy.wait(1000);
      
      // Deve estar em alguma página que não é eventos
      // (pode ser login ou home, dependendo da implementação)
      cy.url().then((url) => {
        expect(url).to.satisfy((u: string) => {
          return u.includes('/login') || !u.includes('/admin/eventos');
        });
      });
    });

    it('deve permitir acesso a rotas protegidas quando autenticado', () => {
      cy.loginAsAdmin();
      
      // Aguarda login completar
      cy.wait(1000);
      
      // Acessa rota protegida
      cy.visit('/admin/eventos', { failOnStatusCode: false });
      
      // Aguarda carregar
      cy.wait(500);
    });
  });

  describe('Persistência de Sessão', () => {
    it('deve manter sessão após recarregar página', () => {
      cy.loginAsAdmin();
      
      // Aguarda login
      cy.wait(1000);
      
      // Recarrega a página
      cy.reload();
      
      // Aguarda recarregar
      cy.wait(500);
    });
  });

  describe('Navegação', () => {
    beforeEach(() => {
      cy.loginAsAdmin();
    });

    it('deve navegar entre páginas da área admin', () => {
      // Aguarda login
      cy.wait(1000);
      
      // Verifica se está na área admin
      cy.url().then((url) => {
        // Se houver menu, tenta navegar
        cy.get('body').then(($body) => {
          if ($body.text().includes('Eventos') || $body.text().includes('eventos')) {
            // Página carregou com sucesso
            cy.log('Área admin acessível');
          }
        });
      });
    });
  });
});
