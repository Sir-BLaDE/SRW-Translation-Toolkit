# -*- coding: utf-8 -*-
"""Traducir strings ASCII en OP.CPK usando null terminators"""
import os

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real.cpk"

print("=" * 80)
print("TRADUCCION OP.CPK - ESPANOL ESPAÑA (null-terminated strings)")
print("=" * 80)

# Leer archivo
with open(P_ORIGINAL, 'rb') as f:
    data = bytearray(f.read())

print(f"Tamaño OP.CPK: {len(data):,} bytes\n")

# Diccionario de traducciones con null terminators considerados
translations = {
    "Ota": "Otó",
    "Mori": "Morí",
    "Misaki": "Misaki",
    "Gamillas Captain": "Capitán Gamillas",
    "High Spec AI": "IA de Alta Especificación",
    "Martian Successor Nadesico": "Sucesora de Marte Nadashiro",
    "Jupiter Empire Soldier": "Soldado del Imperio Júpiter",
    "Neo Zeon Soldier": "Soldado del Nuevo Zeon",
    "Lunar Vessel": "Nave Lunar",
    "Moonbase": "Base Lunar",
}

# Mostrar todos los strings ASCII legibles en el archivo
print("Buscando strings ASCII con null terminators...\n")

strings_found = []
i = 0
while i < len(data):
    if data[i] == 0x00:  # Null terminator - string anterior
        start = i + 1
        
        # Leer hasta el siguiente null o fin de string ASCII
        j = start
        while j < len(data) and (data[j] == 0x00 or (32 <= data[j] <= 126)):
            if data[j] != 0x00:
                pass  # Continuar
            
            j += 1
        
        if j > start + 1:  # String tiene contenido
            text = bytes(data[start:j]).decode('ascii', errors='replace').rstrip('\x00')
            
            # Solo strings de al menos 4 caracteres con letras
            if len(text) >= 4 and any(c.isalpha() for c in text):
                # Verificar que no es un artefacto simple (PPP, JJJ, etc.)
                cleaned = text.replace(' ', '').upper()
                if not re.match(r'^[A-Z]{2,15}$', cleaned):
                    strings_found.append({
                        'start': start,
                        'end': j,
                        'text': text[:80],  # Cortar a 80 chars
                        'length': min(j - start, 80)
                    })

import re

print(f"Strings encontrados: {len(strings_found)}\n")

# Traducir strings con null terminators
modified_count = 0

for s in sorted(strings_found, key=lambda x: -x['length']):
    text = s['text'][:70]  # Max 70 chars
    
    for original_key, value in translations.items():
        if original_key.lower() in text.lower():
            print(f"[MATCH] '{text}' -> '{value}'")
            
            try:
                # Construir bytes del string completo (con null terminators)
                full_text = original_key + '\x00'
                
                # Buscar en el buffer
                full_bytes = bytearray(full_text.encode('ascii'))
                found_pos = data.find(bytes(full_bytes))
                
                if found_pos >= 0:
                    print(f"    Offset {hex(found_pos)}")
                    
                    # Verificar coincidencia exacta
                    existing_text_check = bytes(data[found_pos:found_pos+len(original_key)]).decode('ascii', errors='replace')
                    
                    if original_key.lower() == existing_text_check.lower():
                        # Reemplazar
                        new_bytes = value.encode('ascii')[:len(original_key)]
                        data[found_pos:found_pos+len(original_key)] = new_bytes
                        modified_count += 1
                        print(f"    ✅ Tradujdo")
            except Exception as e:
                pass

print(f"\nTotal traducciones aplicadas: {modified_count}\n")

# Guardar archivo tradujdo
with open(OUTPUT_PATH, 'wb') as f:
    f.write(data)

print(f"✅ Archivo guardado: {OUTPUT_PATH}")
print(f"   Tamaño: {len(data):,} bytes\n")

# Guardar resumen
summary = r"C:/Dev/Default Project/srwv/outputs/traduction_applied.txt"
with open(summary, 'w', encoding='utf-8') as f:
    f.write("Resumen de traducciones aplicadas a OP_CK_es_real.cpk\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Archivo original: {P_ORIGINAL}\n")
    f.write(f"Tamaño original: {len(data):,} bytes\n")
    f.write(f"Traducciones aplicadas: {modified_count}\n\n")
    
    for key, value in translations.items():
        f.write(f"{key:30} -> {value}\n")

print(f"Resumen guardado en: {summary}")
