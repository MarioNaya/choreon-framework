#!/usr/bin/env bash
# sync-agents.sh — Wrapper que llama al generador real en Python.
# El trabajo real lo hace scripts/sync-agents.py (adaptación de front-matter por herramienta).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
  echo "Error: se requiere Python 3 en el PATH." >&2
  echo "Windows: C:\\Users\\mario\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" >&2
  exit 1
fi

PY=$(command -v python3 || command -v python)
exec "$PY" "$SCRIPT_DIR/sync-agents.py" "$@"
