# Instrucciones globales de Copilot — [[NOMBRE_PROYECTO]]

<!--
Rellena los [[PLACEHOLDERS]] tras ejecutar /bootstrap.
Los campos derivados de DECISIONES y ARQUITECTURA se pueden completar con @architect en una iteración posterior.
-->

## Protocolo de inicio de sesión

Al comenzar cualquier sesión, lee `docs/sesion/CONTEXTO.md` para conocer estado, bloqueantes y próxima tarea.

## Descripción del proyecto

[[DESCRIPCION_PROYECTO — 2-3 líneas: qué hace, para quién, cuál es el objetivo principal]]

## Workspace

| Ruta | Rol |
|---|---|
| Raíz del proyecto | ✍️ Escritura permitida (ámbito por agente en `docs/guias/MATRIZ_PERMISOS.md`) |
| [[REPO_VECINO_1]] | 👁️ Solo lectura (por `@context-reader`) |
| [[REPO_VECINO_N]] | 👁️ Solo lectura |

## Stack

<!-- Completar tras /bootstrap fase 3 (architect) -->

- Lenguaje: [[LENGUAJE]]
- Framework principal: [[FRAMEWORK]]
- Testing: [[HERRAMIENTAS]]

Ver `docs/sesion/DECISIONES.md §2 Stack` para el detalle actualizado.

## Arquitectura

Ver `docs/referencia/ARQUITECTURA.md`. Dependencias prohibidas listadas allí.

## Agentes disponibles

9 agentes en `.github/agents/` (generados desde `ai-specs/agents/`):

- **Bootstrap:** `spec-analyst`, `domain-modeler`, `architect`
- **Desarrollo:** `feature-analyst`, `feature-developer`, `code-reviewer`
- **Apoyo:** `context-reader`, `context-manager`, `ci-triage`

## Prompts (slash-commands)

10 prompts en `.github/prompts/`. Lista completa en `docs/guias/COPILOT.md`.

## Convenciones transversales

<!-- Completar tras /bootstrap. Mantener este bloque sincronizado con DECISIONES §Convenciones de código -->

- Idioma de identificadores: [[en/es]]
- Naming: [[convención]]
- Gestión de errores: [[política]]
- Logging: [[nivel/formato]]
- Comentarios: [[cuándo sí/no]]

## Filosofía de desarrollo

- **Gate de Definition-of-Done** antes de escribir código (ver `feature-developer.agent.md`).
- **Pruebas verifican comportamiento observable**, no implementación interna.
- **Decisiones explícitas** — cualquier decisión no trivial va a `DECISIONES.md`.
- **Memoria compacta** — CONTEXTO ≤80 líneas; DECISIONES in-place por categoría.

## Flujos de trabajo

Ver `docs/guias/ONBOARDING.md` (árbol de decisión Mermaid).

| Situación | Flujo |
|---|---|
| Proyecto nuevo | Editar `specs/brief.md` → `/bootstrap` |
| Sesión de trabajo | `/nueva-sesion` → tarea → `/actualizar-contexto` |
| Funcionalidad nueva | `/analizar-funcionalidad` → `/implementar-feature` → `/revisar-codigo` |
| Bug | `/depurar-fallo` |
| CI rojo | `/triage-ci` |

## Referencias

- Matriz de permisos: `docs/guias/MATRIZ_PERMISOS.md`
- Decisiones vigentes: `docs/sesion/DECISIONES.md`
- Estado actual: `docs/sesion/CONTEXTO.md`
- Árbol de decisión: `docs/guias/ONBOARDING.md`
