#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventory English source strings that look like robots / attacks / moves.

Reads the translation maps already produced in datos/ and writes a deduplicated
candidate list so the official Spain-dub glossary can be applied systematically.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATOS = ROOT / "datos"

KEYWORDS = re.compile(
    r"\b(gundam|evangelion|eva[- ]?\d|aestivalis|mazinger|getter|grendizer|"
    r"robot|mobile suit|newtype|psycommu|beam|cannon|rifle|gun|blade|sword|"
    r"lance|missile|attack|strike|drive|slash|kick|punch|claw|fang|shield|"
    r"barrier|field|saber|saber|hammer|axe|spear|shot|burst|wave|ray|laser|"
    r"plasma|positron|photon|particle|vernier|thruster|unit[- ]?\d|type[- ]?\d)\b",
    re.I,
)


def load_json_map(path: Path) -> dict[str, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out: dict[str, str] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(k, str) and isinstance(v, str):
                out[k] = v
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for a, b in item.items():
                    if isinstance(a, str) and isinstance(b, str):
                        out[a] = b
    return out


def main() -> None:
    found: Counter[str] = Counter()
    where: dict[str, set[str]] = {}

    files = [DATOS / "systext_trans.json", DATOS / "prologue_trans_v6.json"]
    files += sorted((DATOS / "es_batches").glob("*.json"))
    files += sorted(DATOS.glob("mtzkn_*_es*.json"))
    files += sorted(DATOS.glob("kpack_*_es.json"))
    files += sorted(DATOS.glob("ln_id*_es*.json"))

    for path in files:
        if not path.exists():
            continue
        for src, dst in load_json_map(path).items():
            if KEYWORDS.search(src):
                found[src] += 1
                where.setdefault(src, set()).add(path.name)

    csv_path = DATOS / "lineas_batalla_final_es6.csv"
    if csv_path.exists():
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                src = row.get("en") or ""
                if KEYWORDS.search(src):
                    found[src] += 1
                    where.setdefault(src, set()).add("CMN00")

    lines = [
        "# Candidatos a glosario oficial (doblaje España)",
        f"# {len(found)} cadenas únicas",
        "",
    ]
    for src in sorted(found, key=str.casefold):
        lines.append(f"{src}\t[{', '.join(sorted(where[src]))}]")

    out = DATOS / "glossary_candidates.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"escrito {out} ({len(found)} cadenas)")


if __name__ == "__main__":
    main()
