---
applyTo: "**/*_test.go"
---

# Instrucciones — Testing Go

## Filosofía

Test = comportamiento observable. Si refactorizas el interior sin cambiar el contrato y el test se rompe, el test está mal.

## Pirámide objetivo

- Unit: 70% — funciones y tipos puros; table-driven tests habituales.
- Integración: 20% — paquetes conectados, BBDD real (testcontainers o SQLite in-memory).
- E2E: 10% — binario completo levantado, cliente http.

Cobertura mínima: **80%** (`go test -coverprofile=cover.out ./... && go tool cover -func=cover.out`), salvo DECISIONES.

## Reglas

- **Sin `time.Sleep`** en tests. Usa `testing/synctest` (Go 1.24+) o abstracción de reloj.
- **`t.Skip` requiere comentario** + entrada en `DECISIONES §5`.
- **Tests independientes** — cada test levanta y tumba su estado.
- **Table-driven** cuando haya varios casos: `tests := []struct { ... }{ ... }` + `for _, tc := range tests`.
- **Nombres:** `TestFoo_CuandoX_Entonces_Y` o `TestFoo/cuando-x`.
- **Paralelos:** `t.Parallel()` salvo que el test necesite estado exclusivo.

## Build tags

Separación por nivel:

```go
//go:build integration
// +build integration
```

- Unit: sin tag → `go test ./... -short`.
- Integración: `//go:build integration` → `go test -tags=integration ./...`.
- E2E: `//go:build e2e` → `go test -tags=e2e ./tests/e2e/...`.

## Comandos

- Unit: `go test ./... -short`
- Integración: `go test -tags=integration ./...`
- E2E: `go test -tags=e2e ./tests/e2e/...`
- Todo: `go test ./...`

## Helpers

- `t.Helper()` en funciones auxiliares de test para que el stack trace señale la línea relevante.
- `t.Cleanup(func)` para teardown — más robusto que `defer` en ciertos escenarios.
- `testdata/` para fixtures (convención Go).
