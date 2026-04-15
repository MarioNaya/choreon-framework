#!/usr/bin/env python3
"""
sync-agents.py — Genera .claude/ y .github/ desde ai-specs/ (hub canonical).

Adaptación real del front-matter a cada herramienta:
- Claude Code (.claude/agents/*.md):
    * tools: string CSV con nombres nativos de herramientas Claude (Read, Grep, Glob, Edit, Write, WebSearch, WebFetch).
    * model: sonnet | opus | haiku.
    * writes y handoffs NO caben en el YAML; se mueven al cuerpo como secciones markdown.
- GitHub Copilot (.github/agents/*.agent.md):
    * Mantiene el YAML rico (writes, handoffs) porque Copilot ignora campos extra.
    * Renombra extensión a .agent.md.

Idempotente: regenera destinos sobrescribiendo.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = ROOT / "ai-specs"
CLAUDE_DIR = ROOT / ".claude"
GH_DIR = ROOT / ".github"
SYNC_LOG = ROOT / "docs" / "archivo" / "sync-log.md"

# Mapeo canonical → herramientas Claude Code
# Claude Code actualmente expone (entre otras): Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch.
# Mantenemos un subconjunto seguro y conservador.
CLAUDE_TOOL_MAP = {
    "read": ["Read"],
    "search": ["Grep", "Glob"],
    "edit": ["Edit", "Write"],
    "web": ["WebSearch", "WebFetch"],
    "bash": ["Bash"],
    "agent": ["Agent"],
}


@dataclass
class AgentSpec:
    name: str
    description: str
    model: str
    tools: list[str]  # canonical tool names
    writes: list[str]
    handoffs: list[str]
    body: str  # markdown body (after the closing ---)


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Return (front_matter_dict, body). Front-matter is the first YAML block between --- lines.
    Only parses a small, well-defined subset (key: value, simple lists)."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    return _parse_simple_yaml(raw), body


def _parse_simple_yaml(raw: str) -> dict:
    """Mini-parser for our limited YAML shape:
       key: value
       key: [a, b, c]
       key:
         - item1
         - item2
    Preserves insertion order."""
    data: dict = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest == "":
            # multi-line list follows
            items: list[str] = []
            j = i + 1
            while j < len(lines) and lines[j].startswith("  -"):
                items.append(lines[j][3:].strip().strip("'\""))
                j += 1
            data[key] = items
            i = j
        elif rest.startswith("[") and rest.endswith("]"):
            inside = rest[1:-1].strip()
            if inside == "":
                data[key] = []
            else:
                data[key] = [x.strip().strip("'\"") for x in inside.split(",")]
            i += 1
        else:
            data[key] = rest.strip().strip("'\"")
            i += 1
    return data


def load_agent(path: Path) -> AgentSpec:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)
    return AgentSpec(
        name=fm.get("name", path.stem),
        description=fm.get("description", ""),
        model=fm.get("model", "sonnet"),
        tools=fm.get("tools", []) if isinstance(fm.get("tools", []), list) else [],
        writes=fm.get("writes", []) if isinstance(fm.get("writes", []), list) else [],
        handoffs=fm.get("handoffs", []) if isinstance(fm.get("handoffs", []), list) else [],
        body=body,
    )


def validate_agent_coherence(spec: AgentSpec, source_path: Path) -> list[str]:
    """Detect incoherencias entre writes y tools del agente canonical.

    Reglas:
    - Si writes no está vacío → tools debe incluir 'edit' (mapeado a Write+Edit en Claude Code).
    - Si writes está vacío → no hay restricción sobre tools (un agente puede leer-solo).

    Returns lista de mensajes de error; vacía si todo coherente.
    """
    errors: list[str] = []
    has_writes = bool(spec.writes)
    tools_lower = [t.strip().lower() for t in spec.tools]
    has_edit = "edit" in tools_lower

    if has_writes and not has_edit:
        writes_fmt = ", ".join(spec.writes)
        errors.append(
            f"{source_path.name}: declara writes ({writes_fmt}) pero 'edit' no está en tools "
            f"{spec.tools}. Añade 'edit' a tools, o retira writes si el agente no escribe."
        )
    return errors


def map_tools_to_claude(canonical_tools: list[str]) -> str:
    """Convert canonical tool names to Claude Code's comma-separated string."""
    seen: list[str] = []
    for t in canonical_tools:
        mapped = CLAUDE_TOOL_MAP.get(t.strip().lower(), [])
        for m in mapped:
            if m not in seen:
                seen.append(m)
    return ", ".join(seen)


