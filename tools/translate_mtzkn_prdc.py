# -*- coding: utf-8 -*-
"""Anade las traducciones de series (PRDC) al mapa de nombres MtZkn."""
import io
import json

P = r"C:/Dev/Default Project/srwv/datos/mtzkn_names_es.json"
tm = json.load(io.open(P, encoding="utf-8"))
NEW = {
    "Brave Express Mightgaine": "Expreso Valiente Mightgaine",
    "Cross Ange: Rondo of Angels and Dragons":
        "Cross Ange: Rondo de ángeles y dragones",
    "EVANGELION 1.0 YOU ARE (NOT) ALONE.":
        "EVANGELION 1.0 ERES TÚ (NO) SOLO.",
    "EVANGELION 2.0 YOU CAN (NOT) ADVANCE.":
        "EVANGELION 2.0 PUEDES (NO) AVANZAR.",
    "EVANGELION 3.0 YOU CAN (NOT) REDO.":
        "EVANGELION 3.0 PUEDES (NO) REHACER.",
    "Full Metal Panic! (Original Novel Version)":
        "Full Metal Panic! (versión original de la novela)",
    "Full Metal Panic! The Second Raid":
        "Full Metal Panic! La segunda incursión",
    "Getter Robo Armageddon": "Getter Robo Armagedón",
    "Martian Successor Nadesico: The Motion Picture – Prince of Darkness":
        "Sucesor Marciano Nadesico: La película – Príncipe de la Oscuridad",
    "Mobile Suit Crossbone Gundam": "Traje móvil Crossbone Gundam",
    "Mobile Suit Crossbone Gundam: Skull Heart":
        "Traje móvil Crossbone Gundam: Corazón de Calavera",
    "Mobile Suit Crossbone Gundam: The Steel Seven":
        "Traje móvil Crossbone Gundam: Los Siete de Acero",
    "Mobile Suit Gundam 00 the Movie: A Wakening of the Trailblazer":
        "Traje móvil Gundam 00: La película – El despertar del pionero",
    "Mobile Suit Gundam SEED Destiny": "Traje móvil Gundam SEED Destiny",
    "Mobile Suit Gundam Unicorn": "Traje móvil Gundam Unicornio",
    "Mobile Suit Gundam ZZ": "Traje móvil Gundam ZZ",
    "Mobile Suit Gundam: Char's Counterattack":
        "Traje móvil Gundam: El contraataque de Char",
    "Mobile Suit Gundam: Hathaway's Flash":
        "Traje móvil Gundam: El destello de Hathaway",
    "Mobile Suit Zeta Gundam": "Traje móvil Zeta Gundam",
    "STAR BLAZERS 2199": "STAR BLAZERS 2199",
    "Super Machine Zambot 3": "Super Máquina Zambot 3",
    "The Unchallengeable Daitarn 3": "El invencible Daitarn 3",
    "True Mazinger Edition Z: The Impact!":
        "Mazinger Z: Edición Verdadera – ¡El Impacto!",
    "True Mazinger ZERO vs Great General of Darkness":
        "Mazinger ZERO vs. el Gran General de la Oscuridad",
    "극장판 기동전사 건담 00 -A wakening of the Trailblazer-":
        "Traje móvil Gundam 00: La película – El despertar del pionero",
    "DYNAMIC PLANNING Original Units":
        "Unidades originales de DYNAMIC PLANNING",
}
n = 0
for a, b in NEW.items():
    if tm.get(a) != b:
        tm[a] = b
        n += 1
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("nombres actualizados:", n)
