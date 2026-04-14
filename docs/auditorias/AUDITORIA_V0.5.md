# Auditoría v0.5 — primer uso real (bootstrap)

**Fecha:** 2026-04-15
**Versión auditada:** v0.4 + hotfix `spec-analyst` (`f41f780`). Bootstrap ejecutado sobre brief `gasto-cli` desde un clon fresco del repo remoto.
**Auditor:** sesión colaborativa con Claude Code.
**Contexto:** **primer uso real del framework con LLM en vivo**. Cubre las 4 fases del bootstrap end-to-end. El ciclo de desarrollo (`/analizar-funcionalidad` → `/implementar-feature` → `/revisar-codigo`) queda **pendiente para la siguiente auditoría**.

---

## Nota global: **8.5 / 10**

Mejora de **+0.7** sobre v0.4 (7.8). Las razones:

- El riesgo más grande de v0.4 — "nada se ha probado con un LLM real" — queda **parcialmente mitigado**: el bootstrap completo funciona end-to-end.
- Solo **un bug** detectado en el primer uso, trivial de arreglar.
- Varias decisiones de diseño se confirman como aciertos (checkpoints, contexto conversacional entre fases, adaptación contextual de los agentes).

No llega a 9 porque:

- El ciclo de desarrollo sigue sin probarse.
- Consumo de tokens y latencia son notables.
- Aparece ambigüedad en contratos (numeración de sesión) que solo se detecta con uso real.

---

## Evidencia empírica del bootstrap real

Proyecto de prueba: `gasto-cli` — CLI para registrar gastos domésticos en Go.

### Métricas de ejecución

| Fase | Agente | Duración | Tokens | Artefactos | Líneas |
|---|---|---|---|---|---|
| 1 | `spec-analyst` (quick-bootstrap) | ~4 min total (1m06s análisis + 1m25s redacción) | 17.7k + 19k = 36.7k | `specs/spec-cerrada-gasto-cli.md` | 116 |
| 2 | `domain-modeler` | no cronometrada explícitamente | ~? | `DOMINIO.md` + `GLOSARIO.md` | 144 + 32 |
| 3 | `architect` | 3m 32s | 36k | `ARQUITECTURA.md` + `CATALOGO.md` + `DECISIONES.md` seedado | 146 + 67 + 85 |
| 4 | `context-manager` | 48 s | 17.5k | `CONTEXTO.md` | 44 (44/80) |
| **Total** | **4 agentes** | **~8 min de cooking** | **~90k tokens** | **7 artefactos canónicos** | **634 líneas** |

### Validación post-bootstrap

- `validar-contexto.sh`: ✅ 44/80 líneas, 6 secciones en orden.
- `validar-decisiones.sh`: ✅ 8 categorías en orden.
- Placeholders `[[...]]` sin resolver en los 7 artefactos generados: **cero**.
- Residuos del origen QA: **cero**.

El framework **produjo documentación ejecutable y válida desde un brief de una página** con ~20 minutos de conversación y ~$3-5 estimados en tokens.

---

## Puntos fuertes confirmados empíricamente

1. **Quick-bootstrap se activa correctamente** cuando el brief cubre ≥4/6 dimensiones. La heurística funciona en la práctica.

2. **Formato Bloque A + Bloque B para confirmación rápida** (propuesta del spec-analyst en tabla) es **óptimo pedagógicamente**: el usuario confirma en una frase ("bloque A ok y bloque B ok") sin ambigüedad. Es un patrón que debería replicarse en otros agentes que piden confirmación.

3. **`@domain-modeler` aplicó criterio contextual no ceremonial**: al detectar que `Gasto` no tiene máquina de estados rica, no forzó un stateDiagram artificial. Modeló "casi inmutable + hard-delete vía undo" sin inflar el ciclo de vida.

4. **`@architect` adaptó decisiones al contexto concreto**: eligió **identificadores en español** (coherencia con glosario, CLI mono-dev personal) en lugar de copiar el golden-path (que usa inglés para TS/React). Esto es evidencia fuerte de que los agentes **razonan**, no solo reproducen plantilla.

