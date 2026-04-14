# Auditoría v0.4 — AI SDLC Framework

**Fecha:** 2026-04-15
**Versión auditada:** v0.4 (144 archivos, tras reescritura pedagógica de documentación)
**Auditor:** sesión colaborativa con Claude Code
**Contexto:** auditoría interna. El sistema **no se ha probado en un proyecto real** con LLM en vivo; todas las conclusiones sobre funcionamiento en producción son tentativas.

---

## Nota global: **7.8 / 10** (redondeo a **8**)

Desglose:

| Dimensión | Nota | Comentario |
|---|---|---|
| Solidez conceptual | 9/10 | Memoria compacta, Gate DoD, SDD, backup dual, hub canonical: ideas potentes y coherentes. |
| Ejecución técnica | 8.5/10 | Sync real, parsers YAML propios, 2 MCP servers funcionales con 17 smoke cases, 13 checks de health. |
| Usabilidad inicial | 7/10 | Docs buenas pero requieren 45–60 min antes de ser productivo. |
| Match con "boilerplate" | 5/10 | Es un framework, no un boilerplate. Detalle abajo. |
| Valor real verificado en producción | desconocido | Ningún proyecto lo ha ejercitado con LLM en vivo. |

---

## Puntos fuertes reales

1. **Memoria compacta exportable.** `CONTEXTO ≤80 líneas + DECISIONES in-place por 8 categorías` funciona sola, incluso sin el resto del sistema. Es lo más transferible del boilerplate.
2. **Gate DoD replicado en developer y reviewer** previene output freestyle de baja calidad. Intervención barata con mucho retorno.
3. **SDD antes de implementar** ataca el problema más habitual con LLMs: alucinar requirements.
4. **Hub canonical con generación multi-tool** resuelve un problema real (drift entre Claude Code, Copilot, Cursor, Codex).
5. **`memory-mcp` y `fs-guard-mcp`** son código técnico real: parsers propios, 17 casos de prueba, path-traversal blindado. No son mock.
6. **Golden-path pedagógico** muestra cómo queda todo antes de que el usuario haga su propio bootstrap.
7. **Docs en 4 capas** (L1 README → L2 ONBOARDING → L3 WALKTHROUGH → L4 referencias) con glosario único sin duplicación.

## Defectos de diseño y puntos de dolor

1. **144 archivos es territorio de framework, no de boilerplate.** Desarrollo aparte más abajo.
2. **Fricción de onboarding alta:** 45–60 min de lectura + 20–40 min de bootstrap conversacional antes de escribir una línea de código. Prohibitivo para hackeos de fin de semana.
3. **23 identidades cognitivas** (9 agentes + 11 prompts + 3 skills) que el usuario debe aprender.
4. **Handoffs NO automáticos.** Toda la arquitectura presume que el usuario escribirá manualmente `@siguiente-agente`. Tras 5–6 handoffs pierde el hilo o salta pasos.
5. **MCP setup es otro puzzle** (Python → pip → `mcp.json` → reiniciar). Si falla silenciosamente, el sistema "parece funcionar" pero pierde memory-mcp sin aviso claro.
6. **Enforcement por convención es hope-based.** Depende de que el LLM obedezca. Único muro real: `fs-guard-mcp`, que no todos activan.
7. **Template packs incompletos.** Hay 3 (TS/Python/Go). Rust, Elixir, Kotlin, mobile, Clojure… quedan fuera. Cobertura de demo, no de producción.
8. **Duplicación sutil de listados de agentes** entre `AGENTS.md`, `CLAUDE.md` (autogenerado) y `.github/copilot-instructions.md`. Solo el `CLAUDE.md` se autogenera tras editar `ai-specs/`; los otros dos pueden quedar desincronizados.
9. **Bootstrap rígido.** 6 dimensiones son válidas para SaaS pero desproporcionadas para una CLI personal o un script de automatización doméstica.
10. **`backup dual (.bak.md)` redundante si usas git.** Solo aporta valor fuera de git o sin commits intermedios.
11. **Sin concepto de equipo.** Dos devs tocando `CONTEXTO.md` en ramas paralelas = merge conflict. Sin lock, sin CRDT, sin estrategia documentada.
12. **Sin versioning del boilerplate.** "v0.3/v0.4" aparece en docs pero no hay tag, changelog ni mecanismo de upgrade preservando personalizaciones.
13. **Sin smoke test real del flujo agéntico.** El CI Health verifica archivos, no que los prompts produzcan buen output con un LLM.
14. **Evidence-free.** Todas las justificaciones se apoyan en "sistema QA origen 8.5/10"; ninguna métrica propia.

