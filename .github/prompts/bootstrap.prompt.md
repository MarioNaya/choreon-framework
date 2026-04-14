---
description: Dispara el workflow Bootstrap-from-Spec. A partir de specs/brief.md, orquesta spec-analyst → domain-modeler → architect → context-manager para auto-inicializar la documentación del proyecto.
agent: spec-analyst
---

# /bootstrap

## Uso

```
/bootstrap            # modo normal (6 preguntas una a una)
/bootstrap --full     # fuerza modo normal aunque el brief sea rico
/bootstrap --resume   # continúa una bootstrap interrumpida
```

El modo **rápido se activa automáticamente** si `@spec-analyst` detecta que `brief.md` ya cubre ≥4 de las 6 dimensiones obligatorias — ver skill `quick-bootstrap`.

## Precondiciones

- Debe existir `specs/brief.md` con una user story, PRD resumido o descripción del proyecto. Formato libre.
- Las plantillas de `docs/referencia/` y `docs/sesion/` deben estar en su estado inicial (placeholders vacíos) o se avisará al usuario antes de sobrescribir.

## Workflow

### 0. Verificación previa
1. Confirma que `specs/brief.md` existe y no está vacío.
2. Si `docs/referencia/DOMINIO.md` ya tiene contenido real (no plantilla), detente y pregunta: "Ya hay dominio modelado. ¿Rehacer desde cero (se perderá), o ejecutar `/bootstrap --resume` para retomar?".

### 1. Fase 1 — spec-analyst
Invoca `@spec-analyst`. Sigue las 6 dimensiones obligatorias. **No avances** hasta que la spec esté cerrada y confirmada por el usuario.

Artefacto esperado: `specs/spec-cerrada-[[SLUG]].md`.

### 2. Checkpoint de confirmación
Antes de pasar a modelado, pregunta explícitamente: **"¿Confirmas la spec cerrada y paso a modelar el dominio?"**. Si el usuario quiere ajustes, vuelve a fase 1.

### 3. Fase 2 — domain-modeler
Invoca `@domain-modeler`. Conversación iterativa hasta cerrar dominio.

Artefactos: `docs/referencia/DOMINIO.md`, `docs/referencia/GLOSARIO.md`.

### 4. Checkpoint
Pregunta: **"¿Confirmas dominio y paso a arquitectura?"**.

### 5. Fase 3 — architect
Invoca `@architect`. Conversación para stack, patrones, convenciones.

Artefactos: `docs/referencia/ARQUITECTURA.md`, `docs/referencia/CATALOGO.md`, `docs/sesion/DECISIONES.md` seedado.

### 6. Checkpoint
Pregunta: **"¿Confirmas arquitectura y cierro bootstrap?"**.

### 7. Fase 4 — context-manager
Invoca `@context-manager`. Escribe el primer `CONTEXTO.md` con:
- Estado: "Recién inicializado"
- Próxima tarea: la primera épica del ROADMAP o lo sugerido por el architect
- Convenciones activas: 6-8 bullets punteros de DECISIONES

### 8. Cierre
Reporta al usuario:
- Ruta de la spec cerrada.
- Archivos rellenados (DOMINIO, GLOSARIO, ARQUITECTURA, CATALOGO, DECISIONES, CONTEXTO).
- Sugerencia: "Ejecuta `/nueva-sesion` o invoca `@feature-analyst` para planificar la primera funcionalidad."

## Modo --resume

Si el usuario pasa `--resume`:
1. Lee qué archivos están rellenos vs plantilla (heurística: ¿hay placeholders `[[...]]` sin resolver?).
2. Empieza desde la primera fase cuyo artefacto esté incompleto.
3. Confirma al usuario el punto de retoma: "Detecto spec cerrada pero dominio sin modelar. ¿Retomo en `@domain-modeler`?".

## Reglas

- **No se avanza entre fases sin confirmación explícita del usuario.**
- Si el usuario quiere reabrir una fase completada (p. ej. modificar dominio tras arquitectura), vuelve a esa fase e incrementa versión del artefacto correspondiente.
- **Nunca sobrescribe** archivos con contenido no-plantilla sin aviso.

## Salida

Al finalizar con éxito, el sistema queda operativo: `/nueva-sesion`, `@feature-analyst`, `@feature-developer`, etc. funcionan con documentación poblada.
