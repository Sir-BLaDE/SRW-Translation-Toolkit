# -*- coding: utf-8 -*-
"""Resume el progreso de traduccion de los lotes de DLC."""
import glob
import io
import json
import os

WORK = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"

en_files = sorted(glob.glob(os.path.join(WORK, "batch_*.json")))
total = 0
done = 0
missing = []
for p in en_files:
    if p.endswith(".es.json"):
        continue
    en = json.load(io.open(p, encoding="utf-8"))
    total += len(en)
    es_path = p.replace(".json", ".es.json")
    if os.path.exists(es_path):
        try:
            es = json.load(io.open(es_path, encoding="utf-8"))
        except Exception:
            print("%s: escribiendose todavía" % os.path.basename(es_path))
            missing.append(os.path.basename(p))
            continue
        changed = sum(1 for a, b in zip(en, es) if a != b)
        same = len(en) - changed
        print("%s: %d/%d traducidas, %d identicas" %
              (os.path.basename(es_path), changed, len(en), same))
        done += changed
    else:
        missing.append(os.path.basename(p))

print("\nbloques traducidos: %d / %d (%.1f%%)" %
      (done, total, 100.0 * done / total if total else 0))
print("lotes pendientes (%d): %s" %
      (len(missing), " ".join(missing) if missing else "ninguno"))
