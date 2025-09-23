
from __future__ import annotations
import argparse, re, sys, hashlib
from pathlib import Path

GUID_HEX_RE = re.compile(r"\b[0-9a-fA-F]{8,40}\b")

def _default_md_path() -> Path | None:
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent / "registry" / "overview.md",
        here / "registry" / "overview.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

def _split_md_row(line: str) -> list[str]:
    # "| a | b |" -> ["a","b"]
    core = line.strip()
    if not (core.startswith("|") and core.endswith("|")):
        return []
    core = core[1:-1]
    # robust gegen einfache Inhalte (Pipes sind in deiner Generierung escaped)
    parts = [p.strip() for p in core.split("|")]
    return parts

def _join_md_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"

def _norm_guid(cell: str) -> str:
    """
    Extrahiert etwas zum Sortieren:
    - Prefer echter Hex-GUID-Hash (8..40 hex) aus Backticks/Badge/Plaintext
    - sonst leerer String
    """
    # entferne Markdown-Backticks
    txt = cell.strip().strip("`")
    # Falls Badge: nimm den Hash aus Alt-Text oder Message, ansonsten suche generell
    m = GUID_HEX_RE.search(txt)
    return (m.group(0).lower() if m else "")

def _guid_badge(guid: str) -> str:
    """Erzeuge farbstabilen Shields.io-Badge aus GUID (hex)."""
    if not guid:
        return "–"
    short = guid[:8].upper()
    h = hashlib.sha1(guid.encode("utf-8")).hexdigest()
    color = h[:6]
    # Helligkeit prüfen (YIQ), zu helle Farbe durch andere 6 Hex ersetzen
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    yiq = (299*r + 587*g + 114*b) / 1000
    if yiq > 200:
        color = h[6:12]
    return f"![GUID {short}](https://img.shields.io/badge/GUID-{short}-%23{color})"

def sort_table_block(lines: list[str], start: int, end: int, use_badge: bool) -> None:
    """
    Sortiert die Tabelle IN-PLACE zwischen indices [start, end) (Header+Sep+Rows).
    """
    header = _split_md_row(lines[start])
    sep    = lines[start+1]
    rows   = lines[start+2:end]

    # Spaltenindex bestimmen
    colmap = {name.strip().lower(): i for i, name in enumerate(header)}
    guid_col = None
    for key in ("guid_hash", "guid"):
        if key in colmap:
            guid_col = colmap[key]
            break
    if guid_col is None:
        return  # nichts zu tun

    name_col = colmap.get("api", 0)  # Fallback: 0

    # Parse rows -> (cells, orig_line)
    parsed: list[tuple[list[str], str]] = []
    for rline in rows:
        cells = _split_md_row(rline)
        if not cells:
            continue
        parsed.append((cells, rline))

    # Sortierschlüssel: guid leer -> 1 (nach hinten), sonst 0; dann guid, dann name
    def sk(p):
        cells, _ = p
        guid_norm = _norm_guid(cells[guid_col])
        name_val = cells[name_col]
        return (0 if guid_norm else 1, guid_norm, name_val.lower())

    parsed.sort(key=sk)

    # Optional: GUID-Badge statt Text
    if use_badge:
        for cells, _ in parsed:
            guid_norm = _norm_guid(cells[guid_col])
            if guid_norm:
                # Kurzer Badge + vollständige GUID im Codeblock
                cells[guid_col] = f"{_guid_badge(guid_norm)} `{guid_norm.upper()}`"
            else:
                cells[guid_col] = "–"
    # zurück in lines schreiben
    new_rows = [_join_md_row(cells) for cells, _ in parsed]
    lines[start:end] = [ _join_md_row(header), sep, *new_rows ]

def process_file(path: Path, inplace: bool, backup: bool, badge: bool) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Tabellenblöcke finden: Header-Zeile + Separator-Zeile
    i = 0
    changed = False
    while i < len(lines)-1:
        if lines[i].lstrip().startswith("|") and lines[i+1].strip().startswith("|---"):
            # finde Ende (erste Nicht-Tabellenzeile)
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            # sortiere nur Tabellen, die guid-Spalte haben
            header_cells = _split_md_row(lines[i])
            if any(h.strip().lower() in ("guid_hash", "guid") for h in header_cells):
                sort_table_block(lines, i, j, use_badge=badge)
                changed = True
            i = j
        else:
            i += 1

    if not changed:
        print(f"[info] nothing to do in {path}")
        return

    out = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if inplace:
        if backup:
            bak = path.with_suffix(path.suffix + ".bak")
            bak.write_text(text, encoding="utf-8")
        path.write_text(out, encoding="utf-8")
        print(f"[ok] sorted: {path}")
    else:
        sys.stdout.write(out)

def main():
    ap = argparse.ArgumentParser(description="Sort markdown overview tables by guid_hash (stable color optional).")
    ap.add_argument("file", nargs="?", help="Path to overview.md (default: ../registry/overview.md)")
    ap.add_argument("--no-inplace", action="store_true", help="Write to stdout instead of overwriting the file")
    ap.add_argument("--no-backup", action="store_true", help="Do not create .bak backup when writing inplace")
    ap.add_argument("--badge", action="store_true", help="Render GUID column as color-stable badge")
    args = ap.parse_args()

    md_path = Path(args.file).resolve() if args.file else _default_md_path()
    if not md_path or not md_path.exists():
        sys.exit("overview.md not found. Give a path or place it under ./registry/ or ../registry/")

    process_file(md_path, inplace=not args.no_inplace, backup=not args.no_backup, badge=args.badge)

if __name__ == "__main__":
    main()
