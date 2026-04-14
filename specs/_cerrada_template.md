# Spec cerrada — [[SLUG]]

<!--
Formato estándar producido por @spec-analyst tras cerrar las 6 dimensiones obligatorias.
Cada sección tiene contenido concreto y verificable. No quedan "TBD".
-->

**Versión:** v1
**Fecha de cierre:** [[YYYY-MM-DD]]
**Autor (usuario):** [[nombre]]
**Analista:** spec-analyst

---

## 1. Problema y JTBD

**Job to be done:** [[qué trabajo resuelve el producto para el usuario]]

**Problema concreto:** [[formulación en 2-3 líneas]]

## 2. Actores y contexto

| Actor | Tipo | Contexto de uso |
|---|---|---|
| [[rol1]] | primario | [[cuándo/cómo/desde dónde lo usa]] |
| [[rol2]] | secundario | [[…]] |

## 3. Alcance

### In

- [[funcionalidad 1 que SÍ entra]]
- [[funcionalidad 2]]

### Out

- [[funcionalidad que explícitamente NO entra — y por qué]]

## 4. Restricciones

| Tipo | Restricción | Motivo |
|---|---|---|
| Técnica | [[ej. sin backend propio]] | [[razón]] |
| Negocio | [[ej. lanzar antes de Q3]] | [[razón]] |
| Legal/compliance | [[ej. RGPD europeo]] | [[razón]] |

## 5. Comportamiento esperado

### Flujo normal

[[1-3 párrafos describiendo el camino feliz]]

### Edge cases

- [[caso límite 1]] → [[respuesta esperada]]
- [[caso límite 2]] → [[respuesta esperada]]

### Fallos esperados

- [[tipo de fallo]] → [[tratamiento — error visible al usuario, retry, fallback]]

## 6. Criterios de éxito

Criterios **verificables** (no subjetivos):

| ID | Criterio | Métrica | Umbral |
|---|---|---|---|
| S01 | [[criterio]] | [[cómo se mide]] | [[valor concreto]] |
| S02 | [[…]] | [[…]] | [[…]] |

---

## Defaults aceptados durante el cierre

- [[decisión asumida + por qué el usuario la aceptó]]

## Defaults rechazados

- [[sugerencia que el usuario rechazó + alternativa elegida]]

## Handoff

Esta spec está lista para `@domain-modeler` (`/bootstrap` fase 2).
