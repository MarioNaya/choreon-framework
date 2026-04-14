"""
parser.py — Extrae la tabla de MATRIZ_PERMISOS.md como reglas ejecutables.

Entrada: texto markdown con la tabla de la sección "## Matriz".
Salida: dict {agent_name: list[Rule]}, donde Rule encapsula pattern + permission + note.
"""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path


# Permisos normalizados
PERM_WRITE = "W"
PERM_READ = "R"
PERM_NONE = "-"


@dataclass
class Rule:
    pattern: str            # glob o prefijo de ruta (p. ej. "specs/spec-cerrada-*.md")
    permission: str         # "W" | "R" | "-"
    note: str = ""          # metainformación: "append", "seed", "§Diagnóstico", etc.
    is_directory: bool = False  # True si termina en "/"
    is_abstract: bool = False   # True si el pattern no es una ruta de archivo (p. ej. "Repos vecinos read-only")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


# Patrones para limpiar la celda de permiso.
_CELL_RE = re.compile(r"\s*\*{0,2}(W|R|—|-)\*{0,2}\s*(.*)$")


def _clean_cell(raw: str) -> tuple[str, str]:
    """Extrae (permission, note) de una celda. Acepta '**W**', 'W (append)', 'R', '—'."""
    raw = raw.strip()
    if not raw:
        return PERM_NONE, ""
    # Normalizar em-dash a guion simple
    if raw in ("—", "-"):
        return PERM_NONE, ""
    m = _CELL_RE.match(raw)
    if not m:
        return PERM_NONE, ""
    perm_char = m.group(1)
    rest = (m.group(2) or "").strip()
    if perm_char == "—":
        return PERM_NONE, rest
    note = ""
    if rest:
        # "(append)" → "append"
        nm = re.match(r"^\(([^)]+)\)\s*$", rest)
        if nm:
            note = nm.group(1).strip()
        else:
            # Otras formas: "completo" tras la celda, etc.
            note = rest
    return perm_char, note


def _clean_path_cell(raw: str) -> tuple[str, bool, bool]:
    """Extrae el path de la primera columna.
    Retorna (pattern, is_directory, is_abstract)."""
    raw = raw.strip()
    # Quitar backticks
    m = re.match(r"^`([^`]+)`", raw)
    if m:
        pattern = m.group(1).strip()
        is_dir = pattern.endswith("/")
        return pattern, is_dir, False
    # Texto sin backticks → path abstracto (ej. "Repos vecinos read-only")
    return raw.strip(), False, True


def parse_matrix(text: str) -> dict[str, list[Rule]]:
    """Parses the markdown matrix and returns {agent: [Rule, ...]}."""
    lines = text.splitlines()
    # Localiza la tabla: primera línea con "| Archivo / Ruta |" en sección Matriz
    header_idx = None
    for i, line in enumerate(lines):
        if "Archivo / Ruta" in line and line.strip().startswith("|"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("No se encontró el header de la tabla de MATRIZ_PERMISOS.md")

    # Header row
    header_cells = [c.strip() for c in lines[header_idx].strip("|").split("|")]
    agents = header_cells[1:]  # primera col es "Archivo / Ruta"

    # Siguiente línea suele ser separador |---|:-:|... — saltarlo
    data_start = header_idx + 1
    while data_start < len(lines) and re.match(r"^\|\s*[-:|\s]+\s*\|?$", lines[data_start].strip()):
        data_start += 1

    result: dict[str, list[Rule]] = {a: [] for a in agents}

    for line in lines[data_start:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            break  # fin de la tabla
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != len(header_cells):
            continue  # fila malformada, ignorar
        pattern, is_dir, is_abstract = _clean_path_cell(cells[0])
        for agent, raw in zip(agents, cells[1:]):
            perm, note = _clean_cell(raw)
            result[agent].append(
                Rule(
                    pattern=pattern,
                    permission=perm,
                    note=note,
                    is_directory=is_dir,
                    is_abstract=is_abstract,
                )
            )
    return result


# ---------------------------------------------------------------------------
# Resolución de permisos
# ---------------------------------------------------------------------------


def _matches_pattern(rel_path: str, pattern: str, is_directory: bool) -> bool:
    """Check if a relative path matches the pattern.
    - Exact path match (`docs/sesion/CONTEXTO.md`).
    - Glob match (`specs/spec-cerrada-*.md`).
    - Directory prefix (`specs/historico/` matches anything under it).
    - Skips unresolved placeholders `[[...]]`.
    - Abstract labels (e.g. 'Repos vecinos read-only') are never matched positively.
    """
    if "[[" in pattern:
        return False
    if is_directory:
        # Aceptar cualquier ruta bajo ese prefijo
        prefix = pattern.rstrip("/") + "/"
        return rel_path.startswith(prefix)
    # fnmatch soporta *, ?, [seq]
    return fnmatch.fnmatchcase(rel_path, pattern) or rel_path == pattern


def check_access(agent: str, rel_path: str, op: str, rules_by_agent: dict[str, list[Rule]]) -> tuple[bool, str]:
    """Returns (allowed, reason).
    op is 'read' or 'write'.
    Policy:
      - Find all rules for `agent` whose pattern matches `rel_path` (and is not abstract).
      - For write: allow if at least one matched rule has permission W.
      - For read: allow if at least one matched rule has W or R.
      - If no rule matches → deny by default (safe fallback).
    """
    if agent not in rules_by_agent:
        return False, f"Agente desconocido: {agent}"

    matched: list[Rule] = []
    for rule in rules_by_agent[agent]:
        if rule.is_abstract:
            continue
        if _matches_pattern(rel_path, rule.pattern, rule.is_directory):
            matched.append(rule)

    if not matched:
        return False, f"Sin regla aplicable para {agent!r} sobre {rel_path!r}. Denegado por defecto."

    if op == "write":
        writers = [r for r in matched if r.permission == PERM_WRITE]
        if writers:
            note = writers[0].note
            suffix = f" (nota: {note})" if note else ""
            return True, f"write permitido por regla '{writers[0].pattern}'{suffix}"
        return False, f"write denegado: ninguna regla da W a {agent!r} sobre {rel_path!r}"

    if op == "read":
        readable = [r for r in matched if r.permission in (PERM_WRITE, PERM_READ)]
        if readable:
            return True, f"read permitido por regla '{readable[0].pattern}'"
        return False, f"read denegado: {agent!r} no tiene R/W sobre {rel_path!r}"

    return False, f"Operación desconocida: {op}"


def list_permissions(agent: str, rules_by_agent: dict[str, list[Rule]]) -> dict[str, list[str]]:
    """Introspección: devuelve {W: [...], R: [...], -: [...]} para el agente."""
    result: dict[str, list[str]] = {PERM_WRITE: [], PERM_READ: [], PERM_NONE: []}
    if agent not in rules_by_agent:
        return result
    for rule in rules_by_agent[agent]:
        label = rule.pattern
        if rule.note:
            label = f"{label} ({rule.note})"
        if rule.is_abstract:
            label = f"{label} [abstract]"
        if "[[" in rule.pattern:
            label = f"{label} [placeholder sin resolver]"
        result[rule.permission].append(label)
    return result


# ---------------------------------------------------------------------------
# Helpers de carga
# ---------------------------------------------------------------------------


def load_matrix_from_file(matrix_path: Path) -> dict[str, list[Rule]]:
    if not matrix_path.exists():
        raise FileNotFoundError(f"No existe {matrix_path}")
    text = matrix_path.read_text(encoding="utf-8")
    return parse_matrix(text)
