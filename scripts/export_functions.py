from __future__ import annotations

from pathlib import Path
from typing import Iterable, Any, List, Dict
from collections.abc import Iterable as CollIterable
import os, re, sys, yaml, json, hashlib

# ----------------------------- Pfade & IO ------------------------------------
def can_read(p: Path) -> bool:
    """Schneller, toleranter Read-Check (z. B. auf Netzlaufwerken)."""
    try:
        return os.access(p, os.R_OK)
    except Exception:
        return True

def info(m: str): print(f"[info] {m}")
def warn(m: str): print(f"[warn] {m}")
def skip(m: str): print(f"[skip] {m}")
def err (m: str): print(f"[err ] {m}", file=sys.stderr)

# ----------------------------- Frontmatter -----------------------------------
FM_RE = re.compile(
    r"^\s*\ufeff?\s*---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)",
    re.DOTALL,
)

def read_frontmatter(p: Path) -> dict | None:
    """
    Liest YAML-Frontmatter aus einer Markdown-Datei.
    - UTF-8 + optional BOM
    - toleriert CRLF/LF
    Gibt dict oder None (bei Fehler / kein Frontmatter) zurück.
    """
    try:
        if not can_read(p):
            skip(f"no read access: {p}")
            return None
        txt = p.read_text(encoding="utf-8")
    except Exception as e:
        skip(f"read error: {p} -> {e}")
        return None

    m = FM_RE.search(txt)
    if not m:
        skip(f"no frontmatter: {p}")
        return None

    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        skip(f"yaml parse error: {p} -> {e}")
        return None
    return fm

# ----------------------------- Tags & Status ---------------------------------
def _normalize_tags(val) -> set[str]:
    """
    Normalisiert verschiedene Tag-Formate in eine lowercase-Menge:
      - Liste von Strings
      - Liste von Objekten (Properties-UI): [{'tag': 'a'}, {'name': 'b'}]
      - String mit Komma/Whitespace/Hash-Separierung
    """
    out: set[str] = set()

    def add_one(s: str):
        s = s.strip()
        if not s:
            return
        if s.startswith("#"):
            s = s[1:]
        out.add(s.lower())

    if val is None:
        return out

    if isinstance(val, list):
        for item in val:
            if isinstance(item, str):
                for part in re.split(r"[,\s]+", item.strip()):
                    if part:
                        add_one(part)
            elif isinstance(item, dict):
                for k in ("tag", "name", "value"):
                    v = item.get(k)
                    if isinstance(v, str) and v.strip():
                        add_one(v)
                        break
    elif isinstance(val, str):
        for t in re.split(r"[,\s]+", val.strip()):
            if t:
                add_one(t)
    return out

def _extract_tags(fm: dict):
    """Findet 'tags' key in beliebiger Groß-/Kleinschreibung."""
    for k, v in fm.items():
        if str(k).lower() == "tags":
            return v
    return None

# ----------------------------- Family / Gruppen ------------------------------
FAMILY_CANON = {
    # eingehende Werte -> kanonischer Key
    "intradev": "intradev",
    "intradev-rest": "intradev",
    "intranet": "intranet",
    "intranet-rest": "intranet",
    "odata": "odata",
}

def derive_family(md_path: Path, fm_family: str | None) -> str:
    """
    Bestimmt die Family:
      1) aus Frontmatter 'family' (falls vorhanden)
      2) aus Pfadteilen (intradev/intranet/odata)
    Liefert kanonische Keys: 'intradev' | 'intranet' | 'odata' | ''.
    """
    if fm_family:
        raw = str(fm_family).lower()
    else:
        parts = [p.lower() for p in md_path.parts]
        if   "intradev" in parts: raw = "intradev-rest"
        elif "intranet" in parts: raw = "intranet-rest"
        elif "odata"    in parts: raw = "odata"
        else: raw = ""
    return FAMILY_CANON.get(raw, raw or "")

# ----------------------------- Sortierung & Badges ---------------------------
STAGE_ORDER = {"GA": 0, "Prod": 0, "Beta": 1, "Alpha": 2, "Dev": 3}
STAGE_BADGE_COLOR = {
    "GA": "brightgreen",
    "Prod": "brightgreen",
    "Beta": "yellow",
    "Alpha": "orange",
    "Dev": "blue",
    "Deprecated": "lightgrey",
}

