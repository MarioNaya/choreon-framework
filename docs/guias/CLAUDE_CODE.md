# Guía — Claude Code

Setup, operativa y troubleshooting del boilerplate cuando la herramienta principal es **Claude Code** (CLI de Anthropic).

Términos: ver [`GLOSARIO_SISTEMA.md`](GLOSARIO_SISTEMA.md).
Modelo mental general: ver [`ONBOARDING.md`](ONBOARDING.md).
Ejemplo completo paso a paso: ver [`WALKTHROUGH.md`](WALKTHROUGH.md).

---

## 1. Prerequisitos

- **Claude Code instalado** y operativo. Verifica con:

  ```bash
  claude --version
  ```

  Si no está instalado: `npm install -g @anthropic-ai/claude-code` (o el método que recomiende la documentación oficial en tu momento).

- **Cuenta Anthropic** con acceso a la API y sesión iniciada en Claude Code.

- **Python 3.10+** en el PATH (necesario para los scripts del boilerplate, no para Claude Code en sí).

- **Opcional pero recomendado:** configurar Claude Code para que pida confirmación antes de escribir archivos. Es el comportamiento por defecto y te da visibilidad de qué hace cada agente.

---

## 2. Cómo Claude Code "descubre" los agentes del boilerplate

Claude Code lee varios archivos al abrirse en un directorio:

| Archivo | Qué contiene |
|---|---|
| `CLAUDE.md` raíz | Instrucciones globales del proyecto (autogenerado por `sync-agents.py`) |
| `.claude/agents/*.md` | Definición de cada subagente |
| `.claude/commands/*.md` | Slash-commands disponibles |
| `.claude/skills/*/SKILL.md` | Skills activables |
| `.claude/mcp.json` (opcional) | Servidores MCP registrados |

Si alguno de estos archivos falta o está mal formado, el agente correspondiente simplemente no aparece. **Siempre regenera con `bash scripts/sync-agents.sh` tras editar algo en `ai-specs/`**.

### Verificación tras clonar

1. Entra al repo:

   ```bash
   cd mi-proyecto
   ```

2. Ejecuta el sync por primera vez:

   ```bash
   bash scripts/sync-agents.sh
   ```

   Deberías ver ~47 archivos generados y el mensaje `✓ Sync v0.2 completado`.

3. Verifica que `CLAUDE.md` raíz existe y lista los 9 subagentes:

   ```bash
   grep -c "^- \*\*\`@" CLAUDE.md
   # → 9
   ```

4. Abre Claude Code:

   ```bash
   claude
   ```

   Prueba a invocar un subagente:

   ```
   @spec-analyst ¿cuál es tu propósito?
   ```

   Debería responder con el rol definido en `ai-specs/agents/spec-analyst.md` (no con una respuesta genérica de Claude).

---

## 3. Primera sesión: de cero a bootstrap en 5 pasos

```bash
# 1. Inicializar placeholders (template pack si tu stack coincide)
bash scripts/init-project.sh --template=web-typescript
# → pide nombre del proyecto + descripción
# → resuelve ~20 placeholders técnicos del stack

# 2. Regenerar .claude/ y .github/ por si init-project tocó algo
bash scripts/sync-agents.sh

# 3. Escribir el brief
$EDITOR specs/brief.md
# → describe tu idea en formato libre, una página basta

# 4. Abrir Claude Code
claude

# 5. Disparar el bootstrap
/bootstrap
```

A partir de aquí el flujo es conversacional. Ver [`WALKTHROUGH.md`](WALKTHROUGH.md) para una narración completa.

### Desbloquear el flujo tras el primer prompt de confirmación

Claude Code, por defecto, pide confirmación interactiva la primera vez que un agente intenta escribir un archivo:

```
Do you want to create spec-cerrada-xyz.md?
  1. Yes
❯ 2. Yes, allow all edits during this session  (shift+tab)
  3. No
```

**Recomendación práctica:** elige **opción 2 ("allow all edits during this session")** en el primer prompt del bootstrap. Razones:

- El bootstrap escribe **7 artefactos** en las 4 fases; confirmar cada uno interrumpe el flow y fricciona la conversación.
- Los agentes respetan `MATRIZ_PERMISOS.md` (con `fs-guard-mcp` activado, de forma ejecutable); no pueden escribir fuera de ámbito aunque les autorices "todo".
- La sesión termina cuando cierras Claude Code; la autorización no persiste.

