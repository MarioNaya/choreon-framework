# Auditoría v0.6 — ciclo de desarrollo (COMPLETA)

**Fecha:** 2026-04-15
**Versión auditada:** v0.4 + hotfix `spec-analyst` (`f41f780`). Ciclo de desarrollo completo sobre proyecto `gasto-cli` (brief → E01 tracer bullet → verificación toolchain Go → review con iteración → aprobación).
**Auditor:** sesión colaborativa con Claude Code.
**Contexto:** **segunda iteración empírica del framework**, complementa v0.5 (bootstrap). Cubre el **ciclo completo end-to-end**: `feature-analyst` + `feature-developer` + `code-reviewer` (dos vueltas con iteración de fix) + `context-manager` (dos cierres de sesión).

---

## Nota global final: **8.7 / 10**

Subida de **+0.4 sobre la parcial** (8.3) y **+0.2 sobre v0.5** (8.5).

Razones para subir a 8.7:

- **El ciclo completo funciona end-to-end.** Reviewer detecta gap real → developer itera → reviewer aprueba. Sin fricción técnica.
- **La iteración es económicamente viable:** el re-review costó 71% menos tokens y 81% menos tiempo que el primero (16.9k vs 58.8k; 1m 3s vs 5m 31s). Prueba que el modelo reviewer → developer → reviewer escala.
- **El reviewer atrapa lo que el developer pasa por alto.** H1 (substring matching en `main.go`) iba a quedar como deuda silenciosa en producción si el reviewer no lo detectara.
- **Gobierno respetado en toda la cascada.** Reviewer no tocó código, escribió solo en `COBERTURA.md`. Developer aplicó los 4 fixes sin tocar la matriz (H3 escalado correctamente).
- **Context-manager coherente:** backups, edición in-place, warnings proactivos, progresión de sesión correcta la segunda vuelta (S2 → S3).

Razones para NO subir a 9:

- 6+ hallazgos P0/P1 acumulados entre v0.4, v0.5 y v0.6 **sin resolver**.
- Coste del ciclo sigue alto: ~360k tokens totales (S1 + S2 completas); ~265k en ciclo recurrente por feature sin contar bootstrap.
- Numeración de sesión S0 → S2 (saltándose S1 en primer cierre) sigue sin fix de contrato.
- Developer sigue introduciendo decisiones tácticas sin anotarlas como artefacto.

Techo realista tras aplicar P1 acumuladas: **9.0 – 9.3**.

---

## Evidencia empírica del ciclo completo (S1 + S2)

### Métricas de ejecución

| Etapa | Agente | Tokens | Cooking |
|---|---|---|---|
| Bootstrap (4 fases) | spec + modeler + arch + ctx-mgr | ~90k | ~8 min |
| Análisis E01 | `feature-analyst` | 43.0k | 2m 42s |
| Implementación E01 | `feature-developer` | 36.3k | 1m 25s |
| Cierre S1 | `context-manager` | 35.3k | 3m 7s |
| **(instalar Go + verificación toolchain local)** | — | — | humano |
| Revisión E01 (1ª vuelta, detecta H1) | `code-reviewer` | 58.8k | 5m 31s |
| Fix H1 + verificación completa | `feature-developer` | 36.2k | 2m 59s |
| Re-revisión E01 (aprobación) | `code-reviewer` | **16.9k** | **1m 3s** |
| Cierre S2 | `context-manager` | 43.0k | 3m 40s |
| **Total ciclo completo** | **9 invocaciones** | **~360k** | **~28 min cooking** |

**Dato clave: re-review 71% más barato en tokens (16.9k vs 58.8k) y 81% más rápido (1m 3s vs 5m 31s).** El reviewer en la segunda vuelta solo verifica el diff contra H1, no relee todo. **Esto prueba que el modelo de iteración reviewer ↔ developer es económicamente viable.**

**Estado del proyecto `gasto-cli` tras S2:**

