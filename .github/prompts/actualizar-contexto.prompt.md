---
description: Cierra una sesión de trabajo. Reescribe CONTEXTO.md y actualiza DECISIONES.md in-place. Crea backup de ambos antes de modificar.
agent: context-manager
---

# /actualizar-contexto

## Entrada esperada (del usuario, al invocar)

- **Resumen de sesión** (3-5 líneas):
  - Qué se hizo.
  - Qué decisiones nuevas se tomaron (y en qué categoría).
  - Qué bloqueantes se resolvieron / aparecieron.
  - Deuda técnica introducida o saldada.
  - Próxima tarea recomendada.

## Workflow

1. Lee `CONTEXTO.md` y `DECISIONES.md` actuales.
2. **Crea backup de ambos** antes de modificar:
   - `CONTEXTO.bak.md` ← copia de CONTEXTO.md
   - `DECISIONES.bak.md` ← copia de DECISIONES.md
3. Identifica qué categorías de DECISIONES tocan las nuevas decisiones.
4. Reescribe `CONTEXTO.md` con las 6 secciones fijas, incrementando `SN` si es nueva sesión.
5. Edita `DECISIONES.md` in-place (modifica bullets existentes o añade en la categoría correcta).
6. Verifica `CONTEXTO.md` ≤80 líneas y que DECISIONES mantiene las 8 categorías.
7. Si DECISIONES >100 líneas, propone al usuario migrar las entradas menos relevantes a `DECISIONES_HISTORICO.md`.
8. Reporta: diff resumido, rutas modificadas, warnings si algo quedó al límite.

## Reglas

- No acumular cronología en DECISIONES. In-place por categoría.
- No eliminar entradas de DECISIONES sin migrarlas a HISTORICO.
- Los backups se sobrescriben en cada ejecución (son puntos de rollback de la última edición, no historial).

## Recuperación

Si el usuario detecta corrupción:
- Restaurar CONTEXTO desde `CONTEXTO.bak.md`.
- Restaurar DECISIONES desde `DECISIONES.bak.md`.
- Ejecutar `scripts/validar-decisiones.sh` para confirmar integridad.
