#!/usr/bin/env python3
"""Final comprehensive Spanish translation for all game text - Status report"""

# Consolidated translation dictionary
FINAL_TRANSLATIONS = {}

import csv
with open('C:/Dev/Default Project/srwv/datos/traducir_lt00.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        en = row.get('en', '').strip()
        es = row.get('es', '').strip()
        if en and es:
            FINAL_TRANSLATIONS[en] = es

with open('C:/Dev/Default Project/srwv/datos/lt00_translations_comprehensive.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if '\t' in line:
            en, es = line.split('\t')
            en = en.strip()
            es = es.strip()
            if en and es and en not in FINAL_TRANSLATIONS:
                FINAL_TRANSLATIONS[en] = es

print(f'Final consolidated translation count: {len(FINAL_TRANSLATIONS)}')

# Save final translation
with open('C:/Dev/Default Project/srwv/datos/final_lt00_translations.txt', 'w', encoding='utf-8') as f:
    for en, es in FINAL_TRANSLATIONS.items():
        f.write(f'{en}\t{es}\n')

print('Saved to: C:/Dev/Default Project/srwv/datos/final_lt00_translations.txt')

# Count English-only strings that have translations
with open('C:/Dev/Default Project/srwv/datos/english_only_lt00_full.txt', 'r', encoding='utf-8') as f:
    en_lines = [l.strip() for l in f if l.strip()]
    matched = 0
    unmatched = []
    for en in en_lines:
        if en in FINAL_TRANSLATIONS:
            matched += 1
        else:
            unmatched.append(en)

print(f'English-only: {len(en_lines)}')
print(f'With translations: {matched}')
print(f'Without translations: {len(unmatched)}')
print()
print('Sample of unmatched English-only strings:')
for en in unmatched[:30]:
    print(f'  {repr(en[:70])}')
