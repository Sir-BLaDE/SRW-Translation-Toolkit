#!/usr/bin/env python3
"""Find story-related files and data in game directory"""

import os

game_path = 'D:/Juegos/-SPARROW-/Super Robot Wars V/'
found = []

for root, dirs, files in os.walk(game_path):
    if '__pycache__' in root or '.git' in root:
        continue
    for fn in files:
        fp = os.path.join(root, fn)
        if fn.lower().endswith(('.cpk', '.bin', '.dat', '.txt', '.csv')):
            found.append(fp)

print('Game files with cpk/bin/dat/txt/csv extensions:')
for fp in found:
    print('  ', fp)
