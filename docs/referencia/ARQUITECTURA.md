# ARQUITECTURA

<!--
Plantilla rellenada por @architect durante /bootstrap fase 3.
Cambios posteriores requieren handoff explícito a @architect y actualización de DECISIONES.
-->

## §1 Stack

| Capa | Tecnología | Versión | Motivo |
|---|---|---|---|
| Lenguaje | [[ej. TypeScript]] | [[versión]] | [[razón]] |
| Framework backend | [[ej. NestJS]] | [[versión]] | [[razón]] |
| Framework frontend | [[ej. React]] | [[versión]] | [[razón]] |
| Persistencia | [[ej. PostgreSQL]] | [[versión]] | [[razón]] |
| Mensajería (si aplica) | [[ej. RabbitMQ]] | [[versión]] | [[razón]] |
| Testing | [[unit / int / e2e tools]] | [[versiones]] | [[razón]] |

## §2 Patrón global

Patrón elegido: **[[monolito modular / hexagonal / microservicios / serverless / …]]**

Motivación: [[por qué este y no otro, referido al alcance de la spec]]

## §3 Módulos y dependencias

```mermaid
graph TD
    [[Presentacion]] --> [[Aplicacion]]
    [[Aplicacion]] --> [[Dominio]]
    [[Aplicacion]] --> [[Infraestructura]]
    [[Infraestructura]] --> [[Dominio]]
```

| Módulo | Responsabilidad | Depende de |
|---|---|---|
| [[Dominio]] | [[entidades, reglas invariantes]] | — |
| [[Aplicacion]] | [[casos de uso, orquestación]] | Dominio |
| [[Infraestructura]] | [[persistencia, integración externa]] | Dominio |
| [[Presentacion]] | [[HTTP/UI]] | Aplicacion |

## §4 Dependencias prohibidas

- [[Dominio no importa Infraestructura]]
- [[Presentacion no importa Dominio directamente]]
- [[otras reglas estructurales]]

## §5 Convenciones transversales

- **Naming:** [[camelCase / snake_case / etc.]]
- **Gestión de errores:** [[excepciones / Result / …]]
- **Logging:** [[nivel por defecto, formato JSON/texto]]
- **Validación:** [[en capa Aplicacion / en boundary Presentacion]]
- **Inyección de dependencias:** [[tool o patrón]]

## §6 Pirámide de testing

| Nivel | Porcentaje objetivo | Herramienta | Alcance |
|---|---|---|---|
| Unit | [[70%]] | [[tool]] | [[qué verifican]] |
| Integración | [[20%]] | [[tool]] | [[qué verifican]] |
| E2E | [[10%]] | [[tool]] | [[qué verifican]] |

Cobertura mínima: **[[X%]]**.