def render_claude_agent(spec: AgentSpec) -> str:
    """Claude Code format: YAML with name/description/tools/model only; writes & handoffs in body."""
    yaml_lines = ["---"]
    yaml_lines.append(f"name: {spec.name}")
    # description may be long; keep single line (Claude Code accepts)
    yaml_lines.append(f"description: {spec.description}")
    if spec.model:
        yaml_lines.append(f"model: {spec.model}")
    tools_str = map_tools_to_claude(spec.tools)
    if tools_str:
        yaml_lines.append(f"tools: {tools_str}")
    yaml_lines.append("---")
    yaml_block = "\n".join(yaml_lines)

    # Inject "Ámbito de escritura" and "Handoffs" as explicit sections at top of body.
    injected = []
    if spec.writes:
        injected.append("## Ámbito de escritura\n")
        for w in spec.writes:
            injected.append(f"- `{w}`")
        injected.append("")
    if spec.handoffs:
        injected.append("## Handoffs declarados\n")
        for h in spec.handoffs:
            injected.append(f"- `@{h}`")
        injected.append("")
    injected_block = "\n".join(injected)

    body = spec.body.lstrip("\n")
    return f"{yaml_block}\n\n{injected_block}\n{body}" if injected_block else f"{yaml_block}\n\n{body}"


def render_copilot_agent(spec: AgentSpec, original_text: str) -> str:
    """Copilot format: keep original YAML + body (Copilot ignores unknown fields)."""
    return original_text


def sync_agents():
    (CLAUDE_DIR / "agents").mkdir(parents=True, exist_ok=True)
    (GH_DIR / "agents").mkdir(parents=True, exist_ok=True)
    written = []

    # Primer paso: validar coherencia de todos los agentes antes de escribir nada.
    # Fail fast: si hay inconsistencias, aborta sin generar destinos a medias.
    all_errors: list[str] = []
    specs_cache: list[tuple[Path, str, AgentSpec]] = []
    for src in sorted((HUB / "agents").glob("*.md")):
        original = src.read_text(encoding="utf-8")
        spec = load_agent(src)
        specs_cache.append((src, original, spec))
        all_errors.extend(validate_agent_coherence(spec, src))

    if all_errors:
        print("✗ Lint falló en ai-specs/agents/:", file=sys.stderr)
        for e in all_errors:
            print(f"  {e}", file=sys.stderr)
        print("\nNo se ha generado nada. Arregla las inconsistencias y reintenta.", file=sys.stderr)
        sys.exit(3)

    # Segundo paso: generar destinos.
    for src, original, spec in specs_cache:
        claude_dest = CLAUDE_DIR / "agents" / src.name
        claude_dest.write_text(render_claude_agent(spec), encoding="utf-8")
        written.append(str(claude_dest.relative_to(ROOT)))

        gh_dest = GH_DIR / "agents" / f"{src.stem}.agent.md"
        gh_dest.write_text(render_copilot_agent(spec, original), encoding="utf-8")
        written.append(str(gh_dest.relative_to(ROOT)))
    return written


def sync_prompts():
    (CLAUDE_DIR / "commands").mkdir(parents=True, exist_ok=True)
    (GH_DIR / "prompts").mkdir(parents=True, exist_ok=True)
    written = []
    for src in sorted((HUB / "prompts").glob("*.md")):
        text = src.read_text(encoding="utf-8")
        claude_dest = CLAUDE_DIR / "commands" / src.name
        claude_dest.write_text(text, encoding="utf-8")
        written.append(str(claude_dest.relative_to(ROOT)))

        gh_dest = GH_DIR / "prompts" / f"{src.stem}.prompt.md"
        gh_dest.write_text(text, encoding="utf-8")
        written.append(str(gh_dest.relative_to(ROOT)))
    return written


def sync_skills():
    (CLAUDE_DIR / "skills").mkdir(parents=True, exist_ok=True)
    (GH_DIR / "skills").mkdir(parents=True, exist_ok=True)
    written = []
    for skill_dir in sorted((HUB / "skills").glob("*/")):
        skill_src = skill_dir / "SKILL.md"
        if not skill_src.exists():
            continue
        text = skill_src.read_text(encoding="utf-8")

        claude_dest_dir = CLAUDE_DIR / "skills" / skill_dir.name
        claude_dest_dir.mkdir(parents=True, exist_ok=True)
        claude_dest = claude_dest_dir / "SKILL.md"
        claude_dest.write_text(text, encoding="utf-8")
        written.append(str(claude_dest.relative_to(ROOT)))

        gh_dest_dir = GH_DIR / "skills" / skill_dir.name
        gh_dest_dir.mkdir(parents=True, exist_ok=True)
        gh_dest = gh_dest_dir / "SKILL.md"
        gh_dest.write_text(text, encoding="utf-8")
        written.append(str(gh_dest.relative_to(ROOT)))
    return written


