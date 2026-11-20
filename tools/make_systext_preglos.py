# -*- coding: utf-8 -*-
"""Genera un systext_trans de prueba con los valores anteriores al glosario."""
import json
from pathlib import Path

D = Path(r"C:/Dev/Default Project/srwv/datos")
CUR = D / "systext_trans.json"
OUT = D / "systext_trans_preglos.json"

OLD = {
    "Artificial Newtype": "Nuevo Tipo Artificial",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-01":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-01",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-00":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-00",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-00 (Mod)":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-00 (Modificado)",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-01 Pseudo-Evolution Initial Arousal Phase":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-01, Fase de Despertar Inicial de Pseudoevolución",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Production Model Unit-02 (First Production Model)":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Modelo de Producción Unidad-02 (Primer Modelo de Producción)",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Production Model (Wille Custom) Unit-08α":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Modelo de Producción (Personalizado por Wille), Unidad-08α",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Production Model (Wille Custom) Unit-08":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Modelo de Producción (Personalizado por Wille), Unidad-08",
    "Baron Ashura Mechanical Beast": "Bestia Mecánica Baron Ashura",
}

data = json.loads(CUR.read_text(encoding="utf-8"))
for k, v in OLD.items():
    if k in data:
        data[k] = v
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("escrito", OUT, "claves", len(data))