5. **Decisiones opinionadas se preguntan explícitamente**: en Fase 3 el architect planteó 3 preguntas con OK del usuario (D3 flock, D6 stdlib testing, D9 idioma identificadores). Nada decidido silenciosamente.

6. **Los checkpoints funcionan al 100%**: el sistema no avanzó ninguna fase sin confirmación explícita del usuario. En 4/4 fases.

7. **Progresión natural con "ok" entre fases** sin necesidad de re-disparar `/bootstrap`. Es **mejor diseño** del que yo había previsto — el orquestador principal mantiene el hilo entre agentes en lugar de forzar nuevos comandos.

8. **`GastoRecurrente` vive aparte con materialización on-the-fly**: decisión de diseño no trivial tomada por `domain-modeler` con 3 razones justificadas. Muestra que el agente razona sobre el dominio, no solo enumera entidades.

---

## Defectos detectados en uso real

### 🐞 P0 — Bug `spec-analyst` sin herramienta Write (CERRADO)

**Síntoma:** tras cerrar la spec, Claude Code mostró:

> "El agente no tiene Write. Persisto yo la spec."

**Causa raíz:** `ai-specs/agents/spec-analyst.md` declaraba `writes: specs/spec-cerrada-*.md` pero `tools: [read, search, web]` (sin `edit`). El parser de `sync-agents.py` no añade `Write/Edit` a los tools de Claude Code si el canonical no lo pide.

**Impacto:** menor — el orquestador principal rescató la operación. Pero rompe la promesa de "cada agente opera dentro de su ámbito" y genera un archivo que el usuario tiene que aceptar explícitamente en vez de que se cree como parte del flujo del agente.

**Fix:** commit `f41f780` — añadido `edit` a `tools` de `spec-analyst`. Los otros 6 agentes con `writes` no triviales ya tenían `edit`.

**Lección estructural:** el campo `writes:` del canonical no se valida contra `tools:`. Un lint automático en `sync-agents.py` ("si tiene `writes` no vacío, `tools` debe incluir `edit`") habría detectado esto antes de pushear. → pendiente para v0.5.1.

### 🐞 P1 — Ambigüedad en numeración de sesión (S0 vs S1)

**Síntoma:** `context-manager` escribió `CONTEXTO.md` con "Estado S0" en Fase 4. En el golden-path yo había puesto "S1".

**Causa raíz:** el contrato de numeración de sesión **no está pineado** en DECISIONES ni en el skill `memory-bank`. La plantilla inicial dice "S0 — plantilla inicial"; la primera sesión tras bootstrap puede interpretarse como "aún no ha habido trabajo real → sigue siendo S0" o como "primera sesión real → S1". Dos agentes razonables escribirían distinto.

**Impacto:** bajo funcionalmente, pero mina la consistencia que el framework promete. Un segundo usuario podría ver S0 en este proyecto y S1 en otro y no entender la convención.

**Fix propuesto:** añadir al skill `memory-bank` una regla explícita: "Tras bootstrap, la primera `CONTEXTO.md` lleva `S1`. `S0` solo existe en la plantilla sin tocar del boilerplate." → pendiente para v0.5.1.

### ⚠ P2 — Consumo de tokens del bootstrap

~**90k tokens** para bootstrappear un proyecto CLI sencillo. A precios típicos de Opus, ~$3-5 por bootstrap. Para un uso recurrente esto no es crítico; para un proyecto de fin de semana que se va a tirar, **es caro**.

**Causa raíz:** cada agente relee varios archivos del repo canonical (`ai-specs/`, plantillas, glosarios). No hay caché entre fases. Además, los prompts de los agentes son largos (descripciones, reglas, anti-patrones).

**Fix propuesto (v0.5.2 o superior):**
- Modo `--lite` con 3 agentes (ya mencionado en auditoría v0.4).
- `memory-mcp` puede reducir la carga si se integra en el bootstrap (los agentes pedirían solo lo que necesitan en vez de releer archivos enteros). Actualmente `memory-mcp` existe pero el bootstrap no lo usa.

### ⚠ P2 — Latencia perceptible

