#!/usr/bin/env python3
"""Create final comprehensive Spanish translation file for LT00 English-only strings"""

TRANSLATIONS = {
    # Combat / Battle
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
    'All': 'Todos',
    'All Attack': 'Todos los Ataques',
    'Ally': 'Aliado',
    'All allied pilots receive 1 Extra Count when sortied.': 'Todos los pilotos aliados reciben 1 Conteo Extra cuando son sorteados.',
    'All ally pilots gain 2 Focus at the': 'Todos los pilotos aliados ganan 2 Enfoque al',
    'All ally pilots gain 2 Focus at the start of the ally phase each turn.': 'Todos los pilotos aliados ganan 2 Enfoque al inicio de la fase de aliados cada turno.',
    'All ally pilots receive 10 Focus when': 'Todos los pilotos aliados reciben 10 Enfoque cuando',
    'All ally pilots receive 10 Focus when sortied.': 'Todos los pilotos aliados reciben 10 Enfoque cuando son sorteados.',
    'All ally pilots receive 20 SP when': 'Todos los pilotos aliados reciben 20 SP cuando',
    'All ally pilots receive 20 SP when sortied.': 'Todos los pilotos aliados reciben 20 SP cuando son sorteados.',
    'All orders executed.': 'Todas las órdenes ejecutadas.',
    'All pilots deployed.': 'Todos los pilotos desplegados.',
    'All weapons gain 50% more Ammo.': 'Todos las armas ganan un 50% más de Munición.',
}

with open('C:/Dev/Default Project/srwv/datos/lt00_translations_comprehensive.txt', 'w', encoding='utf-8') as f:
    for en, es in TRANSLATIONS.items():
        f.write(f'{en}\t{es}\n')

print(f'Created final comprehensive translation with {len(TRANSLATIONS)} entries')
print(f'File: C:/Dev/Default Project/srwv/datos/lt00_translations_comprehensive.txt')