- 7 artefactos canónicos de documentación (634 líneas).
- 26 archivos de código Go (domain + app + storage + cli + cmd + tests).
- **Gate DoD cerrado:** 15/15 CA cubiertos, 100% cobertura domain, 8/8 paquetes verdes (unit + race + e2e).
- `CONTEXTO.md` S3 a 42/80 líneas.
- `DECISIONES.md` a 88/100 líneas (warning proactivo del context-manager: 12 líneas de margen antes del umbral).
- 0 bloqueantes. 3 deudas 🟡 abiertas (H2 testify, H3 matriz, H4 paths).
- E01 ✅ aprobada formalmente por `@code-reviewer`.

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

## Hallazgos nuevos al completar el ciclo (post-parcial)

### Lo que el reviewer confirma — muy positivo

1. **El reviewer NO es redundante con el developer.** H1 (substring matching en `main.go:48-66`) lo atrapó cuando el developer lo había pasado por alto — a pesar de que el developer lo había registrado como deuda en su reporte inicial. Es un caso donde el developer "arreglaba la parte que gofmt le obligaba y dejaba la que no". Sin reviewer, deuda silenciosa en producción.

2. **El reviewer mapeó DECISIONES §4 ↔ código literalmente.** Detectó que el texto del código contradecía la decisión textualmente. Es la revisión que un humano hace a ojo; ahora se ejecuta escalable.

3. **Fixes concretos con línea, tipo y patrón.** El reviewer propuso literalmente: `var ErrIO = errors.New(...)`, envolver con `fmt.Errorf("...: %w", ErrIO)`, sustituir bloque `default` por `errors.Is(err, storage.ErrIO)`. Sin ambigüedad — el developer aplicó mecánicamente.

4. **Iteración limpia en una vuelta.** El developer aplicó los 4 fixes, corrió toda la suite (gofmt + vet + build + test + test -race + test -tags e2e), todo verde, el reviewer re-aprobó en 1m 3s.

5. **Re-review encontró H4 nuevo.** Al revisar el fix, el reviewer no solo verificó "¿arreglaste H1?" sino que hizo análisis arquitectural del fix y levantó H4 (riesgo futuro si paths fuera de storage usan el wrapping). Calidad real, no checkbox.

### Validación cruzada de auditoría parcial

- **H3 confirmado desde 3 fuentes independientes:** developer, reviewer y auditoría parcial detectaron el mismo gap (matriz de permisos no cubre `go.mod`/`go.sum`/`.gitkeep`). Convergencia = alta confianza en criticidad.

### Observaciones sobre coste

- **El ciclo completo S1+S2 consumió ~360k tokens.** Desglose:
  - Bootstrap one-off: ~90k (≈25% del total).
  - Ciclo recurrente por feature (analyst + developer + reviewer doble + cierre): ~265k.
- **Estimación para 10 features:** ~2.7M tokens sin bootstrap, ≈$80-100 en precios Opus. No trivial pero tampoco catastrófico para uso profesional.
- La oportunidad de optimización **clara y de alto retorno** sigue siendo `memory-mcp` integrado: el reviewer hoy relee `DECISIONES.md` entero cuando solo necesita §4 y §5; análogo para el resto de agentes.

### Context-manager en su segundo cierre

- **Numeración correcta esta vez:** S2 → S3 incrementa +1 (vs S0 → S2 saltándose S1 en el primer cierre). Pero el hueco histórico queda. El contrato sigue sin pinear.
- **Warning proactivo sobre umbral de 100 líneas** repetido (88/100, 12 de margen). Consistente con S1.
- **Edición in-place real en §3** (wrapping de `storage.ErrIO`). Retiró la deuda preexistente sobre substring matching. Cerró bloqueante B01. Protocolo cumplido.

---

## Veredicto final

El ciclo de desarrollo **funciona end-to-end con iteración económicamente viable**. Los agentes se comportan ejemplarmente; el gobierno del framework se respeta; los hallazgos que emergen son del framework (no del comportamiento agéntico) y todos son corregibles.

Tres aciertos estructurales confirmados con evidencia:

1. **El patrón reviewer → developer → reviewer escala económicamente.** Re-review cuesta 71% menos.
2. **El reviewer aporta señal independiente crítica** — no es redundante con el developer.
3. **El context-manager mantiene memoria compacta coherente** entre sesiones (42/80, 88/100 con warning).

Tres gaps estructurales que frenan subir la nota:

