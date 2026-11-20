# -*- coding: utf-8 -*-
"""Buscar y listar todos los strings ASCII en OP.CPK"""

data = open('D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK', 'rb').read()

print(f"Tamaño: {len(data):,} bytes\n")

import re

ascii_ranges = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        while i < len(data) and 32 <= data[i] <= 126:
            i += 1
        text = data[start:i].decode('ascii', errors='ignore')[:80]
        
        if len(text) >= 5 and any(c.isalpha() for c in text):
            ascii_ranges.append((start, text))
    i += 1

print(f"Total bloques ASCII: {len(ascii_ranges)}\n")
print("Top 100 bloques ASCII más largos:")
for start, text in sorted(ascii_ranges, key=lambda x: -len(x[1]))[:100]:
    print(f"Offset {hex(start):8}: '{text}'")
