---
applyTo: "**/*.test.ts"
---

# Instrucciones — Testing TypeScript

## Filosofía

Los tests verifican **comportamiento observable**, no implementación interna. Si refactorizas sin cambiar comportamiento y el test se rompe, el test está mal.

## Pirámide objetivo

- Unit: 70% — dominio puro, utilidades, lógica de casos de uso con repos en memoria.
- Integración: 20% — repos reales contra BBDD temporal, end-to-end de casos de uso backend.
- E2E: 10% — flujos críticos con el stack completo.

Cobertura mínima: **80%** medida con v8 (`vitest --coverage`) salvo que DECISIONES indique otro umbral.

## Reglas absolutas

- **Sin esperas fijas.** Nada de `await new Promise(r => setTimeout(r, N))`. Usa `waitFor` / condiciones explícitas.
- **Sin skips sin justificación.** `test.skip` requiere comentario + entrada en `DECISIONES §5 Testing`.
- **Tests independientes.** Cada test configura su propio estado. No dependas del orden.
- **Un assert principal.** Múltiples asserts OK si verifican el mismo comportamiento.
- **Nombres descriptivos:** `it('should reject task with empty title', ...)`.

## Comandos

- Unit: `pnpm test`
- Integración: `pnpm test:integration`
- E2E: `pnpm test:e2e`
- Todo: `pnpm test:all`

## Fixtures y datos

- Ubicación: `tests/fixtures/`
- Fixtures versionadas en git; sin secretos.
- Para fechas/relojes: usar abstracción (`clock`) para determinismo.

## Qué NO probar a este nivel

| ✅ Unit | ❌ No en unit |
|---|---|
| Lógica del dominio | Que un método se llamó (eso es integración) |
| Parsing, validaciones | Configuración del framework |
| Transformaciones puras | Renderizado DOM (usa tests de componentes) |
