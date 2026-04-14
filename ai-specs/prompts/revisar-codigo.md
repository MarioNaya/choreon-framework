---
description: Revisa una implementación contra plan, arquitectura y convenciones. Aplica el Gate DoD explícitamente.
agent: code-reviewer
---

# /revisar-codigo

## Entrada esperada

- Referencia al plan (si existe) y al reporte de `@feature-developer`.
- Diff de archivos tocados (o rama/PR).

## Workflow

0. Lee `CONTEXTO.md`, `DECISIONES.md`, `ARQUITECTURA.md`, `COBERTURA.md`.
1. **Gate de Definition-of-Done (replicado aquí — no solo heredado del skill)**:
   1. ¿Cada criterio de aceptación está cubierto por una prueba automatizada, con mapeo criterio → archivo:línea?
   2. ¿Las pruebas verifican comportamiento observable, no mocks internos?
   3. ¿El cambio respeta las dependencias permitidas de ARQUITECTURA?
2. Invoca `@code-reviewer`.
3. Genera tabla de cobertura de criterios, escaneo de anti-patrones, clasificación 🔴🟡🔵.
4. Actualiza `docs/referencia/COBERTURA.md`.
5. Entrega reporte + veredicto (Aprobado / Aprobado con recomendaciones / Bloqueado).

## Reglas

- Un 🔴 = bloqueo. No "aprobado con condiciones" sobre un 🔴.
- Las recomendaciones 🟡 se registran como deuda en DECISIONES si el usuario acepta.
- No pidas refactors fuera del plan.
