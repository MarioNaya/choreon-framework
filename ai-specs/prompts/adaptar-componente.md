---
description: Adapta tests/código existentes tras un cambio en un componente, contrato o dependencia. Propone cambios mínimos.
agent: feature-developer
---

# /adaptar-componente

## Entrada esperada

- Componente/módulo/contrato que cambió.
- Tipo de cambio: renombrado / eliminación / nuevo parámetro / cambio semántico.
- Descripción breve del cambio.

## Workflow

0. Lee `CONTEXTO.md` y `DECISIONES.md`.
1. Invoca `@context-reader` primero para analizar impacto (qué archivos del proyecto dependen).
2. Revisa con el usuario el inventario de impactos.
3. Invoca `@feature-developer` con la lista de cambios mínimos.
4. El developer aplica el cambio **del alcance acotado**: solo lo necesario para que el proyecto vuelva a verde. No refactora de paso.
5. Ejecuta tests relevantes.
6. Handoff a `@code-reviewer`.

## Reglas

- Gate de Definition-of-Done aplica también a adaptaciones.
- Si el cambio obliga a modificar ARQUITECTURA o DECISIONES, escala a `@architect`.
- Si el cambio afecta al dominio (nuevo estado, capacidad eliminada), vuelve a `@domain-modeler`.