1. **Numeración de sesión sin pinear** (3 auditorías registrándolo ya: v0.4 teórica, v0.5 empírica, v0.6 confirmada).
2. **Matriz de permisos incompleta para archivos auxiliares** (confirmado desde 3 fuentes).
3. **Coste alto del ciclo sin `memory-mcp` integrado** (optimización pendiente con alto retorno).

**Nota final: 8.7 / 10.** Techo realista tras aplicar P1 acumulados: 9.0-9.3.

---

## Próximos pasos (para el usuario, no para la auditoría)

En sesión S3:

1. Escalar H3 a `@architect` → ampliar `MATRIZ_PERMISOS.md` con `go.mod`, `go.sum`, `.gitkeep`, y potencialmente un `PROJECT_MANIFEST_PATHS` en el pack go-service.
2. `/analizar-funcionalidad` sobre E02 (gasto list + flags --fecha/--compartido + autocreación categoría + backup rotatorio).
3. Repetir el ciclo E02. Será el **tercer test empírico** del framework y permitirá consolidar si los patrones observados en E01 (iteración barata, reviewer útil, developer con deuda táctica sin anotar) son estables o accidentales.

## Recomendaciones estructurales para v0.7 (en el framework, no en gasto-cli)

Priorizadas por impacto:

### P0 — inmediato
Ya cerrados en v0.5.

### P1 — antes de más uso a gran escala
Acumulados de v0.4 + v0.5 + v0.6:

1. **Pinear numeración de sesión** en `memory-bank/SKILL.md` ("primera `CONTEXTO.md` tras bootstrap = S1, cada `/actualizar-contexto` incrementa +1").
2. **Ampliar templates con `PROJECT_MANIFEST_PATHS`** y correspondientes filas en `MATRIZ_PERMISOS.md`.
3. **Gate DoD de dos pasos:** pre-escritura (criterio + prueba + arquitectura) vs post-escritura (ejecutada).
4. **Lint en `sync-agents.py`:** si `writes` no vacío, `tools` debe incluir `edit`.
5. **Codificar el patrón "opciones A/B/C con trade-offs + recomendación"** en `memory-bank/SKILL.md` como convención explícita para agentes que piden decisión. **Confirmado en 5/5 agentes que decidieron algo** durante el ciclo (spec-analyst, architect, feature-analyst, feature-developer dos veces, code-reviewer). Es candidato claro.
6. **"Decisión táctica durante implementación"** como artefacto de workflow: el developer la anota y el context-manager la promueve a DECISIONES al cierre.
7. **Documentar en `CLAUDE_CODE.md`** la opción 2 del prompt de Claude Code ("allow all edits during this session") para desbloquear flujo tras primer prompt.

### P2 — alto valor / alto retorno
- **Integrar `memory-mcp` en `feature-analyst`, `feature-developer`, `code-reviewer`, `context-manager`.** Es la mejora con mayor retorno sobre consumo de tokens. Reducción estimada: 30-50%.
- Añadir a `backend.instructions.md` de cada pack: *"archivos de manifest generados por toolchain (go.sum, package-lock.json, Cargo.lock, etc.) nunca se escriben a mano; anotar como pendiente de herramienta"*.

### P3 — pendiente de más evidencia
- Nivel de detalle del plan del analyst (tensión entre ceremonia y improvisación táctica).
- Fusión de 3 agentes de bootstrap en 1 con modos (v0.4 P3 sin cerrar).
- Template packs: evaluar valor real.

---

## Preguntas para la próxima auditoría (v0.7)

Cuando se ejecute E02 (feature real, no tracer bullet):

- ¿Los patrones observados en E01 (iteración barata, reviewer útil, ~115k tokens por feature) son **estables** entre features, o el tracer bullet tuvo sesgos?
- ¿El developer sigue introduciendo decisiones tácticas no anotadas al vuelo?
- ¿El context-manager sigue respetando edición in-place cuando las decisiones a añadir son más numerosas?
- ¿`CONTEXTO.md` se mantiene compacto (<80 líneas) tras 5+ sesiones?
- ¿Aparece algún patrón nuevo del LLM no previsto por el framework?
- ¿Se cruza el umbral de 100 líneas de DECISIONES y cómo actúa el framework ante la migración a histórico?
