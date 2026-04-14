# Checklist de inicialización

Sigue estos pasos la primera vez que uses el boilerplate en un proyecto nuevo.

> **Antes de empezar**, si el sistema es nuevo para ti lee en orden:
> 1. [`README.md`](README.md) — qué es y qué problema resuelve (3 min).
> 2. [`docs/guias/ONBOARDING.md`](docs/guias/ONBOARDING.md) — modelo mental (10 min).
> 3. [`docs/guias/WALKTHROUGH.md`](docs/guias/WALKTHROUGH.md) — tutorial paso a paso sobre un ejemplo real (20 min).
>
> Si un término te suena raro: [`docs/guias/GLOSARIO_SISTEMA.md`](docs/guias/GLOSARIO_SISTEMA.md).

## 1. Reemplazar placeholders globales

```bash
# Modo básico (interactivo, genérico):
bash scripts/init-project.sh

# O con template pack (recomendado si tu stack es uno de los pre-definidos):
bash scripts/init-project.sh --template=web-typescript
bash scripts/init-project.sh --template=python-api
bash scripts/init-project.sh --template=go-service

# Listar packs disponibles:
bash scripts/init-project.sh --list-templates
```

Reemplaza los placeholders **globales** (`[[NOMBRE_PROYECTO]]`, `[[BACKEND_GLOB]]`, `[[TEST_COMMAND_*]]`, etc.) en todos los archivos. Si usas `--template`, además:
- Aplica resoluciones específicas del stack (comandos de test, versión del runtime, globs).
- Copia `.github/instructions/*.md` pre-rellenadas para ese stack.

Crear tu propio pack: ver `templates/README.md`.

## 2. Generar copias para Claude Code y Copilot

```bash
bash scripts/sync-agents.sh   # wrapper que llama a scripts/sync-agents.py
```

Requiere Python 3 en el PATH. El generador **adapta el front-matter** a cada herramienta:

- `.claude/agents/*.md` — `tools` como string CSV con herramientas nativas de Claude Code (`Read, Grep, Glob, Edit, Write, WebSearch, WebFetch`); campos `writes` y `handoffs` se mueven a secciones markdown en el cuerpo (Claude los lee como texto).
- `.github/agents/*.agent.md` — mantiene el YAML rico (Copilot ignora campos extra).
- `.claude/commands/*.md` y `.github/prompts/*.prompt.md` — prompts espejados.
- `.claude/skills/` y `.github/skills/` — skills espejados.
- `CLAUDE.md` raíz — generado con la lista de subagentes y reglas de oro.

Idempotente: los hashes de los destinos no cambian entre ejecuciones sucesivas. Log en `docs/archivo/sync-log.md`.

Antes de continuar, **lee el ejemplo completo**: `examples/golden-path/README.md` muestra cómo luce el sistema después de un bootstrap real.

## 3. Escribir el brief inicial

Edita `specs/brief.md` con tu idea, user story o PRD resumido. Formato libre. Deja huecos en lo que no sepas: `@spec-analyst` preguntará.

## 4. Disparar bootstrap conversacional

Abre el proyecto con Claude Code (`claude`) o Copilot (VS Code Chat) y ejecuta:

```
/bootstrap
```

El workflow pasará por 3 fases con **checkpoints de confirmación**:

1. **`spec-analyst`** cierra 6 dimensiones (problema, actores, alcance, restricciones, comportamiento, éxito) → produce `specs/spec-cerrada-*.md`.
2. **`domain-modeler`** extrae entidades, ciclo de vida, matriz de capacidades → rellena `DOMINIO.md` y `GLOSARIO.md`.
3. **`architect`** propone stack, patrones, convenciones → rellena `ARQUITECTURA.md`, `CATALOGO.md`, seedea `DECISIONES.md`.
4. **`context-manager`** escribe el primer `CONTEXTO.md` (sesión S1).

## 5. Completar plantillas específicas

Tras `/bootstrap`, algunos archivos siguen con placeholders específicos:

