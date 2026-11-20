#!/usr/bin/env python3
"""Analyze BLTU strings and create Spanish translations"""

with open('C:/Dev/Default Project/srwv/datos/bltu_strings.txt', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
    bltu = []
    for l in lines:
        if l.strip():
            parts = l.split('\t')
            gid = int(parts[0])
            s = parts[1]
            bltu.append((gid, s))

print(f'Loaded {len(bltu)} BLTU strings')

# Group by string content
from collections import defaultdict
unique_strings = defaultdict(list)
for gid, s in bltu:
    unique_strings[s].append(gid)

print(f'Unique strings: {len(unique_strings)}')

# Print first 100 unique strings
count = 0
for s, gids in sorted(unique_strings.items()):
    if count < 100:
        print(f'{s!r} -> gids: {gids[:5]}')
        count += 1
