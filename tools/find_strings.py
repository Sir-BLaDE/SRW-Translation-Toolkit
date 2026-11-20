#!/usr/bin/env python
import os, struct, re

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'

with open(INPUT_CPK, 'rb') as f:
    data = f.read()

print('Archivo total:', len(data), 'bytes')

# El CPK tiene strings rodeados por 0x04 (terminador) o 0x00
# Buscar patrones de string terminados por \x04 o nulo
string_pattern = rb'[\x00\x04][\x20-\x7e]{3,80}[\x00\x04]'

matches = list(re.finditer(string_pattern, data))

print('Encontradas', len(matches), 'coincidencias de string')

# Mostrar primeras 100 cadenas que sean texto legible
legible_count = 0
for i, match in enumerate(matches[:150]):
    text_bytes = match.group()
    try:
        text = text_bytes.decode('ascii')
        # Filtrar para strings de longitud razonable (no solo terminadores)
        if len(text.strip()) > 3 and len(text.strip()) < 100:
            legible_count += 1
            preview = text[:60]
            print(str(legible_count).rjust(3) + '. ' + str(match.start()+1).rjust(5) + ': [' + str(len(text)) + '] ' + preview.replace('\n', 'NL').replace('\r', 'CR') + ')')
    except:
        pass

print('Legible count:', legible_count)
