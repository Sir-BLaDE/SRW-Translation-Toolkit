# -*- coding: utf-8 -*-
"""Traduce titulos y frases inglesas restantes en rpw_jstr_es.json."""
import io
import json

P = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"
tm = json.load(io.open(P, encoding="utf-8"))
NEW = {
    "EVANGELION 1.0 YOU ARE (NOT) ALONE.": "EVANGELION 1.0 ERES TÚ (NO) SOLO.",
    "EVANGELION 2.0 YOU CAN (NOT) ADVANCE.": "EVANGELION 2.0 PUEDES (NO) AVANZAR.",
    "EVANGELION 3.0 YOU CAN (NOT) REDO.": "EVANGELION 3.0 PUEDES (NO) REHACER.",
    "Full Metal Panic Series": "Serie Full Metal Panic!",
    "Full Metal Panic! The Second Raid": "Full Metal Panic! La segunda incursión",
    "Soul of Steel": "Alma de acero",
}
n = 0
for k, v in NEW.items():
    if k in tm and tm[k] != v:
        tm[k] = v
        n += 1
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("titulos actualizados:", n)
