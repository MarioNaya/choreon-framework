# Golden Path — Gestor de tareas personal

Este ejemplo muestra **cómo luce el boilerplate tras ejecutar `/bootstrap`** sobre un brief concreto. Léelo de arriba abajo si es tu primera vez con el sistema.

## El punto de partida

Un `specs/brief.md` de una página con la idea inicial. Formato libre: en este caso, la descripción de un gestor de tareas personal con recordatorios push, autoalojable, para un único usuario.

Ver: [`specs/brief.md`](specs/brief.md)

## Qué produjo cada fase

### Fase 1 — `spec-analyst` (conversación con el usuario)

El agente cubrió las **6 dimensiones obligatorias** pregunta a pregunta, con defaults sugeridos donde el brief ya apuntaba a una respuesta:

- **Problema y JTBD** — partió del brief ("capturar en <5s y olvidar") y lo formuló como JTBD verificable.
- **Actores** — cerró que es usuario único, no multi-tenant.
- **Alcance** — negoció In (captura, proyectos 0..1, recordatorios push, sync, hoy view) vs Out (recurrentes, tags, prioridades, app nativa).
- **Restricciones** — formalizó GDPR mínimo, autoalojable en ≤1 GB RAM, PWA en lugar de nativa.
- **Comportamiento** — flujo normal + 5 edge cases + 3 fallos esperados.
- **Criterios de éxito** — 5 criterios S01–S05, todos con métrica y umbral numérico.

Produjo: [`specs/spec-cerrada-gestor-tareas.md`](specs/spec-cerrada-gestor-tareas.md)

**Checkpoint:** "¿Confirmas la spec cerrada y paso a modelar dominio?" → confirmado.

### Fase 2 — `domain-modeler`

El agente partió de la spec cerrada y extrajo:

- **Entidad principal: Tarea** con estados Pendiente ↔ Completada y purga automática a 30 días.
- **Matriz de 9 capacidades (C01–C09)** con actor, estado, capacidad y precondición.
- **3 invariantes** (0..1 proyecto por tarea, timestamp coherente con estado, proyecto archivado bloquea nuevas).
- **Relaciones** con Proyecto (N:0..1) y Recordatorio (1:0..N).
- **Glosario** de 10 términos de negocio clave.

Produjo: [`docs/referencia/DOMINIO.md`](docs/referencia/DOMINIO.md), [`docs/referencia/GLOSARIO.md`](docs/referencia/GLOSARIO.md).

**Checkpoint:** "¿Confirmas dominio y paso a arquitectura?" → confirmado.

### Fase 3 — `architect`

El agente propuso stack y arquitectura **negociando trade-offs** con el usuario:

- **Stack:** TypeScript + Node 20 + Fastify + React/Vite + SQLite + Vitest + Playwright. Justificó cada elección frente a alternativas (SQLite vs PostgreSQL → SQLite por la restricción de RAM; Fastify vs Express → Fastify por ligereza y JSON Schema nativo).
- **Patrón:** monolito modular con capas DDD ligero.
- **Módulos y dependencias prohibidas** formalizados en Mermaid.
- **Convenciones transversales:** naming, errores con Result<T,E>, logging con pino, validación en el borde.
- **Pirámide de testing:** 70/20/10 con 80% cobertura mínima.
- **Catálogo seed:** 13 endpoints + 6 componentes UI + 8 módulos internos + 4 utilidades compartidas, derivados del dominio.
- **Seedeó DECISIONES.md** con 8 categorías cerradas.

Produjo: [`docs/referencia/ARQUITECTURA.md`](docs/referencia/ARQUITECTURA.md), [`docs/referencia/CATALOGO.md`](docs/referencia/CATALOGO.md), [`docs/sesion/DECISIONES.md`](docs/sesion/DECISIONES.md).

**Checkpoint:** "¿Confirmas arquitectura y cierro bootstrap?" → confirmado.

### Fase 4 — `context-manager`

Escribió el primer `CONTEXTO.md` (S1, 47 líneas) con:

- Estado actual: 0 módulos, 0 tests (proyecto recién inicializado).
- Bloqueados: ninguno.
- Deuda técnica: primera feature por seleccionar, CI sin configurar.
- **Próxima tarea:** implementar `captura-rapida` (S01) como primera feature.
- Convenciones activas: 6 punteros a DECISIONES relevantes para esa primera tarea.

También rellenó [`docs/referencia/COBERTURA.md`](docs/referencia/COBERTURA.md) con los 5 criterios de éxito en estado ❌ (sin cubrir).

Produjo: [`docs/sesion/CONTEXTO.md`](docs/sesion/CONTEXTO.md).

## Resultado

Tras ~30 minutos de conversación el proyecto tiene:

- `brief.md` + `spec-cerrada-*.md` con las 6 dimensiones cerradas.
- `DOMINIO.md` con ciclo de vida y 9 capacidades.
- `GLOSARIO.md` con 10 términos.
- `ARQUITECTURA.md` con stack + 5 módulos + 7 secciones.
- `CATALOGO.md` con 13+6+8+4 entradas seed.
- `COBERTURA.md` con 5 criterios trackeables.
- `DECISIONES.md` con 8 categorías rellenas (0 "N/A").
- `CONTEXTO.md` (47/80 líneas) listo para `/nueva-sesion`.

A partir de aquí, `/analizar-funcionalidad` sobre S01 pone en marcha el ciclo de desarrollo normal.

## Cómo usar este ejemplo

```bash
# Validar que el golden-path pasa los invariantes del sistema
cd ../..
bash scripts/validar-contexto.sh examples/golden-path/docs/sesion/CONTEXTO.md
bash scripts/validar-decisiones.sh examples/golden-path/docs/sesion/DECISIONES.md

# Verificar que no hay placeholders sin resolver
grep -r '\[\[' examples/golden-path/ || echo "Sin placeholders — OK"
```

Usa los archivos de este directorio como **referencia visual** al completar tu propio `/bootstrap`: cuánto detalle cabe en cada archivo, cómo se redactan los criterios de aceptación, cómo luce una DECISIONES bien categorizada, etc.

## Qué NO hay aquí

- Código fuente real del gestor de tareas. El boilerplate solo produce **documentación y decisiones**; el código es trabajo del siguiente ciclo (`/analizar-funcionalidad` → `/implementar-feature`).
- Workflows CI rellenos. Los `.yml` del boilerplate siguen siendo plantilla hasta que el usuario decida runner y comandos.
- Instrucciones `.github/instructions/*.md` completadas. Se rellenan cuando hay convenciones específicas del stack que vayan más allá de las ya recogidas en DECISIONES.
