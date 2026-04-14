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
