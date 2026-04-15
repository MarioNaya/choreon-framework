---
name: memory-bank
description: Protocolos de memoria del sistema. Jerarquía de documentos (estables/volátiles/históricos), protocolos de inicio y cierre de sesión, fuentes de verdad canónicas.
---

# Skill: Memory Bank

## Jerarquía de documentos

| Categoría | Archivos | Volatilidad | Quién edita |
|---|---|---|---|
| **Volátiles** | `docs/sesion/CONTEXTO.md` · `docs/sesion/DECISIONES.md` · `docs/sesion/TRIAGE_CI.md` · `.bak.md` de los dos primeros | Cada sesión | `context-manager`, `ci-triage` |
| **Estables** | `docs/referencia/DOMINIO.md` · `GLOSARIO.md` · `ARQUITECTURA.md` · `CATALOGO.md` · `COBERTURA.md` · `docs/planificacion/ROADMAP.md` | Cambia ante decisiones formales | `domain-modeler`, `architect`, `code-reviewer` |
| **Históricos** | `docs/archivo/DECISIONES_HISTORICO.md` · `specs/historico/*.md` | No se modifica, solo se appendea | `context-manager` al migrar, usuario al archivar specs |

## Protocolo de inicio de sesión

1. Lee `docs/sesion/CONTEXTO.md` (≤80 líneas) → estado + bloqueantes + próxima tarea + convenciones pre-seleccionadas.
2. **Bajo demanda**: `DECISIONES.md` cuando toques una categoría concreta.
3. **Bajo demanda**: documento temático según tarea (`DOMINIO.md` si tocas reglas de negocio, `CATALOGO.md` si hay reutilización posible, etc.).
4. Si existe `TRIAGE_CI.md` con fecha <48h, inclúyelo en el resumen inicial.

## Protocolo de fin de sesión

1. Invocar `/actualizar-contexto` o `@context-manager` directamente con un resumen de 3-5 líneas.
2. El manager crea `CONTEXTO.bak.md` y `DECISIONES.bak.md` **antes** de modificar.
3. Reescribe CONTEXTO completo; edita DECISIONES in-place.
4. Verificar ≤80 líneas en CONTEXTO y 8 categorías en DECISIONES.

## Numeración de sesión (contrato pineado)

Reglas invariables:

1. La **plantilla inicial** de `CONTEXTO.md` en el boilerplate sin tocar lleva `S0 — plantilla inicial`. **`S0` no es una sesión real; es el marcador del estado sin proyecto**.
2. La **primera sesión real** tras `/bootstrap` es **`S1`**. El `context-manager` de la fase 4 del bootstrap escribe directamente `CONTEXTO.md` con `S1`, nunca `S0` ni salto.
3. Cada ejecución posterior de `/actualizar-contexto` **incrementa en +1 estrictamente**: `S1 → S2 → S3 → …`. Sin saltos. Sin huecos.
4. Los backups `CONTEXTO.bak.md` y `DECISIONES.bak.md` capturan el estado previo **de la sesión que se va a sobrescribir** (p. ej. al cerrar S2 para abrir S3, los `.bak` contienen S2).
5. Si el `context-manager` detecta inconsistencia (hueco histórico, número fuera de orden, o `S0` al intentar cerrar una sesión real), **debe avisar en el reporte de cierre** y ofrecer al usuario reconciliar la numeración.

Esta regla aplica a todos los agentes que lean o escriban CONTEXTO, no solo al `context-manager`.

## Fuentes de verdad canónicas

| Tipo de regla | Fuente canónica | Dónde se replica (resúmenes) |
|---|---|---|
| Decisión arquitectónica | `DECISIONES.md` categoría "Arquitectura" | `CONTEXTO.md §Convenciones activas` (puntero, no copia) |
| Ciclo de vida entidad principal | `DOMINIO.md` §1 | — (no se replica) |
| Capacidades por estado | `DOMINIO.md` §2 | `COBERTURA.md` (referencia por ID) |
| Naming/convenciones de código | `DECISIONES.md` categoría "Convenciones de código" + `.github/instructions/*.md` | `CONTEXTO.md §Convenciones activas` |
| Stack y dependencias | `DECISIONES.md` categoría "Stack" | `ARQUITECTURA.md §1 Stack` |
| Bloqueantes vigentes | `CONTEXTO.md §Bloqueados` | — |

Regla: **una definición, múltiples punteros**. Si ves información duplicada literalmente, hay riesgo de drift; reemplaza por puntero.

## Cuándo actualizar documentos estables

| Evento | Documento a actualizar |
|---|---|
| Nueva entidad de dominio | `DOMINIO.md`, `GLOSARIO.md` |
| Nuevo estado o capacidad | `DOMINIO.md` |
| Nueva decisión arquitectónica | `ARQUITECTURA.md` + `DECISIONES.md` |
| Nueva convención de código | `DECISIONES.md` (+ `.github/instructions/*` si aplica por tipo de archivo) |
| Nuevo endpoint/componente reutilizable | `CATALOGO.md` |
| Criterio de aceptación cubierto | `COBERTURA.md` |
| Cambio de stack | `DECISIONES.md §Stack` + `ARQUITECTURA.md §1` |
| Nueva épica/hito | `ROADMAP.md` |

