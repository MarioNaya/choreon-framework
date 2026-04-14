# AIboilerplate

Un punto de partida agéntico para proyectos de desarrollo nuevos. Conviertes una idea inicial (una user story, un PRD rápido, una descripción libre) en un proyecto con documentación viva, decisiones técnicas explícitas y un sistema de memoria compacta que sobrevive entre sesiones de IA.

Funciona con **Claude Code** y **GitHub Copilot** como herramientas de primera clase, y con Cursor / Aider / Codex vía `AGENTS.md`.

---

## El problema que resuelve

Trabajar con agentes de IA (Claude, Copilot) en un proyecto real tiene tres fricciones recurrentes:

1. **Cada sesión empieza desde cero.** El agente no recuerda lo que decidiste ayer; tú gastas 10 minutos re-explicando contexto.
2. **Las decisiones se pierden.** Acordaste que la BBDD sería PostgreSQL, pero una semana después el agente propone MongoDB porque nadie lo anotó en un sitio canónico.
3. **El agente "inventa" al principio del proyecto.** Le pides "hazme un backend" sin haber cerrado problema, actores, alcance ni criterios de éxito, y lo que escribe no resiste un segundo review.

AIboilerplate fuerza tres disciplinas que resuelven cada una:

1. **Memoria compacta y persistente** — `CONTEXTO.md` (≤80 líneas) + `DECISIONES.md` (8 categorías fijas). Siempre cabe en la ventana, siempre está sincronizada, siempre es la fuente de verdad.
2. **Decisiones explícitas** — cada decisión de stack, arquitectura o convención vive en `DECISIONES.md` editada *in-place* por categoría. No hay "lo decidimos en un Slack hace dos meses".
3. **Spec-Driven Development** — todo proyecto arranca cerrando 6 dimensiones obligatorias (problema, actores, alcance, restricciones, comportamiento, éxito) antes de hablar de código. Si no puedes responderlas, no implementas.

Ver [glosario](docs/guias/GLOSARIO_SISTEMA.md) si algún término no te suena.

## Qué recibes al clonar

- **9 agentes** (roles con identidad y permisos de escritura acotados): `spec-analyst`, `domain-modeler`, `architect`, `feature-analyst`, `feature-developer`, `code-reviewer`, `context-reader`, `context-manager`, `ci-triage`.
- **11 slash-commands** como punto de entrada: `/bootstrap`, `/nueva-sesion`, `/analizar-funcionalidad`, `/implementar-feature`, `/revisar-codigo`, `/depurar-fallo`, `/adaptar-componente`, `/sincronizar-dominio`, `/triage-ci`, `/actualizar-contexto`, `/import-project`.
- **2 skills** que activan los agentes según contexto: `memory-bank` (protocolos de memoria) y `bootstrap-from-spec` (cascada de inicialización).
- **Plantillas de memoria y documentación** listas para rellenar: `CONTEXTO.md`, `DECISIONES.md`, `DOMINIO.md`, `GLOSARIO.md`, `ARQUITECTURA.md`, `CATALOGO.md`, `COBERTURA.md`, `ROADMAP.md`.
- **Dos servidores MCP locales** opcionales: `memory-mcp` (memoria queryable por categoría, reduce token load) y `fs-guard-mcp` (aplica la matriz de permisos por agente de verdad, no por convención).
- **Template packs** por stack (`web-typescript`, `python-api`, `go-service`) que rellenan placeholders técnicos y traen instrucciones idiomáticas.
- **Un ejemplo completo** (`examples/golden-path/`) de un proyecto ficticio ya bootstrappeado para que veas cómo luce el resultado.
- **Pre-commit hook opcional** y **workflow de health** que vigilan que las invariantes del sistema no se rompan.

## Cómo funciona en 30 segundos

```
brief.md (tú) ─► /bootstrap ─► spec-analyst ─► spec cerrada
                                    │
                                    ▼
                               domain-modeler ─► DOMINIO + GLOSARIO
                                    │
                                    ▼
                                architect ─► ARQUITECTURA + CATALOGO + DECISIONES
                                    │
                                    ▼
                              context-manager ─► CONTEXTO S1 (sistema operativo)
```

A partir de ahí, el ciclo normal es: `/nueva-sesion` → `/analizar-funcionalidad` → `/implementar-feature` → `/revisar-codigo` → `/actualizar-contexto`. Cada agente tiene un ámbito de escritura acotado en `docs/guias/MATRIZ_PERMISOS.md`.

## Quickstart

Prerequisitos: Python 3.10+ en el PATH. Opcional: Claude Code (`npm install -g @anthropic-ai/claude-code`) o VS Code con GitHub Copilot.

