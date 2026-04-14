---
applyTo: "src/**/*.ts"
---

# Instrucciones — Backend TypeScript

## Estilo de código

- Lenguaje: TypeScript 5.4+, `strict: true` en `tsconfig`.
- Formatter: Prettier (config por defecto salvo que DECISIONES §4 indique otra).
- Linter: ESLint con `@typescript-eslint` recomendado + reglas del proyecto.
- Naming: `camelCase` para funciones y variables; `PascalCase` para tipos, clases, interfaces; `kebab-case` para nombres de archivo.
- Sin `any` implícito. `unknown` aceptable solo en boundaries; convertir cuanto antes a tipos concretos.

## Estructura de carpetas recomendada

```
src/
├── domain/           # Entidades, reglas de negocio puras
├── application/      # Casos de uso, orquestación
├── infrastructure/   # Persistencia, integración externa
└── presentation/     # HTTP handlers / controllers
```

## Patrones preferidos

- **Gestión de errores:** `Result<T, DomainError>` en Domain/Application. Excepciones solo en el borde Presentation→HTTP, mapeadas en un middleware único.
- **Validación:** en el borde (zod, yup, JSON Schema del framework). Domain asume entradas ya validadas.
- **Logging:** pino — JSON en producción, pretty en dev. Niveles `info`/`warn`/`error`.
- **Inyección de dependencias:** manual vía factories; sin framework DI salvo que DECISIONES lo pida explícitamente.
- **Async:** `async/await`; evitar `.then()` encadenados.

## Anti-patrones

- Controllers HTTP con lógica de negocio inline — mover a capa Application.
- Llamar a la BBDD desde Presentation — usar Repositorios.
- Mutar objetos recibidos como argumento — preferir devolver nuevos.
- `enum` de TypeScript — preferir literal unions salvo que DECISIONES lo pida.

## Dependencias

- Nuevas dependencias requieren entrada en `DECISIONES.md §2 Stack` (handoff `@architect`).
- Preferir librerías con tipos propios; si usa `@types/*`, documentar versión.
