# -*- coding: utf-8 -*-
"""Acorta traducciones de la fila 594 para no desbordar ExtractSize (u16)."""
import io
import json
import os

W = r"C:/Dev/Default Project/srwv/datos/stgest_bracket_work"

# (archivo, clave EN exacta, valor nuevo)
CAMBIOS = [
    ("b_11_out.json",
     "Nine\r\n（I hope you will stay with me the whole way...）",
     "Nine\r\n（Quédate conmigo hasta el final...）"),
    ("b_16_out.json",
     "Sousuke\r\n（Leonard's real goal is to revise the past\r\n"
     "　by using space-time fusion, which means\r\n"
     "　destroying the world in the process.）",
     "Sousuke\r\n（El objetivo de Leonard es revisar el pasado\r\n"
     "　con la fusión espacio-temporal, y eso significa\r\n"
     "　destruir el mundo.）"),
    ("b_15_out.json",
     "Sousuke\r\n（But that doesn't add up because Kaname rejected\r\n"
     "　Sophia, which put her into that deep sleep. So\r\n"
     "　why would things changes so suddenly?）",
     "Sousuke\r\n（Pero eso no encaja: Kaname rechazó a Sophia\r\n"
     "　y eso la sumió en ese sueño profundo. ¿Por qué\r\n"
     "　cambiarían las cosas tan de repente?）"),
    ("b_10_out.json",
     "Mori\r\n（Aw, I thought we were getting somewhere, too.）",
     "Mori\r\n（Vaya, yo también creía que avanzábamos.）"),
    ("b_16_out.json",
     "Sousuke\r\n（Major Kalinin risked his life to\r\n"
     "　share that information with me. I don't\r\n"
     "　want those efforts to be in vain, either.）",
     "Sousuke\r\n（Kalinin se jugó la vida para\r\n"
     "　compartir esa información conmigo. No quiero\r\n"
     "　que esos esfuerzos sean en vano.）"),
]

for fn, key, new in CAMBIOS:
    path = os.path.join(W, fn)
    data = json.load(io.open(path, encoding="utf-8"))
    if key not in data:
        raise SystemExit("FALTA la clave en %s: %r" % (fn, key[:70]))
    old = data[key]
    # Comprobar que solo cambia el texto, no la estructura
    assert old.count("\r") == new.count("\r"), (fn, "CR")
    assert old.count("\n") == new.count("\n"), (fn, "LF")
    assert old.count("　") == new.count("　"), (fn, "U+3000")
    assert old.count("（") == new.count("（") and old.count("）") == new.count("）")
    ahorro = len(old.encode("utf-8")) - len(new.encode("utf-8"))
    data[key] = new
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("%-16s ahorro=%+4d  %r" % (fn, ahorro, new[:60]))
