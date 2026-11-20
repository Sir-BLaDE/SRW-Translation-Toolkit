#!/usr/bin/env python3
# Generate comprehensive translation for LT00 English-only strings

# Extract and categorize all English-only strings
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

# Group strings by category keywords for better translation
categories = {
    'combat': ['DMG', 'HP', 'EN', 'EXP', 'SKL', 'Tac', 'SPC', 'AC'],
    'focus': ['Focus', 'Focus', 'Extra', 'Enfoque'],
    'spirit': ['Spirit', 'Espiritual', 'Esp.', 'Esp'],
    'skill': ['Skill', 'Habilidad', 'Special'],
    'pilot': ['Pilot', 'Piloto', 'Ace', 'Elite', 'Rookie', 'Comandante', 'Commander'],
    'mech': ['Mech', 'Robot', 'Mecha', 'Mecha'],
    'ammo': ['Ammo', 'Munición'],
    'movement': ['Movement', 'Movimiento', 'Move'],
    'attack': ['Attack', 'Ataque', 'Strike', 'Golpe', 'Hit'],
    'evade': ['Evasion', 'Evadir', 'EVD'],
    'accuracy': ['Accuracy', 'Precisión', 'AC'],
    'critical': ['Critical', 'Crítico', 'Cr', 'Crit'],
    'support': ['Support', 'Apoyo', 'Sup'],
    'count': ['Count', 'Count'],
}

# Print category summary
from collections import defaultdict
cat_counts = defaultdict(int)
for s in only_english:
    s_lower = s.lower()
    for cat, keywords in categories.items():
        if any(k.lower() in s_lower for k in keywords):
            cat_counts[cat] += 1
            break

print("Category distribution for English-only strings:")
for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")
