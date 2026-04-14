# Auditoría v0.6 — ciclo de desarrollo (parcial)

**Fecha:** 2026-04-15
**Versión auditada:** v0.4 + hotfix `spec-analyst` (`f41f780`). Ciclo de desarrollo sobre proyecto `gasto-cli` (brief → E01 tracer bullet → cierre sesión S1).
**Auditor:** sesión colaborativa con Claude Code.
**Contexto:** **segunda iteración empírica del framework**, complementa v0.5 (bootstrap). Cubre `feature-analyst` + `feature-developer` + `context-manager` en modo cierre. **Pendiente:** verificación real del código (requiere Go instalado) + `code-reviewer`.

---

## Nota global (parcial): **8.3 / 10**

Ligera baja respecto a v0.5 (8.5). El ciclo de desarrollo funcionó en general, pero expuso **más gaps de framework de lo esperado**:

- Agentes excelentes en comportamiento (razonan, elevan tensiones, no tragan silenciosamente).
- **Framework con varios agujeros reales** que solo se ven al ejecutar: matriz incompleta, numeración sin pinear, Gate DoD con zona gris.

La nota puede subir a 8.7+ cuando el `code-reviewer` cierre el Gate DoD, si lo hace de forma útil.

---

## Evidencia empírica del ciclo de desarrollo

### Métricas de ejecución S1 (desde bootstrap hasta cierre)

| Etapa | Agente | Tokens | Cooking |
|---|---|---|---|
| Bootstrap (4 fases) | spec + modeler + arch + ctx-mgr | ~90k | ~8 min |
| Análisis E01 | `feature-analyst` | 43.0k | 2m 42s |
| Implementación E01 | `feature-developer` | 36.3k | 1m 25s |
| Cierre S1 | `context-manager` | 35.3k | 3m 7s |
| **Total** | **7 agentes, 11 invocaciones** | **~205k** | **~15 min** |

**Proyecto inicial gasto-cli tras S1:**
- 7 artefactos canónicos de documentación (634 líneas).
- 26 archivos de código Go creados (productivos + tests).
- `CONTEXTO.md` S2 a 43/80 líneas.
- `DECISIONES.md` a 87/100 líneas con 3 ediciones in-place.
- Bloqueante B01 declarado: verificación Go pendiente.

---

## Puntos fuertes confirmados

### Comportamiento emergente excelente de los agentes

1. **Patrón "opciones A/B/C con trade-offs + recomendación" en 4/4 agentes** que decidieron algo:
   - `spec-analyst`: Bloque A + Bloque B.
   - `architect`: 3 preguntas OK (D3 flock, D6 testing, D9 idioma).
   - `feature-analyst`: 3 bloqueantes + 2 no bloqueantes (D1-D5).
   - `feature-developer`: 3 opciones A/B/C al detectar placeholders sin resolver, y 3 tensiones elevadas tras implementar.
   
   Este patrón **no está codificado en los prompts**; emerge del LLM al seguir el espíritu del framework. Es candidato claro a **codificarlo como convención documentada** para consistencia garantizada.

2. **Feature-developer elevó 3 tensiones reales** en vez de tragárselas:
   - Matriz de permisos no cubre go.mod/go.sum/.gitkeep.
   - Mapeo error→exit code heurístico (deuda introducida).
   - go.sum escrito a mano (frágil).
   
   Ningún agente mal diseñado haría esto; los ha elevado al usuario con impacto y propuesta.

3. **Feature-developer paró en el Gate DoD** al detectar que MATRIZ_PERMISOS tenía placeholders sin resolver. Antes de escribir código. **Comportamiento ejemplar.**

### Context-manager operativo

4. **Edición in-place real** en §3 (arquitectura), §4 (convenciones), §8 (despliegue). Sin append cronológico.
5. **Backup dual automático** — `CONTEXTO.bak.md` y `DECISIONES.bak.md` creados antes de modificar. Contrato respetado.
6. **Warning proactivo** sobre umbral de 100 líneas de DECISIONES (87/100). El agente se adelanta al validador — no espera a que falle un check externo.
7. **Tracking de bloqueantes con ID** (B01). Formato consistente para referencias futuras.

### Feature-analyst

8. **Plan con trazabilidad completa**: 15 criterios de aceptación mapeados a S01/S03/S04 e invariantes I01/I02/I09/I10/I11. Un reviewer futuro puede verificar 1-a-1.

