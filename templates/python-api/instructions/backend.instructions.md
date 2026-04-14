---
applyTo: "src/**/*.py"
---

# Instrucciones — Backend Python

## Estilo de código

- Lenguaje: Python 3.12+.
- Formatter: `ruff format` (sustituye a black; consistente con linter).
- Linter: `ruff` con reglas `E`, `F`, `I`, `B`, `UP`, `SIM`.
- Type checking: `mypy --strict` en `src/` (salvo excepciones documentadas en DECISIONES).
- Naming: `snake_case` funciones/variables, `PascalCase` clases, `SCREAMING_SNAKE_CASE` constantes.
- Docstrings solo cuando el nombre no basta.

## Estructura de carpetas recomendada

```
src/
├── domain/           # Entidades (dataclasses o Pydantic), reglas puras
├── application/      # Casos de uso
├── infrastructure/   # Repos, clientes HTTP externos
└── api/              # FastAPI routers / Flask blueprints / Django views
```

## Patrones preferidos

- **Tipos:** `dataclass(frozen=True)` o `pydantic.BaseModel` para entidades. Evita `dict` sueltos como modelos.
- **Errores de dominio:** excepciones propias (`DomainError`) o `Result` tipo `typing.Union`; mapear a HTTP en la capa api.
- **Validación:** Pydantic o `msgspec` en el borde api. Domain no valida de nuevo.
- **Logging:** `logging` estándar con formatter JSON en producción; `structlog` si DECISIONES lo pide.
- **Async:** `async def` en la capa api; el dominio puede ser síncrono si no hace I/O.

## Anti-patrones

- Lógica de negocio en routers/views.
- `except Exception:` sin re-raise o logging.
- Imports circulares por culpa de que domain importa infra.
- Funciones sin tipos (`-> None` cuando realmente es `-> User | None`).

## Dependencias

- `requirements.txt` (o `pyproject.toml` si migras a poetry/uv) pinado a versiones concretas.
- Nuevas dependencias requieren entrada en `DECISIONES §2 Stack`.
