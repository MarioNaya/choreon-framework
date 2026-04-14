# COBERTURA

## Resumen

- Criterios totales: 5 (S01–S05)
- Cubiertos: 0 (proyecto recién inicializado, sin código aún)
- Parcialmente cubiertos: 0
- Sin cubrir: 5

## Matriz por feature

| Feature | Criterio | Estado | Prueba (archivo:línea) |
|---|---|---|---|
| captura-rapida | S01 (<5s captura) | ❌ | — (pendiente primera feature) |
| parser-fechas | S02 (≥85% frases NL) | ❌ | — |
| sync-offline | S03 (<3s reconciliación) | ❌ | — |
| recordatorios | S04 (±5 min notif) | ❌ | — |
| recursos-server | S05 (<200MB RAM) | ❌ | — |

## Criterios excluidos

Ninguno en V1 — los 5 criterios entran en alcance automatizable.

## Notas de cobertura

- El parser de lenguaje natural (S02) se validará con **fixture de 50 frases** que el reviewer debe mantener actualizada.
- S05 se medirá con un test de carga básico (`scripts/load-test.sh`) que se ejecuta en CI nightly.
