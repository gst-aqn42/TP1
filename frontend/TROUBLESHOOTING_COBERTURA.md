# 🔍 Troubleshooting: Cobertura de Código E2E

## ⚠️ Problemas Comuns e Soluções

### 1. Cobertura aparece como 0%

**Causa**: O código Angular não está sendo instrumentado.

**Solução**: Para Angular, a cobertura E2E com Cypress funciona melhor quando:

1. **Adicionar configuração de build customizada** (opcional):
   
   Criar `angular.json` com configuração de instrumentação é complexo para Angular 20+.
   
2. **Alternativa mais simples**: Usar cobertura dos testes unitários como referência principal:
   ```bash
   npm test -- --code-coverage
   ```

3. **Para cobertura E2E real**: Considerar usar plugins adicionais como:
   - `@cypress/code-coverage` com custom webpack config
   - `nyc` com instrumentação manual

**Nota**: A cobertura E2E mede código executado durante testes de interface, não substituindo testes unitários.

---

### 2. Erro: "Cannot find module '@cypress/code-coverage'"

**Solução**:
```bash
cd /home/mostqi/EngSoft/TP1/frontend
sudo npm install --save-dev @cypress/code-coverage
```

---

### 3. Erro: "require is not defined" no cypress.config.ts

**Causa**: TypeScript não reconhece `require()`.

**Solução**: Já configurado! O erro pode ser ignorado ou você pode:

1. Adicionar ao `tsconfig.json`:
```json
{
  "compilerOptions": {
    "types": ["node"]
  }
}
```

2. Ou converter para import ESM (mais complexo).

---

### 4. Nenhum relatório de cobertura é gerado

**Verificações**:

1. **Plugin configurado?**
   ```bash
   grep "code-coverage" /home/mostqi/EngSoft/TP1/frontend/cypress.config.ts
   ```
   Deve mostrar: `require('@cypress/code-coverage/task')`

2. **Support file configurado?**
   ```bash
   grep "code-coverage" /home/mostqi/EngSoft/TP1/frontend/cypress/support/e2e.ts
   ```
   Deve mostrar: `import '@cypress/code-coverage/support'`

3. **.nycrc.json existe?**
   ```bash
   cat /home/mostqi/EngSoft/TP1/frontend/.nycrc.json
   ```

---

### 5. Pasta coverage-e2e não é criada

**Solução**:

1. Verificar configuração do nyc:
   ```bash
   cat /home/mostqi/EngSoft/TP1/frontend/.nycrc.json
   ```

2. Executar nyc manualmente após testes:
   ```bash
   npm run e2e
   npx nyc report --reporter=html --reporter=text
   ```

3. Verificar se há arquivo `.nyc_output`:
   ```bash
   ls -la /home/mostqi/EngSoft/TP1/frontend/.nyc_output/
   ```

---

### 6. Cobertura E2E vs Unit: Qual usar?

**Resposta**: **AMBOS!**

| Tipo | Propósito | Quando usar |
|------|-----------|-------------|
| **Unit** | Testar lógica isolada | Funções, métodos, classes |
| **E2E** | Testar fluxo completo | Navegação, integração UI |

**Cobertura ideal**:
- Unit tests: 80-90% (código de lógica)
- E2E tests: 60-70% (fluxos principais)

---

### 7. Relatório mostra apenas arquivos de teste

**Causa**: Configuração de `exclude` incorreta.

**Solução**: Verificar `.nycrc.json`:
```json
{
  "exclude": [
    "**/*.spec.ts",
    "**/*.cy.ts",
    "**/cypress/**"
  ]
}
```

---

### 8. Como melhorar a cobertura E2E?

**Estratégias**:

1. **Adicionar mais cenários de teste**:
   - Fluxos de erro
   - Validações de formulário
   - Navegação entre páginas

2. **Testar componentes isolados**:
   - Cypress Component Testing
   - Mais focado que E2E full

3. **Combinar com visual testing**:
   - Cypress Snapshots
   - Percy.io

---

### 9. Performance: Testes E2E muito lentos

**Otimizações**:

1. **Executar em paralelo** (Cypress Dashboard):
   ```bash
   npx cypress run --record --parallel
   ```

2. **Reduzir timeouts** (se possível):
   ```typescript
   // cypress.config.ts
   defaultCommandTimeout: 5000 // em vez de 10000
   ```

3. **Mockar APIs externas**:
   ```typescript
   cy.intercept('GET', '/api/external', { fixture: 'mock.json' })
   ```

4. **Usar beforeEach eficientemente**:
   - Não limpar database a cada teste
   - Reusar login quando possível

---

### 10. Comparando relatórios de cobertura

**Visualizar múltiplas coberturas**:

```bash
# Unit
xdg-open /home/mostqi/EngSoft/TP1/frontend/coverage/frontend/index.html

# E2E
xdg-open /home/mostqi/EngSoft/TP1/frontend/coverage-e2e/index.html
```

**Análise**:
- Linhas verdes em Unit mas vermelhas em E2E → Lógica testada, mas não exercida via UI
- Linhas vermelhas em ambos → **ADICIONAR TESTES!**
- Linhas verdes em E2E mas vermelhas em Unit → Adicionar unit tests

---

### 11. Cobertura diferente entre unit e E2E

**É NORMAL!**

- **Unit tests** testam código TypeScript diretamente
- **E2E tests** testam aplicação compilada rodando no navegador

**Exemplo**:
```typescript
// Este código é testado por unit test
calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Este código é testado por E2E test
onSubmit() {
  const total = this.calculateTotal(this.cart.items);
  this.checkout(total);
}
```

---

### 12. Erro: "Coverage data is not available"

**Soluções**:

1. **Verificar se aplicação está instrumentada**:
   - Para Angular, precisa configuração especial
   - Considerar usar apenas cobertura de unit tests

2. **Alternativa**: Usar Cypress Component Testing:
   ```bash
   npm install --save-dev @cypress/angular
   ```

3. **Medir cobertura manualmente**:
   - Mapear quais componentes são testados
   - Usar console.log para verificar código executado

---

## 🎯 Recomendações Finais

### Para este projeto E-Lib:

1. **Use testes unitários (Karma)** para medir cobertura de código TypeScript
   ```bash
   npm test -- --code-coverage
   ```

2. **Use testes E2E (Cypress)** para validar fluxos de usuário
   ```bash
   npm run e2e:open  # Validação visual
   ```

3. **Combine ambos** para cobertura completa:
   - Unit: 136 testes → Alta cobertura de lógica
   - E2E: 74 testes → Cobertura de fluxos principais

### Métricas ideais:

```
Unit Tests (Karma):
  Statements   : > 80%
  Branches     : > 75%
  Functions    : > 80%
  Lines        : > 80%

E2E Tests (Cypress):
  User Flows   : 100% dos fluxos principais
  Components   : Todos os componentes principais testados
  Navigation   : Todas as rotas testadas
```

---

## 📚 Recursos Adicionais

- [Cypress Code Coverage](https://docs.cypress.io/guides/tooling/code-coverage)
- [Angular Testing Guide](https://angular.io/guide/testing)
- [Istanbul/NYC Documentation](https://istanbul.js.org/)
- [Best Practices for Test Coverage](https://martinfowler.com/bliki/TestCoverage.html)

---

**Conclusão**: Cobertura E2E complementa, mas não substitui testes unitários. Use ambos! 🎯