- `.github/instructions/backend.instructions.md`, `frontend.instructions.md`, `testing.instructions.md` — plantillas que puedes completar manualmente o pidiendo a `@architect` una iteración más.
- `.github/workflows/ci-manual.yml`, `ci-nightly.yml` — rellenar `[[RUNNER_GROUP]]`, `[[TEST_COMMAND_*]]`, etc. Ver `docs/guias/CI_GUIDE.md`.

Comprobar placeholders restantes:

```bash
grep -r '\[\[' ai-specs docs .github .claude
```

## 6. Primera sesión de desarrollo

```
/nueva-sesion
```

Te mostrará el estado (recién inicializado), la próxima tarea sugerida por el architect, y las convenciones activas.

Para añadir la primera funcionalidad:

```
/analizar-funcionalidad
```

## 7. Cerrar sesión

Al final de cada sesión:

```
/actualizar-contexto
```

Reescribe `CONTEXTO.md` (≤80 líneas) y actualiza `DECISIONES.md` in-place. Backups automáticos en `CONTEXTO.bak.md` y `DECISIONES.bak.md`.

## Validación en cualquier momento

```bash
bash scripts/validar-contexto.sh
bash scripts/validar-decisiones.sh
```

Comprueban invariantes (≤80 líneas, 8 categorías presentes, sin duplicados, sin cronología).

## Pre-commit hook (opcional, recomendado)

El repo trae `.githooks/pre-commit` que ejecuta los dos validadores automáticamente. Para activarlo una única vez en tu clon:

```bash
git config core.hooksPath .githooks
```

A partir de ahí, cualquier `git commit` bloqueará si `CONTEXTO.md` excede 80 líneas, si faltan categorías de DECISIONES, etc. Desactivación temporal con `git commit --no-verify` (justificar en el mensaje).

## MCP — servidores locales (opcionales)

El boilerplate incluye dos servidores MCP que multiplican el valor del sistema:

### memory-mcp

`scripts/mcp/memory-server/` expone CONTEXTO y DECISIONES como herramientas queryables para que los agentes pidan solo lo que necesitan. **Reduce token load** significativamente.

```bash
pip install -r scripts/mcp/memory-server/requirements.txt
python scripts/mcp/memory-server/server.py --test   # smoke sin MCP
```

Herramientas: `get_context`, `get_section`, `get_decision(category)`, `get_blockers`, `get_next_task`, `record_decision` (con backup automático).

### fs-guard-mcp

`scripts/mcp/fs-guard-server/` convierte `MATRIZ_PERMISOS.md` en **enforcement real**: cada instancia corre con identidad de un agente y rechaza lecturas/escrituras fuera de su ámbito autorizado.

```bash
pip install -r scripts/mcp/fs-guard-server/requirements.txt
python scripts/mcp/fs-guard-server/server.py --test       # smoke sin MCP
python scripts/mcp/fs-guard-server/server.py \
    --agent feature-developer \
    --check docs/referencia/DOMINIO.md --op write          # one-shot
```

Herramientas: `read_file(path)`, `write_file(path, content)`, `list_allowed_paths()`.

**Registro en Claude Code:** copia `.claude/mcp.json.example` a `.claude/mcp.json`. El ejemplo incluye los dos servidores combinados y entradas por-agente para fs-guard.

Ver `scripts/mcp/memory-server/README.md` y `scripts/mcp/fs-guard-server/README.md` para detalles.

## Si algo va mal

- **`CONTEXTO.md` corrupto** → restaurar desde `CONTEXTO.bak.md`.
- **`DECISIONES.md` corrupto** → restaurar desde `DECISIONES.bak.md`; ejecutar `validar-decisiones.sh`.
- **Bootstrap interrumpido** → ejecutar `/bootstrap --resume`.
- **Ya hay contenido en DOMINIO/ARQUITECTURA** y quieres rearrancar → borrar a mano los archivos o ejecutar `/bootstrap --resume`.
