"""
fs-guard-mcp — Servidor MCP que aplica MATRIZ_PERMISOS.md como enforcement real.

Cada instancia del servidor corre con la identidad de UN agente (flag --agent).
Tools expuestas al cliente:
    read_file(path)            → lee el archivo si el agente tiene R/W; error si no
    write_file(path, content)  → escribe si el agente tiene W; error si no
    list_allowed_paths()       → introspección: qué puede leer/escribir este agente

Uso:
    python server.py --agent spec-analyst              # arranca servidor MCP stdio
    python server.py --test                             # smoke test sin MCP (todos los agentes)
    python server.py --agent X --check PATH --op OP    # one-shot: prueba una decisión sin servir

Si MATRIZ_PERMISOS.md contiene placeholders [[PROJECT_SRC_GLOB]] etc. sin resolver,
el servidor deniega por defecto cualquier ruta que solo matchease esos patterns —
seguridad antes que conveniencia. Resuelve los placeholders con scripts/init-project.sh.

Requiere: pip install "mcp>=1.0"  (solo para modo servidor; --test y --check no lo requieren)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser import (  # noqa: E402
    check_access,
    list_permissions,
    load_matrix_from_file,
)

# Raíz del proyecto = 3 niveles arriba de este script
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MATRIX_PATH = PROJECT_ROOT / "docs" / "guias" / "MATRIZ_PERMISOS.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_path(path: str) -> str:
    """Normaliza a path relativo con '/' unix; rechaza path traversal."""
    p = Path(path)
    if p.is_absolute():
        try:
            rel = p.relative_to(PROJECT_ROOT)
        except ValueError:
            raise ValueError(f"Path fuera del proyecto: {path}")
    else:
        rel = p
    norm = rel.as_posix()
    if ".." in norm.split("/"):
        raise ValueError(f"Path con traversal no permitido: {path}")
    return norm


# ---------------------------------------------------------------------------
# Lógica pura (testeable)
# ---------------------------------------------------------------------------


def do_read(agent: str, path: str, rules) -> tuple[bool, str]:
    try:
        rel = _normalize_path(path)
    except ValueError as e:
        return False, str(e)
    ok, why = check_access(agent, rel, "read", rules)
    if not ok:
        return False, why
    abs_path = PROJECT_ROOT / rel
    if not abs_path.exists():
        return False, f"read permitido pero el archivo no existe: {rel}"
    try:
        return True, abs_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Error leyendo {rel}: {e}"


def do_write(agent: str, path: str, content: str, rules) -> tuple[bool, str]:
    try:
        rel = _normalize_path(path)
    except ValueError as e:
        return False, str(e)
    ok, why = check_access(agent, rel, "write", rules)
    if not ok:
        return False, why
    abs_path = PROJECT_ROOT / rel
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        abs_path.write_text(content, encoding="utf-8")
        return True, f"OK ({why})"
    except Exception as e:
        return False, f"Error escribiendo {rel}: {e}"


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------


def run_smoke_test() -> int:
    if not MATRIX_PATH.exists():
        print(f"✗ No existe {MATRIX_PATH}", file=sys.stderr)
        return 1
    try:
        rules = load_matrix_from_file(MATRIX_PATH)
    except Exception as e:
        print(f"✗ Error parseando matriz: {e}", file=sys.stderr)
        return 1

    print(f"✓ Matriz parseada: {len(rules)} agentes, {sum(len(r) for r in rules.values())} reglas totales")

    expected_agents = {
        "spec-analyst", "domain-modeler", "architect",
        "feature-analyst", "feature-developer", "code-reviewer",
        "context-reader", "context-manager", "ci-triage",
    }
    if set(rules.keys()) != expected_agents:
        print(f"✗ Agentes no coinciden con los esperados: {set(rules.keys()) ^ expected_agents}")
        return 1
    print(f"✓ Los 9 agentes canónicos presentes")

    # Verificar casos críticos que NO deben cambiar
    cases = [
        ("spec-analyst", "specs/spec-cerrada-xx.md", "write", True),
        ("spec-analyst", "docs/sesion/CONTEXTO.md", "write", False),
        ("domain-modeler", "docs/referencia/DOMINIO.md", "write", True),
        ("feature-developer", "docs/referencia/DOMINIO.md", "write", False),
        ("feature-developer", "docs/referencia/DOMINIO.md", "read", True),
        ("context-manager", "docs/sesion/CONTEXTO.md", "write", True),
        ("context-manager", "docs/sesion/DECISIONES.md", "write", True),
        ("context-manager", "docs/sesion/CONTEXTO.bak.md", "write", True),
        ("context-manager", "docs/sesion/DECISIONES.bak.md", "write", True),
        ("ci-triage", "docs/sesion/TRIAGE_CI.md", "write", True),
        ("context-reader", "docs/sesion/TRIAGE_CI.md", "write", True),
        ("architect", "docs/referencia/ARQUITECTURA.md", "write", True),
        ("architect", "docs/sesion/DECISIONES.md", "write", True),  # seed
        ("code-reviewer", "docs/referencia/COBERTURA.md", "write", True),
        ("feature-analyst", "docs/referencia/COBERTURA.md", "write", False),
        # Placeholders sin resolver → denegar por defecto
        ("feature-developer", "src/index.ts", "write", False),
        ("feature-developer", "tests/foo.test.ts", "write", False),
    ]
    failed = 0
    for agent, path, op, expected in cases:
        ok, _ = check_access(agent, path, op, rules)
        if ok != expected:
            print(f"✗ {agent}/{op} {path}: esperado {expected}, fue {ok}")
            failed += 1
    if failed:
        print(f"✗ {failed} casos fallaron")
        return 1
    print(f"✓ {len(cases)} casos de prueba pasaron")

    # Verificar list_permissions de un agente clave
    perms = list_permissions("context-manager", rules)
    n_writes = len(perms["W"])
    if n_writes < 4:
        print(f"⚠ context-manager tiene solo {n_writes} permisos W (esperado ≥4)")
    print(f"✓ context-manager tiene {n_writes} permisos W, {len(perms['R'])} R, {len(perms['-'])} sin acceso")

    return 0


def run_one_check(agent: str, path: str, op: str) -> int:
    rules = load_matrix_from_file(MATRIX_PATH)
    ok, why = check_access(agent, path, op, rules)
    symbol = "✓" if ok else "✗"
    print(f"{symbol} {agent} {op} {path}: {why}")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Modo MCP
# ---------------------------------------------------------------------------


def run_mcp_server(agent: str) -> int:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        print("Error: paquete 'mcp' no instalado. Instala con: pip install 'mcp>=1.0'", file=sys.stderr)
        return 2

    rules = load_matrix_from_file(MATRIX_PATH)
    if agent not in rules:
        print(f"Error: agente desconocido: {agent}. Agentes válidos: {sorted(rules.keys())}", file=sys.stderr)
        return 2

    mcp = FastMCP(f"fs-guard:{agent}")

    @mcp.tool()
    def read_file(path: str) -> str:
        """Lee un archivo solo si este agente tiene permiso R o W en MATRIZ_PERMISOS.md."""
        ok, payload = do_read(agent, path, rules)
        if not ok:
            return f"ERROR: {payload}"
        return payload

    @mcp.tool()
    def write_file(path: str, content: str) -> str:
        """Escribe un archivo solo si este agente tiene permiso W en MATRIZ_PERMISOS.md."""
        ok, payload = do_write(agent, path, content, rules)
        if not ok:
            return f"ERROR: {payload}"
        return payload

    @mcp.tool()
    def list_allowed_paths() -> str:
        """Devuelve los patrones de rutas con permiso W/R/- para este agente."""
        perms = list_permissions(agent, rules)
        out = [f"# Permisos de @{agent}", ""]
        for level, label in [("W", "Escritura"), ("R", "Lectura"), ("-", "Sin acceso")]:
            out.append(f"## {label} ({level})")
            for p in perms[level]:
                out.append(f"- {p}")
            out.append("")
        return "\n".join(out)

    mcp.run()
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", help="Identidad del agente para este servidor")
    ap.add_argument("--test", action="store_true", help="Smoke test (todos los agentes, sin MCP)")
    ap.add_argument("--check", metavar="PATH", help="One-shot: prueba acceso de --agent a --check con --op")
    ap.add_argument("--op", choices=["read", "write"], default="write")
    args = ap.parse_args()

    if args.test:
        return run_smoke_test()
    if args.check:
        if not args.agent:
            print("--check requiere --agent", file=sys.stderr)
            return 2
        return run_one_check(args.agent, args.check, args.op)
    if not args.agent:
        print("--agent es requerido salvo en --test", file=sys.stderr)
        return 2
    return run_mcp_server(args.agent)


if __name__ == "__main__":
    sys.exit(main())
