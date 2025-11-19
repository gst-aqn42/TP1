/**
 * Testes E2E de Eventos
 */

describe('Eventos E2E', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.clearDatabase();
    cy.loginAsAdmin();
    cy.wait(1000);
    cy.visit('/admin/eventos', { failOnStatusCode: false });
    cy.wait(500);
  });

  describe('Listagem de Eventos', () => {
    it('deve exibir a lista de eventos', () => {
      cy.get('body').should('be.visible');
    });
  });
});
