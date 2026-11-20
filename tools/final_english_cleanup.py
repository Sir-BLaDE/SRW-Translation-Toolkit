# -*- coding: utf-8 -*-
"""Limpieza final de ingles residual en mapas activos."""
import io
import json

D = r"C:/Dev/Default Project/srwv/datos"

# 1) rpw_jstr: traducciones parciales que dejaron fragmentos EN.
p = D + "/rpw_jstr_es.json"
tm = json.load(io.open(p, encoding="utf-8"))
R = [
    ("All non-exclusive units move as if in Air.",
     "Todas las unidades no exclusivas se mueven como si estuvieran en Aire."),
    ("All non-exclusive units move as if on Grd.",
     "Todas las unidades no exclusivas se mueven como si estuvieran en Tierra."),
    ("All non-exclusive units move as if in Wtr.",
     "Todas las unidades no exclusivas se mueven como si estuvieran en Agua."),
    ("All non-exclusive\nunits move as if in Air.",
     "Todas las unidades no exclusivas\nse mueven como si estuvieran en Aire."),
    ("move as if in Air.", "muerto"),
]
n = 0
for k, v in list(tm.items()):
    out = v
    out = out.replace("All non-exclusive units move as if in Air.",
                      "Todas las unidades no exclusivas se mueven como si estuvieran en Aire.")
    out = out.replace("All non-exclusive units move as if on Grd.",
                      "Todas las unidades no exclusivas se mueven como si estuvieran en Tierra.")
    out = out.replace("All non-exclusive units move as if in Wtr.",
                      "Todas las unidades no exclusivas se mueven como si estuvieran en Agua.")
    out = out.replace("All non-exclusive\nunits move as if in Air.",
                      "Todas las unidades no exclusivas\nse mueven como si estuvieran en Aire.")
    if out != v:
        tm[k] = out
        n += 1
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("rpw_jstr valores corregidos:", n)

# 2) B_LT00: cadena suelta detectada por la auditoria.
p = D + "/b_lt00_rest_es_p7.json"
tm = json.load(io.open(p, encoding="utf-8"))
tm["Mega Beam Launcher DMG by 200."] = "el DMG del Lanzador de Mega Haz en 200."
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("b_lt00 p7:", len(tm))

# 3) sistem: asegurar termino del glosario en el mapa activo.
p = D + "/systext_trans.json"
tm = json.load(io.open(p, encoding="utf-8"))
old = tm.get("Artificial Newtype")
tm["Artificial Newtype"] = "Nuevo Tipo artificial"
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("systext Artificial Newtype:", repr(old), "->", repr(tm["Artificial Newtype"]))
