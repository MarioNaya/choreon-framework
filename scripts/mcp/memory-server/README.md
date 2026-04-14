# memory-mcp

Servidor MCP local que expone `CONTEXTO.md` y `DECISIONES.md` como herramientas queryables por agentes. Reduce token load: un agente pide solo la categoría que necesita en vez de releer todo.

## Herramientas expuestas

| Tool | Descripción |
|---|---|
| `get_context()` | CONTEXTO completo (sesión, estado, bloqueantes, próxima tarea, convenciones) |
| `get_section(name)` | Una sección del CONTEXTO por nombre |
| `get_decision(category)` | Bullets de una categoría de DECISIONES (por nombre o número 1–8) |
| `get_blockers()` | §Bloqueados |
| `get_next_task()` | §Próxima tarea |
| `record_decision(category, text)` | Añade bullet a una categoría, creando backup `.bak.md` antes |

## Instalación

```bash
# Desde la raíz del proyecto
pip install -r scripts/mcp/memory-server/requirements.txt
```

Requiere Python 3.10+.

## Smoke test (sin cliente MCP)

```bash
python scripts/mcp/memory-server/server.py --test
```

Debería imprimir:

```
✓ Parse CONTEXTO: sesión S?, N secciones
✓ Parse DECISIONES: 8 categorías
✓ Las 8 categorías canónicas presentes
✓ tool_get_next_task devuelve N chars
✓ tool_get_decision acepta nombre y número
```

Este modo **no requiere el paquete `mcp`**; útil para CI y para probar el parser.

## Registro en Claude Code

Crear o editar `.claude/mcp.json` en la raíz del proyecto:

```json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": [
        "scripts/mcp/memory-server/server.py"
      ]
    }
  }
}
```

Al abrir Claude Code en el repo, las herramientas aparecen disponibles con prefijo `memory:`. Ejemplo: `memory:get_decision` con argumento `category=Testing`.

## Registro en otros clientes MCP

El servidor habla stdio/JSON-RPC estándar. Cualquier cliente MCP compatible puede conectarse arrancándolo con `python scripts/mcp/memory-server/server.py` y hablando por stdin/stdout.

## Contrato con `context-manager`

`record_decision` **crea backup** `DECISIONES.bak.md` antes de modificar, replicando el protocolo del agente. Esto asegura que invocar la herramienta desde un agente distinto (`@feature-developer`, por ejemplo) no rompe el contrato de backup dual.

La herramienta **no reformatea** ni compacta DECISIONES — es edición aditiva por categoría. Compactación sigue siendo responsabilidad de `@context-manager` vía `/actualizar-contexto`.

## Limitaciones actuales

- Solo edita DECISIONES. La escritura de CONTEXTO sigue siendo exclusiva del `context-manager` (hace sobrescritura completa de 6 secciones; no casa con el modelo de tool atómica).
- Lee archivos en cada llamada (sin cache). Suficiente para tamaños esperados (<200 líneas por archivo).
- No valida invariantes semánticas del contenido de un bullet (p. ej. que no sea cronológico). Los validadores `scripts/validar-*.sh` siguen siendo la red de seguridad.

## Apagar el servidor

`Ctrl+C` en la terminal si se lanzó manualmente. Si lo arrancó el cliente MCP, se apaga al cerrar el cliente.
