---
applyTo: "[[FRONTEND_GLOB]]"
---

<!--
Plantilla para código frontend/UI.
Reemplaza [[FRONTEND_GLOB]] (ej: "src/components/**/*.tsx", "app/**/*.vue").
-->

# Instrucciones — Frontend

## Framework y estilo

<!-- RELLENAR -->

- Framework: [[React 18 / Vue 3 / Svelte 5 / …]]
- Estilos: [[Tailwind / CSS modules / styled-components / …]]
- State management: [[Redux / Zustand / Pinia / señales nativas / …]]
- Router: [[nombre + versión]]

## Estructura de componentes

<!-- RELLENAR -->

```
src/
├── components/       # Componentes reutilizables
│   ├── common/
│   └── [feature]/
├── pages/            # Rutas
├── services/         # Llamadas a API
└── hooks/ | stores/  # Lógica compartida
```

## Convenciones

- Cada componente tiene **selectores estables** para testing: [[atributo, p. ej. `data-testid`]].
- No usar estilos en línea salvo en componentes muy puntuales; preferir clases.
- Props tipadas siempre.

## Accesibilidad

- Roles ARIA cuando no haya semántica HTML nativa.
- Etiquetas asociadas a inputs.
- Contraste mínimo AA.

## Anti-patrones

- Llamadas a API directamente en componentes de presentación (usar services/hooks).
- `useEffect` con arrays de dependencias incompletos.
- Mezclar estado global con estado local sin justificación.

## Testing de componentes

- Cada componente presentacional: snapshot o render test básico.
- Cada componente con lógica: tests de comportamiento (clic, input, fetch).
- E2E solo para flujos críticos identificados en `COBERTURA.md`.

## Referencia a decisiones vigentes

Cita §Categoría de `DECISIONES.md` cuando una regla de UI venga de ahí.
