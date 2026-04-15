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

## Archivos generados por toolchain — NUNCA a mano

Estos archivos los genera el package manager; **no los escribas manualmente**:

- `pnpm-lock.yaml` / `package-lock.json` → `pnpm install` / `npm install`.
- `node_modules/` → `pnpm install`.
- Bundles de build (`dist/`, `build/`) → `pnpm build`.
- `*.tsbuildinfo` → `tsc`.

Si necesitas crear/actualizar alguno, déjalo como deuda explícita ("pendiente `pnpm install` tras añadir dependencia X") en tu reporte de implementación.

Escribir `pnpm-lock.yaml` a mano es un **anti-patrón**: los hashes deben generarse por el package manager; copiar/inventar rompe integridad y CI.
