---
description: Produce un plan de implementación detallado para una funcionalidad concreta en un proyecto ya inicializado.
agent: feature-analyst
---

# /analizar-funcionalidad

## Entrada esperada

- Nombre/descripción breve de la funcionalidad.
- Usuario objetivo / actor si no es obvio.
- Restricciones específicas no recogidas en DECISIONES.

## Workflow

0. Lee `docs/sesion/CONTEXTO.md`. Si hay bloqueantes o deuda que afecten, avísalo antes de planificar.
1. Invoca `@feature-analyst` pasando la descripción.
2. El analyst produce plan en el formato estándar (alcance, matriz de impacto, criterios de aceptación, pruebas recomendadas, reutilización, riesgos).
3. Si el plan identifica que la funcionalidad altera el dominio o requiere decisión arquitectónica nueva, el handoff va a `@domain-modeler` o `@architect` respectivamente; si no, a `@feature-developer`.

## Reglas

- No se escribe código en este prompt.
- Los criterios de aceptación deben ser verificables.
- Si el plan requiere >5 archivos nuevos o toca >3 módulos, sugiere trocearlo en tareas más pequeñas.
