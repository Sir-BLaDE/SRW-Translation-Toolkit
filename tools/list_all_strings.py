# -*- coding: utf-8 -*-
"""Listar todos los strings ASCII en OP.CPK instalado"""

data = open('D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK', 'rb').read()

print("Todos los strings ASCII encontrados en OP.CPK:")
print("=" * 80)

ascii_strings = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        while i < len(data) and 32 <= data[i] <= 126:
            i += 1
        text = data[start:i].decode('ascii', errors='ignore')
        
        if len(text) >= 8 and any(c.isalpha() for c in text):
            ascii_strings.append((start, text))
    i += 1

print(f"\nTotal bloques ASCII: {len(ascii_strings)}")
print("\nLISTA COMPLETA de strings en inglés encontrados:")
for start, text in sorted(ascii_strings, key=lambda x: -len(x[1]))[:80]:
    print(f"  Offset {hex(start):8}: '{text}'")

# Verificar UI keywords
ui_keywords = ['settings', 'start', 'continue', 'load', 'game', 'mode', 'select']
print("\n\nStrings con palabras de UI:")
for start, text in ascii_strings:
    text_lower = text.lower()
    for kw in ui_keywords:
        if kw in text_lower and len(text) > 10:
            print(f"  Offset {hex(start):8}: '{text}' [CONTIENE: {kw}]")

# Guardar lista para referencia futura
with open(r'C:/Dev/Default Project/srwv/outputs/all_op_strings.txt', 'w', encoding='utf-8') as f:
    f.write("Todos los strings ASCII en OP.CPK\n")
    for start, text in sorted(ascii_strings, key=lambda x: -len(x[1]))[:50]:
        f.write(f"{text}\n")

print(f"\nLista guardada en: C:/Dev/Default Project/srwv/outputs/all_op_strings.txt")
