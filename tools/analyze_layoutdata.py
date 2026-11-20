#!/usr/bin/env python
"""Analizar estructura real de LayoutData.cpk para texto UI."""

import os, struct, re, json

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'

with open(INPUT_CPK, 'rb') as f:
    data = f.read()

print("Archivo total:", len(data), "bytes")
print("Header (16 bytes):", repr(data[:16]))
print("Hex:", data[:16].hex())

# Buscar patrones de strings terminados por 0x04 o nulo, con contenido ASCII imprimible
string_pattern = rb'[\x00\x04][\x20-\x7e]{4,100}[\x00\x04]'

matches = list(re.finditer(string_pattern, data))
print("Encontradas", len(matches), "coincidencias de string terminados por 0x04/0x00")

# Mostrar primeras 50 coincidencias que tengan contenido legible como texto UI
legible_count = 0
for i, match in enumerate(matches[:60]):
    text_bytes = match.group()
    try:
        # Saltar el primer byte (terminador) para obtener texto real
        text_content = text_bytes[1:-1] if len(text_bytes) > 2 else b''
        text = text_content.decode('ascii')
        
        # Filtrar strings que parecen ser texto UI (no metadatos técnicos)
        preview = text[:70]
        
        # Buscar términos comunes de UI en ingles
        ui_keywords = ['Select', 'Pilot', 'Mech', 'Info', 'Track', 'Data', 'Type', 'Assign', 
                       'Detach', 'Display', 'Save', 'Power', 'File', 'System', 'Delete',
                       'Bonus', 'Crystal', 'Spirit', 'Hit', 'Attack', 'Skill', 'Level',
                       'Ace', 'Effect', 'Commander', 'Fleet', 'Versus', 'End Phase', 'Organization']
        
        if any(kw in text for kw in ui_keywords) and len(text.strip()) > 3:
            legible_count += 1
            print(str(legible_count).rjust(3) + '. ' + str(match.start()+1).rjust(6) + ': [' + str(len(text)) + '] ' + preview.replace('\n', 'NL'))
    except:
        pass

print("Legible count:", legible_count)

# Ahora, busquemos especificamente en el rango de texto del juego (aproximadamente despues de offset 0x30000 o similar)
# Basado en que los primeros ~1MB parece ser header y metadatos
print("\n--- Buscando strings con keywords especificas ---")

# Buscar por keyword especifica para UI critico
keywords = ['Select Pilot', 'Mech to Change', 'Pilot Info', 'Weapon Info', 
             'Unit Info', 'Data Type', 'Ace Pilot', 'Skill PG', 'The Special-PG']

for kw in keywords:
    kw_bytes = kw.encode('ascii') + b'\x04'
    pos = data.find(kw_bytes)
    if pos != -1:
        end_pos = min(pos + len(kw) + 50, len(data))
        context = data[pos:end_pos].decode('ascii', errors='replace')
        print("ENCONTRADO '" + kw + "' a offset " + str(pos) + ":")
        print("  Contexto: '" + context[:100] + "')")
    else:
        print("NO ENCONTRADO '" + kw + "'")
