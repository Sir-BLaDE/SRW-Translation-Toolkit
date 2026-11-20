#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica un glosario oficial (doblaje España) a los mapas de traducción.

Uso:
  python apply_glossary.py [--dry-run]

El glosario se lee de datos/glosario_españa.json con forma:
  {"English source string": "Traducción oficial España", ...}

Se actualizan:
  - datos/lineas_batalla_final_es6.csv  (columna es, por texto EN exacto)
  - datos/es_batches/*.json             (clave = id; se resuelve el EN desde el CSV)
  - datos/systext_trans.json y demás mapas indexados por texto EN
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATOS = ROOT / "datos"
GLOSSARY = DATOS / "glosario_españa.json"
REPLACEMENTS = DATOS / "glosario_replacements.json"
CSV = DATOS / "lineas_batalla_final_es6.csv"
JSON_MAPS = [
    "systext_trans.json",
    "prologue_trans_v6.json",
    "kpack_rg_es.json",
    "ln_id0_es.json",
    "ln_id1_es.json",
    "ln_id3_descs_es.json",
    "ln_id4_es.json",
]
JSON_GLOBS = ["mtzkn_*_es*.json", "es_batches/*.json"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    gl = load_json(GLOSSARY)
    reps = load_json(REPLACEMENTS) if REPLACEMENTS.exists() else {}
    # ordenar por longitud descendente para no romper variantes largas
    reps = dict(sorted(reps.items(), key=lambda kv: len(kv[0]), reverse=True))
    print(f"glosario: {len(gl)} términos, {len(reps)} reemplazos")

    def apply_reps(text: str) -> str:
        if not isinstance(text, str):
            return text
        for old, new in reps.items():
            text = text.replace(old, new)
        return text

    # CSV: resolver por texto inglés exacto
    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig", newline="")))
    id_to_en = {r["id"]: r["en"] for r in rows}
    changed_csv = 0
    for r in rows:
        new = gl.get(r["en"])
        if new is None:
            new = apply_reps(r["es"])
        if new is not None and r["es"] != new:
            r["es"] = new
            changed_csv += 1
    if not args.dry_run and changed_csv:
        with CSV.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "en", "es"])
            w.writeheader()
            w.writerows(rows)
    print(f"CSV: {changed_csv} filas")

    # Mapas indexados por texto inglés
    files = [DATOS / name for name in JSON_MAPS]
    for pat in JSON_GLOBS:
        files += sorted(DATOS.glob(pat))
    total_changed = 0
    for path in files:
        if not path.exists():
            continue
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        changed = 0
        for key, val in list(data.items()):
            src = key
            if path.parent.name == "es_batches":
                # las claves son ids numéricos -> resolver al texto EN
                src = id_to_en.get(str(key), key)
            new = gl.get(src)
            if new is None:
                new = apply_reps(val)
            if new is not None and isinstance(val, str) and val != new:
                data[key] = new
                changed += 1
        if changed:
            if not args.dry_run:
                save_json(path, data)
            print(f"  {path.relative_to(ROOT)}: {changed}")
            total_changed += changed
    print(f"mapas JSON: {total_changed} valores")
    if args.dry_run:
        print("(dry-run: no se escribió nada)")


if __name__ == "__main__":
    main()
