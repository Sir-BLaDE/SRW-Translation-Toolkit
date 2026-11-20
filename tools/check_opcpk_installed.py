# -*- coding: utf-8 -*-
"""Verificar traducciones en OP.CPK instalado"""
import os

opcpk_path = r'D:\Juegos\-SPARROW\-Super Robot Wars V\Data\BTLC\EN0\OP.CPK'
data = open(opcpk_path, 'rb').read()

print(f"\nOP.CPK instalado:")
print(f"  Tamaño: {len(data):,} bytes")
print(f"  Magic: {repr(data[:4])}")

# Verificar strings tradujdos con acentos españoles
test_strings = [
    b'Akit',        # Akitó (sin tilde)
    b'\xc3\x81muro', # Ámuro con tilde en UTF-8
    b'B\xc3\xa1njo', # Bánjo con tilde/ñ
]

print("\nVerificando strings traducidos:")
for ts in test_strings:
    pos = data.find(ts)
    if pos >= 0:
        text = data[pos:pos+5].decode('utf-8', errors='replace')
        print(f"  ✅ '{text}' encontrado en offset {hex(pos)}")
    else:
        print(f"  ❌ No encontrado")

# Listar todos los strings ASCII legibles (sin null terminators estrictos)
print("\n\nStrings ASCII encontrados en OP.CPK:")
ascii_found = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        j = i + 1
        while j < min(len(data), start + 50) and (data[j] == 0 or (32 <= data[j] <= 126)):
            j += 1
        
        text = data[start:j].decode('ascii', errors='ignore').rstrip('\x00\x10')
        if len(text) >= 8:
            ascii_found.append((start, text))
    
    i += 1

for start, text in sorted(ascii_found, key=lambda x: -len(x[1]))[:25]:
    print(f"  Offset {hex(start):8}: '{text}'")

print(f"\nTotal bloques ASCII: {len(ascii_found)}")
