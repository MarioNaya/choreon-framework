# Auditorías

Informes de auditoría del propio sistema agéntico. Cada entrada es una foto crítica del estado del boilerplate en un momento concreto, con puntos fuertes, defectos, sobreingeniería y líneas de mejora.

No sustituye a la documentación: es input para futuras decisiones de diseño, registrado fuera de `docs/archivo/` porque sigue siendo útil como referencia activa.

## Convención

- Nombre: `AUDITORIA_V<major>.<minor>[-<sufijo>].md` (p.ej. `AUDITORIA_V0.4.md`, `AUDITORIA_V0.4-post-docs.md`).
- Cada archivo es **autocontenido** — no depende de auditorías previas; repite contexto si hace falta.
- Cada auditoría empieza con header estándar: fecha, versión auditada, auditor, contexto.
- Las **recomendaciones priorizadas** (P1/P2/P3/P4) son la sección más accionable; sepáralas claramente.

## Auditorías archivadas

| Versión | Fecha | Nota | Archivo |
|---|---|---|---|
| v0.4 (post-docs) | 2026-04-15 | 7.8 / 10 | [`AUDITORIA_V0.4.md`](AUDITORIA_V0.4.md) |
| v0.5 (primer uso real — bootstrap) | 2026-04-15 | 8.5 / 10 | [`AUDITORIA_V0.5.md`](AUDITORIA_V0.5.md) |

## Cuándo auditar

Recomendado antes de:
- Publicar una versión menor (v0.5, v0.6…).
- Reescribir una subsección grande (agentes, memoria, MCP).
- Adoptar el boilerplate en un proyecto real por primera vez.

El primer uso real en producción genera la siguiente auditoría de mayor valor — la que contrasta diseño contra fricciones empíricas.
