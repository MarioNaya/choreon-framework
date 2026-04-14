# Template pack — python-api

API HTTP en Python 3.12+ con FastAPI o similar.

## Decisiones que asume el pack

- **Lenguaje:** Python 3.12+.
- **Package manager:** pip sobre `requirements.txt` por defecto (compatible; si prefieres `uv` o `poetry`, edita `INSTALL_COMMAND` en pack.json o regístralo en DECISIONES).
- **Testing:** pytest + httpx para tests de API.
- **CI:** ubuntu-latest con `actions/setup-python@v5`.
- **Globs de código:** `src/**/*.py`; tests en `tests/` segmentados por tipo (`unit/`, `integration/`, `e2e/`).

## Lo que NO decide el pack

- Framework web (FastAPI, Flask, Django, Litestar…) — lo decide `@architect`.
- ORM (SQLAlchemy, SQLModel, Tortoise, Django ORM, raw SQL…) — `@architect`.
- Runtime async (`asyncio` puro, `anyio`, `trio`) — `@architect`.

## Uso

```bash
bash scripts/init-project.sh --template=python-api
```
