# CATÁLOGO

## §1 Endpoints (API HTTP)

| Método | Ruta | Propósito | Módulo | Estado |
|---|---|---|---|---|
| POST | /api/tasks | Crear tarea | Api/tasks | SEED |
| GET | /api/tasks | Listar tareas (filtros: estado, proyecto, vista=hoy) | Api/tasks | SEED |
| PATCH | /api/tasks/:id | Editar tarea (título, fecha, proyecto) | Api/tasks | SEED |
| POST | /api/tasks/:id/complete | Marcar completada | Api/tasks | SEED |
| POST | /api/tasks/:id/undo | Deshacer completada | Api/tasks | SEED |
| DELETE | /api/tasks/:id | Eliminar | Api/tasks | SEED |
| GET | /api/projects | Listar proyectos | Api/projects | SEED |
| POST | /api/projects | Crear proyecto | Api/projects | SEED |
| PATCH | /api/projects/:id | Renombrar / archivar | Api/projects | SEED |
| POST | /api/sync | Sync bulk offline→online (cliente envía delta) | Api/sync | SEED |
| POST | /api/push/subscribe | Registrar suscripción push del navegador | Api/push | SEED |
| GET | /api/settings | Obtener ajustes (umbral recordatorio, etc.) | Api/settings | SEED |
| PATCH | /api/settings | Actualizar ajustes | Api/settings | SEED |

## §2 Componentes UI

| Nombre | Propósito | Archivo | Reutilización |
|---|---|---|---|
| TaskQuickAdd | Input de captura rápida con parsing de fechas | src/components/TaskQuickAdd.tsx | SEED — pantalla principal, vista proyecto |
| TaskList | Lista virtualizada de tareas con swipe (móvil) | src/components/TaskList.tsx | SEED — todas las vistas |
| TaskItem | Fila individual, checkbox + título + fecha relativa | src/components/TaskItem.tsx | SEED — dentro de TaskList |
| ProjectSidebar | Sidebar con proyectos + contadores | src/components/ProjectSidebar.tsx | SEED |
| TodayView | Vista "hoy" con vencidas + hoy agrupadas | src/pages/TodayView.tsx | SEED |
| PushSettings | Solicitar permiso de notificaciones, mostrar estado | src/components/PushSettings.tsx | SEED |

## §3 Módulos internos

| Nombre | Responsabilidad | Archivo principal | API expuesta |
|---|---|---|---|
| domain/task | Entidad Tarea, invariantes, parser de fechas natural | src/domain/task/index.ts | `createTask`, `parseNaturalDate`, `canComplete` |
| domain/project | Entidad Proyecto | src/domain/project/index.ts | `createProject`, `archive` |
| application/task | Casos de uso de tareas | src/application/task/*.ts | `CrearTarea`, `CompletarTarea`, `EditarTarea` |
| application/reminders | Generación y disparo de recordatorios | src/application/reminders/index.ts | `scheduleReminders`, `dispatchDue` |
| infra/repo | Repositorios SQLite con better-sqlite3 | src/infra/repo/*.ts | `TaskRepo`, `ProjectRepo`, `SettingsRepo` |
| infra/push | Envío de notificaciones web-push | src/infra/push/index.ts | `sendPush`, `registerSubscription` |
| web/store | Store Zustand con middleware IndexedDB | src/web/store/index.ts | hooks `useTasks`, `useProjects`, `useSync` |
| web/pwa | Service Worker, manifest, install prompts | src/web/pwa/* | handlers de push + offline cache |

## §4 Utilidades compartidas

| Nombre | Uso | Archivo |
|---|---|---|
| result | Tipo `Result<T, E>` con helpers `ok`, `err`, `map`, `andThen` | src/shared/result.ts |
| clock | Abstracción de `Date.now()` para test determinísticos | src/shared/clock.ts |
| logger | Instancia de pino configurada por entorno | src/shared/logger.ts |
| id | Generador de IDs (nanoid, 21 chars) | src/shared/id.ts |
