# -*- coding: utf-8 -*-
"""Añade a systext_trans.json las claves del banco que aún no tenían traducción."""
import json
from pathlib import Path

TRANS = Path(r"C:/Dev/Default Project/srwv/datos/systext_trans.json")

ADD = {
    "BGM名称": "Nombre de BGM",
    "スキルプログラム名称": "Nombre de programa de habilidad",
    "パイロットフルネーム": "Nombre completo del piloto",
    "パイロット表示名称": "Nombre mostrado del piloto",
    "機体詳細名称": "Nombre detallado de la unidad",
    "機体表示名称": "Nombre mostrado de la unidad",
    "作品名称": "Nombre de la obra",
    "特殊能力名称": "Nombre de habilidad especial",
    "武器正式名称": "Nombre oficial del arma",
    "武器表示名称": "Nombre mostrado del arma",
    "All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Production Model (Wille Custom) Unit-08α":
        "Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Modelo de Producción (Personalizado por Wille), Unidad-08α",
}

data = json.loads(TRANS.read_text(encoding="utf-8"))
added = 0
for k, v in ADD.items():
    if k not in data:
        data[k] = v
        added += 1
TRANS.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"añadidas {added} claves; total {len(data)}")
