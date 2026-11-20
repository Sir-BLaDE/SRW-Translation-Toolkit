# -*- coding: utf-8 -*-
"""Valida los 27 lotes traducidos de DLC y resume el resultado."""
import glob
import io
import json
import os
import re
import sys
import subprocess
from collections import Counter

ROOT = r"C:/Dev/Default Project/srwv"
BATCH = os.path.join(ROOT, "datos", "dlc_work", "batches")
CHECK = os.path.join(ROOT, "tools", "dlc_batch_check.py")

sys.path.insert(0, os.path.join(ROOT, "tools"))
from dlc_batch_check import TOK, ENG  # noqa: E402

fails = []
missing = []
ok = 0
for p in sorted(glob.glob(os.path.join(BATCH, "batch_*.json"))):
    if p.endswith(".es.json"):
        continue
    es = p.replace(".json", ".es.json")
    if not os.path.exists(es):
        missing.append(os.path.basename(p))
        continue
    try:
        json.load(io.open(es, encoding="utf-8"))
    except Exception:
        missing.append(os.path.basename(p))
        continue
    r = subprocess.run([sys.executable, "-u", "-X", "utf8", CHECK, p, es],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode == 0:
        ok += 1
    else:
        fails.append(os.path.basename(es))
        print("=== %s ===" % os.path.basename(es))
        print((r.stdout or "")[-3000:])
        print((r.stderr or "")[-1000:])

print("\nvalidos: %d | con fallos: %d | sin traducir: %d" %
      (ok, len(fails), len(missing)))
if missing:
    print("pendientes:", " ".join(missing))
if fails:
    print("fallos:", " ".join(fails))
    raise SystemExit(1)
if missing:
    raise SystemExit(2)
print("TODOS LOS LOTES OK")
