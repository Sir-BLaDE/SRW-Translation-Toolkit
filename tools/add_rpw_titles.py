# -*- coding: utf-8 -*-
"""Anade titulos Gundam pendientes al mapa rpw_jstr_es.json."""
import io
import json

P = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"
tm = json.load(io.open(P, encoding="utf-8"))
NEW = {
    "Mobile Suit Gundam: Char's Counterattack":
        "Traje móvil Gundam: El contraataque de Char",
    "Mobile Suit Gundam: Hathaway's Flash":
        "Traje móvil Gundam: El destello de Hathaway",
    "Mobile Suit Crossbone Gundam: Skull Heart":
        "Traje móvil Crossbone Gundam: Corazón de Calavera",
}
n = 0
for a, b in NEW.items():
    tm[a] = b
    n += 1
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("anadidos:", n)
