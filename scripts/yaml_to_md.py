
# -*- coding: utf-8 -*-

"""
yaml_to_md.py — liest eine apis.yml aus ../registry und erzeugt Markdown-Tabellen.

Ohne Argumente (z. B. VS Code "Run Code"):
    - YAML wird automatisch unter ../registry/{apis.yml|apis.yaml} gesucht
    - Ausgabe: flache Gesamttabelle (ohne Owner-Spalte)

Optional (wenn du doch im Terminal aufrufst):
    python yaml_to_md.py --grouped --owner            # nutzt weiterhin ../registry/…
    python yaml_to_md.py /pfad/zu/apis.yml --grouped  # expliziter Pfad überschreibt Auto-Suche
"""

import sys, re, json, yaml
from pathlib import Path
from typing import Any

# ----------------- Defaults für Zero-Arg-Run -----------------
DEFAULT_YAML_NAMES = ("apis.yml", "apis.yaml")

def _default_yaml_path() -> Path | None:
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent / "registry" / name for name in DEFAULT_YAML_NAMES
    ] + [
        here / "registry" / name for name in DEFAULT_YAML_NAMES  # Fallback: ./registry
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

# ----------------- Stage / Badges / Escapes -----------------
STAGE_COLOR = {
    "GA": "brightgreen",
    "Prod": "brightgreen",
    "Beta": "yellow",
    "Alpha": "orange",
    "Dev": "blue",
    "Deprecated": "lightgrey",
}
STAGE_ORDER = {"GA": 0, "Prod": 0, "Beta": 1, "Alpha": 2, "Dev": 3, "Deprecated": 9}

def esc(s) -> str:
    """Markdown-escapes für Tabellen; robust für beliebige Typen."""
    t = str(s)
    return t.replace("|", r"\|").replace("\n", "<br>")

def stage_badge(stage: str | None) -> str:
    if not stage:
        return "–"
    color = STAGE_COLOR.get(stage, "inactive")
    enc = re.sub(r"\s+", "%20", stage)
    return f"![{stage}](https://img.shields.io/badge/stage-{enc}-{color})"

def code_or_dash(val) -> str:
    """
    Code-formatierte Zelle.
    - Strings: in Backticks, inkl. Obsidian [[...]].
    - Andere Typen: nach str gecastet.
    """
    if val is None or val == "":
        return "–"
    txt = str(val).strip()
    return f"`{esc(txt)}`" if txt else "–"

def link_or_dash(val) -> str:
    if val is None or val == "":
        return "–"
    u = str(val).strip()
    return f"[`{u}`]({u})" if u else "–"


def method_cell(v: Any) -> str:
    if v is None or v == "":
        return "–"
    if isinstance(v, (list, tuple)):
        parts = [str(x).strip().upper() for x in v if x]
        return f"`{esc(', '.join(parts))}`" if parts else "–"
    return f"`{esc(str(v).strip().upper())}`"

def guid_cell(v: Any) -> str:
    return f"`{esc(str(v))}`" if v else "–"

def entities_cell(v: Any) -> str:
    if not v:
        return "–"
    if isinstance(v, (list, tuple)):
        s = ", ".join(str(x) for x in v)
        return esc(s) if s else "–"
    if isinstance(v, dict):
        return esc(json.dumps(v, ensure_ascii=False, separators=(",", ":")))
    return esc(str(v))

def canon_family(f: str | None) -> str:
    f = (f or "").lower()
    if f.startswith("intradev"): return "intradev"
    if f.startswith("intranet"): return "intranet"
    if f == "odata":             return "odata"
    return ""

# ----------------- IO -----------------
def load_apis_from_path(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    apis = data.get("apis", data)
    out: list[dict] = []
    for a in apis:
        out.append({
            "name":          a.get("name") or "–",
            "family":        canon_family(a.get("family")),
            "base":          a.get("base") or a.get("base_url") or "",
            "auth":          a.get("auth") or "",
            "stage":         a.get("stage") or "Dev",
            "spec":          a.get("spec") or "",
            "method":        a.get("method") or a.get("methods"),
            "guid_hash":     a.get("guid_hash") or "",
            "path_entities": a.get("path_entities") or a.get("entities") or "",
            "owner":         a.get("owner") or a.get("owner_ref") or "",
        })
    return out

# ----------------- Render -----------------
def render_table(rows: list[dict], show_owner: bool=False) -> str:
    cols = ["API", "Base", "Auth", "Stage", "Spec", "Method", "guid_hash", "path_entities"]
    if show_owner:
        cols.append("Owner")
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"
    lines = [header, sep]
    for r in rows:
        cells = [
            r["name"],
            code_or_dash(r["base"]),
            (r["auth"] or "–"),
            stage_badge(r["stage"]),
            link_or_dash(r["spec"]),
            method_cell(r.get("method")),
            guid_cell(r.get("guid_hash")),
            entities_cell(r.get("path_entities")),
        ]
        if show_owner:
            cells.append(r.get("owner") or "–")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

# ----------------- Main -----------------
def main():
    # Zero-arg Defaults (für VS Code "Run Code")
    yaml_path: Path | None = None
    grouped = False
    show_owner = False

    # Wenn Argumente vorhanden sind, minimal auswerten (freiwillig)
    args = sys.argv[1:]
    # erlaubte kurze CLI: [yaml_file]? [--grouped]? [--owner]?
    for a in list(args):
        if a == "--grouped":
            grouped = True
            args.remove(a)
        elif a == "--owner":
            show_owner = True
            args.remove(a)

    if args:
        # erstes verbleibendes Argument als Pfad behandeln
        yaml_path = Path(args[0]).resolve()
        if not yaml_path.exists():
            sys.exit(f"YAML file not found: {yaml_path}")
    else:
        yaml_path = _default_yaml_path()
        if not yaml_path:
            sys.exit("No YAML found. Expected one of ../registry/{apis.yml,apis.yaml} or ./registry/{apis.yml,apis.yaml}.")

    rows = load_apis_from_path(yaml_path)

    def sortkey(r): return (STAGE_ORDER.get(r["stage"], 99), r["name"].lower())

    # >>> Ziel-Datei im registry-Ordner (gleiches Verzeichnis wie YAML)
    out_path = (yaml_path.parent / "overview.md").resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not grouped:
        out = render_table(sorted(rows, key=lambda r: (r["family"],) + sortkey(r)), show_owner)
        # vorher: sys.stdout.write(out + "\n")
        out_path.write_text(out + "\n", encoding="utf-8")
        return

    # Gruppiert
    sections = [
        ("intradev",  "## IntraDev-Schnittstellen"),
        ("intranet",  "## Intranet-Schnittstellen"),
        ("odata",     "## OData-Schnittstellen"),
    ]
    chunks: list[str] = []
    known = set()
    for key, title in sections:
        g = [r for r in rows if r["family"] == key]
        if not g:
            continue
        g.sort(key=sortkey)
        chunks.append(title + "\n\n" + render_table(g, show_owner) + "\n")
        known.update(id(x) for x in g)

    rest = [r for r in rows if id(r) not in known]
    if rest:
        rest.sort(key=sortkey)
        chunks.append("## Sonstige Schnittstellen\n\n" + render_table(rest, show_owner) + "\n")

    # vorher: sys.stdout.write("".join(chunks))
    out_path.write_text("".join(chunks), encoding="utf-8")

if __name__ == "__main__":
    main()
