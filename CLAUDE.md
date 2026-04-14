# CLAUDE.md — instrucciones globales para Claude Code

<!-- Archivo generado por scripts/sync-agents.py. No editar a mano; editar ai-specs/ y regenerar. -->

## Protocolo de inicio de sesión

Al comenzar cualquier sesión, lee `docs/sesion/CONTEXTO.md` (≤80 líneas) para conocer estado, bloqueantes y próxima tarea. Si no existe o está vacío, ejecuta `/bootstrap`.

## Descripción del proyecto

[[DESCRIPCION_PROYECTO]]

## Sistema agéntico

Este repo incluye **9 agentes**, **11 prompts** (slash-commands) y **2 skills**. Definiciones canónicas en `ai-specs/`; copias adaptadas en `.claude/` y `.github/` generadas por `scripts/sync-agents.py`.

### Subagentes disponibles

- **`@architect`** — Propone stack técnico, patrones arquitectónicos, estructura de módulos y convenciones. Seedea DECISIONES y produce ARQUITECTURA.md y CATALOGO.md. Fase 3 del workflow bootstrap.
- **`@ci-triage`** — Analiza resultados de CI y clasifica fallos en 4 categorías (🔴 regresión real, 🟡 flaky, 🔵 conocido, ⚪ entorno). Escribe TRIAGE_CI.md y hace handoff a context-reader si hay 🔴.
- **`@code-reviewer`** — Revisa implementaciones contra el plan, la arquitectura y las convenciones. Replica el Gate de Definition-of-Done para detectar tests débiles. No escribe código, solo diagnóstico.
- **`@context-manager`** — Persiste el estado de sesión. Reescribe CONTEXTO.md (≤80 líneas) y actualiza DECISIONES.md in-place por categoría. Crea backups de AMBOS archivos antes de modificarlos.
- **`@context-reader`** — Acceso de lectura a repositorios vecinos read-only y al código del proyecto. Diagnostica regresiones, propone causa raíz, analiza impacto de cambios externos. Solo escribe en TRIAGE.md.
- **`@domain-modeler`** — Toma una spec cerrada y extrae entidades, relaciones, ciclo de vida y matriz de capacidades. Produce DOMINIO.md y GLOSARIO.md. Fase 2 del workflow bootstrap.
- **`@feature-analyst`** — Analiza una funcionalidad concreta (ya en un proyecto inicializado) y produce un plan de implementación detallado con criterios de aceptación. No escribe código.
- **`@feature-developer`** — Implementa funcionalidades siguiendo un plan de feature-analyst. Aplica el Gate de Definition-of-Done antes de escribir cualquier código. Escribe en el workspace del proyecto.
- **`@spec-analyst`** — Dialoga con el usuario a partir de un brief inicial (user story o PRD) y cierra las 6 dimensiones obligatorias antes de redactar la spec. No implementa nada. Fase 1 del workflow bootstrap.

### Slash-commands

- `/actualizar-contexto`
- `/adaptar-componente`
- `/analizar-funcionalidad`
- `/bootstrap`
- `/depurar-fallo`
- `/implementar-feature`
- `/import-project`
- `/nueva-sesion`
- `/revisar-codigo`
- `/sincronizar-dominio`
- `/triage-ci`

## Reglas de oro

1. Lee `docs/sesion/CONTEXTO.md` al inicio de cada sesión.
2. Ningún agente escribe fuera de su fila en `docs/guias/MATRIZ_PERMISOS.md`.
3. Gate de Definition-of-Done es innegociable para `@feature-developer` y `@code-reviewer`.
4. `CONTEXTO.md` ≤80 líneas. `DECISIONES.md` in-place por categoría, nunca append cronológico.
5. Confirmación explícita del usuario antes de redactar en las 3 fases de bootstrap.
6. Backup dual (`.bak.md`) antes de modificar CONTEXTO o DECISIONES.

## Referencias clave

- Árbol de decisión de agentes: `docs/guias/ONBOARDING.md`
- Matriz de permisos: `docs/guias/MATRIZ_PERMISOS.md`
- Guía específica Claude Code: `docs/guias/CLAUDE_CODE.md`
- Ejemplo completo de bootstrap: `examples/golden-path/README.md`
- Decisiones vigentes: `docs/sesion/DECISIONES.md`
- Estado actual: `docs/sesion/CONTEXTO.md`