9. **Reconoce el tracer bullet como concepto**: no fragmentó E01 en micro-épicas "porque el plan es grande". Justificó que fragmentar rompe el valor del tracer.

---

## Defectos detectados en uso real

### 🐞 P0 — Matriz de permisos tiene agujeros reales (confirmado con impacto)

**Síntoma:** `feature-developer` detectó que `go.mod`, `go.sum`, `.gitkeep` **no están cubiertos** por ninguna fila de MATRIZ_PERMISOS. Los globs `**/*.go` y `**/*_test.go` del template go-service no abarcan manifests ni marcadores.

**Impacto:**
- El agente se paró correctamente la primera vez (placeholders sin resolver).
- La segunda vez, tras `init-project`, los globs quedaron resueltos pero los archivos de manifest siguen fuera. El agente escribió `go.mod`/`go.sum` "interpretando implícito". Con `fs-guard-mcp` activo, habría fallado.

**Causa raíz:** los template packs declaran solo globs de código, no archivos auxiliares (`go.mod`, `package.json`, `pyproject.toml`, `Cargo.toml`, `.gitkeep`, `.gitignore`, etc.) que son inevitables en cualquier proyecto real.

**Fix propuesto (v0.6.1):**
- Añadir a cada `templates/*/pack.json` un `PROJECT_MANIFEST_PATHS` con paths explícitos (`go.mod`, `go.sum` para Go; `package.json`, `tsconfig.json` para TS; etc.).
- Ampliar `MATRIZ_PERMISOS.md` con filas correspondientes: `feature-developer` con W sobre esos paths.
- `sync-agents.py` puede validar coherencia al generar.

### 🐞 P1 — Ambigüedad de numeración de sesión, confirmada en uso

**Síntoma:** contextualización: S0 (plantilla inicial bootstrap) → S2 (tras `/actualizar-contexto`). **La sesión S1 se saltó**.

**Causa raíz (inferida):** el `context-manager` primera vez interpretó "primera escritura tras bootstrap = S1" pero al hacer backup del estado previo lo etiquetó S0. Luego el segundo cierre incrementa de "estado previo S0" → S2 como si S1 hubiera sido la sesión cerrada. No hay convención clara.

**Impacto:** bajo técnicamente, pero rompe la consistencia que el framework promete.

**Fix propuesto (v0.5.1, ya P1 en auditoría anterior, ahora confirmado):** regla explícita en `memory-bank/SKILL.md`: "primera `CONTEXTO.md` tras bootstrap = S1; cada `/actualizar-contexto` incrementa a S2, S3...".

### 🐞 P1 — Gate DoD tiene zona gris: "código escrito" vs "verificación ejecutada"

**Síntoma:** `feature-developer` escribió 26 archivos + tests pero **no pudo ejecutar pruebas** (Go no instalado). El Gate DoD queda abierto. El agente lo reconoció y pidió al usuario cerrar sesión con bloqueante.

**Causa raíz conceptual:** el Gate DoD dice "prueba automatizable ejecutada". Pero:
- En muchos flujos reales, el dev escribe en local y verifica en CI.
- Algunos entornos (como este: Go no instalado en la máquina del usuario) imposibilitan ejecución local.
- El Gate actual no distingue:
  - (a) No hay prueba (FAIL absoluto).
  - (b) Hay prueba pero no se pudo ejecutar (FAIL temporal).
  - (c) Prueba ejecutada y pasa (PASS).

**Fix propuesto (v0.6.1):** Gate DoD de **dos pasos**:
1. **Pre-escritura:** ¿criterio verificable? ¿prueba automatizable diseñada? ¿arquitectura respetada?
2. **Post-escritura:** ¿prueba ejecutada y pasa? (Puede hacerla `feature-developer` si el entorno lo permite; puede delegarlo al `code-reviewer` si no).

Si paso 2 falla o no se puede ejecutar, el estado es "pendiente de verificación", NO "aprobado".

### 🐞 P2 — Deuda técnica introducida por el developer (heurística substring)

**Síntoma:** el developer mapeó errores a exit codes usando `strings.Contains` por substring, en lugar de sentinelas tipadas + `errors.Is`. Él mismo lo reconoció como deuda.

