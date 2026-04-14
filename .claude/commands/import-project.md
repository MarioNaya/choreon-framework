---
description: Ingiere un proyecto YA EXISTENTE (con código) y reconstruye documentación, dominio y arquitectura a partir del código real. Alternativa a /bootstrap cuando no se parte de un brief.
agent: context-reader
---

# /import-project

## Cuándo usar

Cuando adoptas el boilerplate sobre un proyecto **que ya tiene código**, en lugar de arrancar desde cero. Ejemplos:

- Repo legacy que quieres regir con este sistema agéntico.
- Fork que adoptas como propio.
- Proyecto heredado de otro equipo sin documentación viva.

## Precondiciones

- El directorio tiene código fuente (manifest de dependencias reconocible: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.).
- Las plantillas de `docs/referencia/` y `docs/sesion/` siguen sin tocar, o acepta sobrescribirlas.

## Workflow

### 0. Verificación previa

1. Confirma que existe al menos un manifest de dependencias.
2. Si `docs/referencia/DOMINIO.md` ya tiene contenido no-plantilla, preguntar: "¿Reemplazar con inferencia desde código, o cancelar?".
3. **No** se usa `specs/brief.md` como entrada. El input es el propio código.

### 1. Escaneo — `@context-reader`

El reader escanea el repo (solo lectura) y produce un **informe inicial** en chat:

- **Manifest detectado** y stack inferido (lenguaje, frameworks, build tool).
- **Estructura de directorios** relevante (top-level + 1 nivel).
- **Entidades candidatas** detectadas: buscar archivos/carpetas con nombres que parezcan entidades de dominio (`models/`, `entities/`, `domain/`, clases con sufijos comunes).
- **Puntos de entrada**: `main`, `index`, handlers HTTP, CLI.
- **Tests existentes**: marco y cobertura aparente.
- **Dependencias externas** (APIs, DBs) visibles.
- **Señales de arquitectura**: monolito vs servicios, capas vs flat, DI framework.

**Checkpoint:** "¿Qué de lo detectado son entidades de dominio vs infraestructura? ¿Falta algo?"

### 2. Validación del dominio — `@domain-modeler`

Con la lista refinada por el usuario, el modeler:

- Formaliza entidades en `DOMINIO.md` (stateDiagram + matriz de capacidades).
- Si detecta `enum`, `status` columns, state machines → propone el ciclo de vida.
- Escribe `GLOSARIO.md` con términos de negocio (nombres de entidades, campos clave, términos del README/docs existentes si los hay).

**Checkpoint:** "¿Confirmas el modelo inferido o hay matices que el código no revela?"

### 3. Inferencia de arquitectura — `@architect`

El architect:

- Lee el manifest detectado y rellena `ARQUITECTURA.md §1 Stack` con versiones reales.
- Infere el patrón (capas, hexagonal, microservicios) por la forma del repo.
- Rellena `CATALOGO.md` con endpoints detectados (parseando rutas), componentes UI, módulos internos, utilidades.
- Rellena `DECISIONES.md` con las 8 categorías basándose en lo que ya es verdad del repo:
  - Stack: versiones reales.
  - Testing: marco y comando detectados.
  - Despliegue: CI/CD existente, Dockerfile, deploy scripts.
  - Convenciones: formatter/linter configurados.
  - Etc.

Marca con `[[INFERIDO]]` las entradas que necesitan confirmación del usuario.

**Checkpoint:** "¿Confirmas las decisiones inferidas o ajustas?"

### 4. JTBD retroactivo — `@spec-analyst`

El analyst pregunta retrospectivamente las dimensiones que el código no puede responder por sí mismo:

- **Problema y JTBD**: ¿qué problema resuelve este proyecto?
- **Actores**: ¿quién lo usa?
- **Alcance vivo**: ¿qué está en scope hoy vs qué está congelado?
- **Criterios de éxito**: ¿cómo mide el equipo que funciona?

Produce `specs/spec-cerrada-[[PROYECTO]]-heredado.md` (sufijo `-heredado` para distinguir de uno nacido de brief).

### 5. Cierre — `@context-manager`

Escribe `CONTEXTO.md` S1 con:

- Estado actual: métricas reales del repo (nº módulos, tests existentes, cobertura actual si hay report).
- Bloqueados: vacío o lo que el usuario mencione.
- **Deuda técnica heredada**: lista tentativa extraída por el reader (TODOs en código, `any`/`unknown`, tests ignorados, dependencias desactualizadas).
- Próxima tarea: sugerencia basada en la deuda más visible.
- Convenciones activas: 6-8 punteros a DECISIONES.

## Reglas

- **Nadie modifica código del proyecto.** Este flujo solo produce documentación.
- **Sin sobrescribir archivos con contenido real sin confirmar.** Pregunta antes.
- Cada inferencia marcada como `[[INFERIDO]]` en DECISIONES requiere confirmación del usuario o convertirse en `[[DEUDA]]` si no se puede cerrar ahora.
- Si el repo no tiene manifest reconocible, abortar con mensaje: "No detecto stack; usa `/bootstrap` con un brief descriptivo en su lugar."

## Salida

Al finalizar, el proyecto tiene:

- `specs/spec-cerrada-[[PROYECTO]]-heredado.md`
- `docs/referencia/{DOMINIO,GLOSARIO,ARQUITECTURA,CATALOGO,COBERTURA}.md`
- `docs/sesion/{CONTEXTO,DECISIONES}.md`

A partir de aquí, el sistema opera normalmente (`/nueva-sesion`, `@feature-analyst`, etc.).

## Diferencias con /bootstrap

| Aspecto | `/bootstrap` | `/import-project` |
|---|---|---|
| Input | `specs/brief.md` (idea) | código existente + manifest |
| Fase 1 | spec-analyst pregunta 6 dimensiones | context-reader escanea código |
| Fuente de verdad inicial | lo que el usuario explica | lo que el código dice |
| Riesgo | invención de requisitos | perder contexto que solo el usuario conoce |
| JTBD | dimensión de entrada | dimensión al final (retroactiva) |
| Uso típico | proyecto nuevo | proyecto existente sin docs vivas |
