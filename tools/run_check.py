# -*- coding: utf-8 -*-
import os

opcpk_path = r'D:\Juegos\-SPARROW\-Super Robot Wars V\Data\BTLC\EN0\OP.CPK'
data = open(opcpk_path, 'rb').read()

print(f"\n=== OP.CPK INSTALADO ACTUAL ===")
print(f"Tamaño: {len(data):,} bytes")
print(f"Magic bytes: {repr(data[:4])}")

# Verificar strings clave tradujdos con acentos españoles
check_patterns = [
    (b'Akit', 'Aki'),
    (b'\xc3\x81muro', 'Ámuro con tilde UTF-8'),
    (b'B\xc3\xa1njo', 'Bánjo con tilde UTF-8'),
    (b'Gamillas Captain', 'Capitán Gamillas sin tilde en Inglés'),
]

print("\n=== Verificando traducciones con acentos ===")
for pattern, desc in check_patterns:
    pos = data.find(pattern)
    if pos >= 0:
        text = data[pos:pos+15].decode('utf-8', errors='replace')
        print(f"  ✅ {desc}: '{text}' en offset {hex(pos)}")
    else:
        pattern_str = pattern.decode('latin-1', errors='replace')[:20]
        print(f"  ❌ {desc}: NO encontrado")

print("\n=== Bloques ASCII encontrados ===")
ascii_strings = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        j = i + 1
        while j < min(len(data), start + 60) and (data[j] == 0 or (32 <= data[j] <= 126)):
            j += 1
        
        text = data[start:j].decode('ascii', errors='ignore').rstrip('\x00\x10')
        if len(text) >= 8:
            ascii_strings.append((start, text))
    i += 1

# Ordenar por longitud descendente y mostrar top strings
for start, text in sorted(ascii_strings, key=lambda x: -len(x[1]))[:30]:
    print(f"  Offset {hex(start):8}: '{text}'")

print(f"\nTotal bloques ASCII con texto legible: {len(ascii_strings)}")
