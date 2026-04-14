# Guía — GitHub Copilot

Setup, operativa y troubleshooting del boilerplate cuando la herramienta principal es **GitHub Copilot Chat** en VS Code.

Términos: ver [`GLOSARIO_SISTEMA.md`](GLOSARIO_SISTEMA.md).
Modelo mental general: ver [`ONBOARDING.md`](ONBOARDING.md).
Ejemplo completo paso a paso (narrado para Claude Code pero equivalente en Copilot): ver [`WALKTHROUGH.md`](WALKTHROUGH.md).

---

## 1. Prerequisitos

- **VS Code** versión reciente (≥1.90 recomendado).
- **Extensión oficial de GitHub Copilot Chat** instalada y activada.
- **Suscripción a Copilot** (Individual, Business o Enterprise) con la extensión autenticada.
- **Python 3.10+** en el PATH (para scripts del boilerplate).

---

## 2. Cómo Copilot "descubre" los agentes y prompts

Copilot Chat lee varios archivos del repo al abrirlo en VS Code:

| Archivo | Qué contiene |
|---|---|
| `.github/copilot-instructions.md` | Instrucciones globales del proyecto |
| `.github/agents/*.agent.md` | Definición de cada agente (convención visible para Copilot como contexto) |
| `.github/prompts/*.prompt.md` | Slash-commands disponibles |
| `.github/skills/*/SKILL.md` | Skills (uso depende de versión) |
| `.github/instructions/*.instructions.md` | Instrucciones por tipo de archivo con `applyTo` |

