# Guía — Continuous Integration

El boilerplate incluye **tres workflows** de GitHub Actions, cada uno con un propósito distinto. Esta guía explica qué hace cada uno, cómo adaptarlo a tu proyecto o a otros sistemas de CI (GitLab, CircleCI, Jenkins), y cómo debugear fallos.

Términos: ver [`GLOSARIO_SISTEMA.md`](GLOSARIO_SISTEMA.md).

---

## Los tres workflows

| Workflow | Archivo | Trigger | Propósito |
|---|---|---|---|
| **CI Manual** | `.github/workflows/ci-manual.yml` | `workflow_dispatch` (manual) | Lanzar tests de tu proyecto bajo demanda por entorno/suite |
| **CI Nightly** | `.github/workflows/ci-nightly.yml` | `schedule` diario + manual | Regresión completa nocturna en 2 entornos |
| **Boilerplate Health** | `.github/workflows/ci-boilerplate-health.yml` | `push` / `pull_request` a `main` | Vigila que el propio boilerplate no se rompa (no es para tu proyecto, es para el sistema) |

---

## 1. CI Manual — `ci-manual.yml`

**Propósito:** ejecutar pruebas de tu proyecto bajo demanda, eligiendo entorno y suite. Útil para validación manual antes de un merge grande o para cazar regresiones específicas.

**Trigger:** dispatch manual desde la UI de GitHub Actions (`workflow_dispatch`).

**Inputs:**
- `environment` — `dev` / `staging` / `prod` (elegible desde la UI).
- `suite` — `unit` / `integration` / `e2e` / `all`.

**Pasos:**
1. **Checkout** del código.
2. **Setup runtime** con `[[SETUP_ACTION]]` (p.ej. `actions/setup-node@v4` si aplicaste `--template=web-typescript`; `actions/setup-python@v5` para `python-api`; `actions/setup-go@v5` para `go-service`).
3. **Install dependencies** con `[[INSTALL_COMMAND]]` (ej: `pnpm install`, `pip install -r requirements.txt`, `go mod download`).
4. **Run suite** — elige comando según input:
   - `unit` → `[[TEST_COMMAND_UNIT]]`.
   - `integration` → `[[TEST_COMMAND_INTEGRATION]]`.
   - `e2e` → `[[TEST_COMMAND_E2E]]`.
   - `all` → `[[TEST_COMMAND_ALL]]`.
5. **Collect artifacts** — sube `[[ARTIFACT_PATH]]` (reportes, screenshots, lo que produzca tu stack) incluso si los tests fallaron (`if: always()`). Retención: 14 días.

**Placeholders a resolver:** se rellenan con `scripts/init-project.sh --template=NOMBRE` o, si tu stack no coincide con ningún pack, editando el YAML a mano.

---

## 2. CI Nightly — `ci-nightly.yml`

**Propósito:** regresión completa cada noche en dos entornos secuenciales. Pensado para pillar drift entre entornos y problemas que solo aparecen con dataset completo.

**Trigger:** cron `0 0 * * *` (00:00 UTC) + manual.

**Jobs:**
- `nightly-env1` — ejecuta suite completa en `[[ENV1]]` (por defecto `dev`).
- `nightly-env2` — ejecuta suite completa en `[[ENV2]]` (por defecto `staging`), con `needs: nightly-env1` + `if: always()` (no se cancela aunque env1 falle).

**Pasos (idénticos en ambos jobs):**
Checkout → Setup runtime → Install → `[[TEST_COMMAND_ALL]]` → Collect artifacts. Retención: 30 días.

**Adaptaciones típicas:**
- Añadir un tercer entorno (`prod`) como job adicional con `needs: nightly-env2`.
- Cambiar el cron (por ejemplo a las 03:00 de tu zona horaria).
- Notificar a Slack/Teams añadiendo un step al final con `if: failure()`.

---

## 3. Boilerplate Health — `ci-boilerplate-health.yml`

**Propósito:** vigilar que el **sistema del propio boilerplate** no se rompe al editar agentes, prompts o scripts. **No es un workflow para tu proyecto**; es meta-CI del sistema agéntico.

Si forkeas el boilerplate o lo vas evolucionando, este workflow te avisa de que:

- El sync no es idempotente (error al volver a correrlo).
- Los validadores de CONTEXTO o DECISIONES fallan.
- El golden-path ha dejado de ser válido.
- Aparecen residuos del origen QA del que se derivó este boilerplate (ver comprobación en el workflow).
- Los smoke tests de los servidores MCP fallan.
- Los template packs no se listan o no aplican.

**Trigger:** push y PR a `main`, más manual.

**Los 13 checks (simplificados):**