**Causa raíz:** el plan del `feature-analyst` no bajó a ese nivel de detalle. El developer improvisó. El `context-manager` luego registró la decisión correcta en §4 (sentinelas tipadas prohíben substring matching) — pero post-mortem.

**Tensión estructural:** ¿Plan detallado (riesgo: ceremonia) o plan abstracto (riesgo: improvisación)? Sin resolución clara todavía.

**Fix propuesto (v0.6.1):** el `feature-developer`, al detectar que va a tomar una decisión táctica no cubierta por DECISIONES, debe **registrar la decisión al vuelo** y dejarla como "decisión sin aprobar, candidata a DECISIONES §4". El `context-manager` al cierre lo confirma o invalida.

### 🐞 P2 — `go.sum` escrito a mano (síntoma de sobreimplementación)

**Síntoma:** el developer escribió `go.sum` con hashes inventados "de librerías conocidas". Es un archivo que en Go **siempre** se genera con `go mod tidy`.

**Causa raíz:** el developer intentó "completar el entregable" más de lo que debería. Idealmente habría dejado `go.sum` sin crear y anotado "pendiente `go mod tidy`".

**Fix propuesto:** en las `.github/instructions/backend.instructions.md` del pack go-service, añadir explícitamente: "archivos generados por el toolchain (go.sum, package-lock.json, Cargo.lock, etc.) NUNCA se escriben a mano; anotar como pendiente de herramienta."

### ⚠ P2 — Coste del ciclo de desarrollo

~115k tokens por ciclo recurrente (analyst 43k + developer 36k + ctx-mgr 35k). Si el usuario hace 10 features, son ~1.15M tokens solo en ceremonia del framework.

**Comparación de costes:**

| Actividad | Tokens |
|---|---|
| Bootstrap completo (one-off) | ~90k |
| Análisis de 1 feature | ~43k |
| Implementación de 1 feature | ~36k |
| Cierre de sesión | ~35k |
| **Total por feature (sin bootstrap)** | **~115k** |

El **cierre de sesión consumiendo 35k tokens es particularmente sorprendente** — solo edita 3 líneas de DECISIONES y reescribe CONTEXTO de ~44 líneas.

**Fix propuesto (v0.7, ya recogido en v0.5):** integrar `memory-mcp` en los 3 agentes del ciclo. Reduce relectura completa de archivos; pide solo categorías relevantes. Estimación conservadora: -30% a -50% de tokens.

### ⚠ P3 — Feature-developer consumió ~36k tokens para un plan ya cerrado

Si el plan del analyst es exhaustivo, el developer no debería volver a deliberar. 36k tokens es alto para "traducir plan a código". Posibles causas:
- Releyó todos los documentos canónicos aunque ya tenía el plan.
- Decidió muchos detalles tácticos (exit codes, formato stdout) que el plan no cerró.

Combinado con la P2 de "plan detallado vs abstracto", hay espacio para **especificar en el plan del analyst un nivel de detalle mínimo** o aceptar que el developer elabore.

---

## Qué se confirma y qué se matiza de v0.5

### Confirmado

| Afirmación v0.5 | Evidencia v0.6 |
|---|---|
| "Los agentes razonan contextualmente" | ✅ developer elevó 3 tensiones reales; analyst no fragmentó tracer bullet |
| "Patrón Bloque A+B pedagógico emergente" | ✅ **confirmado en 4/4 agentes que deciden algo** |
| "Checkpoints respetados" | ✅ 100% de las invocaciones paran al usuario cuando toca |
| "Numeración S0/S1 ambigua" | ✅ **materializado**: S0 → S2 saltándose S1 |
| "Coste del bootstrap alto" | ✅ confirmado, y el ciclo de desarrollo es **peor** por feature recurrente |

### Matices nuevos

| Nota | Comentario |
|---|---|
| Matriz de permisos incompleta para archivos auxiliares | **No previsto en v0.4/v0.5**. Solo se ve al implementar. |
| Gate DoD tiene zona gris "escrito pero no ejecutado" | Tampoco previsto. Surge al no poder ejecutar Go. |
| Developer introduce deuda sin anotar en el momento | Nueva. Candidata a workflow. |

---

## Recomendaciones priorizadas

### P0 — inmediato, previo a siguiente sesión

- [x] Bug `spec-analyst` sin `edit` (cerrado en v0.5, `f41f780`).

