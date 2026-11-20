# -*- coding: utf-8 -*-
"""Pasada final: traduce prefijos de rol y terminos antes preservados en los lotes ES.

Los nombres propios de personajes, mechas, naves y organizaciones conocidas
(Crossbone Vanguard, Celestial Being, Huckebein, Gundam, Yamato...) se dejan.
"""
import glob
import io
import json
import os
import re

BATCH = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"

# Prefijos de hablante genericos -> Spanish (se aplican a la primera linea).
PREFIX = {
    "Federation Soldier": "Soldado de la Federación",
    "Exev Subordinate": "Subalterno de Exev",
    "Civilian": "Civil",
    "Soldier": "Soldado",
    "Sensei": "Maestro",
}

# Sustituciones en todo el cuerpo. Ordenadas: primero las mas largas.
REPL = [
    ("Space Pirates", "Piratas Espaciales"),
    ("space pirates", "piratas espaciales"),
    ("Federation Soldier", "Soldado de la Federación"),
    ("Federation soldier", "Soldado de la Federación"),
    ("Exev Subordinate", "Subalterno de Exev"),
    ("Supreme Leader", "Líder Supremo"),
    ("supreme leader", "líder supremo"),
    ("Jupiter Empire", "Imperio de Júpiter"),
    ("Jupiter War", "Guerra de Júpiter"),
    ("Martian Successors", "Sucesores Marcianos"),
    ("Martian Successor", "Sucesor Marciano"),
    ("Mobile Suits", "Trajes móviles"),
    ("Mobile suits", "Trajes móviles"),
    ("mobile suits", "trajes móviles"),
    ("Mobile Suit", "Traje móvil"),
    ("mobile suit", "traje móvil"),
    ("Newtypes", "Nuevos Tipos"),
    ("Newtype", "Nuevo Tipo"),
    ("Lieutenant", "Teniente"),
    ("lieutenant", "teniente"),
    ("Commander", "Comandante"),
    ("commander", "comandante"),
    ("Captain", "Capitán"),
    ("captain", "capitán"),
    ("Sergeant", "Sargento"),
    ("sergeant", "sargento"),
    ("Professor", "Profesor"),
    ("professor", "profesor"),
    ("Admiral", "Almirante"),
    ("admiral", "almirante"),
    ("Officer", "Oficial"),
    ("officer", "oficial"),
    ("Operator", "Operador"),
    ("operator", "operador"),
    ("Major", "Mayor"),
    ("major", "mayor"),
    ("Pilots", "Pilotos"),
    ("pilots", "pilotos"),
    ("Pilot", "Piloto"),
    ("pilot", "piloto"),
    ("Soldiers", "Soldados"),
    ("soldiers", "soldados"),
    ("Soldier", "Soldado"),
    ("soldier", "soldado"),
    ("Civilian", "Civil"),
    ("civilian", "civil"),
    ("Knight", "Caballero"),
    ("knight", "caballero"),
]

total = 0
for p in sorted(glob.glob(os.path.join(BATCH, "*.es.json"))):
    arr = json.load(io.open(p, encoding="utf-8"))
    changed = False
    for i, s in enumerate(arr):
        new = s
        # 1) prefijo del hablante
        m = re.search(r"([「（])", new)
        if m:
            head = new[:m.start()]
            parts = head.split("\r\n")
            name = parts[0]
            if name in PREFIX:
                parts[0] = PREFIX[name]
                new = "\r\n".join(parts) + new[m.start():]
        # 2) cuerpo
        for a, b in REPL:
            new = new.replace(a, b)
        if new != s:
            arr[i] = new
            changed = True
            total += 1
    if changed:
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(arr, f, ensure_ascii=False, indent=1)
        print(os.path.basename(p), "actualizado")
print("entradas cambiadas:", total)
