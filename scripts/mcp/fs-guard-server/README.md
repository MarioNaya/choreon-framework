# fs-guard-mcp

Servidor MCP que aplica `docs/guias/MATRIZ_PERMISOS.md` como **enforcement real**, no por convención. Cada instancia corre con la identidad de **un agente** y sus lecturas/escrituras quedan acotadas a lo que la matriz permita para ese agente.

## Herramientas expuestas

| Tool | Descripción |
|---|---|
| `read_file(path)` | Lee si el agente tiene `R` o `W`; error con razón legible si no |
| `write_file(path, content)` | Escribe si el agente tiene `W`; error si no |
| `list_allowed_paths()` | Introspección: devuelve los patrones W/R/- del agente |

## Instalación

```bash
pip install -r scripts/mcp/fs-guard-server/requirements.txt
```

Requiere Python 3.10+.

## Smoke test (sin MCP)

```bash
python scripts/mcp/fs-guard-server/server.py --test
```

Verifica que:
- La matriz se parsea y expone los 9 agentes canónicos.
- 17 decisiones clave coinciden con el comportamiento esperado (ej. `feature-developer` **no** escribe en `DOMINIO.md`; `context-manager` escribe backups de CONTEXTO y DECISIONES).
- Rutas con placeholders `[[...]]` sin resolver quedan denegadas por defecto.

## One-shot check (depuración)

```bash
# ¿Puede feature-developer escribir en DOMINIO.md?
python scripts/mcp/fs-guard-server/server.py --agent feature-developer \
    --check docs/referencia/DOMINIO.md --op write
# → ✗ write denegado: ninguna regla da W ... (exit 1)

python scripts/mcp/fs-guard-server/server.py --agent feature-developer \
    --check docs/referencia/DOMINIO.md --op read
# → ✓ read permitido ... (exit 0)
```

## Registro en Claude Code (por-agente)

El servidor tiene **identidad única por instancia**: arranca con `--agent NAME`. Registra una entrada de `mcpServers` distinta por cada agente que quieras proteger:

```json
{
  "mcpServers": {
    "fs-guard-feature-developer": {
      "command": "python",
      "args": [
        "scripts/mcp/fs-guard-server/server.py",
        "--agent", "feature-developer"
      ]
    },
    "fs-guard-context-manager": {
      "command": "python",
      "args": [
        "scripts/mcp/fs-guard-server/server.py",
        "--agent", "context-manager"
      ]
    }
  }
}
```

Al invocar a `@feature-developer`, configura Claude Code para usar solo `fs-guard-feature-developer`. El servidor rechaza cualquier `write_file` que la matriz no permita para ese agente, incluso si el prompt del agente "pide" escribir fuera.

## Comportamiento con placeholders

`MATRIZ_PERMISOS.md` contiene entradas como `[[PROJECT_SRC_GLOB]]` y `[[PROJECT_TEST_GLOB]]` que se resuelven al ejecutar `scripts/init-project.sh`. Hasta que se resuelvan:

- Cualquier ruta que solo matchease uno de esos patrones queda **denegada por defecto** (seguridad antes que conveniencia).
- El servidor seguirá reconociendo los patrones exactos del repo (`docs/**`, `specs/**`, etc.) porque esos no tienen placeholders.

Tras `init-project.sh`, las reglas del código de producción y de tests quedan operativas.

## Casos límite protegidos

| Caso | Resultado |
|---|---|
| Path absoluto fuera del proyecto | Rechazado (`Path fuera del proyecto`) |
| Path con `..` (traversal) | Rechazado (`Path con traversal no permitido`) |
| Agente desconocido | Rechazado con lista de agentes válidos |
| Agente conocido pero sin regla que matchease | Denegado por defecto |

## Combinación con `memory-mcp`

Los dos servidores son complementarios:

- `memory-mcp` devuelve **contenido** parcial de CONTEXTO/DECISIONES (baja de tokens).
- `fs-guard-mcp` controla **a qué archivos** puede acceder un agente (safety).

Puedes registrar ambos simultáneamente. Ver `.claude/mcp.json.example`.

## Limitaciones actuales

- Una instancia = un agente. No hay modo "multi-tenant"; es intencional para mantener la identidad clara.
- Las **notas** de la matriz (`(append)`, `(seed)`, `(§Diagnóstico)`) se detectan y exponen en `list_allowed_paths()`, pero **no se aplican como restricción adicional**. Un agente con `W (append)` técnicamente puede sobrescribir el archivo — el contrato se mantiene por convención del propio agente.
- No hay log de auditoría local. Si se quiere, puede envolverse con un wrapper que loguee a stderr.
