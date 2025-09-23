from __future__ import annotations
from pathlib import Path
from export_functions import (
    info, err, build_rows_from_sources, write_yaml, write_overview_md, group_rows
)

# ---------- Pfade (robust, unabhängig vom CWD) ----------
HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent  # Repo/Vault-Root = Ordner über "scripts"

# Quellbäume: passe an, falls OData (noch) nicht existiert
SRC_DIRS = [
    ROOT / "API_Endpoints" / "IntraDev",
    ROOT / "API_Endpoints" / "Intranet",
    ROOT / "API_Endpoints" / "OData-Dienste",  # optional
]

OUT_YAML = ROOT / "registry" / "apis.yml"
OUT_MD   = ROOT / "registry" / "overview.md"
OUT_YAML.parent.mkdir(parents=True, exist_ok=True)

def main() -> int:
    info(f"ROOT: {ROOT}")
    info("SRC_DIRS:\n  - " + "\n  - ".join(str(p) for p in SRC_DIRS))

    rows, scanned, kept = build_rows_from_sources(SRC_DIRS)

    try:
        write_yaml(rows, OUT_YAML)
    except Exception as e:
        err(f"write error: {OUT_YAML} -> {e}")
        return 2

    grouped = group_rows(rows)
    try:
        write_overview_md(grouped, OUT_MD)
    except Exception as e:
        err(f"write error: {OUT_MD} -> {e}")
        return 2

    info(f"wrote {OUT_YAML} and {OUT_MD} | entries={len(rows)} (scanned={scanned}, kept={kept})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
