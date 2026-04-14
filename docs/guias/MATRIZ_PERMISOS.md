# Matriz de permisos agente ↔ archivo

## Por qué existe esta matriz

Un problema común al usar múltiples agentes en un repo es el **solapamiento de escrituras**: dos agentes se disputan el mismo archivo, o un agente toca algo que no debería. Para prevenirlo, este boilerplate declara **explícitamente** qué puede escribir cada agente.

La matriz es:

- **Una especificación** que los agentes canónicos (`ai-specs/agents/*.md`) referencian en sus reglas absolutas.
- **Una documentación** que facilita razonar sobre el sistema.
- **Opcionalmente, un contrato ejecutable** si usas el servidor MCP [`fs-guard-mcp`](GLOSARIO_SISTEMA.md#fs-guard-mcp), que rechaza lecturas/escrituras fuera de la matriz.

## Dos niveles de enforcement

### Nivel 1 — convención

Por defecto, los permisos se cumplen **por convención**: el prompt de cada agente dice explícitamente "solo escribo en X, nunca en Y". Claude o Copilot siguen esas instrucciones porque son IA entrenada para seguir el sistema.

Este nivel **depende del agente**. Un agente bien diseñado respeta la matriz; un agente distraído o un modelo con poca capacidad podrían equivocarse.

### Nivel 2 — ejecutable (fs-guard-mcp)

Cuando registras [`fs-guard-mcp`](../../scripts/mcp/fs-guard-server/README.md) en Claude Code, cada agente tiene una instancia del servidor con su identidad. El servidor **rechaza** cualquier `read_file` o `write_file` que la matriz no permita. Un intento de `@feature-developer` escribiendo `DOMINIO.md` devuelve error en lugar de ejecutarse.

Este nivel es el que querrás en producción o en equipos donde la disciplina no se puede asumir.

## Cómo interpretar la tabla

### Leyenda

- **W** = puede escribir (crear, modificar, sobrescribir).
- **R** = solo lectura.
- **—** = sin acceso.

### Notas entre paréntesis

Algunas celdas llevan anotaciones como `W (append)`, `W (seed)`, `W (§Diagnóstico)`. Son **metadatos para humanos y parsers**: describen el modo correcto de escritura. **`fs-guard-mcp` NO las aplica como restricción adicional** — un agente con `W (append)` técnicamente puede sobrescribir el archivo. La disciplina queda en el agente.

Significados habituales:

| Nota | Significado |
|---|---|
| `W (append)` | Solo añadir al final; no modificar entradas existentes |
| `W (seed)` | Solo para escritura inicial durante bootstrap |
| `W (§Sección)` | Solo en una sección específica del archivo |
| `W (completo)` | Puede sobrescribir el archivo completo |

### Placeholders `[[...]]` sin resolver

Patrones como `[[PROJECT_SRC_GLOB]]` y `[[PROJECT_TEST_GLOB]]` son placeholders que resuelve `scripts/init-project.sh` cuando inicializas un proyecto concreto.

Mientras no se resuelvan:

- En enforcement por convención, el agente no sabe qué interpretar y típicamente se comporta prudente.
- En enforcement con `fs-guard-mcp`, cualquier ruta que solo matchearía el patrón placeholder queda **denegada por defecto** (seguridad antes que conveniencia). Ejecuta `bash scripts/init-project.sh --template=TU_STACK` o el modo interactivo para resolverlos.

## Cómo añadir un agente nuevo a la matriz

1. Define el agente en `ai-specs/agents/nuevo-agente.md` con su YAML canónico (nombre, descripción, modelo, tools, writes, handoffs).

2. Añade una **columna** al final de la tabla en este archivo con el nombre exacto del agente (sin `@`). Rellena todas las filas:

   - Usa `W` solo donde el agente vaya a escribir.
   - Usa `R` en lo que deba poder leer.
   - Usa `—` para todo lo demás (denegación explícita).

3. Re-ejecuta el sync:

   ```bash
   bash scripts/sync-agents.sh
   ```

4. Si usas `fs-guard-mcp`, añade una entrada en `.claude/mcp.json`:

   ```json
   "fs-guard-nuevo-agente": {
     "command": "python",
     "args": ["scripts/mcp/fs-guard-server/server.py", "--agent", "nuevo-agente"]
   }
   ```

5. Verifica:

   ```bash
   python scripts/mcp/fs-guard-server/server.py --test
   # Debe seguir verde (171 → 190 reglas si añadiste una columna)
   ```

## Cómo añadir una fila (ruta nueva)

Cuando el proyecto crece y aparece una nueva ruta o familia de archivos que requiere permisos explícitos:

1. Añade una **fila** a la tabla con el glob o ruta exacta en la primera columna (entre backticks para distinguirla de conceptos abstractos).

   - Rutas concretas: `` `docs/sesion/NUEVO.md` ``
   - Globs: `` `tests/e2e/*.spec.ts` ``
   - Directorios: `` `docs/nuevo-dir/` `` (el trailing slash indica que aplica a cualquier archivo bajo él)

2. Rellena **todas las columnas** (los 9 agentes). No dejes celdas vacías — una celda vacía se lee como `—` (sin acceso) pero por claridad pon `—` explícito.

3. Valida:

   ```bash
   python scripts/mcp/fs-guard-server/server.py --test
   ```

## Casos abstractos

La fila "Repos vecinos read-only" y similares son **abstracciones textuales**, no rutas glob. `fs-guard-mcp` las ignora (marcadas como `is_abstract=True` en el parser). Su valor es **documental**: comunican al humano qué espera el sistema.

Si quieres enforcement real de "context-reader puede leer `../lib-otro-repo/` pero nadie más", añade una fila con un path absoluto concreto (ej: `/workspace/lib-otro-repo/`) en lugar del texto abstracto. El parser lo reconocerá.

---

## Matriz

| Archivo / Ruta | spec-analyst | domain-modeler | architect | feature-analyst | feature-developer | code-reviewer | context-reader | context-manager | ci-triage |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `specs/brief.md` | R | R | R | R | R | R | R | R | R |
| `specs/spec-cerrada-*.md` | **W** | R | R | R | R | R | R | R | R |
| `specs/historico/` | — | — | — | — | — | — | — | R | — |
| `docs/referencia/DOMINIO.md` | R | **W** | R | R | R | R | R | R | R |
| `docs/referencia/GLOSARIO.md` | R | **W** | R | R | R | R | R | R | R |
| `docs/referencia/ARQUITECTURA.md` | R | R | **W** | R | R | R | R | R | R |
| `docs/referencia/CATALOGO.md` | R | R | **W** | R | R | R | R | R | R |
| `docs/referencia/COBERTURA.md` | — | — | — | R | R | **W** | R | R | R |
| `docs/planificacion/ROADMAP.md` | R | R | R | R | R | R | R | R | R |
| `docs/sesion/CONTEXTO.md` | R | R | R | R | R | R | R | **W** | R |
| `docs/sesion/CONTEXTO.bak.md` | — | — | — | — | — | — | — | **W** | — |
| `docs/sesion/DECISIONES.md` | R | R | **W** (seed) | R | R | R | R | **W** | R |
| `docs/sesion/DECISIONES.bak.md` | — | — | — | — | — | — | — | **W** | — |
| `docs/sesion/TRIAGE_CI.md` | — | — | — | R | R | R | **W** (§Diagnóstico) | R | **W** (completo) |
| `docs/archivo/DECISIONES_HISTORICO.md` | — | — | — | — | — | — | — | **W** (append) | — |
| `[[PROJECT_SRC_GLOB]]` (código producción) | — | — | — | R | **W** | R | R | — | R |
| `[[PROJECT_TEST_GLOB]]` | — | — | — | R | **W** | R | R | — | R |
| Repos vecinos read-only | — | — | — | — | — | — | R | — | — |
| `.github/`, `.claude/`, `ai-specs/` (config agéntica) | — | — | — | — | — | — | R | — | — |

## Reglas derivadas de la tabla

1. **Un agente nunca escribe fuera de su fila W.** Si lo intenta, error (con `fs-guard-mcp`) o violación de contrato (sin `fs-guard-mcp`).
2. **`context-reader` es el único con lectura autorizada de repos vecinos.** Todos los demás leen solo el proyecto.
3. **`context-manager` es el único con escritura a archivos volátiles de sesión.**
4. **`architect` puede seedear DECISIONES (fase 3 bootstrap), pero tras eso las edita `context-manager` in-place.**
5. **`ci-triage` sobrescribe `TRIAGE_CI.md` completo; `context-reader` solo añade §Diagnóstico al final.**
6. **Nadie escribe en `.github/`, `.claude/` o `ai-specs/` desde el flujo normal.** Esos directorios son configuración del sistema; se editan por `scripts/sync-agents.sh` o a mano en modo mantenimiento.

---

## Verificación

Para comprobar que un caso concreto funciona como esperas, sin lanzar el servidor entero:

```bash
python scripts/mcp/fs-guard-server/server.py \
    --agent feature-developer \
    --check docs/referencia/DOMINIO.md --op write
# → ✗ write denegado: ninguna regla da W ...

python scripts/mcp/fs-guard-server/server.py \
    --agent feature-developer \
    --check docs/referencia/DOMINIO.md --op read
# → ✓ read permitido por regla 'docs/referencia/DOMINIO.md'
```

Para correr los 17 casos canónicos de golden:

```bash
python scripts/mcp/fs-guard-server/server.py --test
```

Si añades filas o columnas y el smoke test falla, revisa los casos en `scripts/mcp/fs-guard-server/server.py` y actualízalos si la nueva regla los contradice legítimamente.
