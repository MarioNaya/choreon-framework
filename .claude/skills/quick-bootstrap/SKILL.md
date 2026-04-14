---
name: quick-bootstrap
description: Modo acelerado del workflow Bootstrap-from-Spec. Si el brief ya responde a ≥4 de las 6 dimensiones, salta preguntas y propone confirmación en lote. Reduce diálogo para usuarios experimentados con briefs detallados.
---

# Skill: Quick Bootstrap

## Propósito

Acelerar `/bootstrap` cuando el `brief.md` ya es suficientemente rico: en lugar de preguntar las 6 dimensiones una por una, `@spec-analyst` detecta cuáles están respondidas, propone una versión compacta de la spec cerrada, y solo pregunta lo que falte.

**No sustituye** a `bootstrap-from-spec`; es una **variante** que se activa por heurística.

## Cuándo se activa

`@spec-analyst` evalúa al leer `brief.md`:

| Dimensión | Señal de "respondida" |
|---|---|
| Problema y JTBD | Hay ≥1 oración describiendo el trabajo que resuelve, y menciona al usuario o contexto |
| Actores y contexto | Hay mención explícita de quién lo usa (rol o tipo) |
| Alcance | Hay lista de funcionalidades "In" con ≥3 ítems |
| Restricciones | Hay ≥1 restricción técnica o de negocio explícita |
| Comportamiento | Hay ≥1 flujo descrito o edge case mencionado |
| Criterios de éxito | Hay ≥1 métrica o umbral verificable |

**Disparador:** ≥4 de las 6 señales presentes → modo rápido.
**Umbral estricto:** <4 señales → modo normal (preguntas una a una de `bootstrap-from-spec`).

## Protocolo en modo rápido

### 1. Resumen inicial

`@spec-analyst` publica en el chat:

```
He detectado que tu brief ya cubre:
✓ Problema y JTBD: "[extracto literal del brief]"
✓ Actores: [extracto]
✓ Alcance: [N items detectados]
✓ Restricciones: [N explícitas]
⚠ Comportamiento: parcial — hay un flujo pero faltan edge cases
✗ Criterios de éxito: no detecto métricas verificables

Puedo proceder en modo rápido: te propongo la spec cerrada completa con lo que hay y te pregunto SOLO por las dimensiones marcadas ⚠ y ✗. ¿De acuerdo?
```

### 2. Confirmación de modo

- **"Sí, modo rápido"** → siguiente paso.
- **"No, preguntas todo"** → cae a `bootstrap-from-spec` normal.
- **"Vuelve a preguntar X pero no Y"** → modo mixto: rellenar parcialmente, preguntar solo X.

### 3. Borrador directo

`@spec-analyst` redacta `specs/spec-cerrada-[[SLUG]]-draft.md` rellenando las dimensiones detectadas, y marca las pendientes con `[[POR_CERRAR]]`.

### 4. Preguntas focalizadas

Una pasada por cada `[[POR_CERRAR]]` con default sugerido si es posible.

### 5. Checkpoint de cierre

Igual que en el modo normal: "¿Confirmas la spec cerrada y paso a modelar dominio?".

### 6. Handoff a `@domain-modeler`

El resto del bootstrap continúa como en `bootstrap-from-spec`. **Quick-bootstrap solo afecta a la fase 1**; fases 2 (dominio) y 3 (arquitectura) mantienen su ritmo conversacional normal — el código y las decisiones técnicas no admiten atajos.

## Cuándo NO usar modo rápido

- Brief muy corto (<300 palabras): probablemente no cubre 4 dimensiones aunque tú creas que sí.
- Proyecto con dominio complejo (compliance, seguridad crítica, sistemas críticos): el diálogo lento es red de seguridad.
- Primera vez que usas el sistema: mejor familiarizarte con las 6 dimensiones en modo normal antes de saltarlas.

## Ejemplo de activación

Si el brief del golden-path (`examples/golden-path/specs/brief.md`) se pasara por el clasificador:

```
✓ JTBD: "capturar una tarea debe costar menos de 5 segundos"
✓ Actores: "Lo uso yo personalmente... usuario único"
✓ Alcance: 6 funcionalidades listadas
✓ Restricciones: 3 restricciones técnicas/negocio/compliance
⚠ Comportamiento: menciona sync y push pero no edge cases
✗ Criterios éxito: menciona <5s pero sin forma de medición
```

5 señales claras + 1 parcial → modo rápido. Pregunta solo edge cases + cómo medir S01.

## Reglas

- **Nunca inventar lo que el brief no dice.** Si una señal es dudosa, marcarla como `[[POR_CERRAR]]` y preguntar.
- **Un draft marcado `[[POR_CERRAR]]` nunca se cierra** sin que el usuario resuelva esos huecos.
- El usuario puede forzar modo normal con `/bootstrap --full` (variante del prompt).
- La heurística es solo ayuda de entrada — si detecta 4/6 pero el brief es contradictorio, `@spec-analyst` sigue pudiendo reabrir dimensiones.

## Invariantes

- La spec final producida en modo rápido **es indistinguible** de una producida en modo normal: mismo formato, mismos campos cerrados.
- El archivo intermedio `...-draft.md` se renombra a `spec-cerrada-[[SLUG]].md` solo tras la confirmación final.
- Si durante el proceso el usuario quiere volver atrás, el draft se descarta; se vuelve a `bootstrap-from-spec` completo.
