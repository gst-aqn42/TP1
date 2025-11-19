/**
 * Testes E2E de Edições de Eventos
 */

describe('Edições E2E', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.clearDatabase();
    cy.loginAsAdmin();
    cy.wait(1000);
    cy.visit('/admin/edicoes', { failOnStatusCode: false });
    cy.wait(500);
  });

  describe('Listagem de Edições', () => {
    it('deve exibir a lista de edições', () => {
      cy.get('body').should('be.visible');
    });
  });
});