### P1 — antes de más uso real (algunos ya venían de v0.5)

- Pinear numeración de sesión en `memory-bank/SKILL.md` (**reincidente**: registrado en v0.5 y materializado en v0.6).
- Ampliar templates/*/pack.json con `PROJECT_MANIFEST_PATHS` + filas correspondientes en `MATRIZ_PERMISOS.md`.
- Gate DoD de dos pasos: pre-escritura (criterio + prueba + arquitectura) vs post-escritura (ejecutada).
- Añadir al pack go-service (y equivalentes) en `backend.instructions.md`: "archivos de manifest generados (go.sum, package-lock.json, etc.) nunca se escriben a mano".
- Lint `sync-agents.py`: si `writes` no vacío, `tools` debe incluir `edit`.
- Documentar opción 2 del primer prompt de Claude Code en `CLAUDE_CODE.md`.

### P2 — alto valor

- **Integrar `memory-mcp` en `feature-analyst`, `feature-developer`, `context-manager`.** Es el cambio con mayor retorno sobre consumo de tokens.
- Codificar el patrón "opciones A/B/C con trade-offs + recomendación" en `memory-bank/SKILL.md` como convención explícita de agentes que piden decisión al usuario.
- Definir "decisión táctica en implementación" como artefacto de workflow: el developer la anota y el `context-manager` la promueve a DECISIONES al cierre.

### P3 — pendiente de más evidencia

- Medir si el nivel de detalle del plan del analyst debería ser mayor, menor o similar. Criterio: "¿cuántas decisiones tácticas improvisa el developer por feature?".
- Evaluar si los 3 agentes de bootstrap deberían fusionarse (v0.4 P3 sin cerrar).
- Template packs: evaluar si aportan valor dada la observación de que el bootstrap decide stack independientemente (v0.4/v0.5 P3).

---

## Veredicto parcial

El ciclo de desarrollo **funciona** pero revela **más fricción estructural que el bootstrap**. Los agentes siguen comportándose muy bien; los gaps son del framework.

Los tres gaps más serios:
1. La matriz de permisos es incompleta para archivos auxiliares.
2. El Gate DoD no cubre el caso común "escribí pero no pude ejecutar".
3. El coste por feature (~115k tokens) es económicamente alto sin `memory-mcp` integrado.

Ninguno es bloqueante, todos son corregibles. La nota se mantiene en territorio de **8.3-8.5** a la espera del bloque final.

---

## Pendiente para cerrar v0.6

Cuando Mario instale Go y retome:

1. `/nueva-sesion` — ver si resume bien el estado S2 y el bloqueante B01.
2. Ejecutar verificación: `go mod tidy`, `gofmt -l .`, `go vet ./...`, `go test ./...`, `go test -race ./...`, `go test -tags e2e ./cmd/gasto/...`, coverage ≥90% en domain.
3. `/revisar-codigo` con `@code-reviewer`:
   - ¿Mapea los 15 criterios del analyst a tests concretos con archivo:línea?
   - ¿Detecta las 3 tensiones ya registradas (matriz, heurística substring, go.sum)?
   - ¿Detecta deuda adicional no vista aún?
   - ¿Consume menos o más tokens que developer (36k)?
   - ¿Clasifica 🔴🟡🔵 correctamente?
4. Si hay 🔴, re-implementar con developer. Si no, cerrar sesión S2 con `/actualizar-contexto`.

Preguntas empíricas críticas:

- ¿El Gate DoD se puede cerrar post-hoc cuando antes no se podía ejecutar, o el contrato se rompió ya?
- ¿El `code-reviewer` aporta señal independiente útil o es redundante con lo que el developer ya reportó?
- ¿El CONTEXTO S2 → S3 mantiene compacidad (<80 líneas) o empieza a inflarse?

---

## Anexo: estado final tras v0.6 parcial

- 6 hallazgos P0/P1/P2 detectados en sesión S1 (ciclo completo bootstrap + 1 feature).
- 0 bugs catastróficos.
- Ciclo de desarrollo **completable** pero con fricciones que valen la pena atacar antes de v0.7.
- Material suficiente para pinear 3-4 mejoras estructurales del framework (matriz expandida, Gate dos pasos, `memory-mcp` integrado, decisiones tácticas como artefacto).

Cuando se cierre el `@code-reviewer`, reescribiré el veredicto y la nota final.
