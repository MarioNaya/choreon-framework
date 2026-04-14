"""
parser.py — Parser minimalista para CONTEXTO.md y DECISIONES.md.

Expone funciones puras, sin I/O, testeables.
El server.py envuelve estas funciones sobre lectura/escritura de archivos.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# CONTEXTO.md
# ---------------------------------------------------------------------------

CONTEXTO_SECTIONS = [
    "Estado actual",
    "Bloqueados",
    "Deuda técnica",
    "Próxima tarea",
    "Mocks disponibles",
    "Convenciones activas",
]


@dataclass
class Contexto:
    session: str  # ej. "S44"
    last_update: str  # ej. "2026-04-14"
    sections: dict[str, str]  # nombre → texto de la sección

    def get_section(self, name: str) -> str | None:
        return self.sections.get(name)


def parse_contexto(text: str) -> Contexto:
    """Parses CONTEXTO.md. Sections are ## headers matching CONTEXTO_SECTIONS."""
    session_match = re.search(r"sesión\s+(S\d+)", text)
    update_match = re.search(r"Última actualización:\s*([^\n]+)", text)
    session = session_match.group(1) if session_match else "S?"
    last_update = update_match.group(1).strip() if update_match else ""

    sections: dict[str, str] = {}
    # Match ## <section-name> and capture until next ## or end.
    for name in CONTEXTO_SECTIONS:
        pattern = re.compile(
            rf"^##\s+{re.escape(name)}\s*\n(.*?)(?=^##\s+|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        m = pattern.search(text)
        if m:
            sections[name] = m.group(1).strip()
    return Contexto(session=session, last_update=last_update, sections=sections)


# ---------------------------------------------------------------------------
# DECISIONES.md
# ---------------------------------------------------------------------------

DECISIONES_CATEGORIES = [
    "Filosofía de desarrollo",
    "Stack",
    "Arquitectura",
    "Convenciones de código",
    "Testing",
    "Datos y persistencia",
    "Seguridad y auth",
    "Despliegue",
]


@dataclass
class Decisiones:
    last_update: str
    categories: dict[str, list[str]]  # category name → list of bullet texts

    def get_category(self, name: str) -> list[str]:
        # Permite búsqueda tolerante (case-insensitive, sin ordinal).
        needle = name.strip().lower()
        for key, bullets in self.categories.items():
            if key.lower() == needle or key.lower().endswith(needle):
                return bullets
        # También acepta número como "5" o "5." (índice 1-based sobre la lista canónica)
        if needle.rstrip(".").isdigit():
            idx = int(needle.rstrip(".")) - 1
            if 0 <= idx < len(DECISIONES_CATEGORIES):
                canonical = DECISIONES_CATEGORIES[idx]
                return self.categories.get(canonical, [])
        return []


def parse_decisiones(text: str) -> Decisiones:
    """Parses DECISIONES.md. Categories are '## N. <name>' headers."""
    update_match = re.search(r"Última actualización:\s*([^\n]+)", text)
    last_update = update_match.group(1).strip() if update_match else ""

    categories: dict[str, list[str]] = {}
    # Find all "## N. <name>" headers and capture bullets until next category or EOF.
    header_re = re.compile(r"^##\s+\d+\.\s+(.+?)\s*$", re.MULTILINE)
    headers = list(header_re.finditer(text))
    for i, m in enumerate(headers):
        name = m.group(1).strip()
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end]
        bullets = re.findall(r"^\s*-\s+(.+?)$", body, flags=re.MULTILINE)
        # Filtrar comentarios HTML o líneas vacías
        bullets = [b.strip() for b in bullets if b.strip() and not b.strip().startswith("<!--")]
        categories[name] = bullets
    return Decisiones(last_update=last_update, categories=categories)


def append_decision_in_place(text: str, category: str, bullet: str) -> str:
    """Adds a new bullet to the given category, in-place. Returns the new text.
    Raises ValueError if the category is not found."""
    # Acepta matching case-insensitive
    header_re = re.compile(r"^(##\s+\d+\.\s+)(.+?)(\s*)$", re.MULTILINE)
    needle = category.strip().lower()
    target = None
    for m in header_re.finditer(text):
        if m.group(2).strip().lower() == needle:
            target = m
            break
    if target is None:
        # Permite el número de categoría como alias
        if needle.rstrip(".").isdigit():
            idx = int(needle.rstrip(".")) - 1
            if 0 <= idx < len(DECISIONES_CATEGORIES):
                canonical = DECISIONES_CATEGORIES[idx]
                return append_decision_in_place(text, canonical, bullet)
        raise ValueError(f"Categoría no encontrada: {category!r}")

    # Localiza el final de la categoría (antes del próximo "## " o EOF)
    after = text[target.end() :]
    next_cat = re.search(r"^##\s+", after, re.MULTILINE)
    insert_pos = target.end() + (next_cat.start() if next_cat else len(after))

    # Asegura que hay un salto de línea antes del bullet nuevo
    section = text[target.end() : insert_pos]
    if not section.endswith("\n"):
        section_fixed = section + "\n"
        diff = 1
    else:
        section_fixed = section
        diff = 0

    new_bullet = f"- {bullet.strip()}\n"
    # Inserta al final de la sección, antes del próximo encabezado
    new_text = (
        text[: target.end()] + section_fixed.rstrip() + "\n" + new_bullet + ("" if next_cat else "") + text[insert_pos:]
    )
    # Normaliza fin de línea
    return new_text if diff == 0 else new_text
