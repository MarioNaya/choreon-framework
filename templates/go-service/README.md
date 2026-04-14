# Template pack — go-service

Servicio en Go 1.22+ con librería estándar + testing.

## Decisiones que asume el pack

- **Lenguaje:** Go 1.22+ (aprovecha `range over int`, loop var semantics, `min`/`max`).
- **Package manager:** `go mod`.
- **Testing:** `testing` estándar con build tags (`-tags=integration`, `-tags=e2e`) para separar niveles.
- **CI:** ubuntu-latest con `actions/setup-go@v5`.
- **Globs:** `**/*.go` (Go layout es plano por paquetes, no por `src/`).

## Lo que NO decide el pack

- Framework HTTP (`net/http` puro, `chi`, `echo`, `gin`, `fiber`) — `@architect`.
- Persistencia (`database/sql`, `sqlc`, `gorm`, `ent`) — `@architect`.
- Estilo de arquitectura (Clean, hexagonal, flat por paquete) — `@architect`.
- Observabilidad (opentelemetry, prometheus) — `@architect`.

## Uso

```bash
bash scripts/init-project.sh --template=go-service
```

## Nota sobre tests por build tag

Este pack usa la convención de **build tags** para separar niveles:

```go
//go:build integration

package foo_test
// ...
```

Corre solo unit tests rápidos con `go test ./... -short`; integración e E2E con su tag. Alternativa válida: carpeta `tests/integration/` sin tags, pero el pack fija la convención tags porque es más idiomática en Go.