def stage_badge(stage: str) -> str:
    """Markdown-Image für Shields.io Stage-Badge."""
    color = STAGE_BADGE_COLOR.get(stage, "inactive")
    return f"![{stage}](https://img.shields.io/badge/stage-{stage.replace(' ', '%20')}-{color})"

# ----------------------------- Markdown Helpers ------------------------------
def md_code(s: str) -> str:
    return f"`{s}`" if s else "–"

def md_link(text: str, href: str) -> str:
    if not href:
        return "–"
    return f"[`{text or href}`]({href})"

GROUP_TITLES = {
    "intradev": "IntraDev-Schnittstellen",
    "intranet": "Intranet-Schnittstellen",
    "odata":    "OData-Schnittstellen",
}

def render_group_table(group_key: str, rows: List[Dict]) -> str:
    """
    Baut eine Markdown-Tabelle für eine Gruppe.

    Spalten: API | Base | Auth | Stage | Spec | Method | guid_hash | path_entities | path_prefix
    Erwartet rows mit Keys: name, base, auth, stage, spec, method, guid_hash, path_entities, path_prefix.
    """
    if not rows:
        return ""

    def esc_md(s: str) -> str:
        # Pipes escapen, Newlines in <br> umwandeln
        return s.replace("|", r"\|").replace("\n", "<br>")

    def fmt(val, *, code=False):
        if val is None or val == "" or val == []:
            return "–"
        if isinstance(val, (list, tuple)):
            s = ", ".join(map(str, val))
        elif isinstance(val, dict):
            s = json.dumps(val, ensure_ascii=False, separators=(",", ":"))
        else:
            s = str(val)
        s = esc_md(s)
        return f"`{s}`" if code and s != "–" else s

    title = GROUP_TITLES.get(group_key, group_key.title())

    cols = ["API", "Base", "Auth", "Stage", "Spec", "Method", "guid_hash", "path_entities", "path_prefix"]
    header = "| " + " | ".join(cols) + " |"
    sep    = "|" + "|".join("---" for _ in cols) + "|"

    lines = [f"## {title}\n", header, sep]

    for r in rows:
        name        = fmt(r.get("name") or "–")
        base        = fmt(r.get("base"), code=True)
        auth        = fmt(r.get("auth") or "–")
        badge       = stage_badge(r.get("stage", "Dev"))  # Badge kann Markdown/HTML sein
        spec_url    = r.get("spec")
        spec        = md_link(spec_url, spec_url) if spec_url else "–"
        method      = fmt((r.get("method") or "–"))
        method      = f"`{method.upper().strip('`')}`" if method != "–" else "–"
        guid_hash   = fmt(r.get("guid_hash") or "–")
        path_prefix = fmt(r.get("path_prefix"))
        path_ents   = fmt(r.get("path_entities"))

        lines.append(
            f"| {name} | {base} | {auth} | {badge} | {spec} | {method} | {guid_hash} | {path_ents} | {path_prefix} | "
        )

    lines.append("")  # trailing newline
    return "\n".join(lines)

def write_overview_md(grouped: dict[str, list[dict]], out_path: Path) -> None:
    """
    Schreibt 'overview.md' mit fester Gruppen-Reihenfolge.
    Überspringt leere Gruppen.
    """
    order = ["intradev", "intranet", "odata"]
    parts: list[str] = []
    for key in order:
        section = render_group_table(key, grouped.get(key, []))
        if section:
            parts.append(section)
    content = "\n".join(parts).rstrip() + "\n"
    out_path.write_text(content, encoding="utf-8")

def write_yaml(rows: list[dict], out_path: Path) -> None:
    """Schreibt die flache Registry YAML: {'apis': rows}."""
    out_path.write_text(
        yaml.safe_dump({"apis": rows}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

# --- schlanke Helfer ---
_RE_CURLY = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_RE_COLON = re.compile(r":([A-Za-z_][A-Za-z0-9_]*)")

def _short_hash(s: str, n: int = 8) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]

def _extract_path_entities(*texts: Any) -> list[str] | None:
    seen: list[str] = []
    def add(x: str):
        if x and x not in seen:
            seen.append(x)
    for t in texts:
        if not t:
            continue
        s = str(t)
        for m in _RE_CURLY.findall(s): add(m)
        for m in _RE_COLON.findall(s): add(m)
    return seen or None

# ----------------------------- Scan / Build Rows -----------------------------
def _as_list(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple, set)):
        return [x for x in v if x is not None]
    if isinstance(v, str):
        parts = re.split(r"[;,]", v)
        return [p.strip() for p in parts if p.strip()]
    return [v]