~**8 minutos de cooking** acumulado en las 4 fases, más tiempo de conversación humano. Para un brief rico (5/6 dimensiones), el total desde `/bootstrap` hasta sistema operativo ronda los **25-30 minutos reales**.

Aceptable para un bootstrap único, pero si el usuario interrumpe y retoma (`/bootstrap --resume`), el coste se repite parcialmente. No hay forma de saltar fases.

### ⚠ P3 — El usuario tuvo que aprobar cada creación de archivo

Claude Code pidió confirmación interactiva (`Do you want to create spec-cerrada-gasto-cli.md? 1/2/3`) varias veces. Es comportamiento default de Claude Code y una garantía de seguridad, pero fricciona el flujo del bootstrap.

**Mitigación existente:** la opción "2. Yes, allow all edits during this session" del prompt. Recomendable documentarla explícitamente en `CLAUDE_CODE.md` como "tras el primer prompt del bootstrap, elige opción 2 para dejar al sistema completar sin interrupciones".

---

## Qué se confirma y qué se invalida de la auditoría v0.4

### Confirmado por evidencia

| Afirmación v0.4 | Evidencia v0.5 |
|---|---|
| "El concepto de memoria compacta es sólido" | ✅ CONTEXTO 44/80 líneas producido correctamente |
| "SDD antes de implementar previene output freestyle" | ✅ 6 dimensiones cerradas con negociación explícita |
| "Agentes con identidad separada funcionan" | ✅ domain-modeler y architect produjeron outputs claramente distintos, adaptados a su rol |
| "Hub canonical + sync multi-tool" | ✅ Claude Code interpretó los agentes correctamente desde `.claude/agents/` |
| "Validadores aportan red de seguridad" | ✅ ambos validadores pasaron sobre artefactos reales |

### Invalidado (o matizado) por evidencia

| Afirmación v0.4 | Matiz v0.5 |
|---|---|
| "Handoffs no automáticos → usuario pierde el hilo tras 5-6" | **Invalidado parcialmente**: el orquestador principal mantuvo el hilo entre las 4 fases con "ok" como disparador. El usuario nunca tuvo que recordar al siguiente agente. |
| "Carga cognitiva de 9 agentes + 11 prompts" | **Matizado**: durante el bootstrap, el usuario solo interactuó con 4 agentes (`spec-analyst`, `domain-modeler`, `architect`, `context-manager`). No fue abrumador. |
| "Enforcement por convención es hope-based" | **Confirmado parcialmente**: los 4 agentes respetaron su ámbito... salvo que `spec-analyst` no podía escribir por el bug detectado. |

### Lo que v0.4 subestimó (positivamente)

- **El patrón Bloque A + Bloque B** que `spec-analyst` emitió por iniciativa propia no estaba previsto en v0.4. Es una aportación del propio LLM, no de la spec del agente. Muy bueno. Extensible al resto.

---

## Sobreingeniería: confirmada, parcialmente refutada

| Sospecha v0.4 | Veredicto v0.5 |
|---|---|
| "Los 3 agentes de bootstrap separados son ceremonia" | **Parcialmente refutada**. Cada uno produjo outputs distintos y de calidad razonable; la separación parece tener valor real. Pero no he medido si 1 agente con 3 modos lo haría peor. Queda abierto. |
| "CI Boilerplate Health con 13 checks es CI del CI del CI" | **Confirmada**: el usuario nunca ha tocado ese workflow, ni lo tocará en uso normal. Es carga útil solo para quien evoluciona el propio framework. |
| "Template packs insuficientes" | **Confirmado empíricamente**: `gasto-cli` es Go pero no se usó `--template=go-service` (se fue directo a `/bootstrap`). El pack no aporta si el bootstrap ya decide stack con el usuario. → plantear si los template packs deben existir. |
| "fs-guard-mcp por-agente es desproporcionado" | **Sin probar**: no se activó fs-guard-mcp en este test. Pendiente. |

---

## Hallazgos nuevos (no previstos en v0.4)

