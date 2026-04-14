---
description: Diagnostica un fallo (test rojo, bug en runtime, regresión) y propone fix mínimo. No lo aplica.
agent: context-reader
---

# /depurar-fallo

## Entrada esperada

- Descripción del fallo: qué se esperaba, qué ocurre, desde cuándo.
- Stacktrace o log si se dispone.
- Archivo/test relacionado si se conoce.

## Workflow

0. Lee `CONTEXTO.md` para confirmar que no es un bloqueante conocido.
1. Invoca `@context-reader`.
2. El reader localiza origen (fichero:línea), rastrea dependientes, clasifica causa (contrato / comportamiento / precondición / timing / selector / dato).
3. Propone **fix mínimo** en archivo concreto, sin aplicarlo.
4. Indica **otros impactos** posibles del fix.
5. Handoff a `@feature-developer` si el fix está claro, o respuesta directa al usuario si requiere decisión.

## Reglas

- El reader no escribe código.
- Cada afirmación debe ir con archivo:línea.
- Si la causa es externa al proyecto (librería vecina), deja claro que el fix puede no ser responsabilidad del proyecto.