## Sobreingeniería identificable

1. **`fs-guard-mcp` como MCP server por-agente.** Arrancar N servidores para autocontenerse es desproporcionado. Un check en pre-commit sobre paths tocados cubriría el 90% de los casos.
2. **CI Boilerplate Health con 13 checks** — CI del CI del CI. Útil durante el desarrollo del propio boilerplate; carga para el usuario que lo adopta.
3. **3 agentes de bootstrap separados.** `spec-analyst` + `domain-modeler` + `architect` podrían ser un único `bootstrapper` con 3 modos. La "separación de responsabilidades" es teatro cuando el usuario final es una persona.
4. **`quick-bootstrap` como skill aparte.** Podría ser un flag del bootstrap principal. Un skill dedicado es abstracción extra.
5. **Parser YAML propio en `sync-agents.py`.** `pyyaml` (dependencia ya habitual) habría ahorrado 30 líneas y ganado robustez.
6. **Template packs con instrucciones pre-rellenadas completas** duplican lo que `@architect` ya produce durante el bootstrap. El architect podría leer `pack.json` como entrada en vez de re-leer `.github/instructions/`.
7. **Validadores `.sh` como wrappers de `.py`.** Dos scripts para la misma cosa; el `.sh` solo existe por legado.

## Dónde se queda corto

1. **Sin modo "lite"** para proyectos pequeños. 3 agentes (feature-dev + reviewer + context-manager) cubrirían el 80% del valor sin el overhead del bootstrap SDD.
2. **Bootstrap 1-shot** para briefs ya ricos. Hoy es siempre iterativo.
3. **`/import-project` es narrativo, no automático.** No escanea realmente manifests; describe qué haría.
4. **Sin integración con trackers externos.** Si `ROADMAP.md` sincronizase con Linear / Jira / GitHub Projects, pasaría de uso personal a uso de equipo.
5. **Sin telemetría local opcional.** Imposible medir si el usuario completa ciclos `analizar → implementar → revisar` o se salta pasos.
6. **Sin modo offline.** Si Claude.ai y Copilot caen, el sistema no opera.
7. **Sin mecanismo "actualizar al nuevo boilerplate"** preservando personalizaciones.
8. **Sin ejemplos para stacks adicionales** (mobile, ML pipelines, infra as code).

## Sobre el número de archivos: 144 es territorio de framework

Comparativa:

| Referencia | Archivos al clonar |
|---|---|
| `create-react-app` | ~15 |
| `create-next-app` (con ejemplo) | ~30 |
| `rails new` | ~60 |
| `nest new` | ~20 |
| `cookiecutter-django` | ~100 |
| **AIboilerplate (v0.4)** | **144** |

Desglose de los 144:

| Categoría | Archivos | ¿Necesarios día 1? |
|---|---|---|
| Agentes canónicos + 2 espejos (Claude, Copilot) | 27 | Sí |
| Prompts canónicos + 2 espejos | 33 | Sí |
| Skills × 3 copias | 9 | Sí |
| Docs (10 guías + memoria + referencia) | 30 | Parcial — ONBOARDING y WALKTHROUGH son grandes |
| Scripts (init, sync, validadores, MCP servers) | 10 | Sí |
| Templates × 3 stacks | 14 | Solo si usas uno de esos stacks |
| Golden-path (ejemplo) | 10 | No (se puede borrar) |
| Workflows CI | 3 | No (opcional) |
| Infra (.gitignore, AGENTS.md, README, INIT, CLAUDE.md, mcp.json.example) | 8 | Sí |

**Mínimo viable real:** ~75 archivos (quitando golden-path, templates no-usados, workflows, algunas guías).

**Posicionamiento honesto:** esto **no es un boilerplate**. La etimología de "boilerplate" sugiere punto de partida mínimo y reutilizable; 144 archivos con 23 roles y 3 servidores MCP es una plataforma.

Nombres más honestos:
- **"AI SDLC Framework"** (ya reflejado en el nombre del repo remoto).
- **"Agentic Project Starter"**.
- **"SDD System"**.

Con ese reposicionamiento, los 144 archivos dejan de ser crítica y pasan a ser "normal para un framework de este alcance".

## Líneas para aportar más valor

En orden de impacto estimado:

1. **Modo `--lite` (3 agentes, sin bootstrap SDD)** — desbloquea uso en proyectos pequeños. ~2 días.
2. **Bootstrap 1-shot** — si `spec-analyst` detecta 6/6 señales, genera la spec en un turno. ~1 día.
3. **Integración `ROADMAP.md` ↔ GitHub Projects** — script `sync-roadmap.py` bidireccional con issues etiquetadas. Valor grande para equipos. ~3–5 días.
4. **Telemetría local opcional** — `.ai-metrics/usage.jsonl` anónimo que registra invocaciones de agentes. Solo disco local, sin envío. ~1 día.
5. **Smoke test agéntico end-to-end** — workflow opcional que ejecuta el bootstrap con LLM real sobre un brief simulado y verifica que los artefactos pasan validación. Caro en API pero confirma que los prompts no se han roto. ~2–3 días.
6. **`/upgrade-boilerplate`** — prompt/script que detecta versión actual en el repo del usuario y aplica diffs preservando personalizaciones. No trivial. ~5–10 días.
7. **2–3 template packs más relevantes** — mobile (Flutter/RN), ML pipeline (Python + notebooks), infra (Terraform + Pulumi). ~1 día cada uno.
8. **Reorganización para bajar el file count** — fusionar 3 agentes de bootstrap en 1 con modos, fusionar scripts `.sh`/`.py`, eliminar duplicación de listados de agentes. ~2–3 días; bajaría a ~125 archivos.

## Recomendaciones priorizadas

### P1 — bajo coste, alto retorno

- Añadir `CHANGELOG.md` con v0.1 → v0.4 y protocolo semver para futuras versiones.
- Reposicionamiento explícito (opcional): renombrar el proyecto a "AI SDLC Framework" o similar en los docs. El nombre del repo remoto ya lo refleja.
- Eliminar `sync-agents.sh` e `init-project.sh` (wrappers); dejar solo `.py` y actualizar docs. **−2 archivos, −inconsistencia**.
- Consolidar `AGENTS.md` y `CLAUDE.md` (ambos "instrucciones globales") o autogenerar ambos desde el mismo template. **−1 vector de drift**.

### P2 — refactors medianos

- Modo `--lite` con 3 agentes (feature-dev, reviewer, context-manager).
- Extraer el golden-path a un repo aparte (`AIboilerplate-example`). Deja el repo principal más limpio.
- Migrar el parser YAML propio a `pyyaml`. **−30 líneas, +robustez**.

### P3 — evolución estratégica

- Smoke test agéntico con LLM real (punto 5 de líneas de valor).
- Integración con trackers externos (punto 3).
- Versioning + `/upgrade-boilerplate` (puntos 6 y 7).

## Veredicto

El sistema tiene **piezas reales y valiosas** (memoria compacta, Gate DoD, SDD, MCP funcional, docs pedagógicas) junto a **capas de ceremonia innecesaria** (3 agentes de bootstrap separados, `fs-guard-mcp` por-agente, CI Health con 13 checks, cobertura insuficiente de stacks en templates).

El **mayor riesgo**: no se ha probado en producción con un LLM real sobre un proyecto de verdad. Todo el diseño es lógicamente coherente, pero hasta que alguien complete un ciclo bootstrap → 10 features → 2 sprints, no sabemos si los prompts funcionan en vivo.

Recomendación fuerte antes de v0.5 con nuevas features:

> **Hacer un smoke test real.** Coger un proyecto personal pequeño (1 feature), correr el bootstrap completo en Claude Code, hacer 3–5 ciclos `analizar → implementar → revisar → actualizar-contexto`, y documentar las fricciones reales encontradas.

Vale más que cualquier feature teórica. Es el único camino honesto a un 9–9.5.

---

## Notas para la siguiente auditoría

La próxima auditoría (post-uso real) debería cubrir:

- ¿Cuántos minutos del día real gastas en ceremonia agéntica vs haciendo código?
- ¿Los handoffs manuales son soportables o el usuario los salta?
- ¿Se activa de verdad el Gate DoD o es ruido?
- ¿Los MCP servers se usan o se olvidan al tercer día?
- ¿El bootstrap SDD se completa la primera vez o lo abandonas a mitad?
- ¿La memoria compacta sigue siendo compacta tras 20 sesiones, o se corrompe/infla?
- ¿Cuántos placeholders quedan sin resolver tras el bootstrap?
- ¿El golden-path te orientó o lo ignoraste?
