"""
memory-mcp — Servidor MCP que expone CONTEXTO.md y DECISIONES.md como herramientas queryables.

Uso:
    python server.py                    # arranca el servidor en modo stdio (para Claude Code / Copilot MCP)
    python server.py --test              # ejecuta smoke test sin MCP (útil en CI)

Herramientas expuestas:
    get_context()                 → resumen compacto del CONTEXTO actual
    get_section(name)             → una sección concreta de CONTEXTO
    get_decision(category)        → bullets de una categoría de DECISIONES
    get_blockers()                → §Bloqueados
    get_next_task()               → §Próxima tarea
    record_decision(category, text) → añade bullet a DECISIONES in-place, creando backup

Antes de modificar DECISIONES, crea `DECISIONES.bak.md` — replica la lógica del agente context-manager.

Requiere: pip install "mcp>=1.0"
Modo --test no requiere mcp instalado.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Permite importar parser.py del mismo directorio
sys.path.insert(0, str(Path(__file__).parent))
from parser import (  # noqa: E402
    append_decision_in_place,
    parse_contexto,
    parse_decisiones,
)

# Raíz del proyecto = dos niveles arriba (scripts/mcp/memory-server/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONTEXTO_PATH = PROJECT_ROOT / "docs" / "sesion" / "CONTEXTO.md"
DECISIONES_PATH = PROJECT_ROOT / "docs" / "sesion" / "DECISIONES.md"


# ---------------------------------------------------------------------------
# Núcleo de negocio (sin MCP) — testeable en aislado
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def tool_get_context() -> str:
    ctx = parse_contexto(_read(CONTEXTO_PATH))
    if not ctx.sections:
        return "CONTEXTO.md vacío o no inicializado. Ejecuta /bootstrap."
    lines = [f"# Sesión {ctx.session} — actualizado {ctx.last_update}", ""]
    for name, body in ctx.sections.items():
        lines.append(f"## {name}")
        lines.append(body)
        lines.append("")
    return "\n".join(lines)


def tool_get_section(name: str) -> str:
    ctx = parse_contexto(_read(CONTEXTO_PATH))
    body = ctx.get_section(name)
    if body is None:
        return f"Sección no encontrada: {name!r}. Secciones disponibles: {list(ctx.sections.keys())}"
    return body


def tool_get_decision(category: str) -> str:
    dec = parse_decisiones(_read(DECISIONES_PATH))
    bullets = dec.get_category(category)
    if not bullets:
        return f"Sin decisiones registradas en la categoría: {category!r}"
    return "\n".join(f"- {b}" for b in bullets)


def tool_get_blockers() -> str:
    return tool_get_section("Bloqueados")


def tool_get_next_task() -> str:
    return tool_get_section("Próxima tarea")


def tool_record_decision(category: str, text: str) -> str:
    if not DECISIONES_PATH.exists():
        return "Error: DECISIONES.md no existe todavía. Ejecuta /bootstrap primero."
    # Backup antes de modificar (contrato del context-manager)
    bak_path = DECISIONES_PATH.with_name("DECISIONES.bak.md")
    shutil.copy2(DECISIONES_PATH, bak_path)
    original = _read(DECISIONES_PATH)
    try:
        new_text = append_decision_in_place(original, category, text)
    except ValueError as e:
        return f"Error: {e}"
    _write(DECISIONES_PATH, new_text)
    return f"Decisión añadida a '{category}'. Backup en {bak_path.name}."


# ---------------------------------------------------------------------------
# Modo --test (smoke test sin MCP)
# ---------------------------------------------------------------------------


def run_smoke_test() -> int:
    """Smoke test: verifica que los parsers leen CONTEXTO y DECISIONES actuales."""
    errors: list[str] = []

    if not CONTEXTO_PATH.exists():
        errors.append(f"No existe {CONTEXTO_PATH}")
    if not DECISIONES_PATH.exists():
        errors.append(f"No existe {DECISIONES_PATH}")

    if errors:
        for e in errors:
            print(f"✗ {e}", file=sys.stderr)
        return 1

    ctx = parse_contexto(_read(CONTEXTO_PATH))
    dec = parse_decisiones(_read(DECISIONES_PATH))

    print(f"✓ Parse CONTEXTO: sesión {ctx.session}, {len(ctx.sections)} secciones")
    print(f"✓ Parse DECISIONES: {len(dec.categories)} categorías")

    # Verifica que las 8 categorías canónicas están
    from parser import DECISIONES_CATEGORIES

    missing = [c for c in DECISIONES_CATEGORIES if c not in dec.categories]
    if missing:
        print(f"⚠ Faltan categorías: {missing}")
        return 1
    print(f"✓ Las 8 categorías canónicas presentes")

    # Verifica tool_get_next_task
    next_task = tool_get_next_task()
    print(f"✓ tool_get_next_task devuelve {len(next_task)} chars")

    # Verifica tool_get_decision por nombre y por número
    stack_by_name = tool_get_decision("Stack")
    stack_by_num = tool_get_decision("2")
    if stack_by_name != stack_by_num:
        print(f"⚠ get_decision('Stack') != get_decision('2')")
        return 1
    print(f"✓ tool_get_decision acepta nombre y número")

    return 0


# ---------------------------------------------------------------------------
# Modo MCP (servidor stdio)
# ---------------------------------------------------------------------------


def run_mcp_server() -> int:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        print(
            "Error: paquete 'mcp' no instalado. Instala con: pip install 'mcp>=1.0'",
            file=sys.stderr,
        )
        return 2

    mcp = FastMCP("memory-mcp")

    @mcp.tool()
    def get_context() -> str:
        """Devuelve el CONTEXTO.md completo (sesión, estado, bloqueantes, próxima tarea, convenciones)."""
        return tool_get_context()

    @mcp.tool()
    def get_section(name: str) -> str:
        """Devuelve una sección concreta del CONTEXTO (p. ej. 'Bloqueados', 'Convenciones activas')."""
        return tool_get_section(name)

    @mcp.tool()
    def get_decision(category: str) -> str:
        """Devuelve los bullets de una categoría de DECISIONES (por nombre o por número 1-8)."""
        return tool_get_decision(category)

    @mcp.tool()
    def get_blockers() -> str:
        """Devuelve la sección §Bloqueados del CONTEXTO."""
        return tool_get_blockers()

    @mcp.tool()
    def get_next_task() -> str:
        """Devuelve la sección §Próxima tarea del CONTEXTO."""
        return tool_get_next_task()

    @mcp.tool()
    def record_decision(category: str, text: str) -> str:
        """Añade un bullet nuevo a una categoría de DECISIONES, creando backup (.bak.md) antes."""
        return tool_record_decision(category, text)

    mcp.run()
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="Smoke test sin MCP (útil en CI)")
    args = ap.parse_args()

    if args.test:
        return run_smoke_test()
    return run_mcp_server()


if __name__ == "__main__":
    sys.exit(main())
