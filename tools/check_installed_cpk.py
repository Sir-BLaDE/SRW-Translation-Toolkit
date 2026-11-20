# -*- coding: utf-8 -*-
"""Verificar qué traducciones hay en OP.CPK instalado actualmente"""

data = open('D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK', 'rb').read()

print("OP.CPK actual en el juego:")
print(f"  Tamaño: {len(data):,} bytes")

# Verificar strings de personaje tradujdos
test_strings = [b'Ot\x00', b'Mor\x00', b'Akit', b'\xc3\x81muro', b'B\xc3\xa1njo', b'Tobi\x00a']
print("\nVerificando strings tradujdos:")

for ts in test_strings:
    pos = data.find(ts)
    if pos >= 0:
        found_text = data[pos:pos+5].decode('utf-8', errors='replace')
        print(f"  ✅ '{found_text}' encontrado en offset {hex(pos)}")
    else:
        print(f"  ❌ '{ts.decode('latin-1')[:4]}' NO encontrado")

# Listar todos los strings ASCII legibles
print("\n\nStrings ASCII encontrados:")
ascii_strings = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        while i < len(data) and 32 <= data[i] <= 126:
            i += 1
        text = data[start:i].decode('ascii', errors='ignore')[:80]
        if len(text) >= 10 and any(c.isalpha() for c in text):
            ascii_strings.append((start, text))
    i += 1

for start, text in sorted(ascii_strings, key=lambda x: -len(x[1]))[:30]:
    print(f"  Offset {hex(start):8}: '{text}'")

# Verificar strings con acentos (UTF-8)
print("\n\nVerificando traducciones con acentos:")
accent_tests = [
    ('\xc3\x81', 'Ámuro'),  # Ámuro con tilde
    ('\xc3\xa1', 'a con tilde'),
    ('\xc3\xb1', 'ñ'),
]

for pattern, desc in accent_tests:
    pos = data.find(bytes([*pattern]))
    if pos >= 0:
        print(f"  ✅ '{desc}' encontrado")
    else:
        print(f"  ❌ '{desc}' NO encontrado")
