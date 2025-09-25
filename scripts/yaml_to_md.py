# -*- coding: utf-8 -*-

"""
yaml_to_md.py — liest eine apis.yml aus ../registry und erzeugt Markdown-Tabellen.

Ohne Argumente (z. B. VS Code "Run Code"):
    - YAML wird automatisch unter ../registry/{apis.yml|apis.yaml} gesucht
    - Ausgabe: flache Gesamttabelle (ohne Owner-Spalte)
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

# Mapping & Priorität für Status-Tags
_STATUS_TO_STAGE = {
    "status/active":     "Prod",
    "status/wip":        "Dev",
    "status/deprecated": "Deprecated",
    "status/http-4xx":   "Alpha",
    "status/http-5xx":   "Alpha",
}
_STATUS_PRIO = ["status/http-5xx", "status/http-4xx", "status/deprecated", "status/wip", "status/active"]

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

# ----------------- Tag-Helfer -----------------
def _normalize_status(v) -> list[str]:
    """Akzeptiert String oder Liste; gibt normalisierte (lowercase) Liste zurück."""
    if not v:
        return []
    if isinstance(v, str):
        s = v.strip().lower()
        return [s] if s else []
    if isinstance(v, (list, tuple, set)):
        out = [str(x).strip().lower() for x in v if str(x).strip()]
        # Duplikate entfernen, Reihenfolge stabilisieren
        seen = set(); uniq = []
        for s in out:
            if s not in seen:
                uniq.append(s); seen.add(s)
        return uniq
    s = str(v).strip().lower()
    return [s] if s else []

def _normalize_tags(v) -> list[str]:
    """Tags in Liste normalisieren (lowercase). Akzeptiert String oder Liste."""
    if not v:
        return []
    if isinstance(v, str):
        # Komma- oder Whitespace-getrennt
        parts = re.split(r"[,\s]+", v.strip())
        return [p.strip().lower() for p in parts if p.strip()]
    if isinstance(v, (list, tuple, set)):
        out = []
        seen = set()
        for x in v:
            s = str(x).strip().lower()
            if s:
                # führendes '#' entfernen
                if s.startswith("#"): s = s[1:]
                if s not in seen:
                    seen.add(s); out.append(s)
        return out
    s = str(v).strip().lower()
    return [s] if s else []

def _status_from_tags_or_status_field(a: dict) -> list[str]:
    """
    Liefert alle status/*-Tags. Quelle:
      1) 'status' Feld (String oder Liste),
      2) sonst aus 'tags' gefiltert (prefix status/).
    """
    st = _normalize_status(a.get("status"))
    if st:
        return [x for x in st if x.startswith("status/")]
    tags = _normalize_tags(a.get("tags"))
    return [t for t in tags if t.startswith("status/")]

def _primary_stage_for_sort(a: dict) -> str:
    """
    Bestimmt die primäre Stage (für Sortierung/Fallback-Badge):
    - nehme erste Stage gemäß _STATUS_PRIO aus den status/*,
    - sonst vorhandene 'stage',
    - sonst 'Dev'.
    """
    statuses = _status_from_tags_or_status_field(a)
    for key in _STATUS_PRIO:
        if key in statuses:
            return _STATUS_TO_STAGE.get(key, "Dev")
    return a.get("stage") or "Dev"

def _stage_badges_cell(a: dict) -> str:
    """
    Baut die Stage-Zelle:
    - alle Badges gemäß allen status/*-Tags (in _STATUS_PRIO-Reihenfolge, dedupliziert),
    - Fallback: ein Badge aus 'stage'.
    """
    statuses = _status_from_tags_or_status_field(a)
    stages: list[str] = []
    seen = set()
    for key in _STATUS_PRIO:
        if key in statuses:
            st = _STATUS_TO_STAGE.get(key)
            if st and st not in seen:
                stages.append(st); seen.add(st)
    if not stages:
        stages = [a.get("stage") or "Dev"]
    # zusammen rendern (nebeneinander)
    return " ".join(stage_badge(s) for s in stages if s)

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
            # Stage-Wert primär aus Status ableiten (für Sortierung/Fallback),
            # aber alle Status-Badges später separat rendern
            "stage":         _primary_stage_for_sort(a),
            "spec":          a.get("spec") or "",
            "method":        a.get("method") or a.get("methods"),
            "guid_hash":     a.get("guid_hash") or "",
            "path_entities": a.get("path_entities") or a.get("entities") or "",
            "owner":         a.get("owner") or a.get("owner_ref") or "",
            "path_prefix":   a.get("path_prefix") or "-",
            # alle Tags/Status mitnehmen (für spätere Anzeige, wenn gewünscht)
            "tags":          _normalize_tags(a.get("tags")),
            "status":        _normalize_status(a.get("status")),
        })
    return out

# ----------------- Render -----------------
def render_table(rows: list[dict], show_owner: bool=False) -> str:
    cols = ["API", "Base", "Auth", "Stage", "Spec", "Method", "guid_hash", "path_entities", "path_prefix"]
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
            _stage_badges_cell(r),               # <<== Mehrfach-Badges aus allen Status-Tags
            link_or_dash(r["spec"]),
            method_cell(r.get("method")),
            guid_cell(r.get("guid_hash")),
            entities_cell(r.get("path_entities")),
            code_or_dash(r.get("path_prefix")),
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

    def sortkey(r): 
        # Sortierung nach der primären Stage (bereits vorab gesetzt) und Name
        return (STAGE_ORDER.get(r["stage"], 99), r["name"].lower())

    # >>> Ziel-Datei im registry-Ordner (gleiches Verzeichnis wie YAML)
    out_path = (yaml_path.parent / "overview.md").resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not grouped:
        out = render_table(sorted(rows, key=lambda r: (r["family"],) + sortkey(r)), show_owner)
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

    out_path.write_text("".join(chunks), encoding="utf-8")

if __name__ == "__main__":
    main()
