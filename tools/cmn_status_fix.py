# -*- coding: utf-8 -*-
"""Rellena las traducciones de nombres de estado/ tecnologia en el CSV de CMN00."""
import csv
import io

CSV = r"C:/Dev/Default Project/srwv/datos/lineas_batalla_final_es6.csv"

NEW = {
    "VPS Armor": "Blindaje VPS",
    "Beam Coat": "Capa de Haz",
    "Barrier Field": "Campo de Barrera",
    "Lambda Driver": "Lambda Driver",
    "Psycho Field": "Campo Psíquico",
    "Positron Reflector": "Reflector de Positrones",
    "Wave Motion Barrier": "Barrera de Onda de Movimiento",
    "Barrier": "Barrera",
    "Distortion Field": "Campo de Distorsión",
    "Defend": "Defender",
    "Shield Defend": "Defensa con Escudo",
    "Shadow": "Sombra",
    "Shin Getter Vision": "Visión Shin Getter",
    "Quantization": "Cuantización",
    "Ariel Mode": "Modo Ariel",
    "Status Drain": "Drenaje de Estado",
    "Unable to Act": "Incapaz de Actuar",
    "Focus Drain": "Drenaje de Enfoque",
    "SP Drain": "Drenaje de PE",
    "EN Drain": "Drenaje de EN",
    "Mobility Down": "Bajada de Movilidad",
    "Accuracy Down": "Puntería baja",
    "Armor Down": "Bajada de Armadura",
    "Focus Up": "Subida de Enfoque",
    "SP Recovery": "Recuperación de PE",
    "Status Up": "Subida de Estado",
    "HP Recovery": "Recuperación de PV",
    "Spirit Effect": "Efecto Espiritual",
    "Move Up": "Subida de Movimiento",
    "Max Focus Up": "Subida de Enfoque Máx.",
}

with io.open(CSV, encoding="utf-8", newline="") as fh:
    reader = csv.DictReader(fh)
    rows = list(reader)
    fields = reader.fieldnames

changed = 0
for r in rows:
    en = r["en"]
    if en in NEW and not r["es"].strip():
        r["es"] = NEW[en]
        changed += 1

with io.open(CSV, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print("actualizadas", changed, "de", len(NEW))