1. **La numeración de sesión no está pineada** — gap real en contrato de memoria.
2. **El bootstrap NO usa memory-mcp** — los agentes releen archivos enteros en vez de queryar categorías. Oportunidad clara de optimización.
3. **La confirmación interactiva de Claude Code por cada archivo nuevo fricciona el flujo** — no es bug del framework pero sí algo que el usuario debe aprender a navegar.
4. **`sync-agents.py` no valida coherencia entre `writes:` y `tools:`** — gap de linter que permitió el bug de `spec-analyst`.
5. **El patrón Bloque A+B emitido por el LLM** es extensible a otros agentes como convención documentada.

---

## Recomendaciones priorizadas para v0.5.x

### P0 — inmediato
- [x] Fix `spec-analyst` sin `edit` (hecho en `f41f780`).

### P1 — antes de más uso real
- Pinear numeración de sesión en `memory-bank/SKILL.md`: "primera sesión tras bootstrap = S1".
- Añadir lint en `sync-agents.py`: si un agente tiene `writes:` no vacío, debe tener `edit` en `tools`. Fail fast.
- Documentar en `CLAUDE_CODE.md`: "opción 2 del primer prompt de confirmación para desbloquear flujo".

### P2 — alto valor
- **Integrar `memory-mcp` en el bootstrap**: que los agentes pidan solo las categorías que necesitan en vez de releer archivos enteros. Reducción estimada de tokens: 30-50%.
- **Modo `--lite`** (3 agentes: feature-dev + reviewer + context-manager, sin bootstrap SDD). Para proyectos donde el bootstrap conversacional es overkill.
- **Codificar el patrón Bloque A+B** como parte del prompt de agentes que piden confirmación al usuario (spec-analyst, architect, quizás feature-analyst).

### P3 — pendiente de más evidencia
- Replantear si los template packs aportan valor suficiente (el bootstrap real no usó el pack).
- Replantear si 3 agentes de bootstrap son mejores que 1 con 3 modos (medir: calidad del output + tokens).

---

## Veredicto

El framework **funciona** en el caso de uso para el que fue diseñado (bootstrap de proyecto nuevo desde brief). La mayor incógnita de v0.4 queda despejada.

El diseño general es sólido. Los defectos encontrados son corregibles y los más graves ya están cerrados. Las oportunidades de optimización (integrar `memory-mcp` en bootstrap, modo lite, codificar patrones emergentes) son claras.

**Recomendación estratégica:** no añadir funcionalidad nueva hasta cerrar las P1 detectadas. Después, probar el ciclo de desarrollo (`/analizar-funcionalidad` → `/implementar-feature` → `/revisar-codigo`) para una **auditoría v0.6 del ciclo de desarrollo**, que es el siguiente eslabón crítico sin datos.

---

## Qué queda por auditar (para v0.5.1 o v0.6)

**Pendiente de este mismo proyecto `gasto-cli`:**

1. `/nueva-sesion` — ¿lee correctamente el CONTEXTO S0/S1 y resume?
2. `/analizar-funcionalidad` sobre E01 — ¿`feature-analyst` produce un plan útil?
3. `/implementar-feature` — ¿`feature-developer` aplica Gate DoD de verdad? ¿Escribe código Go idiomático? ¿Corre tests?
4. `/revisar-codigo` — ¿`code-reviewer` detecta anti-patrones reales? ¿El Gate replicado es útil o ruido?
5. `/actualizar-contexto` — ¿la migración in-place de DECISIONES funciona? ¿Respeta el backup dual?
6. `/triage-ci` — solo probable tras CI real.
7. `/sincronizar-dominio` — cuando el código y el dominio discrepan.
8. `/adaptar-componente` — tras un cambio externo.
9. `/depurar-fallo` — tras el primer test rojo.
10. `/import-project` — no es prioritario (requiere un proyecto existente para probarlo).

**Preguntas empíricas para cuando haya más datos:**

- ¿Los handoffs siguen siendo asumibles en el ciclo de desarrollo (donde hay más transiciones que en el bootstrap)?
- ¿`CONTEXTO.md` permanece compacto tras 5 sesiones? ¿O se infla?
- ¿Las DECISIONES `.bak.md` aportan valor real, o git los hace redundantes?
- ¿Algún agente se atasca en detalles que un humano resolvería rápido?
- ¿Cuántos tokens consume un ciclo normal `analizar → implementar → revisar`?
