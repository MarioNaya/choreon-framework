---
applyTo: "src/components/**/*.tsx"
---

# Instrucciones — Frontend TypeScript

## Stack

- Framework UI a definir en ARQUITECTURA (React 18, Vue 3, Svelte 5 u otros).
- Build: Vite.
- Estilos: a elección del arquitecto (Tailwind, CSS modules, styled-components…).
- State: local primero; si necesita global, preferir la opción más simple compatible con el framework UI.

## Convenciones

- Props tipadas siempre (interfaces o type aliases).
- Componentes de presentación **sin** llamadas a API — delegar en services/hooks.
- Selectores estables para testing: `data-testid` en elementos interactivos.
- Accesibilidad: roles ARIA cuando no haya semántica HTML nativa; etiquetas asociadas a inputs; contraste AA mínimo.

## Anti-patrones

- `useEffect` con arrays de dependencias incompletos.
- Mezclar estado local y global sin criterio claro.
- Estilos inline salvo puntos muy específicos.
- Lógica de negocio en componentes — debería vivir en hooks o services.

## Testing

- Snapshot para componentes puramente presentacionales.
- Tests de comportamiento (clic, input, fetch) para componentes con lógica.
- E2E solo para flujos críticos identificados en `COBERTURA.md`.