Estos archivos son **generados** por `scripts/sync-agents.py` a partir del [hub canonical](GLOSARIO_SISTEMA.md#hub-canonical) en `ai-specs/`. Siempre regenera tras editar algo en `ai-specs/`:

```bash
bash scripts/sync-agents.sh
```

### Verificación tras clonar

1. Entra al repo:

   ```bash
   cd mi-proyecto
   ```

2. Ejecuta el sync:

   ```bash
   bash scripts/sync-agents.sh
   ```

3. Abre VS Code en la raíz:

   ```bash
   code .
   ```

4. Abre Copilot Chat (`Ctrl+Alt+I` o el icono del chat). Teclea:

   ```
   Lee .github/copilot-instructions.md y dime qué rol tiene el agente @spec-analyst según las definiciones en .github/agents/
   ```

   Copilot debería resumir el agente correctamente. Si responde con algo genérico o dice que no encuentra archivos, revisa que `.github/agents/` existe y tiene 9 archivos `.agent.md`.

---

## 3. Primera sesión: de cero a bootstrap

```bash
# 1. Inicializar placeholders (template pack si aplica)
bash scripts/init-project.sh --template=web-typescript

# 2. Regenerar el directorio .github
bash scripts/sync-agents.sh

# 3. Escribir el brief
code specs/brief.md   # o el editor que prefieras

# 4. Abrir VS Code + Copilot Chat
code .
# Ctrl+Alt+I para abrir el chat

# 5. En el chat, disparar el bootstrap
/bootstrap
```

A partir de ahí es conversacional. Ver [`WALKTHROUGH.md`](WALKTHROUGH.md) para narración completa.

---

## 4. Invocación de agentes y prompts en Copilot

### Slash-commands

Teclea directamente en el chat:

```
/bootstrap
/nueva-sesion
/analizar-funcionalidad
/implementar-feature
/revisar-codigo
/depurar-fallo
/adaptar-componente
/sincronizar-dominio
/triage-ci
/actualizar-contexto
/import-project
```

VS Code muestra autocomplete con los 11 prompts disponibles mientras tecleas `/`.

### Agentes

Copilot Chat **no tiene subagentes nativos** como Claude Code. En este boilerplate, invocar `@spec-analyst` es una **convención**: le estás diciendo a Copilot "actúa según el rol definido en `.github/agents/spec-analyst.agent.md`". Es el propio Copilot quien lee ese archivo y adopta el rol.

Ejemplo:

```
@spec-analyst Sigue el rol que tienes definido en .github/agents/spec-analyst.agent.md.
Acabo de escribir specs/brief.md; aplica tu workflow.
```

O más breve si ya has "entrenado" al Copilot en la sesión:

```
@spec-analyst procede con el brief
```

En la práctica funciona bien: Copilot respeta el rol mientras el archivo `.agent.md` sea legible y esté en el workspace abierto.

---

## 5. Instrucciones por archivo (`applyTo`)

Las plantillas `backend.instructions.md`, `frontend.instructions.md` y `testing.instructions.md` declaran en su front-matter un `applyTo`:

```yaml
---
applyTo: "src/**/*.ts"
---
```

VS Code + Copilot **aplican estas instrucciones automáticamente** cuando editas archivos que encajan con el glob. Ejemplo: al editar `src/api/tasks.ts`, Copilot sabe las convenciones de backend TypeScript definidas en el pack web-typescript.

### Verificación

1. Abre un archivo que encaje (p.ej. `src/index.ts` si aplicaste el pack web-typescript).
2. Pregunta a Copilot:

   ```
   ¿Cuáles son las convenciones de naming de este proyecto?
   ```

3. Debería citar las reglas de `backend.instructions.md` (camelCase, PascalCase, etc.). Si responde genérico, la instrucción no se está aplicando — revisa el `applyTo` y el glob.

---

## 6. Ejemplo de sesión corta

Con el proyecto ya bootstrappeado:

```
Usuario: /nueva-sesion

Copilot: @context-manager — Sesión S2 (2026-04-15).

Estado: captura-rapida (S01) implementada, 20 tests pasando, cobertura 82%.
Bloqueantes: ninguno.
Próxima tarea: parser NL con fixture de 50 frases (S02).
Convenciones activas:
- Parser NL vive en Domain (DECISIONES §3).
- Fixture en tests/fixtures/nl-dates.json.

Handoff: /analizar-funcionalidad + @feature-analyst.

Usuario: /analizar-funcionalidad parser NL con fixture 50 frases para S02

Copilot: @feature-analyst — Plan:

Matriz de impacto:
- Domain: ampliar src/domain/task/parser.ts
- Tests: tests/unit/parser.test.ts + tests/fixtures/nl-dates.json

Criterios de aceptación:
1. Parser acepta ≥85% de las 50 frases del fixture (S02).
2. Cada frase del fixture tiene input, expected_due_at, expected_title.
3. Test falla si precisión baja del 85%.
4. Frases ambiguas ("en un rato") devuelven {title, dueAt: null}.

Pruebas: unit (parser contra fixture).
Reutilización: src/domain/task/parser.ts base de S01.
Riesgos: zonas horarias — usar Intl.DateTimeFormat.

Handoff: @feature-developer.

Usuario: /implementar-feature

Copilot: @feature-developer — Gate DoD:
1. Criterio verificable? ✓ (test cuenta porcentaje).
2. Prueba automatizable? ✓ (unit test).
3. Respeta ARQUITECTURA? ✓ (parser en Domain).

Escribo fixture y tests. ¿Quieres que incluya casos edge
(título vacío, fecha imposible)?
```

---

## 7. Fricciones típicas con Copilot

### "Invoco `@spec-analyst` pero Copilot responde genérico"

Copilot no reconoce el `@agente` como subagente nativo. Dale contexto explícito la primera vez:

```
@spec-analyst — adopta el rol definido en .github/agents/spec-analyst.agent.md
y aplica tu workflow sobre specs/brief.md
```

En la misma conversación, sucesivas invocaciones de `@spec-analyst` mantendrán el rol.

### "Los slash-commands no aparecen en autocomplete"

1. Verifica que existe `.github/prompts/*.prompt.md`. Si no, ejecuta `bash scripts/sync-agents.sh`.
2. Algunas versiones de Copilot requieren que los archivos estén en `.vscode/prompts/` o una carpeta configurable. Revisa la configuración de Copilot en tu VS Code si es distinta.
3. Cierra y vuelve a abrir VS Code para refrescar.

### "Las instrucciones `applyTo` no se aplican"

- Confirma que el glob coincide con el archivo abierto. Prueba con un glob más amplio temporalmente (`**/*.ts`) para descartar.
- Algunas versiones tempranas de Copilot solo soportan instrucciones globales (`copilot-instructions.md`). Comprueba en la config de Copilot si "Code instructions from files" está habilitado.

### "Copilot propone violar la matriz de permisos"

Copilot **no aplica** la matriz automáticamente; es convención. Si un agente te sugiere escribir en un archivo que no debería tocar, recuérdaselo:

```
@feature-developer — según MATRIZ_PERMISOS.md, tú solo escribes en src/**/*.ts
y tests/**, no en docs/referencia/DOMINIO.md.
```

Si quieres enforcement real, usa `fs-guard-mcp` (requiere que Copilot soporte MCP en tu versión; si no, espera a próxima versión o usa Claude Code para ese flujo).

### "El brief no se aplica"

Asegúrate de que el path que menciona Copilot es correcto. Si VS Code abrió el workspace en una carpeta padre del repo, los paths relativos pueden fallar.

### "Diff muy grande después de un cambio en `ai-specs/`"

Es normal — `sync-agents.sh` regenera `.github/agents/`, `.github/prompts/`, `.github/skills/` y `CLAUDE.md`. Confirma que el diff solo toca archivos generados. Si toca otros (p.ej. `docs/`), investiga antes de commit.

---

## 8. Diferencias con Claude Code en la práctica

Resumen ya incluido en [`CLAUDE_CODE.md §7`](CLAUDE_CODE.md#7-diferencias-con-copilot-en-la-práctica). En corto:

- Copilot no tiene subagentes nativos; es convención.
- `applyTo` de `.github/instructions/` es una ventaja de Copilot — activación automática por tipo de archivo.
- MCP tiene soporte parcial y depende de versión.
- No puedes elegir modelo por agente — lo fija el plan de suscripción.

---

## 9. Buenas prácticas

- **Mantén el workspace abierto en la raíz** para que Copilot vea `.github/` y `CLAUDE.md`.
- **Re-ejecuta `sync-agents.sh` tras editar `ai-specs/`** — si no, Copilot seguirá leyendo la versión anterior.
- **Recuerda los handoffs explícitamente.** Copilot no los ejecuta — eres tú quien escribe `@siguiente-agente`.
- **Cita el archivo canónico al invocar un agente** la primera vez en la sesión. Copilot lo lee una vez y mantiene el rol durante la conversación.
- **Para features grandes, divide en sesiones.** Cada sesión corta es más fiable que un hilo largo donde Copilot "olvida" el rol adoptado.
