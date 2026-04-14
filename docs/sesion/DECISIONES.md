# DECISIONES

<!--
Editado in-place por @context-manager.
8 categorías fijas. Cada bullet ≤2 líneas. Sin cronología.
Si el archivo supera 100 líneas, migrar las entradas menos relevantes a docs/archivo/DECISIONES_HISTORICO.md.
-->

Última actualización: [[YYYY-MM-DD]]

## 1. Filosofía de desarrollo

- [[Principios transversales: DRY/KISS/YAGNI/etc., nivel de documentación esperado, trade-offs aceptados]]
- [[Ej: "Los cambios incluyen pruebas en el mismo commit"]]

## 2. Stack

- Lenguaje: [[lenguaje + versión]]
- Framework principal: [[nombre + versión]]
- Persistencia: [[motor + versión]]
- Testing: [[herramientas unit / integración / e2e]]
- Gestión de dependencias: [[tool]]

## 3. Arquitectura

- Patrón global: [[monolito modular / hexagonal / microservicios / …]]
- Módulos principales: [[nombres]]
- Dependencias prohibidas: [[ej. dominio no importa infraestructura]]

## 4. Convenciones de código

- Idioma de identificadores: [[en / es]]
- Naming: [[camelCase / snake_case / PascalCase por tipo]]
- Gestión de errores: [[excepciones / Result / …]]
- Logging: [[nivel por defecto, formato]]
- Comentarios: [[política — cuándo sí / cuándo no]]

## 5. Testing

- Pirámide objetivo: [[%unit / %int / %e2e]]
- Cobertura mínima: [[X%]]
- Comandos: [[cómo correr cada tipo]]
- Prohibido: [[sleeps fijos, mocks de base de datos, etc.]]

## 6. Datos y persistencia

- Migraciones: [[herramienta + política]]
- Seed data: [[fuente + cuándo se regenera]]
- Transacciones: [[política]]

## 7. Seguridad y auth

- Método auth: [[OAuth2 / JWT / sesión / …]]
- Secrets: [[dónde viven]]
- Sanitización/validación: [[en qué capa]]

## 8. Despliegue

- Entornos: [[lista]]
- Pipeline CI: [[referencia a .github/workflows]]
- Estrategia de release: [[tag / canary / blue-green / …]]
