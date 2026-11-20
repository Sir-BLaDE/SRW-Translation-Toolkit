#!/usr/bin/env python
import os, struct, re

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'

with open(INPUT_CPK, 'rb') as f:
    data = f.read()

print('Archivo total:', len(data), 'bytes')

# Buscar texto ASCII imprimible continuo (sin nulos o control)
ascii_pattern = rb'[\x20-\x7e]{1,64}'
matches = list(re.finditer(ascii_pattern, data))

print('Encontradas', len(matches), 'coincidencias de texto ASCII')

# Mostrar primeras 50 cadenas que sean legibles (solo letras, espacios, puntuacion basica)
legible_count = 0
for i, match in enumerate(matches[:100]):
    text_bytes = match.group()
    try:
        text = text_bytes.decode('ascii')
        # Filtrar para solo letras/espacios/puntuacion (sin control chars)
        if all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:!"?-_ \u00a1\u00af' for c in text.replace('_', '')):
            legible_count += 1
            preview = text[:50]
            print(str(legible_count).rjust(3) + '. ' + str(match.start()).rjust(5) + ': ' + preview + '...' + ' (len=' + str(len(text)) + ')')
    except:
        pass

print('Legible count:', legible_count)
