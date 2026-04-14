---
description: Sincroniza DOMINIO.md, GLOSARIO.md y CATALOGO.md cuando el código ha evolucionado y la documentación se ha quedado atrás.
agent: context-reader
---

# /sincronizar-dominio

## Entrada esperada

- Motivo del desfase: nueva entidad detectada / nuevo estado / endpoints nuevos / componentes añadidos.
- Opcionalmente: área concreta a revisar.

## Workflow

0. Lee `DOMINIO.md`, `GLOSARIO.md`, `CATALOGO.md` actuales.
1. Invoca `@context-reader` para escanear el código del proyecto:
   - Entidades y modelos nuevos
   - Estados/enums introducidos
   - Endpoints/componentes/módulos nuevos
2. El reader produce un **informe de diff documental**: qué hay en código que no está en los .md.
3. Presenta al usuario opciones:
   - Actualizar solo GLOSARIO/CATALOGO (cambios no-estructurales).
   - Escalar a `@domain-modeler` (si aparece entidad o ciclo de vida nuevo).
   - Escalar a `@architect` (si aparecen patrones nuevos que ameriten decisión).
4. Ejecuta la actualización acordada.

## Reglas

- El context-reader no escribe en DOMINIO/CATALOGO directamente; solo produce el informe.
- Si el diff es trivial (<5 entradas nuevas), puede el usuario pedir al reader que redacte un borrador pero **validación humana antes de commit**.
