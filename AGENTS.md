# AGENTS.md

<!--
Punto de entrada estándar multi-herramienta para agentes de IA.
Lo consumen: Claude Code, GitHub Copilot, Cursor, Aider, Codex, y otros que soporten la convención AGENTS.md.
-->

## Proyecto

**Nombre:** [[NOMBRE_PROYECTO]]

**Descripción:** [[DESCRIPCION_PROYECTO]]

## Arquitectura del sistema agéntico

> Glosario de términos (agente, skill, prompt, handoff, Gate DoD, memoria compacta, SDD): [`docs/guias/GLOSARIO_SISTEMA.md`](docs/guias/GLOSARIO_SISTEMA.md).
> Tutorial paso a paso con ejemplo real: [`docs/guias/WALKTHROUGH.md`](docs/guias/WALKTHROUGH.md).

Este repositorio usa un sistema de 9 agentes + 11 prompts + 3 skills organizados alrededor de dos principios:

1. **Separación estricta de responsabilidades**, con superficie de escritura acotada por agente (`docs/guias/MATRIZ_PERMISOS.md`).
2. **Memoria disciplinada**: `CONTEXTO.md` ≤80 líneas y `DECISIONES.md` editado in-place por categoría (ambos con backup automático).

## Estructura

```
ai-specs/                  ← FUENTE DE VERDAD de agentes, prompts y skills
├── agents/                (9 agentes en formato neutro)
├── prompts/               (10 prompts)
└── skills/                (bootstrap-from-spec, memory-bank)

.claude/                   ← generado desde ai-specs/ por scripts/sync-agents.sh
.github/agents|prompts|skills/  ← generado desde ai-specs/ por scripts/sync-agents.sh
.github/instructions/      ← plantillas manuales por tipo de archivo
.github/workflows/         ← CI templateado

specs/                     ← brief.md (input) + spec-cerrada-*.md (output de spec-analyst)

docs/
├── sesion/                CONTEXTO.md · DECISIONES.md · TRIAGE_CI.md + backups
├── referencia/            DOMINIO.md · GLOSARIO.md · ARQUITECTURA.md · CATALOGO.md · COBERTURA.md
├── planificacion/         ROADMAP.md
├── guias/                 COPILOT.md · CLAUDE_CODE.md · ONBOARDING.md · MATRIZ_PERMISOS.md · CI_GUIDE.md
└── archivo/               DECISIONES_HISTORICO.md (append-only)

scripts/                   sync-agents.sh · init-project.sh · validar-contexto.sh · validar-decisiones.sh
```

## Quickstart

```bash
# 1. Inicializar placeholders globales
bash scripts/init-project.sh

# 2. Generar las copias para Claude Code y Copilot desde el hub canonical
bash scripts/sync-agents.sh

# 3. Escribir la idea inicial del proyecto
$EDITOR specs/brief.md

# 4. Abrir con tu herramienta agéntica:
claude                      # Claude Code
# o abrir VS Code con Copilot Chat

# 5. Disparar el bootstrap conversacional
/bootstrap
```

## Agentes

| Agente | Propósito | Fase |
|---|---|---|
| `spec-analyst` | Cierra 6 dimensiones de la spec inicial | Bootstrap 1 |
| `domain-modeler` | Extrae entidades, ciclo de vida, capacidades | Bootstrap 2 |
| `architect` | Propone stack, patrones, convenciones | Bootstrap 3 |
| `feature-analyst` | Plan de funcionalidad | Desarrollo |
| `feature-developer` | Implementación con Gate de Definition-of-Done | Desarrollo |
| `code-reviewer` | Revisión con Gate replicado | Desarrollo |
| `context-reader` | Diagnóstico read-only (repos vecinos, regresiones) | Apoyo |
| `context-manager` | Persiste CONTEXTO + DECISIONES (con backup dual) | Apoyo |
| `ci-triage` | Clasificación 🔴🟡🔵⚪ de fallos CI | Apoyo |

## Prompts disponibles

`/bootstrap`, `/nueva-sesion`, `/analizar-funcionalidad`, `/implementar-feature`, `/revisar-codigo`, `/depurar-fallo`, `/adaptar-componente`, `/sincronizar-dominio`, `/triage-ci`, `/actualizar-contexto`.

## Reglas de oro

1. Lee `docs/sesion/CONTEXTO.md` al inicio de cada sesión.
2. Ningún agente escribe fuera de su fila de `MATRIZ_PERMISOS.md`.
3. Gate de Definition-of-Done es innegociable para `feature-developer` y `code-reviewer`.
4. `CONTEXTO.md` ≤80 líneas. `DECISIONES.md` in-place por categoría, nunca append cronológico.
5. Confirmación explícita del usuario antes de redactar en las 3 fases de bootstrap.

## Herramientas soportadas

- **Claude Code** — agentes en `.claude/agents/`, prompts en `.claude/commands/`, skills en `.claude/skills/`.
- **GitHub Copilot** — agentes en `.github/agents/`, prompts en `.github/prompts/`, skills en `.github/skills/`, instrucciones por archivo en `.github/instructions/`.
- **Otros** — pueden leer directamente `ai-specs/` (formato markdown neutro).

## Origen

Este boilerplate se deriva de un sistema auditado de QA E2E que obtuvo 8.5/10 (`../auditoria/AUDITORIA.md` si lo tienes disponible) y del patrón Spec-Driven Development del repo `manual-SDD`.