def generate_claude_md() -> str:
    """Generate CLAUDE.md at the repo root. Reads metadata from ai-specs/agents/ to list subagents."""
    agents = [load_agent(p) for p in sorted((HUB / "agents").glob("*.md"))]
    prompts = sorted((HUB / "prompts").glob("*.md"))

    lines = []
    lines.append("# CLAUDE.md — instrucciones globales para Claude Code\n")
    lines.append(
        "<!-- Archivo generado por scripts/sync-agents.py. No editar a mano; editar ai-specs/ y regenerar. -->\n"
    )
    lines.append("## Protocolo de inicio de sesión\n")
    lines.append(
        "Al comenzar cualquier sesión, lee `docs/sesion/CONTEXTO.md` (≤80 líneas) para conocer estado, bloqueantes y próxima tarea. Si no existe o está vacío, ejecuta `/bootstrap`.\n"
    )

    lines.append("## Descripción del proyecto\n")
    lines.append("[[DESCRIPCION_PROYECTO]]\n")

    lines.append("## Sistema agéntico\n")
    lines.append(
        f"Este repo incluye **{len(agents)} agentes**, **{len(prompts)} prompts** (slash-commands) y **2 skills**. Definiciones canónicas en `ai-specs/`; copias adaptadas en `.claude/` y `.github/` generadas por `scripts/sync-agents.py`.\n"
    )

    lines.append("### Subagentes disponibles\n")
    for a in agents:
        lines.append(f"- **`@{a.name}`** — {a.description}")
    lines.append("")

    lines.append("### Slash-commands\n")
    for p in prompts:
        lines.append(f"- `/{p.stem}`")
    lines.append("")

    lines.append("## Reglas de oro\n")
    lines.append("1. Lee `docs/sesion/CONTEXTO.md` al inicio de cada sesión.")
    lines.append("2. Ningún agente escribe fuera de su fila en `docs/guias/MATRIZ_PERMISOS.md`.")
    lines.append("3. Gate de Definition-of-Done es innegociable para `@feature-developer` y `@code-reviewer`.")
    lines.append("4. `CONTEXTO.md` ≤80 líneas. `DECISIONES.md` in-place por categoría, nunca append cronológico.")
    lines.append("5. Confirmación explícita del usuario antes de redactar en las 3 fases de bootstrap.")
    lines.append("6. Backup dual (`.bak.md`) antes de modificar CONTEXTO o DECISIONES.\n")

    lines.append("## Referencias clave\n")
    lines.append("- Árbol de decisión de agentes: `docs/guias/ONBOARDING.md`")
    lines.append("- Matriz de permisos: `docs/guias/MATRIZ_PERMISOS.md`")
    lines.append("- Guía específica Claude Code: `docs/guias/CLAUDE_CODE.md`")
    lines.append("- Ejemplo completo de bootstrap: `examples/golden-path/README.md`")
    lines.append("- Decisiones vigentes: `docs/sesion/DECISIONES.md`")
    lines.append("- Estado actual: `docs/sesion/CONTEXTO.md`\n")

    return "\n".join(lines)


def write_sync_log(written: list[str]):
    """Append entry to docs/archivo/sync-log.md with timestamp and files written."""
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    entry = [
        f"## {stamp}",
        f"- Versión transformación: v0.2 (Python)",
        f"- Archivos generados: {len(written)}",
        "",
    ]
    existing = SYNC_LOG.read_text(encoding="utf-8") if SYNC_LOG.exists() else "# Sync log\n\n"
    SYNC_LOG.write_text(existing + "\n".join(entry) + "\n", encoding="utf-8")


def main():
    if not HUB.exists():
        print(f"Error: no existe {HUB}", file=sys.stderr)
        sys.exit(1)

    print(f"→ Sincronizando desde {HUB}")
    written: list[str] = []
    written += sync_agents()
    written += sync_prompts()
    written += sync_skills()

    claude_md_path = ROOT / "CLAUDE.md"
    claude_md_path.write_text(generate_claude_md(), encoding="utf-8")
    written.append("CLAUDE.md")

    for w in written:
        print(f"  {w}")

    write_sync_log(written)

    print(f"\n✓ Sync v0.2 completado. Archivos generados: {len(written)}")
    print(f"  Transformaciones aplicadas: Claude Code adapter, Copilot passthrough, CLAUDE.md root.")
    print(f"  Log: docs/archivo/sync-log.md")


if __name__ == "__main__":
    main()
