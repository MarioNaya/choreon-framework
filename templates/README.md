# Template packs

Paquetes de **placeholders pre-resueltos** por stack tecnológico. Un template pack convierte el boilerplate genérico en uno adaptado a un stack concreto sin pasar por `/bootstrap` para elementos triviales (comandos de test, globs, runtime version, etc.).

Los template packs **no** reemplazan a `/bootstrap` — reducen el ruido de placeholders genéricos para que `@architect` pueda concentrarse en decisiones reales. Siempre se combinan con el bootstrap conversacional.

## Uso

```bash
bash scripts/init-project.sh --template=web-typescript
```

1. Aplica `templates/web-typescript/pack.json` reemplazando los placeholders del pack (globs, comandos, versiones) en todos los `.md` y `.yml` del proyecto.
2. Copia `templates/web-typescript/instructions/*.md` sobre `.github/instructions/` (sobrescribe las plantillas).
3. Luego pide los globales restantes (nombre del proyecto, descripción) como el flujo normal.

Tras esto: `bash scripts/sync-agents.sh` + `$EDITOR specs/brief.md` + `/bootstrap`.

## Packs incluidos

| Pack | Stack principal | Testing | CI runner |
|---|---|---|---|
| `web-typescript` | TypeScript + Node 20 + Fastify + React/Vite | Vitest + Playwright | ubuntu-latest |
| `python-api` | Python 3.12 + FastAPI + SQLAlchemy | pytest + httpx | ubuntu-latest |
| `go-service` | Go 1.22 + net/http | testing + testify | ubuntu-latest |

## Crear un pack propio

Cada pack tiene la estructura:

```
templates/<nombre>/
├── README.md            ← explica qué decisiones asume el pack
├── pack.json            ← mapping placeholder → valor
└── instructions/
    ├── backend.instructions.md     ← con applyTo y reglas del stack
    ├── frontend.instructions.md    ← (opcional, si aplica)
    └── testing.instructions.md     ← con comandos del stack
```

### `pack.json`

Diccionario plano de placeholders. Ejemplo mínimo:

```json
{
  "LENGUAJE": "Rust",
  "BACKEND_GLOB": "src/**/*.rs",
  "TEST_GLOB": "**/*_test.rs",
  "PROJECT_SRC_GLOB": "src/**/*.rs",
  "PROJECT_TEST_GLOB": "tests/**/*.rs",
  "INSTALL_COMMAND": "cargo fetch",
  "TEST_COMMAND_UNIT": "cargo test --lib",
  "TEST_COMMAND_INTEGRATION": "cargo test --test '*'",
  "TEST_COMMAND_E2E": "cargo test --test e2e",
  "TEST_COMMAND_ALL": "cargo test",
  "RUNNER_GROUP": "ubuntu-latest",
  "SETUP_ACTION": "actions-rs/toolchain@v1",
  "RUNTIME_VERSION_KEY": "toolchain",
  "RUNTIME_VERSION_VALUE": "stable",
  "ARTIFACT_PATH": "target/reports/",
  "ENV1": "dev",
  "ENV2": "prod"
}
```

Las claves **NO** incluyen los corchetes; el script los añade al hacer el replace.

### Instrucciones

Pre-rellenadas con reglas del stack (naming, antipatrones, dependencias prohibidas). Siguen el mismo front-matter `applyTo` que las plantillas base.

## Limitaciones

- El pack resuelve **placeholders sintácticos**, no toma decisiones de diseño. Seguirás necesitando `/bootstrap` para dominio + arquitectura conceptual.
- Si aplicas un pack sobre un boilerplate ya bootstrappeado, sobrescribirás las `instructions/`. Haz commit antes.
- Los packs **no** modifican `DECISIONES.md`: esas decisiones las escribe `@architect` con tu conversación.
