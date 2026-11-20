#!/usr/bin/env python3
"""Create final comprehensive Spanish translation for LT00 English-only strings"""

import csv
import sys

# Comprehensive translations: English -> Spanish
translations = {}

# From datos/traducir_lt00.csv (existing 140 entries)
with open('C:/Dev/Default Project/srwv/datos/traducir_lt00.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        en = row.get('en', '').strip()
        es = row.get('es', '').strip()
        if en and es:
            translations[en] = es

# From translate_lt00.py - manual translations
manual = {
    'Gains 50 Focus when sortied.': 'Gana 50 Enfoque al ser sorteado.',
    'pilots by 10%.': 'los pilotos por un 10%.',
    'Triggers spirit command Instinct': 'Activa el comando espiritual Instinto.',
    'Focus is above 140.': 'El Enfoque es superior a 140.',
    'Ignore an enemy unit\'s barrier when attacking.': 'Ignora la barrera de la unidad enemiga al atacar.',
    'Nearby allies gain 3 Focus at the': 'Los aliados cercanos ganan 3 Enfoque al.',
    'Strong Luck ': 'Buena Suerte ',
    'Double Action': 'Acción Doble',
    'Restores 5 SP at the start of player': 'Restaura 5 SP al inicio del jugador.',
    'Triggers spirit command Disturb': 'Activa el comando espiritual Molestar.',
    'Save E L1': 'Guarda E L1',
    'for women and increases Final Evasion': 'para mujeres y aumenta la Evitación Final.',
    'command to change forms. This change cannot be reversed.': 'comando para cambiar de forma. Este cambio no puede revertirse.',
    'Air-S.': 'Air-S.',
    'Gains 1 extra Focus when attacking, return attacking,': 'Gana 1 Enfoque extra al atacar, ataque de retorno.',
    '1. Increases SKL by 20.': '1. Incrementa HAB por 20.',
    'Atacante ': 'Atacante ',
    'Duplica el aumento de la Tasa de Sincro.': 'Duplica el aumento de la Tasa de Sincro.',
    'Ataque': 'Ataque',
    'n L1': 'n L1',
    'n son esenciales para': 'n son esenciales para',
    'nivel aumenta un 30%.': 'nivel aumenta un 30%.',
    'RNG, SKL, DEF, EVD y HIT de los enemigos': 'RNG, HAB, DEF, EVA y AC de los enemigos',
    'Desbloquea la parte de poder Efector Espiral, disponible en ': 'Desbloquea el Efector Espiral de poder, disponible en',
    'Comandante L1': 'Comandante L1',
    'Este icono se ilumina cuando un mecha tiene Dividir.': 'Este ícono se ilumina cuando un mecha tiene Dividir.',
    'El Enfoque es 170 en condiciones': 'El Enfoque es 170 en condiciones',
    'Inicio de turno': 'Inicio de turno',
    'Presidente': 'Presidenta',
    'en 1 salvo armas de mapa y armas con alcance 1.': 'en 1 disparo de mapa y armas con alcance 1.',
    'con Enfoque superior a 110.': 'con Enfoque superior a 110.',
    'Toda unidad con ExC de 3 aumenta su Movimiento en 1.': 'Toda unidad con ExC de 3 incrementa su Movilidad en 1.',
    'Adapt. unidad y armas al terreno (Esp) S': 'Adapt. unidad y armas al terreno (Esp) S',
    'dispersa nanom': 'dispersa nanom',
}

# Add manual new translations
new_manual = {
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

all_translations = dict(translations)
all_translations.update(manual)

with open('C:/Dev/Default Project/srwv/datos/lt00_translations_comprehensive.txt', 'w', encoding='utf-8') as f:
    for en, es in all_translations.items():
        f.write(f'{en}\t{es}\n')

print(f'Created final translation with {len(all_translations)} entries')
print('Saved to datos/lt00_translations_comprehensive.txt')
