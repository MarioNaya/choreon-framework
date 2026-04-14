---
name: bootstrap-from-spec
description: Orquesta la cascada SDD spec → dominio → arquitectura → contexto inicial. Convierte un brief ambiguo en documentación ejecutable a través de 3 agentes conversacionales con checkpoints de confirmación.
---

# Skill: Bootstrap from Spec

## Propósito

Transformar un `specs/brief.md` (user story, PRD o descripción libre) en el conjunto completo de documentación inicial del proyecto:

- `specs/spec-cerrada-[[SLUG]].md`
- `docs/referencia/DOMINIO.md`
- `docs/referencia/GLOSARIO.md`
- `docs/referencia/ARQUITECTURA.md`
- `docs/referencia/CATALOGO.md`
- `docs/sesion/DECISIONES.md` (8 categorías seedadas)
- `docs/sesion/CONTEXTO.md` (primera sesión)

## Protocolo

### Invariantes

1. **Nunca redactar sin confirmación.** Cada agente presenta un borrador y espera aprobación explícita del usuario.
2. **Nunca sobrescribir contenido no-plantilla.** Si un archivo ya tiene datos reales, detener y preguntar.
3. **Secuencialidad estricta.** No hay paralelismo entre agentes: spec → dominio → arquitectura → contexto.
4. **Checkpoints explícitos.** Entre fase y fase, una pregunta de confirmación cerrada.

### Fases

#### Fase 1 — spec-analyst

**Input:** `specs/brief.md`.

**Actividad:** Conversación iterativa cubriendo 6 dimensiones obligatorias:
1. Problema y JTBD
2. Actores y contexto
3. Alcance (In / Out)
4. Restricciones
5. Comportamiento esperado
6. Criterios de éxito

**Patrón de pregunta:** open-ended → validación con default grounded → confirmación de cierre de esa dimensión antes de pasar a la siguiente.

**Output:** `specs/spec-cerrada-[[SLUG]].md`.

**Checkpoint:** "¿Confirmas la spec cerrada y paso a modelar dominio?"

#### Fase 2 — domain-modeler

**Input:** spec cerrada.

**Actividad:**
- Extracción de entidades candidatas → validación con usuario
- Ciclo de vida (stateDiagram Mermaid) → iterar transiciones/estados
- Matriz de capacidades (ID · Estado · Capacidad · Actor · Precondición)
- Glosario de términos de negocio

**Output:** `DOMINIO.md`, `GLOSARIO.md`.

**Checkpoint:** "¿Confirmas dominio y paso a arquitectura?"

#### Fase 3 — architect

**Input:** spec cerrada + dominio.

**Actividad:**
- Stack por capa (2-3 candidatos con trade-offs → elegir uno)
- Patrón arquitectónico global
- Estructura de módulos (Mermaid) + dependencias prohibidas
- Convenciones transversales (naming, errores, logging, testing, seguridad)
- Catálogo seed (endpoints/componentes/módulos derivados del dominio)

**Output:** `ARQUITECTURA.md`, `CATALOGO.md` (con entradas `[[SEED]]`), `DECISIONES.md` (8 categorías seedadas).

**Checkpoint:** "¿Confirmas arquitectura y cierro bootstrap?"

#### Fase 4 — context-manager

**Input:** todo lo anterior.

**Actividad:** Escribe `CONTEXTO.md` inicial (≤80 líneas):
- Estado: "Recién inicializado"
- Bloqueantes: "ninguno"
- Deuda técnica: "pendiente de primera feature"
- Próxima tarea: sugerencia del `architect` o primera épica del ROADMAP
- Convenciones activas: 6-8 punteros a DECISIONES relevantes

**Output:** `CONTEXTO.md` primera versión (S1).

## Modo --resume

Detecta la primera fase incompleta por heurística (placeholders `[[...]]` sin resolver en los artefactos esperados) y retoma desde ahí. Pregunta confirmación al usuario antes de invocar el agente correspondiente.

## Reapertura de fases

Si tras completar el bootstrap el usuario quiere modificar:
- **Spec**: reabrir fase 1, incrementar versión del archivo (`spec-cerrada-v2`), y revisar si el cambio obliga a reabrir fases posteriores.
- **Dominio**: reabrir fase 2. Si cambian capacidades, avisar que la arquitectura puede necesitar revisión.
- **Arquitectura**: reabrir fase 3. No afecta dominio pero sí catálogo y DECISIONES.

Cada reapertura queda trazada con un bullet en §Deuda técnica de CONTEXTO hasta que se haya consolidado.

## Errores comunes a evitar

| Error | Corrección |
|---|---|
| Redactar spec antes de confirmar las 6 dimensiones | Pasar una dimensión a la vez con checkpoint |
| `domain-modeler` proponiendo stack | Rechazar sugerencias técnicas y volver al modelado conceptual |
| `architect` saltando el modelado porque "es trivial" | Nunca; dominio siempre antes que arquitectura |
| Dejar categorías de DECISIONES vacías | Rellenar cada una, usando "N/A — [motivo]" si corresponde |
| Ejecutar bootstrap sobre un proyecto ya inicializado | Verificar al inicio; exigir `--resume` o borrado previo explícito |