def build_rows_from_sources(
    sources: Iterable[Path],
) -> tuple[list[dict], int, int]:
    """
    Traversiert source-Ordner, liest Frontmatter und baut Zeilen.
    Exportiert **alle** Tags und **alle** status/*-Tags (keine Filterung).
    Return: (rows, scanned_count, kept_count)
    """
    rows: list[dict] = []
    scanned = kept = 0

    for src in sources:
        if not src.exists():
            warn(f"source not found: {src}")
            continue

        for md in src.rglob("*.md"):
            scanned += 1
            fm = read_frontmatter(md)
            if not fm:
                continue

            # Alle Tags normalisieren und Status-Tags ableiten (keine Filterung)
            norm_tags: set[str] = _normalize_tags(_extract_tags(fm))
            status_list = sorted(t for t in norm_tags if t.startswith("status/"))

            family = derive_family(md, fm.get("family"))
            row = {
                "name":        fm.get("name") or fm.get("title") or md.stem,
                "family":      family,
                "base":        fm.get("base") or fm.get("base_url") or "",
                "auth":        fm.get("auth") or "",
                "stage":       fm.get("stage") or "Dev",
                "spec":        fm.get("spec") or "",
                "path_prefix": fm.get("path_prefix") or "",
                "status":      status_list,          # alle status/* als Liste
                "tags":        sorted(norm_tags),    # alle Tags (normalisiert)
                "path":        str(md),
            }

            # method → String (bei Liste kommasepariert)
            m = fm.get("method")
            if not m and fm.get("methods"):
                mm = [str(x).strip() for x in _as_list(fm.get("methods")) if str(x).strip()]
                m = ", ".join(mm) if mm else None
            if m:
                row["method"] = m

            # guid_hash → übernehmen oder kurz aus guid/app_guid ableiten
            gh = fm.get("guid_hash")
            if not gh:
                src_guid = fm.get("guid") or fm.get("app_guid")
                if src_guid:
                    gh = _short_hash(str(src_guid))
            if gh:
                row["guid_hash"] = str(gh)

            # path_entities – bevorzugt direkt aus dem Frontmatter übernehmen
            pe = fm.get("path_entities")
            if isinstance(pe, str):
                pe = [pe]
            pe = [str(x).strip() for x in (pe or []) if str(x).strip()]

            if pe:
                row["path_entities"] = pe
            else:
                # Fallback: aus Pfadfeldern extrahieren (nur Platzhalter)
                pe_fb = _extract_path_entities(
                    fm.get("path"),
                    row["base"],
                    fm.get("endpoint"),
                    fm.get("endpoints"),
                    fm.get("paths"),
                    fm.get("path_prefix"),
                )
                if pe_fb:
                    row["path_entities"] = pe_fb

            # optionale Felder
            if fm.get("app_guid"):
                row["app_guid"] = fm["app_guid"]
            if fm.get("owner_ref"):
                row["owner_ref"] = fm["owner_ref"]
            if fm.get("owner"):
                row["owner"] = fm["owner"]

            rows.append(row)
            kept += 1
            if "THETAGTESTERFILER" in md.name:
                info(f"[APPEND] added row for tester: {row.get('name')} | family={row.get('family')} | status={row.get('status')}")

    # Primär: Family, sekundär: Stage (definierte Ordnung), tertiär: Name
    rows.sort(key=lambda r: (
        r.get("family", ""),
        STAGE_ORDER.get(r.get("stage", "Dev"), 9),
        r.get("name", "").lower()
    ))
    return rows, scanned, kept

def group_rows(rows: list[dict]) -> dict[str, list[dict]]:
    """Gruppiert rows nach 'family' und sortiert jede Gruppe konsistent."""
    grouped: dict[str, list[dict]] = {}
    for r in rows:
        g = r.get("family") or ""
        grouped.setdefault(g, []).append(r)
    for g in grouped.values():
        g.sort(key=lambda r: (STAGE_ORDER.get(r.get("stage","Dev"), 9), r.get("name","").lower()))
    return grouped
