# Spec cerrada — gestor-tareas

**Versión:** v1
**Fecha de cierre:** 2026-04-14
**Autor (usuario):** Mario
**Analista:** spec-analyst

---

## 1. Problema y JTBD

**Job to be done:** Cuando pienso en algo que tengo que hacer, quiero capturarlo en menos de 5 segundos y olvidarme, para que me lo recuerde cuando toque sin tener que revisarlo compulsivamente.

**Problema concreto:** Las herramientas existentes (Todoist, Things) son lentas en captura o cobran por lo básico. Mi cerebro deja de capturar si la fricción supera 5 segundos → tareas olvidadas.

## 2. Actores y contexto

| Actor | Tipo | Contexto de uso |
|---|---|---|
| Propietario único | primario | Escritorio durante el trabajo (navegador) y móvil durante desplazamientos (misma webapp responsive) |

No hay otros actores. No es multi-tenant en V1.

## 3. Alcance

### In

- Crear tarea con título obligatorio y fecha límite opcional.
- Asociar tarea a un proyecto (0 o 1 proyecto por tarea).
- Crear, renombrar y archivar proyectos.
- Marcar tarea como completada y deshacer.
- Vista "hoy": tareas vencidas + que vencen hoy.
- Vista por proyecto y vista global pendiente.
- Recordatorio: notificación push N horas antes de la fecha límite (configurable global, no por tarea).
- Sincronización móvil ↔ escritorio (misma webapp; se logra con backend único).

### Out

- Subtareas, etiquetas, prioridades, tareas recurrentes — V2.
- Colaboración multi-usuario, compartir proyectos — nunca.
- App nativa — nunca en V1.
- Integración con calendario externo — V2.

## 4. Restricciones

| Tipo | Restricción | Motivo |
|---|---|---|
| Técnica | Autoalojable en VPS pequeño (≤1 GB RAM) | Sin presupuesto; tiene que vivir en un server del usuario |
| Técnica | PWA responsive en lugar de nativa | Un solo codebase; push en web con notificaciones del navegador |
| Negocio | Usuario único; no hay registro público | Proyecto personal |
| Compliance | GDPR mínimo: datos solo en el servidor del usuario, sin telemetría externa | Mínimo respeto a normativa por si algún día se abre |

## 5. Comportamiento esperado

### Flujo normal

1. El usuario abre la PWA (móvil o escritorio).
2. Pulsa "Nueva tarea" o atajo `n`. Input focaliza en el título.
3. Escribe "Llamar al dentista jueves" y pulsa Enter. La tarea queda creada con fecha parseada del lenguaje natural ("jueves" → próximo jueves, 09:00).
4. La tarea aparece en la vista actual con animación breve.
5. Cuando faltan N horas para la fecha límite (configurable, default 2h), el navegador notifica.
6. El usuario pulsa la notificación → la PWA abre y muestra la tarea.
7. El usuario marca completada → desaparece de "hoy" y se ve en el log de completadas del día (auto-purga a los 30 días).

### Edge cases

- Título vacío → error inline, no crea tarea.
- Fecha en el pasado → permitir; entra directa a "hoy" sección "vencidas".
- Sin conexión → crear tarea en local (IndexedDB), sincronizar al volver online.
- Conflicto de sync (tarea editada en dos dispositivos sin conexión) → last-write-wins por timestamp del cliente, log del conflicto para el usuario.
- Proyecto eliminado con tareas dentro → preguntar: mover a "sin proyecto" o archivar tareas también.

### Fallos esperados

- Backend caído → operación local sigue; banner "offline".
- Notificación push no soportada por el navegador → mensaje informativo en configuración; la app funciona sin recordatorios activos.
- BBDD corrupta → script de restore desde backup nocturno (ver ARQUITECTURA §6).

## 6. Criterios de éxito

| ID | Criterio | Métrica | Umbral |
|---|---|---|---|
| S01 | Captura rápida | Tiempo desde abrir la app hasta confirmar tarea creada (p95, usuario con manos libres) | < 5 s |
| S02 | Parsing de fechas en lenguaje natural | Porcentaje de frases "título + fecha coloquial" parseadas correctamente en un set de 50 ejemplos | ≥ 85 % |
| S03 | Sync offline→online | Tiempo máximo de reconciliación tras volver a conexión con ≤20 tareas pendientes | < 3 s |
| S04 | Notificación puntual | Desfase entre hora prevista y recepción de la notificación, en server saludable | ± 5 min |
| S05 | Recursos del server | Consumo de RAM del backend en uso típico (≤ 1000 tareas, 10 proyectos) | < 200 MB |

---

## Defaults aceptados durante el cierre

- Fecha por defecto para "jueves" (sin hora) → 09:00 local del usuario.
- Umbral de recordatorio global (no por tarea) → simplifica UI y cubre el 90% de casos.
- Auto-purga de completadas a los 30 días → evita crecimiento indefinido.

## Defaults rechazados

- Sugerencia: "multi-usuario con roles desde V1" → rechazado: el JTBD es personal; complejidad no justificada.
- Sugerencia: "prioridades P0/P1/P2 en V1" → rechazado: se pospone a V2; V1 usa orden manual.

## Handoff

Spec cerrada. Siguiente fase: `@domain-modeler` para extraer entidades, ciclo de vida de la tarea y matriz de capacidades.