```bash
# 1. Clonar
git clone <ruta-a-este-repo> mi-proyecto
cd mi-proyecto

# 2. Inicializar (opcional --template para stacks conocidos)
bash scripts/init-project.sh --template=web-typescript
#   → resuelve placeholders globales y específicos del stack
#   → copia instrucciones pre-rellenadas a .github/instructions/

# 3. Generar copias adaptadas para Claude Code y Copilot
bash scripts/sync-agents.sh
#   → produce .claude/, .github/agents, .github/prompts, CLAUDE.md

# 4. Escribir tu idea inicial
$EDITOR specs/brief.md
#   → formato libre; una página suele bastar

# 5. Abrir con tu herramienta y disparar bootstrap
claude         # o abrir VS Code con Copilot Chat
/bootstrap
```

El `/bootstrap` hará preguntas conversacionales durante 20-40 minutos para cerrar las 6 dimensiones, modelar el dominio y proponer arquitectura. Tras completarse, tu proyecto tiene toda la documentación viva lista y `CONTEXTO.md` en sesión S1.

Siguiente lectura recomendada: [`docs/guias/ONBOARDING.md`](docs/guias/ONBOARDING.md) (modelo mental) y [`docs/guias/WALKTHROUGH.md`](docs/guias/WALKTHROUGH.md) (tutorial paso a paso sobre un ejemplo real).

## Cuándo SÍ usarlo, cuándo NO

| Encaja bien si... | Mejor no lo uses si... |
|---|---|
| Arrancas un proyecto nuevo y quieres memoria viva desde el día 1 | Ya tienes un sistema de documentación maduro (Notion/Confluence) y no quieres duplicar |
| Trabajas con IA de forma habitual y te frustra re-explicar contexto | Prefieres conversación libre con la IA sin estructura impuesta |
| Eres 1-5 personas en el equipo | Organización grande (>20) con procesos de documentación propios |
| Valoras decisiones explícitas y trazables | Prefieres velocidad pura, con documentación mínima |
| Adoptas un repo existente y quieres regirlo con este sistema | El repo existente tiene ya su propio sistema agéntico que funciona |
| Stack común (TS, Python, Go) o estás dispuesto a crear un pack propio | Stack exótico y no quieres perder tiempo adaptando plantillas |

## Estructura del repo

```
AGENTS.md            ← entrada multi-tool (Cursor, Aider, Codex)
CLAUDE.md            ← autogenerado; punto de entrada para Claude Code
README.md            ← este archivo
INIT.md              ← checklist de inicialización paso a paso

ai-specs/            ← FUENTE DE VERDAD (agentes, prompts, skills canónicos)
.claude/             ← generado por sync-agents.py (Claude Code)
.github/             ← generado + plantillas manuales (Copilot)

specs/               ← brief.md + specs cerradas
docs/
├── sesion/          ← CONTEXTO, DECISIONES, TRIAGE_CI (memoria volátil)
├── referencia/      ← DOMINIO, GLOSARIO, ARQUITECTURA, CATALOGO, COBERTURA (estable)
├── planificacion/   ← ROADMAP
├── guias/           ← esta documentación
└── archivo/         ← histórico append-only

examples/
└── golden-path/     ← ejemplo completo de proyecto bootstrappeado

scripts/             ← sync, init, validadores, MCP servers
templates/           ← template packs por stack
```

## Documentación

Por orden de lectura recomendada:

| Nivel | Documento | Para qué |
|---|---|---|
| L1 | Este README | Orientación inicial |
| L2 | [`ONBOARDING.md`](docs/guias/ONBOARDING.md) | Modelo mental completo del sistema |
| L3 | [`WALKTHROUGH.md`](docs/guias/WALKTHROUGH.md) | Tutorial paso a paso con el golden-path |
| L4 | [`GLOSARIO_SISTEMA.md`](docs/guias/GLOSARIO_SISTEMA.md) | Definiciones canónicas de cada término |
| L4 | [`CLAUDE_CODE.md`](docs/guias/CLAUDE_CODE.md) / [`COPILOT.md`](docs/guias/COPILOT.md) | Setup y operativa por herramienta |
| L4 | [`MATRIZ_PERMISOS.md`](docs/guias/MATRIZ_PERMISOS.md) | Qué puede escribir cada agente |
| L4 | [`CI_GUIDE.md`](docs/guias/CI_GUIDE.md) | Workflows de CI incluidos |

## Origen y estado

El diseño se deriva de dos fuentes:

- Un sistema de QA agéntico probado en producción durante 3 meses, auditado con nota **8.5/10**.
- El patrón Spec-Driven Development del repo de referencia `manual-SDD`.

Estado actual: **v0.3** (142 archivos). Los 13 checks del workflow `ci-boilerplate-health.yml` están en verde. Falta probarlo en un proyecto real — el autor valora como **~9.2/10** las piezas construidas, con el gap restante en observación empírica de fricciones reales al usarlo end-to-end.

## Herramientas soportadas

| Herramienta | Estado | Entrada |
|---|---|---|
| Claude Code | Primera clase | `CLAUDE.md` raíz + `.claude/` generado |
| GitHub Copilot | Primera clase | `.github/copilot-instructions.md` + `.github/` generado |
| Cursor / Aider / Codex | Funcional vía `AGENTS.md` | Leen directamente `ai-specs/` |

## Licencia

[[LICENCIA]]
