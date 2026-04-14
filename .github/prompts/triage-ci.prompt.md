---
description: Clasifica fallos de una ejecución de CI en 🔴🟡🔵⚪ y escribe TRIAGE_CI.md. Handoff automático a context-reader si hay 🔴.
agent: ci-triage
---

# /triage-ci

## Entrada esperada

- Referencia al run de CI (URL, job ID, o ruta local a artefactos).
- Entorno (ej: nightly, PR check, manual).
- Rama.

## Workflow

1. Lee el reporte bruto (JSON de test results, logs, stacktraces).
2. Lee `CONTEXTO.md` y `DECISIONES.md` para identificar fallos ya conocidos.
3. Invoca `@ci-triage`.
4. El triager agrupa por fingerprint y clasifica en 🔴🟡🔵⚪.
5. Cruza con `COBERTURA.md`: qué criterios quedan descubiertos.
6. Sobrescribe `docs/sesion/TRIAGE_CI.md` con el formato estándar.
7. Si hay ≥1 🔴, hace handoff automático a `@context-reader` para diagnóstico de causa raíz.

## Reglas

- Sobrescribe TRIAGE_CI.md completo (no acumular).
- No propongas fix en este prompt.
- Si todos los fallos son ⚪ (entorno), recomienda relanzar sin invocar context-reader.
