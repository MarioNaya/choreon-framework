# Glosario del sistema

Términos que aparecen en la documentación del boilerplate. **Una definición canónica** por término; el resto de documentos enlazan aquí en vez de redefinir.

Ordenado alfabéticamente (con anclas para enlace directo).

---

## Agente

<a id="agente"></a>

Un **rol especializado** ejecutado por un modelo de IA (Claude o Copilot) con instrucciones propias, modelo asignado y permisos de escritura acotados. No es un proceso de software: es un prompt estructurado con identidad.

En este boilerplate hay **9 agentes**: 3 de inicialización (`spec-analyst`, `domain-modeler`, `architect`), 3 de desarrollo (`feature-analyst`, `feature-developer`, `code-reviewer`), y 3 de apoyo (`context-reader`, `context-manager`, `ci-triage`).

Definición canónica de cada agente: `ai-specs/agents/*.md`. Copias adaptadas a cada herramienta: `.claude/agents/*.md` y `.github/agents/*.agent.md` (generadas por [sync-agents.py](#hub-canonical)).

Un agente se invoca con `@nombre-del-agente` en el chat.

## Backup dual

<a id="backup-dual"></a>

Protocolo del [`context-manager`](#agente): antes de modificar `CONTEXTO.md` o `DECISIONES.md`, crea (o sobrescribe) los respaldos `CONTEXTO.bak.md` y `DECISIONES.bak.md`. Permite rollback manual si la escritura corrompe algo, y que el script `validar-decisiones.sh` detecte ediciones "fantasma" no declaradas.

Los `.bak.md` se sobrescriben en cada ejecución: son puntos de rollback **de la última edición**, no historial.

## Bootstrap (SDD)

<a id="bootstrap"></a>

Proceso conversacional que **auto-inicializa la documentación del proyecto** a partir de un brief inicial (`specs/brief.md`). Tiene 3 fases más cierre:

1. `spec-analyst` cierra las 6 dimensiones obligatorias (ver [SDD](#sdd)).
2. `domain-modeler` extrae entidades, ciclo de vida y capacidades.
3. `architect` propone stack, patrones, convenciones; seedea `DECISIONES.md`.
4. `context-manager` escribe el primer `CONTEXTO.md` (sesión S1).

Se dispara con `/bootstrap`. Alternativa desde código existente: `/import-project`. Alternativa acelerada: ver [quick-bootstrap](#quick-bootstrap).

## CLAUDE.md

<a id="claude-md"></a>

Archivo raíz **autogenerado** (por `scripts/sync-agents.py`) que Claude Code lee al abrir el proyecto. Equivale a "instrucciones globales" para esa herramienta. Incluye:

- Protocolo de inicio de sesión.
- Descripción del proyecto.
- Lista de subagentes y slash-commands disponibles.
- Reglas de oro del sistema.

No editar a mano. Si cambia algo en `ai-specs/`, regenerar con `bash scripts/sync-agents.sh`.

## CONTEXTO.md

<a id="contexto"></a>

Documento **volátil de memoria de sesión**, ≤80 líneas, con 6 secciones fijas (Estado actual, Bloqueados, Deuda técnica, Próxima tarea, Mocks disponibles, Convenciones activas).

Se sobrescribe completo en cada cierre de sesión — **no se acumula cronología**. Gestionado exclusivamente por [`context-manager`](#agente) vía `/actualizar-contexto`. Ver también [memoria compacta](#memoria-compacta).

## DECISIONES.md

<a id="decisiones"></a>

Documento **volátil-canónico** de decisiones vigentes del proyecto. 8 categorías fijas: Filosofía de desarrollo, Stack, Arquitectura, Convenciones de código, Testing, Datos y persistencia, Seguridad y auth, Despliegue.

**Edición in-place** por categoría, nunca append cronológico. Si crece >100 líneas, las entradas menos relevantes migran a `docs/archivo/DECISIONES_HISTORICO.md`.

## Gate DoD (Definition of Done)

<a id="gate-dod"></a>

Control de calidad obligatorio **antes de escribir código**, aplicado por [`feature-developer`](#agente) y replicado por [`code-reviewer`](#agente). Consiste en responder explícitamente a tres preguntas:

1. ¿Hay criterio de aceptación verificable? (no "debe funcionar bien")
2. ¿Hay prueba automatizada posible que lo verifique?
3. ¿El cambio respeta `ARQUITECTURA.md`?

Si alguna es "no", el agente se detiene y escala a quien corresponda (`@feature-analyst`, `@architect` o `@domain-modeler`).

## Golden path

<a id="golden-path"></a>

Ejemplo completo de proyecto bootstrappeado bajo `examples/golden-path/`. Pensado como **referencia visual** de cómo lucen los artefactos tras un `/bootstrap` real. Incluye brief, spec cerrada, DOMINIO, GLOSARIO, ARQUITECTURA, CATALOGO, COBERTURA, CONTEXTO y DECISIONES rellenos, sin placeholders.

Tutorial narrado: [`docs/guias/WALKTHROUGH.md`](WALKTHROUGH.md).

## Handoff

<a id="handoff"></a>

Transferencia explícita del siguiente paso de un agente a otro. Se declara en el YAML canónico del agente (`handoffs: [siguiente-agente]`) y se sugiere al usuario al final del turno. **No es automático** en las herramientas actuales: el usuario invoca manualmente al siguiente agente siguiendo la recomendación.

Ejemplo: tras cerrar la spec, `spec-analyst` termina con "Spec cerrada. Invoca `@domain-modeler` para extraer entidades y ciclo de vida."

## Hub canonical

<a id="hub-canonical"></a>

Directorio `ai-specs/` que contiene las **definiciones fuente** de agentes, prompts y skills. Todo lo que vive en `.claude/` y `.github/` es **generado** a partir de aquí por `scripts/sync-agents.py`, con adaptaciones por herramienta (formato de front-matter, extensiones, mapeos de herramientas nativas).

No se edita `.claude/` ni `.github/agents|prompts|skills/` a mano. Se edita `ai-specs/` y se regenera.

## memory-mcp

<a id="memory-mcp"></a>

Servidor MCP local (`scripts/mcp/memory-server/`) que expone `CONTEXTO.md` y `DECISIONES.md` como **herramientas queryables** para agentes compatibles: `get_context()`, `get_decision(category)`, `get_blockers()`, `record_decision(...)`, etc.

Reduce el token load: un agente pide solo la categoría que necesita en vez de releer el archivo completo. Ver `scripts/mcp/memory-server/README.md`.

## Memoria compacta

<a id="memoria-compacta"></a>

Principio de diseño: la memoria de sesión (`CONTEXTO.md`) se mantiene **≤80 líneas** y sin cronología. Los detalles viven en documentos estables (`DOMINIO`, `ARQUITECTURA`, `CATALOGO`) o en el histórico. El valor: cabe entera en cualquier ventana de contexto + se revisa en 30 segundos al abrir sesión.

Contrasta con "log interminable en el README" o "wiki descentralizada". Invariante fijado y validado por `scripts/validar-contexto.sh`.

## fs-guard-mcp

<a id="fs-guard-mcp"></a>

Servidor MCP por-agente (`scripts/mcp/fs-guard-server/`) que convierte [MATRIZ_PERMISOS.md](MATRIZ_PERMISOS.md) en enforcement real. Cada instancia se arranca con identidad de un agente y rechaza cualquier `read_file`/`write_file` que la matriz no permita.

Complementa [memory-mcp](#memory-mcp). Ver `scripts/mcp/fs-guard-server/README.md`.

## Prompt (slash-command)

<a id="prompt"></a>

Invocación con prefijo `/` que dispara un flujo concreto. Son el punto de entrada habitual al sistema. Hay 11 en total: `/bootstrap`, `/nueva-sesion`, `/analizar-funcionalidad`, `/implementar-feature`, `/revisar-codigo`, `/depurar-fallo`, `/adaptar-componente`, `/sincronizar-dominio`, `/triage-ci`, `/actualizar-contexto`, `/import-project`.

Definición canónica: `ai-specs/prompts/*.md`. Espejos: `.claude/commands/` (slash-commands de Claude Code) y `.github/prompts/*.prompt.md` (Copilot).

Un prompt habitualmente invoca uno o más agentes como parte de su flujo.

## quick-bootstrap

<a id="quick-bootstrap"></a>

[Skill](#skill) que acelera el [bootstrap](#bootstrap) cuando el `brief.md` ya es suficientemente detallado (≥4 de 6 dimensiones visibles). En vez de preguntar una por una, [`spec-analyst`](#agente) redacta la spec compacta y pregunta solo lo que falta.

Se activa automáticamente. Forzar modo normal: `/bootstrap --full`.

## SDD (Spec-Driven Development)

<a id="sdd"></a>

Metodología por la que toda feature arranca con una **spec cerrada**: un documento que responde explícitamente a 6 dimensiones obligatorias (problema/JTBD, actores, alcance, restricciones, comportamiento, criterios de éxito). Hasta que no están cerradas no se modela dominio ni se propone arquitectura.

El boilerplate aplica SDD en la fase de [bootstrap](#bootstrap); a nivel de feature individual usa un flujo paralelo más ligero (`/analizar-funcionalidad` → `/implementar-feature`).

Inspirado en `C:\Users\mario\Desktop\sdd\manual-SDD`.

## Skill

<a id="skill"></a>

Conocimiento procedimental reutilizable que un agente puede **activar** según contexto. A diferencia de un [prompt](#prompt) (que el usuario invoca), un skill lo invoca el propio agente cuando detecta que aplica.

Hay 2 skills en `ai-specs/skills/`:
- **`memory-bank`** — protocolos de inicio/cierre de sesión, fuentes de verdad canónicas.
- **`bootstrap-from-spec`** — orquesta la cascada de 3 fases del bootstrap.
- **`quick-bootstrap`** — variante rápida del anterior.

## Template pack

<a id="template-pack"></a>

Paquete en `templates/<nombre>/` con **resoluciones de placeholders** específicas de un stack + instrucciones pre-rellenadas. Aplicable con `bash scripts/init-project.sh --template=NAME`.

Hoy hay 3: `web-typescript`, `python-api`, `go-service`. Un pack resuelve placeholders técnicos (globs, comandos de test, versión del runtime) — **no** decide dominio ni arquitectura; eso lo sigue haciendo el bootstrap conversacional.

Ver `templates/README.md` para crear uno propio.

---

## Términos adyacentes (no del sistema pero usados)

- **MCP (Model Context Protocol)** — protocolo abierto para que clientes de IA (Claude Code, Cursor, etc.) llamen a herramientas externas vía JSON-RPC sobre stdio. Este boilerplate incluye dos servidores MCP propios: [memory-mcp](#memory-mcp) y [fs-guard-mcp](#fs-guard-mcp).
- **JTBD (Jobs to be Done)** — framework para definir qué trabajo contratas a un producto. Una de las 6 dimensiones obligatorias de la spec cerrada.
- **DDD (Domain-Driven Design)** — separación en capas Domain / Application / Infrastructure / Presentation. Usada como patrón por defecto en varios template packs, pero no impuesta.
- **PWA (Progressive Web App)** — aparece en el ejemplo `golden-path`; no forma parte del boilerplate.
