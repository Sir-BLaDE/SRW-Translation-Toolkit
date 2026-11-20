# -*- coding: utf-8 -*-
"""Traducciones de B_LT00, lote 5 (residuos y falsos positivos)."""
import json
import os

D = r"C:/Dev/Default Project/srwv/datos"

T = {
"Increases Accuracy % and Evasion %. Expands certain weapon ranges.": "Aumenta la puntería y la evasión. Amplía el alcance de ciertas armas.",
"Reduce en 10 los PE del piloto principal enemigo.": "Reduce en 10 los PE del piloto principal enemigo.",
"Reduce en 30 la movilidad de una unidad enemiga durante un turno.": "Reduce en 30 la movilidad de una unidad enemiga durante un turno.",
"Reduce en 5 el Enfoque del piloto principal enemigo.": "Reduce en 5 el Enfoque del piloto principal enemigo.",
"Reduce en 200 la armadura de una unidad enemiga.": "Reduce en 200 el blindaje de una unidad enemiga.",
"Reduce a la mitad el CQB, RNG, HIT, EVD, DEF y SKL de una unidad enemiga": "Reduce a la mitad el CQB, RNG, HIT, EVD, DEF y SKL de una unidad enemiga",
"Reduce en 30 la EN de una unidad enemiga.": "Reduce en 30 la EN de una unidad enemiga.",
"Reduce en 10 el Enfoque de un piloto enemigo al atacar su": "Reduce en 10 el Enfoque de un piloto enemigo al atacar su",
"Reduce en 5 el Enfoque del atacante.": "Reduce en 5 el Enfoque del atacante.",
}

with open(os.path.join(D, "b_lt00_rest_es_p5.json"), "w", encoding="utf-8") as fh:
    json.dump(T, fh, ensure_ascii=False, indent=1)
print("lote 5:", len(T))
