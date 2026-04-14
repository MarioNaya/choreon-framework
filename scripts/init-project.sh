#!/usr/bin/env bash
# init-project.sh — Wrapper que invoca scripts/init-project.py (cross-platform, sin sed).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
  echo "Error: se requiere Python 3 en el PATH." >&2
  exit 1
fi

PY=$(command -v python3 || command -v python)
exec "$PY" "$SCRIPT_DIR/init-project.py" "$@"
