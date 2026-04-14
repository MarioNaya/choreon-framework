---
applyTo: "[[TEST_GLOB]]"
---

<!--
Plantilla para archivos de test.
Reemplaza [[TEST_GLOB]] (ej: "**/*.test.ts", "**/*_test.go", "tests/**/*.py").
-->

# Instrucciones — Testing

## Filosofía

Un test verifica **comportamiento observable**, no implementación interna. Si el test se rompe al refactorizar sin que el comportamiento cambie, el test está mal.

## Pirámide objetivo

<!-- RELLENAR tras fijar en DECISIONES §Testing -->

- Unit: [[70%]] — cubren lógica de dominio y utilidades.
- Integración: [[20%]] — cubren interacción entre módulos.
- E2E: [[10%]] — cubren flujos críticos completos.

## Qué probar y qué NO

| ✅ Probar | ❌ No probar en este nivel |
|---|---|
| Lógica de dominio (reglas, invariantes) | Que un método se haya llamado (usa test de integración) |
| Flujos de caso de uso con dependencias reales o test doubles ligeros | Implementación interna privada |
| Contratos de integración con externos | Configuración del framework |
| E2E del camino feliz y 1-2 edge críticos | Que un botón existe (usa smoke test UI) |

## Reglas absolutas

- **Sin esperas fijas.** No `sleep(N)` ni `wait(N)`. Usa condiciones explícitas.
- **Sin flags de bypass.** `force`, `skip`, `disable` requieren comentario justificando.
- **Tests independientes.** Cada test configura su propio estado; no depende del orden.
- **Nombre descriptivo.** `should [hacer X] when [condición Y]` o equivalente claro.
- **Un assert principal.** Varios asserts son aceptables si verifican el mismo comportamiento.

## Fixtures y datos

<!-- RELLENAR -->

- Ubicación: [[ruta]]
- Regeneración: [[comando si aplica]]
- Secretos: nunca en fixtures versionados.

## Comandos

<!-- RELLENAR -->

- Unit: `[[TEST_COMMAND_UNIT]]`
- Integración: `[[TEST_COMMAND_INTEGRATION]]`
- E2E: `[[TEST_COMMAND_E2E]]`

## Cuando un test falla

1. Verifica si es regresión real, flaky o entorno (ver `ci-triage`).
2. **No comentar el test** ni ponerlo `skip` sin registrar deuda en `DECISIONES §Testing`.
3. Si no es del alcance actual, reportar y continuar; si lo es, arreglar.
