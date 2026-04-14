#!/usr/bin/env python3
"""
init-project.py — Asistente de inicialización del boilerplate.

Modo básico (interactivo):
    python scripts/init-project.py

Modo con template-pack:
    python scripts/init-project.py --template web-typescript

El template-pack aplica placeholders sintácticos del stack (globs, comandos,
versiones) y copia instructions/ pre-rellenadas. Después pregunta los globales
restantes (nombre, descripción) interactivamente.

Reemplazo cross-platform (sin sed, sin diferencias BSD/GNU).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
TARGET_EXTENSIONS = {".md", ".yml", ".yaml", ".json", ".sh", ".py", ".txt"}
TARGET_ROOTS = [
    ROOT / "ai-specs",
    ROOT / "docs",
    ROOT / ".github",
    ROOT / ".claude",
    ROOT / "specs",
    ROOT / "scripts",
]
# Archivos raíz a procesar puntualmente
TARGET_ROOT_FILES = [
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "INIT.md",
    ROOT / "CLAUDE.md",
]


# ---------------------------------------------------------------------------
# Reemplazo de placeholders
# ---------------------------------------------------------------------------


def iter_target_files():
    for base in TARGET_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in TARGET_EXTENSIONS:
                yield path
    for path in TARGET_ROOT_FILES:
        if path.exists():
            yield path


def apply_replacements(mapping: dict[str, str]) -> int:
    """Reemplaza [[KEY]] por VALUE en todos los archivos objetivo. Devuelve nº de archivos modificados."""
    count = 0
    keys = list(mapping.keys())
    for path in iter_target_files():
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        new_text = text
        for key in keys:
            new_text = new_text.replace(f"[[{key}]]", mapping[key])
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            count += 1
    return count


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------


def load_pack(name: str) -> dict[str, str]:
    pack_path = TEMPLATES_DIR / name / "pack.json"
    if not pack_path.exists():
        raise FileNotFoundError(f"No existe el pack: {pack_path}")
    with pack_path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"pack.json debe ser un objeto JSON plano")
    return {str(k): str(v) for k, v in data.items()}


def copy_pack_instructions(name: str) -> int:
    """Copia templates/<name>/instructions/*.md sobre .github/instructions/."""
    src = TEMPLATES_DIR / name / "instructions"
    dest = ROOT / ".github" / "instructions"
    if not src.exists():
        return 0
    dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    for f in src.glob("*.instructions.md"):
        shutil.copy2(f, dest / f.name)
        copied += 1
    return copied


def list_available_packs() -> list[str]:
    if not TEMPLATES_DIR.exists():
        return []
    return sorted([p.name for p in TEMPLATES_DIR.iterdir() if p.is_dir() and (p / "pack.json").exists()])


# ---------------------------------------------------------------------------
# Prompts interactivos
# ---------------------------------------------------------------------------


def prompt(text: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{text}{suffix}: ").strip()
    return val or default


def collect_globals(has_template: bool) -> dict[str, str]:
    """Pregunta globales mínimos. Si ya hay pack, no pregunta globs."""
    mapping: dict[str, str] = {}
    print("=" * 50)
    print(" Datos del proyecto")
    print("=" * 50)
    mapping["NOMBRE_PROYECTO"] = prompt("Nombre del proyecto")
    mapping["DESCRIPCION_PROYECTO"] = prompt("Descripción breve (1 línea)")
    if not has_template:
        mapping["LENGUAJE"] = prompt("Lenguaje principal", "TypeScript")
        mapping["BACKEND_GLOB"] = prompt("Glob backend", "src/**/*.ts")
        mapping["FRONTEND_GLOB"] = prompt("Glob frontend (vacío si no aplica)", "")
        mapping["TEST_GLOB"] = prompt("Glob tests", "**/*.test.ts")
        mapping["PROJECT_SRC_GLOB"] = mapping["BACKEND_GLOB"]
        mapping["PROJECT_TEST_GLOB"] = mapping["TEST_GLOB"]
    return mapping


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", help=f"Template pack a aplicar. Packs disponibles: {', '.join(list_available_packs()) or '(ninguno)'}")
    ap.add_argument("--list-templates", action="store_true", help="Lista packs disponibles y sale")
    ap.add_argument("--non-interactive", action="store_true", help="No prompt interactivo — solo aplica el pack si se indicó --template")
    args = ap.parse_args()

    if args.list_templates:
        packs = list_available_packs()
        if not packs:
            print("No hay packs en templates/")
            return 0
        for p in packs:
            readme = TEMPLATES_DIR / p / "README.md"
            first_line = ""
            if readme.exists():
                for line in readme.read_text(encoding="utf-8").splitlines():
                    if line.strip() and not line.startswith("#"):
                        first_line = line.strip()
                        break
            print(f"  {p} — {first_line}")
        return 0

    mapping: dict[str, str] = {}
    template_used = args.template

    if template_used:
        try:
            pack = load_pack(template_used)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"→ Aplicando template pack: {template_used} ({len(pack)} placeholders)")
        mapping.update(pack)

    if not args.non_interactive:
        user_mapping = collect_globals(has_template=bool(template_used))
        mapping.update(user_mapping)

    if not mapping:
        print("Nada que aplicar.")
        return 0

    n_files = apply_replacements(mapping)
    print(f"✓ {len(mapping)} placeholders reemplazados en {n_files} archivos.")

    if template_used:
        n_copied = copy_pack_instructions(template_used)
        if n_copied:
            print(f"✓ {n_copied} instrucciones copiadas desde templates/{template_used}/instructions/")

    # Informar de placeholders restantes
    remaining: dict[str, int] = {}
    for path in iter_target_files():
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        import re
        for m in re.findall(r"\[\[([A-Z_][A-Z0-9_]*)\]\]", text):
            remaining[m] = remaining.get(m, 0) + 1
    if remaining:
        print("\nPlaceholders pendientes (se resuelven durante /bootstrap):")
        for k, v in sorted(remaining.items(), key=lambda kv: -kv[1])[:15]:
            print(f"  [[{k}]] × {v}")
    else:
        print("\n✓ 0 placeholders pendientes.")

    print("\nSiguiente paso:")
    print("  bash scripts/sync-agents.sh")
    print("  $EDITOR specs/brief.md")
    print("  claude  # y ejecuta /bootstrap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
