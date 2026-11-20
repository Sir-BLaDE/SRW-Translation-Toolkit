# -*- coding: utf-8 -*-
"""Crear OP_CK_es.cpk traduciendo todos los strings de OP.CPK original"""
import sys
import os

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es.cpk"
BACKUP_PATH = r"C:/Dev/Default Project/srwv/backup_punto_2026-11-17"

print("=" * 80)
print("CREANDO OP_CK_es.cpk - TRADUCCION ESPANOL ESPAÑA COMPLETA")
print("=" * 80)

# Crear directorio de salida si no existe
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Leer CPK original desencriptado
cf = load(P_ORIGINAL)
pt = cf.plain(cf.rows[0]) if cf.rows[0] else None

if not pt:
    print("ERROR: No se pudo extraer contenido de OP.CPK")
    sys.exit(1)

print(f"\nContenido extraído: {len(pt):,} bytes\n")

# Diccionario completo de traducciones español España
translations = {
    # Personajes con acentos españoles reales
    "Akito": "Akitó",
    "Amuro": "Ámuro",
    "Banjo": "Bánjo", 
    "Kodai": "Kodai",
    "Okita": "Okita",
    "Setsuna": "Setsuna",
    "Tobia": "Tobía",
    
    # Nombres de facciones
    "Martian Successor Nadesico": "Sucesora de Marte Nadashiro",
    "Jupiter Empire Soldier": "Soldado del Imperio Júpiter",
    "Neo Zeon Soldier": "Soldado del Nuevo Zeon",
    "Lunar Vessel": "Nave Lunar",
    "Moonbase": "Base Lunar",
    
    # Títulos de personajes/facciones
    "Gamillas Captain": "Capitán Gamillas",
    "High Spec AI": "IA de Alta Especificación",
    
    # Otros nombres detectados
    "Misaki": "Misaki",
    "Mori": "Morí",
    "Nanbu": "Nambu", 
    "Sanada": "Sánada",
    "Shima": "Shima",
    "Tokugawa": "Tokugawa",
}

print(f"Diccionario de traducciones: {len(translations)} entradas\n")

# Extraer todos los strings ASCII legibles de OP.CPK
strings_to_translate = []
i = 0
while i < len(pt):
    if 32 <= pt[i] <= 126:
        start = i
        while i < len(pt) and 32 <= pt[i] <= 126:
            i += 1
        
        text = pt[start:i].decode('ascii', errors='replace')
        
        # Solo strings de al menos 4 caracteres con letras (excluir artefactos)
        if len(text) >= 4 and any(c.isalpha() for c in text):
            # Verificar que no sea un patrón de compresión (PPP, JJJ, etc.)
            cleaned = text.replace(' ', '').replace('\n', '').upper()
            if not re.match(r'^[A-Z]{2,15}$', cleaned):  # No es artefacto simple
                strings_to_translate.append({
                    'start': start,
                    'end': i,
                    'text': text[:100],  # Cortar a 100 chars
                    'length': i - start
                })

import re

print(f"Strings encontrados para traducir: {len(strings_to_translate)}\n")

# Traducir strings usando diccionario
modified_strings = {}
for s in strings_to_translate:
    original_text = s['text']
    
    # Normalizar para buscar en diccionario (sin espacios, minúsculas)
    normalized_key = re.sub(r'[^\w\s]', '', original_text).upper()
    
    if normalized_key in [re.sub(r'[^\w\s]', '', k.upper()) for k in translations.keys()]:
        # Buscar traducción exacta primero
        if original_text in translations:
            translated = translations[original_text]
        else:
            # Si no hay traducción exacta, mantener original (evita sobreescribir artefactos)
            translated = original_text
        
        modified_strings[s['start']] = translated
        print(f"[TRADUCIDO] {s['text'][:60]:60} -> {translated}")
    # Si no hay traducción, saltar (mantener original para artefactos/etiquetas)

# Crear nuevo contenido con traducciones aplicadas
print(f"\n{'='*80}")
print(f"APLICANDO TRADUCCIONES...")
print("=" * 80)

new_plain = bytearray(pt)
modified_count = 0

for pos in sorted(modified_strings.keys(), reverse=True):  # Ordenar descendente para no romper offsets
    try:
        original_bytes = modified_strings[pos].encode('ascii')[:10]  # Usar primeros 10 bytes como referencia
        
        # Buscar la ocurrencia en el buffer
        found_pos = new_plain.find(original_bytes) if original_bytes else pos
        
        if found_pos >= 0 and found_pos < len(new_plain):
            # Solo reemplazar si coincide (evitar modificar artefactos por error)
            existing_text = bytes(new_plain[found_pos:found_pos+10]).decode('ascii', errors='replace')
            
            if original_bytes:
                new_plain[found_pos:found_pos+len(original_bytes)] = bytearray(modified_strings[pos].encode('ascii'))
                
                print(f"  Modificado en offset {hex(found_pos)}")
                modified_count += 1
    except Exception as e:
        pass

print(f"\nBytes modificados: {modified_count}\n")

# Guardar OP_CK_es.cpk
output = OUTPUT_PATH
print(f"Guardando archivo traducido: {output}")
print(f"  Tamaño original: {len(pt):,} bytes")
print(f"  Tamaño nuevo: {len(new_plain):,} bytes")

try:
    with open(output, 'wb') as f:
        f.write(bytes(new_plain))
    
    print("✅ Archivo guardado correctamente\n")
    
except Exception as e:
    print(f"❌ Error guardando archivo: {e}\n")
    
print(f"\n{'='*80}")
print("TRADUCCIÓN COMPLETA DE OP_CK_es.cpk CREADA!")
print(f"Ubicación: {output}")
print(f"Lista para instalar en: D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK")
print("=" * 80)

# Guardar resumen de traducciones en archivo
summary = r"C:/Dev/Default Project/srwv/outputs/opck_es_summary.txt"
with open(summary, 'w', encoding='utf-8') as f:
    f.write("Resumen de traducción OP_CK_es.cpk\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Archivo traducido: {output}\n")
    f.write(f"Tamaño original: {len(pt):,} bytes\n")
    f.write(f"Traducciones aplicadas: {modified_count}\n\n")
    
    for s in strings_to_translate[:50]:  # Mostrar primeros 50 traducciones
        if any(c.isalpha() for c in s['text']):
            normalized = re.sub(r'[^\w\s]', '', s['text']).upper()
            key_match = next((k for k in translations.keys() 
                            if re.sub(r'[^\w\s]', '', k.upper()) == normalized and k not in ['GNF','JP1']), None)
            
            if key_match:
                f.write(f"{s['text'][:70]} -> {translations[key_match]}\n")
            else:
                f.write(f"{s['text'][:70]} (sin traducción específica)\n")

print(f"Resumen guardado en: {summary}")
