# -*- coding: utf-8 -*-\n"""Anade al mapa de rpw_jstr las cadenas inglesas que faltaban."""
import io
import json
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"C:/Dev/Default Project/srwv/backup/rpw_jstr_original.cpk"
TM = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"
POOL, PEND = 0x48, 0x1EE10

TITLES = {
    "Mobile Suit Crossbone Gundam: The Steel Seven": "Traje móvil Crossbone Gundam: Los Siete de Acero",
    "Mobile Suit Gundam 00 the Movie: A Wakening of the Trailblazer":
        "Traje móvil Gundam 00: La película – El despertar del pionero",
    "Martian Successor Nadesico: The Motion Picture – Prince of Darkness":
        "Sucesor Marciano Nadesico: La película – Príncipe de la Oscuridad",
    "True Mazinger Edition Z: The Impact!": "Mazinger Z: Edición Verdadera – ¡El Impacto!",
    "Cross Ange: Rondo of Angels and Dragons": "Cross Ange: Rondo de ángeles y dragones",
    "Soul of Steel": "Alma de acero",
}

R = [
    ("Changes terrain handling for units/weapons to ", "Cambia la adaptación al terreno de unidades/armas a "),
    ("Changes terrain handling for all types of terrain for\nunits/weapons to ",
     "Cambia la adaptación al terreno de todo tipo de terreno para\nunidades/armas a "),
    ("Changes terrain handling for all types\nof terrain for units/weapons to ",
     "Cambia la adaptación al terreno de todo tipo\nde terreno para unidades/armas a "),
    ("Changes adaptivity for units/weapons\nto ", "Cambia la adaptación de unidades/armas\na "),
    ("Changes adaptivity for units/weapons to ", "Cambia la adaptación de unidades/armas a "),
    ("Changes adaptivity for units/wpns to ", "Cambia la adaptación de unidades/armas a "),
    ("Adaptivity for\nunits/weapons to ", "Adaptación de\nunidades/armas a "),
    ("Adaptivity for units/weapons to ", "Adaptación de unidades/armas a "),
    ("Adaptivity for units/wpns to ", "Adaptación de unidades/armas a "),
    ("All non-exclusive units move as if in Air.",
     "Todas las unidades no exclusivas se mueven como si estuvieran en Aire."),
    ("All non-exclusive units move as if on Grd.",
     "Todas las unidades no exclusivas se mueven como si estuvieran en Tierra."),
    ("All non-exclusive units move as if in Wtr.",
     "Todas las unidades no exclusivas se mueven como si estuvieran en Agua."),
    ("Air-S, Movement +2.", "Aire-E, Movimiento +2."),
    ("Increases weapon damage by 200.", "Aumenta el daño de las armas en 200."),
    ("Increases Targeting by 20 and Critical by 20.",
     "Aumenta la Puntería en 20 y el Crítico en 20."),
    ("Increases Max HP by 1500, Armor by 300,\nand 10% of Max EN/HP recovered\nat the start of the player's action phase.",
     "Aumenta los PV máx. en 1500 y el Blindaje en 300,\ny recupera un 10 % de EN/PV máx.\nal inicio de la fase de acción del jugador."),
    ("Increases Max HP by 1500, Armor by 300,\nand 10% of Max EN/HP recovered at the start of the player's action phase.",
     "Aumenta los PV máx. en 1500 y el Blindaje en 300, y recupera un 10 % de EN/PV máx. al inicio de la fase de acción del jugador."),
    ("Mob. + 20, and Range + 1 for wpns besides\nmap wpns and wpns with a Range of 1.",
     "Mov. +20 y Alcance +1 para armas excepto\nlas armas de mapa y las de Alcance 1."),
    ("DL Bonus.", "Bonificación DL."),
    ("DL Bonus", "Bonificación DL"),
    ("Air-S", "Aire-E"), ("Grd-S", "Tie-E"), ("Wtr-S", "Agua-E"), ("Spc-S", "Esp-E"),
    (" to A.", " a A."), (" to S.", " a S."),
]

def tr(s):
    if s in TITLES:
        return TITLES[s]
    out = s
    for a, b in R:
        out = out.replace(a, b)
    return out

cf = load(SRC)
pt = cf.plain(cf.rows[0])
tm = json.load(io.open(TM, encoding="utf-8"))
EN = re.compile(r"\b(the|and|you|your|that|this|with|from|they|for|are|will|when|unit|units|weapon|weapons|damage|move|movement|turn|phase|start|all|by|to|of|in|on|at|is|be|it|its|as|or|an|a)\b", re.I)
ES = re.compile(r"[áéíóúñÁÉÍÓÚ¿¡]|\b(el|la|los|las|de|del|que|y|con|por|para|no|es|son|un|una)\b", re.I)
pos = POOL
added = 0
bad = []
while pos < PEND:
    end = pt.find(b"\0", pos)
    try:
        s = pt[pos:end].decode("utf-8")
    except Exception:
        pos = end + 1
        continue
    if s and s not in tm and EN.search(s) and not ES.search(s):
        t = tr(s)
        if EN.search(t) and not ES.search(t):
            bad.append((s, t))
        else:
            tm[s] = t
            added += 1
    pos = end + 1
with io.open(TM, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("anadidas:", added)
for s, t in bad:
    print("SIN TRADUCIR:", repr(s), "->", repr(t))
