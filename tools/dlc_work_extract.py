# -*- coding: utf-8 -*-
"""Extrae los bloques [[...]] traducibles de los 30 DLC en orden estable.

Salida:
  datos/dlc_work/blocks_en.json   lista ordenada de textos unicos
  datos/dlc_work/index.json       metadatos (por fichero, filas, ocurrencias)
  datos/dlc_work/batches/batch_NNN.json   lotes de 200 cadenas
"""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk"
WORK = r"C:/Dev/Default Project/srwv/datos/dlc_work"
BLOCK = re.compile(r"\[\[(.*?)\]\]", re.S)


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(os.path.join(WORK, "batches"), exist_ok=True)

    order = []
    seen = {}
    by_file = {}
    rows_of = {}
    total_occ = 0
    for p in sorted(glob.glob(SRC)):
        base = os.path.basename(p)
        c = load(p)
        idxs = []
        rows = []
        for r in c.rows:
            if r["id"] in (1, 2):
                continue
            raw = c.plain(r)
            try:
                txt = raw.decode("utf-8")
            except Exception:
                continue
            if "[[" not in txt:
                continue
            rows.append(r["id"])
            for m in BLOCK.finditer(txt):
                body = m.group(1)
                total_occ += 1
                if body not in seen:
                    seen[body] = len(order)
                    order.append(body)
                    idxs.append(seen[body])
                elif seen[body] not in idxs:
                    idxs.append(seen[body])
        by_file[base] = idxs
        rows_of[base] = rows

    print("ficheros:", len(by_file), "ocurrencias:", total_occ, "unicos:", len(order))
    json.dump(order, io.open(os.path.join(WORK, "blocks_en.json"), "w",
                             encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0)
    json.dump({"by_file": by_file, "rows": rows_of, "unique": len(order),
               "occurrences": total_occ},
              io.open(os.path.join(WORK, "index.json"), "w", encoding="utf-8",
                      newline="\n"), ensure_ascii=False, indent=0)

    size = 200
    nbatches = 0
    for i in range(0, len(order), size):
        chunk = order[i:i + size]
        path = os.path.join(WORK, "batches", "batch_%03d.json" % nbatches)
        json.dump(chunk, io.open(path, "w", encoding="utf-8", newline="\n"),
                  ensure_ascii=False, indent=0)
        nbatches += 1
    print("lotes:", nbatches, "de", size)

    for base in sorted(by_file):
        n = sum(1 for i in by_file[base])
        chars = sum(len(order[i]) for i in by_file[base])
        print("  %-16s filas=%-8s unicos=%3d chars=%6d"
              % (base, rows_of[base], n, chars))


if __name__ == "__main__":
    main()