1. `sync-agents.py` ejecuta sin error.
2. Sync idempotente: segunda ejecución = mismos hashes SHA256.
3. `validar-contexto.sh` pasa sobre la plantilla raíz.
4. `validar-decisiones.sh` pasa sobre la plantilla raíz.
5. `validar-contexto.sh` pasa sobre el golden-path.
6. `validar-decisiones.sh` pasa sobre el golden-path.
7. El golden-path no tiene placeholders `[[...]]` sin resolver.
8. Ningún residuo del origen QA del que se derivó el boilerplate en el repo.
9. `memory-mcp` smoke test pasa.
10. `fs-guard-mcp` smoke test pasa.
11. Los 3 template packs se listan.
12. `--template=web-typescript` aplica en una copia temporal y deja `pnpm test` en los workflows.
13. Estructura esperada: 9 agentes + 10+ prompts + CLAUDE.md existe.

**¿Qué hacer si falla?** Cada step tiene nombre legible en la UI de Actions. Localiza el step rojo, abre el log, y replica localmente lo que el step ejecuta. Todos los steps son reproducibles en local con `bash` + `python`.

Si estás desarrollando sobre el boilerplate, **ejecuta estos checks localmente antes de pushear**:

```bash
# Equivalente aproximado en local
python scripts/sync-agents.py
bash scripts/validar-contexto.sh
bash scripts/validar-decisiones.sh
bash scripts/validar-contexto.sh examples/golden-path/docs/sesion/CONTEXTO.md
bash scripts/validar-decisiones.sh examples/golden-path/docs/sesion/DECISIONES.md
python scripts/mcp/memory-server/server.py --test
python scripts/mcp/fs-guard-server/server.py --test
python scripts/init-project.py --list-templates
```

---

## Adaptar a otros CI (no GitHub Actions)

El boilerplate usa GitHub Actions por defecto, pero la lógica es portable. Conversiones típicas:

### GitLab CI

Los workflows se convierten a `.gitlab-ci.yml`:

```yaml
stages:
  - test

ci_manual:
  stage: test
  image: node:20   # o la imagen de tu stack
  script:
    - pnpm install
    - pnpm test
  when: manual
  variables:
    ENVIRONMENT: dev
  artifacts:
    paths:
      - reports/
    expire_in: 14 days
```

### CircleCI

`.circleci/config.yml` — similar estructura con `jobs` y `workflows`.

### Jenkins

`Jenkinsfile` declarativo con `pipeline` + `stages` + `parameters` para los inputs.

### Common denominator

Independientemente del CI, el **sistema agéntico** del boilerplate es CI-agnóstico: los agentes no dependen de GitHub Actions. Solo los workflows YAML son específicos; puedes borrarlos o reemplazarlos sin afectar al resto.

---

## Integración con `@ci-triage`

Cuando un run de CI falla, `/triage-ci` + `@ci-triage` clasifican los fallos en 4 categorías (🔴🟡🔵⚪). Para que el agente pueda consumir los resultados, **publica los reportes de tests como artefactos** del workflow:

```yaml
- name: Collect artifacts
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: reports/   # o donde tu test framework escriba JSON/JUnit
```

Descarga manualmente el artifact (o configura el agente para leerlo), luego invoca:

```
/triage-ci
```

Pega el contenido del reporte o proporciónale la ruta local. El agente lo analiza y escribe `docs/sesion/TRIAGE_CI.md`. Si hay 🔴, hace handoff automático a `@context-reader` para diagnóstico de causa raíz.

---

## Debug de fallos

### "CI Health falla en el step 2 (idempotencia)"

Has editado algo que hace que `sync-agents.py` produzca output distinto en cada ejecución. Causas típicas:

- Una marca de tiempo aleatoria en el YAML generado.
- Diferencias de fin de línea (LF vs CRLF) en archivos fuente.

Solución: `python scripts/sync-agents.py` dos veces localmente y `git diff` entre ejecuciones. Lo que aparezca es la fuente de no-determinismo.

### "CI Manual falla instalando dependencias"

Causas:

- `[[INSTALL_COMMAND]]` no se resolvió. Ejecuta `bash scripts/init-project.sh --template=TU_STACK` o edita el YAML.
- El runner no tiene el runtime instalado. Verifica el step `Setup runtime` y la versión.

### "Nightly falla solo en el segundo entorno"

El primer job funciona, el segundo no, incluso aunque los comandos sean idénticos. Típicamente:

- Credenciales del segundo entorno no están en `secrets.*`.
- Alguna variable de entorno diferente entre `dev` y `staging`.

Añade un step `env` explícito con los secrets del entorno correspondiente.

### "Uploads de artefactos lentos o fallan"

Si `[[ARTIFACT_PATH]]` apunta a un directorio grande (p.ej. `node_modules/`), el upload se eterniza o supera el límite. Revisa que el path solo incluye reportes relevantes.

---

## Desactivar workflows

Si tu proyecto no usa CI, o usa un sistema distinto:

```bash
# Eliminar workflows de proyecto pero mantener el health del boilerplate
rm .github/workflows/ci-manual.yml .github/workflows/ci-nightly.yml

# O eliminar todos si no usas GitHub Actions en absoluto
rm -rf .github/workflows/
```

El sistema agéntico sigue funcionando. Ver `docs/guias/ONBOARDING.md` para el flujo local sin CI.
