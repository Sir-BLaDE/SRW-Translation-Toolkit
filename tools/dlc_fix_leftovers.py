# -*- coding: utf-8 -*-
REPL = {
    "Martian Successors": "Sucesores Marcianos",
    "Martian Successor": "Sucesor Marciano",
    "Jupiter Empire": "Imperio de Júpiter",
    "Jupiter War": "Guerra de Júpiter",
}
import glob
import io
import json
import os

BATCH = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"
total = 0
for p in sorted(glob.glob(os.path.join(BATCH, "*.es.json"))):
    arr = json.load(io.open(p, encoding="utf-8"))
    changed = False
    for i, s in enumerate(arr):
        new = s
        for a, b in REPL.items():
            new = new.replace(a, b)
        if new != s:
            print(os.path.basename(p), i, repr(s[:110]), "->", repr(new[:110]))
            arr[i] = new
            changed = True
            total += 1
    if changed:
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(arr, f, ensure_ascii=False, indent=1)
print("entradas corregidas:", total)
