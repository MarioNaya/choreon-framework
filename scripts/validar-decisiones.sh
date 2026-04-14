#!/usr/bin/env bash
# validar-decisiones.sh — Verifica invariantes de docs/sesion/DECISIONES.md
#   1. Las 8 categorías presentes y en orden
#   2. Ningún bullet duplicado entre categorías
#   3. Sin referencias cronológicas ("el martes", "nuevo hoy", etc.)
#   4. Si existe .bak.md, alerta si hay diffs no triviales
# Uso: bash scripts/validar-decisiones.sh [ruta]  (por defecto: docs/sesion/DECISIONES.md)

set -euo pipefail

FILE="${1:-docs/sesion/DECISIONES.md}"
BAK="${FILE%.md}.bak.md"

if [[ ! -f "$FILE" ]]; then
  echo "✗ No existe: $FILE" >&2
  exit 1
fi

EXIT=0

# 1. Las 8 categorías en orden
CATEGORIES=(
  "## 1. Filosofía de desarrollo"
  "## 2. Stack"
  "## 3. Arquitectura"
  "## 4. Convenciones de código"
  "## 5. Testing"
  "## 6. Datos y persistencia"
  "## 7. Seguridad y auth"
  "## 8. Despliegue"
)

PREV_LINE=-1
for cat in "${CATEGORIES[@]}"; do
  LINE_NO=$(grep -n -F "$cat" "$FILE" | head -1 | cut -d: -f1 || true)
  if [[ -z "$LINE_NO" ]]; then
    echo "✗ Falta categoría: $cat"
    EXIT=1
  elif (( LINE_NO <= PREV_LINE )); then
    echo "✗ Categoría fuera de orden: $cat (línea $LINE_NO)"
    EXIT=1
  else
    echo "✓ $cat (línea $LINE_NO)"
    PREV_LINE=$LINE_NO
  fi
done

# 2. Duplicados entre categorías (aprox: bullets que se repiten literales)
DUPLICATES=$(grep -E "^- " "$FILE" | sort | uniq -d || true)
if [[ -n "$DUPLICATES" ]]; then
  echo "⚠ Bullets posiblemente duplicados:"
  echo "$DUPLICATES" | sed 's/^/    /'
  EXIT=1
fi

# 3. Referencias cronológicas
TEMPORAL_PATTERN="(lunes|martes|miércoles|jueves|viernes|sábado|domingo|ayer|hoy|mañana|nuevo el|hace [0-9])"
TEMPORAL_HITS=$(grep -iE "$TEMPORAL_PATTERN" "$FILE" || true)
if [[ -n "$TEMPORAL_HITS" ]]; then
  echo "⚠ Posibles referencias cronológicas (DECISIONES no debe tener historial):"
  echo "$TEMPORAL_HITS" | sed 's/^/    /'
  EXIT=1
fi

# 4. Diff vs backup si existe
if [[ -f "$BAK" ]]; then
  ADDED=$(diff "$BAK" "$FILE" | grep -c '^>' || true)
  REMOVED=$(diff "$BAK" "$FILE" | grep -c '^<' || true)
  if (( ADDED > 0 || REMOVED > 0 )); then
    echo "ℹ Diferencias vs backup: +$ADDED / -$REMOVED líneas"
    echo "  Verifica que los cambios coinciden con el resumen de sesión."
  else
    echo "✓ Sin cambios vs backup."
  fi
else
  echo "ℹ No existe backup $BAK (normal si aún no has ejecutado /actualizar-contexto)."
fi

exit $EXIT
