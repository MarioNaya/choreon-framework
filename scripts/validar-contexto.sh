#!/usr/bin/env bash
# validar-contexto.sh — Verifica invariantes de docs/sesion/CONTEXTO.md
#   1. ≤ 80 líneas
#   2. Las 6 secciones fijas presentes y en orden
# Uso: bash scripts/validar-contexto.sh [ruta]  (por defecto: docs/sesion/CONTEXTO.md)

set -euo pipefail

FILE="${1:-docs/sesion/CONTEXTO.md}"

if [[ ! -f "$FILE" ]]; then
  echo "✗ No existe: $FILE" >&2
  exit 1
fi

LINES=$(wc -l < "$FILE")
if (( LINES > 80 )); then
  echo "✗ CONTEXTO.md tiene $LINES líneas (>80). Compactar."
  EXIT=1
else
  echo "✓ Líneas: $LINES / 80"
  EXIT=0
fi

EXPECTED=(
  "## Estado actual"
  "## Bloqueados"
  "## Deuda técnica"
  "## Próxima tarea"
  "## Mocks disponibles"
  "## Convenciones activas"
)

PREV_LINE=-1
for section in "${EXPECTED[@]}"; do
  LINE_NO=$(grep -n -F "$section" "$FILE" | head -1 | cut -d: -f1 || true)
  if [[ -z "$LINE_NO" ]]; then
    echo "✗ Falta sección: $section"
    EXIT=1
  elif (( LINE_NO <= PREV_LINE )); then
    echo "✗ Sección fuera de orden: $section (línea $LINE_NO)"
    EXIT=1
  else
    echo "✓ $section (línea $LINE_NO)"
    PREV_LINE=$LINE_NO
  fi
done

exit $EXIT
