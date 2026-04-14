---
applyTo: "tests/**/*.py"
---

# Instrucciones — Testing Python

## Filosofía

Test = verificar comportamiento observable. Si refactorizas sin cambiar comportamiento y el test se rompe, el test está mal.

## Pirámide objetivo

- Unit: 70% — dominio puro, casos de uso con fakes.
- Integración: 20% — repos reales contra BBDD temporal (SQLite en memoria o testcontainers).
- E2E: 10% — API completa con cliente httpx.

Cobertura mínima: **80%** con `coverage` (`pytest --cov=src --cov-report=term-missing`), salvo otro umbral en DECISIONES.

## Reglas

- **Sin `time.sleep`** en tests. Usa `freezegun` o abstracción de reloj.
- **`pytest.mark.skip` requiere comentario justificativo** + entrada en `DECISIONES §5 Testing`.
- Tests independientes — cada uno configura su estado.
- Usa `pytest.fixture` con scope adecuado; no abuses de `autouse`.

## Comandos

- Unit: `pytest tests/unit`
- Integración: `pytest tests/integration`
- E2E: `pytest tests/e2e`
- Todo: `pytest`

## Fixtures

- Ubicación: `tests/fixtures/` (datos) + `conftest.py` por nivel.
- Sin secretos versionados.
- Para HTTP externo, usar `responses` o `respx` (nunca hits reales en CI).
