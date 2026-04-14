# CONTEXTO (sesión S1)
Última actualización: 2026-04-14

## Estado actual

| Métrica | Valor |
|---|---|
| Módulos implementados | 0 (proyecto recién inicializado) |
| Tests unitarios | 0 / 0 |
| Cobertura | 0% |
| Entorno funcional | local (sin deploy todavía) |

## Bloqueados

| ID | Motivo | Acción pendiente |
|---|---|---|
| — | — | — |

## Deuda técnica

- Primera feature por seleccionar en ROADMAP.
- Sin pipeline CI configurado aún (workflows plantilla pendientes de rellenar).
- Sin volumen persistente provisionado para SQLite.

## Próxima tarea

Implementar `captura-rapida` (S01) como primera feature: endpoint POST /api/tasks + componente TaskQuickAdd + test unit del parser de fechas. Handoff: `/analizar-funcionalidad` + `@feature-analyst`.

## Mocks disponibles

- Ninguno aún. Al implementar sync, crear mock de IndexedDB para tests unit de store.

## Convenciones activas

- Result<T, DomainError> en Domain y Application (DECISIONES §4 Convenciones de código).
- Excepciones solo en el borde Api→HTTP (DECISIONES §4).
- better-sqlite3 sincrónico como repo — no async innecesario (DECISIONES §6 Datos).
- Naming camelCase/PascalCase/kebab-case por tipo (DECISIONES §4).
- Cobertura mínima 80% con v8 (DECISIONES §5 Testing).
- Parser de fechas NL en Domain, no en Api (DECISIONES §3 Arquitectura).
