---
applyTo: "**/*.go"
---

# Instrucciones — Go

## Estilo de código

- Lenguaje: Go 1.22+.
- Formatter: `gofmt` + `goimports`.
- Linter: `golangci-lint` con `errcheck`, `staticcheck`, `govet`, `revive`.
- Naming: según convenciones Go (PascalCase exportado, camelCase privado). Abreviaturas consistentes (`URL`, `HTTP`, `ID`).
- Errores: **idiomático Go** — `if err != nil { return ... }`. No `try/catch` simulado.

## Estructura de paquetes

Go se organiza por **paquete**, no por capa horizontal. Estructura recomendada:

```
.
├── cmd/
│   └── <nombre-binario>/  # main.go
├── internal/              # paquetes no exportables
│   ├── domain/
│   ├── application/
│   └── infra/
├── pkg/                   # (solo si de verdad vas a exportar APIs públicas)
└── tests/
    ├── integration/
    └── e2e/
```

## Patrones preferidos

- **Errores envueltos:** `fmt.Errorf("algo falló: %w", err)`; comprobar con `errors.Is/As`.
- **Context primero:** toda función I/O recibe `ctx context.Context` como primer argumento.
- **Interfaces pequeñas** donde se consumen (principio de definición consumidora), no donde se implementan.
- **Inyección:** constructor `NewFoo(deps...)` explícito; sin framework DI.
- **Logging:** `slog` estándar (Go 1.21+). JSON en producción, text en dev.

## Anti-patrones

- `panic` fuera de `init()` o `main()`. Devolver error.
- Ignorar errores con `_`.
- Interfaces con un solo método exportado y un solo implementador — probablemente no hace falta.
- `struct` gigantes con 20 campos — signo de responsabilidad excesiva.
- `interface{}` (o `any`) sin necesidad real.

## Dependencias

- `go.mod` con `require` pinado. `go.sum` versionado.
- Nuevas deps → `DECISIONES §2 Stack`.
- Prefiere librería estándar cuando sea razonable.
