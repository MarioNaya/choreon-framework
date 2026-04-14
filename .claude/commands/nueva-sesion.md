---
description: Kick-off de sesión. Lee CONTEXTO, resume estado, bloqueantes y próxima tarea. Activa convenciones relevantes.
agent: context-manager
---

# /nueva-sesion

## Workflow

1. Lee `docs/sesion/CONTEXTO.md` completo.
2. Extrae: estado actual (métricas clave), bloqueantes activos, próxima tarea, convenciones activas.
3. Si hay `docs/sesion/TRIAGE_CI.md` con contenido reciente (<48h), inclúyelo en el resumen.
4. Presenta en formato fijo:

```
## Sesión S[[N]] — [[fecha actual]]

**Estado:** [resumen de 1-2 líneas del estado actual]

**Bloqueantes activos:** [lista o "ninguno"]

**Próxima tarea:** [lo que dice CONTEXTO §Próxima tarea]

**Convenciones activas relevantes:**
- [bullet 1]
- [bullet 2]
- [...]

**Triage CI reciente:** [solo si hay <48h, resumen 1 línea]

**Handoff recomendado:** [agente + prompt sugerido para la próxima tarea]
```

5. Pregunta al usuario: "¿Avanzamos con la próxima tarea o cambiamos de rumbo?".

## Reglas

- Si `CONTEXTO.md` no existe o está en estado plantilla, sugiere ejecutar `/bootstrap` primero.
- No modifiques CONTEXTO en este prompt. Solo lectura.
