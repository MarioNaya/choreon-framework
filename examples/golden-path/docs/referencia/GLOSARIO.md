# GLOSARIO

| Término | Definición | Alias | Dónde se usa |
|---|---|---|---|
| Captura | Acto de crear una Tarea con fricción mínima (<5s). | inbox, quick-add | UI pantalla principal, S01 |
| Fecha límite | Timestamp opcional tras el cual una Tarea aparece como "vencida". | deadline, due_at | Tarea, vista "hoy" |
| Notificación push | Aviso enviado por el navegador (Web Push API) al acercarse `fecha_limite`. | recordatorio, push | Recordatorio, C06 |
| Proyecto | Contenedor opcional que agrupa Tareas bajo un nombre. | lista, carpeta | Tarea, UI sidebar |
| PWA | Progressive Web App instalable en móvil/escritorio con soporte offline y push. | — | ARQUITECTURA §1 |
| Sync | Reconciliación entre datos locales (IndexedDB) y remotos (backend) cuando vuelve la conectividad. | sincronización | ARQUITECTURA §3, edge case offline |
| Tarea | Unidad mínima de trabajo a recordar. Estados: Pendiente, Completada. | to-do, item | Entidad principal |
| Umbral de recordatorio | Número de horas antes de `fecha_limite` al que se dispara la notificación. Configurable global. | reminder_window | Ajustes, C06 |
| Vencida | Tarea Pendiente con `fecha_limite` anterior al momento actual. | atrasada | vista "hoy" |
| Vista "hoy" | Pantalla que agrupa tareas vencidas + que vencen hoy. | today view | UI |
