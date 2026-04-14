# Template pack — web-typescript

Stack típico de web app full-stack en TypeScript sobre Node 20 LTS.

## Decisiones que asume el pack

- **Lenguaje:** TypeScript 5.4+ en front y back.
- **Package manager:** pnpm (preferido por velocidad e instalación determinística).
- **Runtime backend:** Node 20 LTS.
- **Testing:** Vitest para unit + integración, Playwright para E2E (habitual pero no impuesto por el pack — solo fija los comandos).
- **CI:** ubuntu-latest con `actions/setup-node@v4`.
- **Globs de código:** `src/**/*.ts` backend, `src/components/**/*.tsx` frontend.
- **Globs de tests:** `tests/**/*.test.ts`.

## Lo que NO decide el pack

- Framework web (Fastify, Express, Hono, NestJS…) — queda para `@architect`.
- Framework UI (React, Vue, Svelte…) — queda para `@architect`.
- Persistencia — queda para `@architect`.
- Estilo de arquitectura (monolito, DDD, hexagonal) — queda para `@architect`.

## Uso

```bash
bash scripts/init-project.sh --template=web-typescript
```

Tras aplicar, `.github/instructions/backend.instructions.md`, `frontend.instructions.md` y `testing.instructions.md` llevan reglas específicas de TypeScript/Node. Los workflows CI tienen `setup-node@v4` con versión 20 y comandos `pnpm test*`.
