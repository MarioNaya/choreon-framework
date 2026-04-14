# DECISIONES

Última actualización: 2026-04-14

## 1. Filosofía de desarrollo

- Cambios incluyen pruebas en el mismo commit; no se acepta "tests después".
- KISS por encima de DRY cuando hay tensión: preferir dos funciones claras que una abstracción forzada.
- Deuda técnica visible en `CONTEXTO.md §Deuda técnica`; nunca oculta en comentarios "TODO" sueltos.

## 2. Stack

- Lenguaje: TypeScript 5.4 en todo el codebase (front y back).
- Runtime backend: Node.js 20 LTS.
- Framework backend: Fastify 4.x con JSON Schema.
- Frontend: React 18 + Vite 5 + vite-plugin-pwa.
- Estado cliente: Zustand 4.x con middleware de persistencia IndexedDB.
- Persistencia: SQLite 3.45+ vía better-sqlite3 11.x (sincrónico).
- Web Push: librería `web-push` 3.x con VAPID keys generadas al instalar.
- Testing: Vitest 1.x (unit + integración) y Playwright 1.44+ (E2E).
- Gestión de dependencias: pnpm 9.x con workspaces (front/back comparten tipos).

## 3. Arquitectura

- Patrón global: monolito modular con capas (Domain / Application / Infrastructure / Api / Web).
- Domain es puro (sin dependencias externas); el parser de lenguaje natural vive aquí.
- Application orquesta casos de uso usando Result<T, E>.
- Infrastructure encapsula SQLite, web-push y cron scheduler.
- Web habla con Api solo por HTTP; no conoce la BBDD.
- Dependencias prohibidas: Domain → Infra/Api/Web; Application → Api/Web; Infra → Api/Web.

## 4. Convenciones de código

- Identificadores en inglés (código); documentación y comentarios en español.
- Naming: camelCase funciones/variables, PascalCase tipos/clases, kebab-case archivos.
- Gestión de errores: `Result<T, DomainError>` en Domain/Application; excepciones solo en el borde Api→HTTP, mapeadas en un único middleware.
- Logging: pino; JSON en producción, pretty en dev; niveles `info`/`warn`/`error`.
- Comentarios: solo cuando el porqué no es obvio; nunca narrar qué hace el código.
- Inyección de dependencias manual vía factories; sin framework DI.

## 5. Testing

- Pirámide: 70% unit, 20% integración, 10% E2E.
- Cobertura mínima: 80% medida con v8 (vitest --coverage).
- Comandos: `pnpm test` (unit), `pnpm test:int` (integración con SQLite tmp), `pnpm test:e2e` (Playwright).
- Prohibido: `sleep` fijos, mocks de base de datos (usar SQLite en memoria), tests dependientes del orden.
- Parser NL (S02) se valida contra fixture de ≥50 frases en `tests/fixtures/nl-dates.json`.

## 6. Datos y persistencia

- SQLite archivo único `data.sqlite` en volumen persistente.
- Migraciones con umzug 3.x, archivos numerados `migrations/NNN-descripcion.ts`.
- Sin transacciones explícitas salvo en sync bulk; better-sqlite3 es transaccional por defecto en escrituras simples.
- Backup: cron diario copia a `backups/data-YYYY-MM-DD.sqlite`; retiene 14 días.
- Sin seed fijo; el primer arranque crea ajustes por defecto (umbral recordatorio = 2h).

## 7. Seguridad y auth

- Usuario único; auth por cookie de sesión firmada (iron-session o equivalente).
- Secrets (session key, VAPID keys) en `.env` fuera del repo; ejemplo en `.env.example`.
- Validación en el borde Api con JSON Schema; Domain asume datos ya validados.
- Sin telemetría externa. Sin tracking.
- Headers de seguridad: Helmet con defaults + CSP restrictiva para la PWA.

## 8. Despliegue

- Entornos: local (dev) y production (VPS autoalojado).
- Pipeline CI: `.github/workflows/ci-manual.yml` y `ci-nightly.yml` (plantillas — pendientes de rellenar placeholders de runner y comandos).
- Build: `pnpm build` genera `dist/` con server + estáticos.
- Runtime: un proceso Node con systemd unit; sirve API y estáticos.
- Deploy: `rsync` desde local + `systemctl restart`; sin Docker en V1 por la restricción de RAM.
