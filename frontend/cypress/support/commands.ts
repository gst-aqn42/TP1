// ***********************************************
// This file contains custom commands
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

/**
 * Login como admin
 */
Cypress.Commands.add('loginAsAdmin', () => {
  cy.visit('/admin/login');
  
  // Aguarda a página carregar
  cy.get('input[formControlName="username"]', { timeout: 10000 }).should('be.visible');
  
  // Preenche o formulário de login
  cy.get('input[formControlName="username"]').clear().type('admin@admin.com');
  cy.get('input[formControlName="password"]').clear().type('admin');
  
  // Clica no botão de login
  cy.get('button[type="submit"]').click();
  
  // Aguarda redirecionamento ou sucesso (pode ser que redirecione ou mostre mensagem)
  cy.wait(1000);
});

/**
 * Limpa o localStorage (deve ser chamado após visitar uma página)
 */
Cypress.Commands.add('clearDatabase', () => {
  cy.clearLocalStorage();
  cy.clearCookies();
});

// Export para TypeScript
export {};