## Cuándo actualizar tests (4 caminos)

| Situación | Prompt/agente |
|---|---|
| Un test rojo por bug en el código | `/depurar-fallo` + `@context-reader` |
| Un test rojo por cambio legítimo en el contrato | `/adaptar-componente` + `@feature-developer` |
| Cobertura insuficiente de un criterio | `/analizar-funcionalidad` + `@feature-analyst` |
| Refactor de pruebas (sin cambiar criterios) | `/implementar-feature` con plan explícito del refactor |

## Patrón de decisión al usuario (opciones A/B/C con trade-offs)

Cuando un agente necesita que el usuario decida entre alternativas no triviales, **el formato canónico** es:

```
[Contexto mínimo: qué hay que decidir y por qué.]

┌───┬────────────────────┬─────────────┬──────────────────┐
│ # │      Acción        │    Coste    │   Consecuencia   │
├───┼────────────────────┼─────────────┼──────────────────┤
│ A │ [acción breve]     │ [tiempo/    │ [qué se gana/    │
│   │                    │  líneas]    │  qué se pierde]  │
├───┼────────────────────┼─────────────┼──────────────────┤
│ B │ [alternativa]      │ …           │ …                │
├───┼────────────────────┼─────────────┼──────────────────┤
│ C │ [alternativa]      │ …           │ …                │
└───┴────────────────────┴─────────────┴──────────────────┘

Recomendación: [A/B/C con una frase de por qué].

¿Cuál aplico?
```

Invariantes:

- **2 a 4 opciones.** Menos = falsa dicotomía; más = parálisis.
- **Cada opción trae coste y consecuencia visibles.** No solo etiqueta.
- **Recomendación explícita** con justificación de una frase. No "depende".
- **Ejemplo de respuesta** cuando proceda (p. ej. `"ok, A"` o `"A + B"`).

Agentes donde aplica: cualquiera que cierre una fase pidiendo confirmación (`spec-analyst`, `domain-modeler`, `architect`, `feature-analyst`, `feature-developer` ante obstáculos, `code-reviewer` con recomendaciones).

Rationale: patrón emergente en 5/5 agentes durante el primer uso empírico (ver `docs/auditorias/AUDITORIA_V0.6.md`). Codificarlo garantiza consistencia.

## Decisiones tácticas durante implementación

Cuando `feature-developer` (u otro agente escritor) tiene que decidir un **detalle táctico no cubierto por `DECISIONES.md`**:

1. **Registrar la decisión al vuelo** en un bloque del reporte de implementación bajo `## Decisiones tácticas introducidas`, con: qué se decidió, qué alternativas se descartaron, categoría tentativa de DECISIONES.
2. **No** introducir la decisión en `DECISIONES.md` directamente (el developer no tiene `W` sobre ese archivo).
3. Al cerrar sesión, `context-manager` lee el reporte del developer y **promueve** esas decisiones tácticas a `DECISIONES.md` en la categoría correcta, o las **marca como deuda** si el usuario no las aprueba.

Ejemplo:

```
## Decisiones tácticas introducidas

- Exit codes: mapeo 0/1/2 en main.go vía switch explícito sobre sentinelas
  tipadas + errors.Is. Descartado: substring matching del mensaje (frágil).
  Candidata a DECISIONES §4 Convenciones.
- Formato stdout de add: `✓ 12.50€ comida "descripción"`. Minimalista;
  descartado incluir ID porque no aporta al usuario en add.
  Candidata a DECISIONES §4 Convenciones (formato CLI) o deuda.
```

Rationale: observado en v0.6 que el developer improvisa detalles tácticos y el reviewer los atrapa tarde. Registrar al vuelo reduce latencia del feedback.

## Anti-patrones de memoria

| Anti-patrón | Corrección |
|---|---|
| Acumular cronología en DECISIONES | Editar in-place por categoría |
| CONTEXTO >80 líneas | Compactar; mover detalle a estables o a archivo |
| Duplicar DECISIONES en `.github/instructions/` | Hacer que instrucciones citen categorías de DECISIONES |
| Editar DOMINIO sin checkpoint | Invocar `@domain-modeler` aunque parezca trivial |
| Borrar entradas de DECISIONES sin migrar | Migrar primero a `DECISIONES_HISTORICO.md` |

## Verificación

Scripts asociados:
- `scripts/validar-contexto.sh` → ≤80 líneas, 6 secciones.
- `scripts/validar-decisiones.sh` → 8 categorías, sin duplicados, sin cronología; compara vs `.bak` y alerta si hay diffs no declarados.

Ejecutar ambos tras cada `/actualizar-contexto` es baja fricción y alto valor.
