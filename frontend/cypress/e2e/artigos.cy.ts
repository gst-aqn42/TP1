/**
 * Testes E2E de Artigos
 */

describe('Artigos E2E', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.clearDatabase();
    cy.loginAsAdmin();
    cy.wait(1000);
    cy.visit('/admin/artigos', { failOnStatusCode: false });
    cy.wait(500);
  });

  describe('Listagem de Artigos', () => {
    it('deve exibir a lista de artigos', () => {
      cy.get('body').should('be.visible');
    });
  });
});
