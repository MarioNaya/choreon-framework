---
applyTo: "[[BACKEND_GLOB]]"
---

<!--
Plantilla de instrucciones para código backend.
Reemplaza [[BACKEND_GLOB]] con el patrón del proyecto (ej: "src/api/**/*.ts", "app/**/*.py").
Completa las secciones marcadas con <!-- RELLENAR --> durante o después del /bootstrap.
-->

# Instrucciones — Backend

## Estilo de código

<!-- RELLENAR: lenguaje, versión, convenciones de naming, formateador/linter -->

- Lenguaje: [[p. ej. TypeScript 5.x]]
- Formatter: [[p. ej. Prettier]]
- Linter: [[p. ej. ESLint con reglas X]]
- Naming: [[camelCase para funciones, PascalCase para clases]]

## Estructura de carpetas

<!-- RELLENAR: capas, dónde vive cada tipo de archivo -->

```
src/
├── domain/           # Entidades, reglas de negocio
├── application/      # Casos de uso, orquestación
├── infrastructure/   # Persistencia, integración externa
└── presentation/     # HTTP controllers, handlers
```

## Patrones preferidos

<!-- RELLENAR: 3-6 ejemplos correctos vs incorrectos -->

- **Gestión de errores:** [[excepciones tipadas / Result<T,E> / …]]
- **Logging:** `logger.info({evento, contexto})`, no `console.log`
- **Inyección de dependencias:** [[método]]
- **Validación de entrada:** en la capa de presentación, antes de llegar al caso de uso

## Anti-patrones

<!-- RELLENAR: 3-5 cosas prohibidas con razón -->

- No usar `any` sin comentario justificativo.
- No mezclar lógica de negocio en handlers HTTP.
- No llamar directamente a la base de datos desde controllers.

## Dependencias

- Nuevas dependencias requieren entrada en `DECISIONES.md §Stack` (handoff `@architect`).
- Dependencias vetadas: [[lista si aplica]]

## Testing

- Cobertura mínima por módulo: [[X%]]
- Todo caso de uso nuevo incluye test unitario + al menos 1 de integración.
- Tests de infraestructura usan [[test containers / fixtures reales]], no mocks de base de datos.

## Referencia a decisiones vigentes

Cuando sigas estas reglas, cítalas por §Categoría de `docs/sesion/DECISIONES.md` en los comentarios del PR.
