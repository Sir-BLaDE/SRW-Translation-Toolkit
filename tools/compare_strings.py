# -*- coding: utf-8 -*-
"""Comparar OP.CPK con strings de UI en inglés"""

original_game = r"D:\Juegos\-SPARROW\-Super Robot Wars V\Data\BTLC\EN0\OP.CPK"

print("Analizando OP.CPK instalado en el juego...\n")

data = open(original_game, 'rb').read()
print(f"Tamaño: {len(data):,} bytes\n")

# Extraer strings ASCII
ascii_strings = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        j = i + 1
        while j < min(len(data), start + 50) and (data[j] == 0x00 or 32 <= data[j] <= 126):
            j += 1
        
        text = bytes(data[start:j]).decode('ascii', errors='ignore').rstrip('\x00\x10')
        
        if len(text) >= 8 and any(c.isalpha() for c in text):
            ascii_strings.append((start, text))
    i += 1

print(f"Total bloques ASCII: {len(ascii_strings)}")
print("\nTodos los bloques encontrados:")
for start, text in sorted(ascii_strings, key=lambda x: -len(x[1]))[:30]:
    print(f"  Offset {hex(start):8}: '{text}'")

# Guardar para referencia
with open(r'C:/Dev/Default Project/srwv/outputs/opck_current_strings.txt', 'w', encoding='utf-8') as f:
    f.write("Strings ASCII en OP.CPK actual\n")
    for start, text in ascii_strings:
        f.write(f"{text}\n")

print(f"\nLista guardada en: C:/Dev/Default Project/srwv/outputs/opck_current_strings.txt")
