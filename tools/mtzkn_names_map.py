# -*- coding: utf-8 -*-
"""Construye datos/mtzkn_names_es.json: nombres de unidad/piloto de los MtZkn.

Reutiliza las traducciones de datos/rpw_jstr_es.json (mismas cadenas compartidas)
y anade las variantes descriptivas que solo aparecen en los MtZkn.
"""
import io
import json

D = r"C:/Dev/Default Project/srwv/datos/"

NEW = {
    "Destoria-class Astro Heavy Battlecruiser (Elite Space Guard Coating)":
        "Crucero de batalla espacial pesado clase Destoria (revestimiento de élite de la Guardia Espacial)",
    "Geara Zulu (Heavy Armament)": "Geara Zulu (armamento pesado)",
    "Meltoria-class": "Clase Meltoria",
    "Meltoria-class Astro Battlecruiser":
        "Crucero de batalla espacial clase Meltoria",
    "Meltoria-class Astro Battlecruiser (Elite Space Guard Coating)":
        "Crucero de batalla espacial clase Meltoria (revestimiento de élite de la Guardia Espacial)",
    "Polmeria-class Assault Astro Carrier (Elite Space Guard Coating)":
        "Portaaviones espacial de asalto clase Polmeria (revestimiento de élite de la Guardia Espacial)",
    "Special Class 1 Astro Combatant Ship Desura II":
        "Nave de combate espacial especial de clase 1 Desura II",
    "Airborne Battleship Blanca": "Acorazado volador Blanca",
}


def main():
    work = json.load(io.open(D + "mtzkn_names_worklist.json", encoding="utf-8"))
    shared = json.load(io.open(D + "rpw_jstr_es.json", encoding="utf-8"))
    out = {}
    for n in work:
        if n in shared:
            out[n] = shared[n]
    for k, v in NEW.items():
        if k in work:
            out[k] = v
        else:
            print("AVISO: no esta en la lista de trabajo:", repr(k))
    print("nombres con traduccion:", len(out), "de", len(work))
    same = [k for k, v in out.items() if k == v]
    print("identicas (nombres oficiales conservados):", len(same))
    json.dump(out, io.open(D + "mtzkn_names_es.json", "w", encoding="utf-8",
                           newline="\n"), ensure_ascii=False, indent=0, sort_keys=True)
    print("escrito datos/mtzkn_names_es.json")
    for k in sorted(out):
        if out[k] != k:
            print("  %-58s -> %s" % (k[:58], out[k][:70]))


if __name__ == "__main__":
    main()
