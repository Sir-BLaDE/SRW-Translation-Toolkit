#!/usr/bin/env python
"""Buscar contenido de LayoutData.cpk - buscar tanto inglés como español."""

import os, struct, re

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'

with open(INPUT_CPK, 'rb') as f:
    data = f.read()

print("Archivo total:", len(data), "bytes")

# Buscar cualquier texto ASCII imprimible de longitud razonable
string_pattern = rb'[\x00\x04][\x20-\x7e]{3,60}[\x00\x04]'

matches = list(re.finditer(string_pattern, data))
print("Encontradas", len(matches), "coincidencias de string")

# Buscar específicamente por keywords tanto en inglés como español (traducidas)
keywords_to_search = [
    ('Select Pilot to Change Mech', 'Cambiar Robot-Piloto'),
    ('Select Mech to Cambiar pil.', 'Seleccionar Mech/Piloto'),
    ('Pilot Info', 'Info piloto'),
    ('Weapon Info', 'Info arma'),
    ('Unit Info', 'Info unidad'),
    ('Ace Pilot', 'Piloto ace'),
    ('Skill PG', 'PG habilidad'),
]

found_in_english = []
found_in_spanish = []

for i, match in enumerate(matches[:200]):
    text_bytes = match.group()
    try:
        # Saltar el primer y último byte (terminadores)
        text_content = text_bytes[1:-1] if len(text_bytes) > 2 else b''
        text = text_content.decode('ascii')
        
        # Filtrar strings de longitud razonable
        preview = text[:70]
        
        # Verificar keywords
        for en_kw, es_kw in keywords_to_search:
            if en_kw.lower() in text.lower():
                found_in_english.append((en_kw, str(match.start()), preview))
            if es_kw.lower() in text.lower():
                found_in_spanish.append((es_kw, str(match.start()), preview))
    except:
        pass

print("\n=== ENCONTRADO EN INGLÉS ===")
for en_kw, offset, preview in found_in_english[:20]:
    print("  '" + en_kw + "' @ " + offset + ": [" + str(len(preview)) + "] " + preview)

print("\n=== ENCONTRADO EN ESPAÑOL ===")  
for es_kw, offset, preview in found_in_spanish[:20]:
    print("  '" + es_kw + "' @ " + offset + ": [" + str(len(preview)) + "] " + preview.replace('\n', 'NL'))

if not found_in_english and not found_in_spanish:
    print("NO se encontraron términos de texto UI conocidos (puede estar en formato binario o ya traducido)")
else:
    # Guardar para traducción
    output_file = 'C:/Dev/Default Project/srwv/datos/layoutdata_strings_found.json'
    import json
    data_to_save = {
        'found_in_english': found_in_english,
        'found_in_spanish': found_in_spanish
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
print("\nResultados guardados en layoutdata_strings_found.json")
