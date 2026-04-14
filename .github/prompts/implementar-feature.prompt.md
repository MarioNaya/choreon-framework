---
description: Implementa una funcionalidad a partir de un plan cerrado. Aplica el Gate de Definition-of-Done antes de tocar código.
agent: feature-developer
---

# /implementar-feature

## Entrada esperada

- Plan producido por `@feature-analyst` (o referencia a él en el chat).
- Opcionalmente: restricciones adicionales no recogidas.

## Workflow

0. Lee `docs/sesion/CONTEXTO.md` y `docs/sesion/DECISIONES.md`.
1. **Gate de Definition-of-Done** — responde las 3 preguntas ANTES de escribir código:
   1. ¿Hay criterio de aceptación verificable?
   2. ¿Hay prueba automatizada posible?
   3. ¿El cambio respeta `ARQUITECTURA.md`?
   Si alguna es "no", detente.
2. Lee `CATALOGO.md` para detectar reutilización.
3. Invoca `@feature-developer`.
4. Implementación mínima + pruebas que cubran los criterios.
5. Ejecuta comandos de test si están definidos en DECISIONES (§Testing).
6. Reporte estándar y handoff a `@code-reviewer`.

## Reglas

- No refactorices código no relacionado.
- No introduzcas dependencias nuevas sin escalar a `@architect`.
- Solo escribes en rutas permitidas por `docs/guias/MATRIZ_PERMISOS.md`.
