# Brief — Gestor de tareas personal con recordatorios

## Idea general

Una aplicación que me permita capturar tareas rápidamente desde el móvil o el ordenador, agruparlas por proyecto, y recibir recordatorios por notificación push cuando se acerque la fecha límite. Quiero que sea ágil: capturar una tarea debe costar menos de 5 segundos.

## Contexto del usuario/negocio

Lo uso yo personalmente. Tengo Todoist y Things probados y no termino de adoptarlos porque la captura es lenta o requieren pagar para lo básico. Quiero algo mío, simple, sin cuentas de otros. Usuario único — no es multi-tenant.

## Funcionalidades que imaginas

- Crear tarea con título y fecha opcional.
- Agrupar tareas por proyecto (máximo 1 proyecto por tarea).
- Marcar como completada.
- Recordatorio por notificación push cuando quedan X horas para la fecha límite.
- Lista "hoy" con lo vencido + lo que vence hoy.
- Sincronización entre móvil y ordenador.

## Restricciones conocidas

- Técnica: prefiero un único backend simple que sirva a una webapp responsive. No quiero app nativa aún.
- Negocio: es proyecto personal, sin presupuesto; debe poder autoalojarse.
- Compliance: GDPR básico — yo mismo soy el usuario, pero si algún día lo abro, que no viole nada obvio.

## Referencias

- Todoist (lo que quiero igualar en velocidad de captura)
- Things (lo que quiero igualar en sensación de "vacío" cuando no hay pendientes)

## Dudas abiertas

- ¿Compensa una BBDD relacional o puedo usar SQLite embebido?
- ¿Cómo gestiono las notificaciones push desde un backend autoalojado?
- ¿Qué hago con las tareas recurrentes? No las incluyo en V1, pero quiero que el modelo las admita luego.
