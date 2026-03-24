---
name: unit-testing
description: "Generate comprehensive unit tests for JavaScript functions using Jest, including edge cases, mocks, and assertions. Use when: writing tests for new functions, improving test coverage, or ensuring edge case handling."
---

# Unit Testing with Jest

## Purpose
Generate comprehensive, production-ready unit tests for JavaScript functions using Jest framework, ensuring edge cases, error handling, and mock scenarios are covered.

## When to Use
- ✅ Writing tests for new JavaScript/TypeScript functions
- ✅ Improving test coverage for existing code
- ✅ Need to test edge cases and error scenarios
- ✅ Setting up test structure for a new module
- ✅ Creating test fixtures and mocks

## When NOT to Use
- ❌ Integration tests (use separate integration testing patterns)
- ❌ E2E tests (use Cypress, Playwright, or Selenium)
- ❌ Performance/load testing (use dedicated tools)
- ❌ Testing non-JavaScript code (use language-specific testing tools)

---

## Pre-Conditions

Before generating tests:
1. **Function signature is defined** — Know input parameters and return type
2. **Jest is configured** — `package.json` has Jest dependency
3. **Test file location** — Follow convention: `[filename].test.js` or `__tests__/[filename].test.js`
4. **Function purpose is clear** — Understand what the function is supposed to do

---

## Test Structure Standards

### File Organization
```
<userPrompt>
Provide the fully rewritten file, incorporating the suggested code change. You must produce the complete file.
</userPrompt>