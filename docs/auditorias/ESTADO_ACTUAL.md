# Estado actual — AI SDLC Framework

**Última actualización:** 2026-04-15
**Versión efectiva:** v0.7-pre (v0.6 + P1 aplicados en commit `5c5f98a`)
**Nota estimada:** 9.0 / 10 (subida desde 8.7 tras aplicar P1; pendiente validar empíricamente).

Este documento es el **punto de reentrada**. Si retomas el trabajo en otro ordenador o tras un tiempo sin tocarlo, **léelo primero**. Contiene el estado autosuficiente, no depende de conversación ni de memoria local de Claude Code.

---

## Cómo retomar en <5 minutos

Orden de lectura según qué quieras hacer:

| Si quieres… | Lee en este orden |
|---|---|
| **Entender qué es el framework** | `README.md` → `docs/guias/ONBOARDING.md` |
| **Continuar evolucionando el framework** | Este archivo → `AUDITORIA_V0.6.md` sección *"Recomendaciones estructurales para v0.7"* |
| **Retomar el test empírico (`gasto-cli`)** | `CONTEXTO.md` del test project local (ruta abajo) + `/nueva-sesion` |
| **Ver la historia completa de decisiones** | `AUDITORIA_V0.4.md` → `V0.5.md` → `V0.6.md` en orden |

---

## Qué está dónde (las 3 fuentes)

### 1. Repo remoto — fuente canónica del framework

```
URL:  https://github.com/MarioNaya/ai-sdlc-framework
Rama: main
```

Todo el código del framework, las 3 auditorías, el ejemplo `golden-path`, los fixes P1. **Commit actual:** `5c5f98a`.

Para arrancar en cualquier máquina:

```bash
git clone https://github.com/MarioNaya/ai-sdlc-framework
cd ai-sdlc-framework
cat docs/auditorias/ESTADO_ACTUAL.md   # este archivo
```

### 2. Test empírico `gasto-cli` — SOLO en laptop personal de Mario

```
Ruta: C:\Users\mario\Desktop\pruebaframework\ai-sdlc-framework\
```

**Importante:** este proyecto **NO está en ningún remote**. Existe solo en el laptop personal. Es el conejillo de indias que validó el framework en sesión S1 + S2 (ver v0.5 y v0.6).

Estado: `CONTEXTO.md` en sesión S3, 42/80 líneas. Bloqueantes: 0. Deudas 🟡 abiertas: H2 (testify transitiva), H3 (escalar ampliación matriz a `@architect` — **ya mitigado en v0.7-pre con `PROJECT_MANIFEST_PATHS`**), H4 (anotación arquitectural). Próxima tarea registrada en `§Próxima tarea`: escalar H3 + arrancar E02.

Si retomas `gasto-cli` desde ese laptop:

```bash
cd C:/Users/mario/Desktop/pruebaframework/ai-sdlc-framework
git pull               # trae los fixes P1 del framework
claude
/nueva-sesion          # @context-manager resume y guía
```

Si no estás en ese laptop: puedes ignorarlo. El framework se evoluciona sin `gasto-cli`. Cuando vuelvas al laptop personal y quieras validar v0.7 empíricamente, se puede reiniciar con un proyecto de prueba nuevo.

### 3. Memoria local de Claude Code — por máquina

Cada ordenador donde uses Claude Code tiene su propia memoria en `~/.claude/projects/.../memory/`. **No se sincroniza entre máquinas.**

Si es la primera vez que usas Claude Code en una máquina nueva, dime explícitamente *"trabajamos con el framework AI SDLC"* y yo leo el repo para construir contexto desde aquí. Si ya usé el framework en esa máquina, tendré una memoria de referencia apuntando a este documento.

---

## Resumen de lo construido hasta hoy

**8 archivos y 4 sistemas transversales:**

- **9 agentes canónicos** (3 bootstrap + 3 desarrollo + 3 apoyo) en `ai-specs/agents/`.
- **11 prompts** (slash-commands) en `ai-specs/prompts/`.
- **3 skills** (`memory-bank`, `bootstrap-from-spec`, `quick-bootstrap`).
- **Hub canonical + generación multi-tool** (`ai-specs/` → `.claude/` + `.github/` vía `scripts/sync-agents.py`).
- **2 servidores MCP**: `memory-mcp` (memoria queryable) + `fs-guard-mcp` (enforcement de matriz por-agente, ahora con soporte CSV para manifests).
- **3 template packs**: `web-typescript`, `python-api`, `go-service` (todos con `PROJECT_MANIFEST_PATHS`).
- **Ejemplo completo** en `examples/golden-path/` (gestor de tareas personal, bootstrappeado).
- **CI Boilerplate Health**: workflow con 13 checks que vigila el propio framework.

---

## Auditorías (cronología)

