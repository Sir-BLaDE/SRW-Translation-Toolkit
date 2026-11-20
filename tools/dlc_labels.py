# -*- coding: utf-8 -*-
"""Genera datos/dlc_work/labels_es.json con etiquetas de lugar y rótulos.

Conserva exactamente el prefijo (saltos y espacios ideográficos) de cada
bloque original y sustituye solo el texto visible.
"""
import io
import json
import os
import re

WORK = r"C:/Dev/Default Project/srwv/datos/dlc_work"

CAPTIONS = {
    "Yamato Bridge": "Puente de mando del Yamato",
    "Yamato Hangar": "Hangar del Yamato",
    "Factory": "Fábrica",
    "Yamato Mess Hall": "Comedor del Yamato",
    "Yamato Aircraft Squad Briefing Room":
        "Sala de briefing del escuadrón aéreo del Yamato",
    "Yamato Observation Deck": "Mirador del Yamato",
    "Yamato Commanding Officer's Cabin":
        "Camarote del comandante del Yamato",
    "Ptolemaios 2 Custom Hangar": "Hangar del Ptolemy 2 personalizado",
    "Earth Federation Forces General Headquarters":
        "Cuartel General de las Fuerzas de la Federación Terrestre",
    "Nadesico B Bridge": "Puente de mando del Nadesico B",
    "Jasmine Mall": "Centro comercial Jasmine",
    "Arzenal Hangar": "Hangar de Arzenal",
    "Tuatha de Danaan Hangar": "Hangar del Tuatha de Danaan",
    "Tuatha de Danaan Mess Hall": "Comedor del Tuatha de Danaan",
    "Nahel Argama Captain's Cabin": "Camarote del capitán del Nahel Argama",
    "Nouvelle Tokyo City": "Ciudad de Nouvelle Tokyo",
    "Earth Federation Forces Battleship Hangar":
        "Hangar del acorazado de las Fuerzas de la Federación Terrestre",
    "Earth Federation Force Battleship Hangar":
        "Hangar del acorazado de las Fuerzas de la Federación Terrestre",
    "Axis Living Quarters": "Alojamiento de Axis",
    "Garencieres Bridge": "Puente de mando del Garencieres",
    "Garencieres Hangar": "Hangar del Garencieres",
    "Near Nouvelle Tokyo City": "Cerca de la ciudad de Nouvelle Tokyo",
    "Yamato Central Strategy Room": "Sala central de estrategia del Yamato",
    "VangRay Cockpit": "Cabina del VangRay",
    "Shinguji Residence Living Room": "Salón de la residencia Shinguji",
    "$r Cockpit": "Cabina del $r",
}

LABELS = {
    "ヤマト\u3000ブリッジ": "Yamato\u3000puente de mando",
    "ヤマト\u3000格納庫": "Yamato\u3000hangar",
    "ヤマト格納庫": "Hangar del Yamato",
    "ヤマト\u3000食堂": "Yamato\u3000comedor",
    "航空隊\u3000ブリーフィングルーム":
        "Escuadrón aéreo\u3000sala de briefing",
    "ヤマト\u3000展望室": "Yamato\u3000mirador",
    "ヤマト艦長室": "Camarote del capitán del Yamato",
    "$r\u3000コックピット": "$r\u3000cabina",
    "ヴァングレイ\u3000コックピット": "Vangray\u3000cabina",
    "プトレマイオス２改\u3000格納庫": "Ptolemy 2 Kai\u3000hangar",
    "軍\u3000オフィス": "Oficina militar",
    "ナデシコＢ\u3000ブリッジ": "Nadesico B\u3000puente de mando",
    "ジャスミンモール": "Centro comercial Jasmine",
    "アルゼナル格納庫": "Hangar de Arzenal",
    "トゥアハー・デ・ダナン\u3000格納庫": "Tuatha de Danaan\u3000hangar",
    "トゥアハー・デ・ダナン\u3000食堂": "Tuatha de Danaan\u3000comedor",
    "艦長室": "Camarote del capitán",
    "公園": "Parque",
    "街中": "Calle",
    "夜空": "Cielo nocturno",
    "ラー・カイラム格納庫": "Hangar del Ra Cailum",
    "汎用レストルーム": "Sala de descanso",
    "ガランシェールブリッジ": "Puente de mando del Garencieres",
    "ガランシェール\u3000格納庫": "Garencieres\u3000hangar",
    "ヤマト\u3000中央作戦室": "Yamato\u3000sala central de operaciones",
    "ヤマト食堂": "Comedor del Yamato",
    "和室": "Sala japonesa",
}


def main():
    blocks = json.load(io.open(os.path.join(WORK, "blocks_en.json"),
                               encoding="utf-8"))
    out = {}
    caps = re.compile(r"^(.*-)([^-]+)(-)$", re.S)
    for b in blocks:
        if b in LABELS:
            out[b] = LABELS[b]
            continue
        m = caps.match(b)
        if m and "\r\n" in b:
            name = m.group(2)
            if name in CAPTIONS:
                out[b] = m.group(1) + CAPTIONS[name] + m.group(3)
            else:
                print("sin traduccion de rotulo:", repr(name))
    print("etiquetas:", len(out))
    json.dump(out, io.open(os.path.join(WORK, "labels_es.json"), "w",
                           encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    for k, v in sorted(out.items()):
        print("  %r -> %r" % (k[-42:], v[-48:]))


if __name__ == "__main__":
    main()