Si prefieres máxima cautela, opción 1 en cada prompt — el bootstrap sigue funcionando, solo es más verboso. Lo que **no** recomiendo es quedarse a la mitad por fatiga de prompts y perder contexto.

Observado empíricamente en la primera ejecución real del framework: los prompts repetidos fricciona hasta el punto de distraer del contenido real de las fases. Opción 2 al inicio es la elección pragmática.

---

## 4. Registrar los servidores MCP

El boilerplate incluye dos servidores MCP locales que **multiplican el valor del sistema**:

- [`memory-mcp`](GLOSARIO_SISTEMA.md#memory-mcp) — expone CONTEXTO y DECISIONES como herramientas queryables. Reduce token load (un agente pide solo la categoría que necesita).
- [`fs-guard-mcp`](GLOSARIO_SISTEMA.md#fs-guard-mcp) — enforcement real de la matriz de permisos. Cada instancia corre con identidad de un agente.

### Paso a paso

1. Instalar dependencias (una vez, globalmente o en venv):

   ```bash
   pip install -r scripts/mcp/memory-server/requirements.txt
   pip install -r scripts/mcp/fs-guard-server/requirements.txt
   ```

2. Copiar la plantilla de configuración:

   ```bash
   cp .claude/mcp.json.example .claude/mcp.json
   ```

3. Editar `.claude/mcp.json` si quieres más de un agente protegido por `fs-guard`. El ejemplo trae `feature-developer` y `context-manager` — puedes añadir entradas análogas para cualquier otro agente.

4. Verificar que los servidores arrancan sin errores (fuera de Claude Code):

   ```bash
   python scripts/mcp/memory-server/server.py --test
   # → ✓ Parse CONTEXTO: ...
   # → ✓ 8 categorías canónicas presentes
   # → ✓ tool_get_decision acepta nombre y número

   python scripts/mcp/fs-guard-server/server.py --test
   # → ✓ Matriz parseada: 9 agentes, 171 reglas
   # → ✓ 17 casos de prueba pasaron
   ```

5. Reiniciar Claude Code. Al abrir, deberías ver los servidores conectados y las herramientas disponibles con prefijo `memory:` y `fs-guard-*:`.

### Usar los servidores desde un agente

Ejemplo: dentro de una sesión con `@feature-analyst`, en lugar de pedir que lea todo `DECISIONES.md`, pídele:

```
Consulta memory:get_decision con category="Testing" y dime qué comando corre los tests unit.
```

El agente llama la tool directamente, recibe los 6 bullets de testing (no las 80 líneas completas), y responde.

---

## 5. Ejemplo de sesión corta

```
$ claude
Claude Code — /clear o /exit para salir.

> /nueva-sesion

@context-manager:
Sesión S1 — 2026-04-14

**Estado:** proyecto recién inicializado; 0 módulos, 0 tests.
**Bloqueantes activos:** ninguno.
**Próxima tarea:** implementar `captura-rapida` (S01).
**Convenciones activas relevantes:**
- Result<T, DomainError> en Domain (DECISIONES §4).
- Parser NL en Domain, no en Api (DECISIONES §3).
- Cobertura mínima 80% (DECISIONES §5).

Handoff recomendado: `/analizar-funcionalidad` + `@feature-analyst`.

> /analizar-funcionalidad captura-rapida con parser de fechas en lenguaje natural

@feature-analyst:
## Plan: captura-rapida (S01)

- Alcance: crear tarea con título + fecha opcional parseada de texto libre.
- Matriz de impacto:
  | Capa | Archivo | Cambio |
  |---|---|---|
  | Domain | src/domain/task/parser.ts | Nuevo |
  | Application | src/application/task/CrearTarea.ts | Nuevo |
  | Api | src/api/tasks/post.ts | Nuevo |
  | Web | src/web/components/TaskQuickAdd.tsx | Nuevo |

- Criterios de aceptación:
  1. POST /api/tasks con {title: "Llamar al dentista jueves"}
     crea tarea con due_at = próximo jueves 09:00 local.
  2. POST con title vacío → 400.
  3. Título sin fecha → crea tarea con due_at = null.
  4. Parser devuelve {title, dueAt?} con ≥85% precisión en fixture de 50 frases.
  5. Componente TaskQuickAdd focaliza input al montar y envía con Enter.

- Pruebas recomendadas:
  - Unit: parser contra fixture (tests/fixtures/nl-dates.json).
  - Integración: POST end-to-end con SQLite tmp.
  - E2E: abrir PWA → teclear → Enter → ver tarea en lista.

- Reutilización detectada: ninguna (primera feature).
- Riesgos: timezone del cliente vs servidor. Resolver en Domain con Intl.

- Handoff: @feature-developer.
```

Mario continúa con `/implementar-feature`, `/revisar-codigo`, y al final `/actualizar-contexto`.

---

## 6. Fricciones típicas con Claude Code

### "Escribí `@spec-analyst` y Claude responde como Claude genérico"

Causas posibles:

1. **No se generó `.claude/agents/`.** Ejecuta `bash scripts/sync-agents.sh` y verifica que existe `.claude/agents/spec-analyst.md`.
2. **Claude Code tiene caché antigua.** Cierra y vuelve a abrir Claude Code en el repo.
3. **Versión de Claude Code sin soporte de subagentes.** Actualiza con `npm update -g @anthropic-ai/claude-code`.

### "Los servidores MCP no aparecen"

1. **`.claude/mcp.json` falta.** Copia desde `.claude/mcp.json.example`.
2. **Python no está en el PATH de Claude Code.** En Windows, especifica la ruta absoluta en `mcp.json`:

   ```json
   "command": "C:/Users/mario/AppData/Local/Programs/Python/Python312/python.exe"
   ```

3. **Instalación de `mcp` falta.** `pip install -r scripts/mcp/memory-server/requirements.txt`.

### "Al hacer `/bootstrap`, el agente dice 'brief.md vacío'"

El brief tiene solo placeholders `[[...]]` o está literalmente en blanco. Edítalo con contenido real (ver [`examples/golden-path/specs/brief.md`](../../examples/golden-path/specs/brief.md) como referencia).

### "CLAUDE.md no se carga"

Verifica que existe en la raíz. Si no, ejecuta `bash scripts/sync-agents.sh`. Si existe pero Claude Code lo ignora, comprueba que arrancas Claude **desde la raíz del repo**, no desde un subdirectorio.

### "Un agente dice que no puede escribir un archivo"

Esto es **correcto** — el agente está respetando la matriz de permisos. Si crees que la matriz está mal, edita `docs/guias/MATRIZ_PERMISOS.md` y regenera (no requiere sync, la matriz se lee directamente). Si estás usando `fs-guard-mcp`, el servidor también aplicará las nuevas reglas en el siguiente arranque.

### "Cambié algo en `ai-specs/` pero no veo el cambio en Claude Code"

Siempre tras editar `ai-specs/`:

```bash
bash scripts/sync-agents.sh
```

Y reinicia Claude Code si ya estaba abierto.

### "Windows bloquea un script con permisos"

Los `.sh` son wrappers; puedes llamar al `.py` directamente:

```bash
python scripts/sync-agents.py
python scripts/init-project.py --template=web-typescript
```

### "El pre-commit hook no se activa"

Una sola vez por clon:

```bash
git config core.hooksPath .githooks
```

---

## 7. Diferencias con Copilot en la práctica

| Aspecto | Claude Code | Copilot Chat |
|---|---|---|
| Subagentes nativos | Sí, vía `.claude/agents/` | No; `@agente` es un "rol" simulado por convención |
| Slash-commands nativos | Sí, `.claude/commands/` | Sí, `.github/prompts/*.prompt.md` |
| Skills activables | Sí | Soporte parcial, vía `.github/skills/` |
| MCP | Soporte directo | Soporte limitado, depende de versión |
| Instrucciones por archivo | `CLAUDE.md` global + contexto explícito | `.github/instructions/*.md` con `applyTo` automático |
| Modelos seleccionables | Por agente (`model: opus` vs `sonnet`) | No — usa el modelo del plan de suscripción |

Conclusión práctica: con Claude Code **el sistema funciona tal cual lo diseñamos**. Con Copilot, funciona, pero los agentes son "convenciones" y los skills tienen menos presencia.

---

## 8. Cosas que no van a funcionar (aún)

- **Handoffs automáticos entre agentes.** Cada transición la escribes tú manualmente siguiendo la sugerencia.
- **Validación automática del Gate DoD.** El agente `feature-developer` la aplica porque está en su prompt, pero no hay un sistema externo que la enforce si el agente decide ignorarla (Claude sigue las instrucciones, pero es IA no infalible).
- **Sincronización entre sesiones simultáneas.** Si tú y otra persona editáis `CONTEXTO.md` al mismo tiempo en ramas distintas, el merge requiere intervención manual. No hay lock ni CRDT.