| Versión | Fecha | Nota | Foco |
|---|---|---|---|
| [v0.4](AUDITORIA_V0.4.md) | 2026-04-15 | 7.8 | Audit teórico post-docs, antes del primer uso real |
| [v0.5](AUDITORIA_V0.5.md) | 2026-04-15 | 8.5 | Primer uso real — bootstrap completo con LLM en vivo |
| [v0.6](AUDITORIA_V0.6.md) | 2026-04-15 | 8.7 | Ciclo de desarrollo end-to-end con iteración reviewer↔developer |
| v0.7 (pre) | 2026-04-15 | **≈9.0** estimada | P1 aplicados: 8 fixes estructurales (ver abajo). Pendiente validación empírica. |

---

## P1 ya aplicados en v0.7-pre (commit `5c5f98a`)

1. **Numeración de sesión pineada** (S0 plantilla → S1 primera real → +1 estricto).
2. **Patrón "opciones A/B/C con trade-offs"** codificado como convención en `memory-bank/SKILL.md`.
3. **Decisiones tácticas durante implementación** como artefacto de workflow (developer anota, context-manager promueve).
4. **Matriz ampliada con `PROJECT_MANIFEST_PATHS`** + filas en `MATRIZ_PERMISOS.md` + parser CSV en `fs-guard-server`.
5. **Gate DoD de dos pasos** (pre-escritura + post-escritura) en `feature-developer` y replicado en `code-reviewer`.
6. **Lint writes↔tools** en `sync-agents.py` (fail fast con exit 3).
7. **Regla "archivos generados por toolchain nunca a mano"** en las 3 `backend.instructions.md`.
8. **Opción 2 de Claude Code documentada** en `CLAUDE_CODE.md`.

Verificación: 13/13 checks del CI Health en verde. 20/20 casos del smoke fs-guard-mcp pasan.

---

## Qué queda pendiente (v0.7-alpha y más allá)

### P2 estratégico (alto valor, cambio grande)

- **Integrar `memory-mcp` en los 4 agentes del ciclo** (`feature-analyst`, `feature-developer`, `code-reviewer`, `context-manager`). Requiere:
  - Modificar prompts para que usen tools MCP (`get_decision("Testing")`) en vez de leer archivos enteros.
  - Medir tokens antes/después con feature real.
  - Validar que no rompe flujo agéntico.
- **Retorno estimado:** reducción 30-50% de tokens por feature (hoy ~115k recurrente). Probablemente la mejora con mayor ROI pendiente.

### P3 — pendiente de más evidencia empírica

- Nivel de detalle del plan del analyst (tensión ceremonia vs improvisación).
- Fusión de 3 agentes de bootstrap en 1 con modos (registrado desde v0.4, sin cerrar).
- Template packs: evaluar valor real dado que `@architect` ya decide stack.

### Preguntas para la próxima auditoría empírica (v0.7)

Cuando se implemente una segunda feature real (tras v0.7-alpha memory-mcp):

- ¿Patrones observados en E01 (iteración 71% más barata, reviewer útil, ~115k tokens/feature) son estables?
- ¿Developer sigue introduciendo decisiones tácticas no anotadas tras aplicar P1 #3?
- ¿CONTEXTO se mantiene compacto (<80 líneas) tras 5+ sesiones?
- ¿Memory-mcp integrado cumple la reducción estimada del 30-50%?

---

## Comandos para verificar salud en cualquier máquina

Después de clonar:

```bash
# 1. Generar .claude/ y .github/ desde ai-specs/
python scripts/sync-agents.py

# 2. Validar memoria base
bash scripts/validar-contexto.sh
bash scripts/validar-decisiones.sh

# 3. Validar golden-path
bash scripts/validar-contexto.sh examples/golden-path/docs/sesion/CONTEXTO.md
bash scripts/validar-decisiones.sh examples/golden-path/docs/sesion/DECISIONES.md

# 4. Smoke tests MCP (no requiere `pip install mcp`)
python scripts/mcp/memory-server/server.py --test
python scripts/mcp/fs-guard-server/server.py --test

# 5. Templates disponibles
python scripts/init-project.py --list-templates
```

Si alguno falla, **no está en mantenimiento** — arreglarlo es P0 antes de cualquier otra cosa.

---

## Contrato de este documento

- **Se actualiza** tras cada auditoría menor o mayor, y tras cada tanda de P1 aplicados.
- **Es autosuficiente**: un humano o agente que lee esto sin más contexto puede retomar.
- **Apunta a detalle, no lo duplica**: cada sección enlaza a la fuente canónica.
- **Prioridad de actualización**: este documento > cualquier otra vía de comunicación de estado.

Si algo cambia sustancialmente y este archivo queda desfasado, **actualízalo antes de cerrar la sesión**. Es el tendedero del proyecto.
