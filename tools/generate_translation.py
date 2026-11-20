#!/usr/bin/env python3
"""Generate full Spanish translation set for LT00 English-only strings"""

import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data

def extract_all_printable_strings(path, min_len=3):
    c = Cpk(path)
    raw = c.read_file(0)
    dec = maybe_decompress(raw)
    x = decrypt_data(dec)
    strings = []
    i = 0
    while i < len(x):
        if not (32 <= x[i] < 127):
            i += 1
            continue
        start = i
        while i < len(x) and 32 <= x[i] < 127:
            i += 1
        s = x[start:i]
        if len(s) >= min_len:
            try:
                strings.append(s.decode('ascii'))
            except:
                pass
    return strings

spanish = extract_all_printable_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')
english = extract_all_printable_strings('D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk')

spanish_set = set(spanish)
english_set = set(english)
only_english = english_set - spanish_set

# Build translation dictionary with all known Spanish translations
translations = {
    # Combat - core system
    ' map is cleared even when ExC goes down.': ' el mapa se limpia aunque el ExC baje.',
    '% by 30% when attacked by men.': '% un 30% cuando se ataca por hombres.',
    '%, Defend to lower DMG taken by 10%. If it\'s a map': ', Defender para reducir el DMG tomado en un 10%. Si es un mapa',
    '%d EXP earned respectively.': 'Obtenido %d EXP respectivamente.',
    '%d Turns': '%d Turnos',
    '%d enemies killed respectively.': '%d enemigos derrotados respectivamente.',
    '%d pilot selections remaining.': '%d selecciones de pilotos restantes.',
    '%d total Tac Pts acquired.': 'Obtenido %d Pts Tác en total.',
    '%d total money acquired.': 'Obtenido %d dinero en total.',
    '(50% of the original DMG dealt.)': '(El 50% del DMG original causado).',
    '(DMG taken is equivalent to when applying Defend.)': '(El DMG tomado equivale al al aplicar Defender).',
    '(For level 2, opponent S size is considered L size.)': '(Para nivel 2, el tamaño S del oponente se considera L).',
    '(Only once.)': '(Solo una vez).',
    '-Factory: Power Part Unlock Conditions-': '-Fábrica: Condiciones de Desbloqueo de Parte de Poder-',
    '1. Increases SKL by 20.': '1. Incrementa HAB por 20.',
    '100, also ignores Haze.': '100, también ignora la Niebla.',
    '2 Phase': '2 Fase',
    '20% for allies within the reach of': 'Un 20% para aliados dentro del alcance de',
    '20% when sortied.': 'Un 20% cuando son sorteados.',
    '3 pilots reach level 4 of the': '3 pilotos alcanzan el nivel 4 del',
    '3 pilots reach level 4 of the special skill Commander.': '3 pilotos alcanzan el nivel 4 de la habilidad especial Comandante.',
    '40 SP.': '40 SP.',
    '400. Increases Max EN by 50.': '400. Incrementa el PN máximo en 50.',
    '5 times the number of downed enemies in TAC points.': '5 veces el número de enemigos derribados en Pts Tác.',
    '50% HP.': 'El 50% de la PV.',
    ':Back': ':Atrás',
}

# Save full translation
with open('C:/Dev/Default Project/srwv/datos/lt00_translations_comprehensive.txt', 'w') as f:
    for en, es in translations.items():
        f.write(f'{en}\t{es}\n')

print(f'Saved {len(translations)} comprehensive translations')
print(f'Total English-only: {len(only_english)}')
print(f'Matched in translations: {len([k for k in translations if k in only_english])}')
print(f'Not in translations: {len([k for k in only_english if k not in translations])}')
