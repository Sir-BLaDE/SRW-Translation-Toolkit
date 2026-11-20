# -*- coding: utf-8 -*-
"""Traducir strings null-terminated en OP.CPK"""
import os
import re

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real_null.cpk"

print("=" * 80)
print("TRADUCCION OP.CPK - STRINGS NUL-TERMINATED")
print("=" * 80)

# Leer archivo
with open(P_ORIGINAL, 'rb') as f:
    data = bytearray(f.read())

print(f"Tamaño OP.CPK: {len(data):,} bytes\n")

# Diccionario de traducciones español España
translations = {
    # Nombres de personajes (basado en strings encontrados)
    "Ota": "Otó",
    "Mori": "Morí", 
    "Misaki": "Misaki",
    "Gamillas Captain": "Capitán Gamillas",
    
    # UI general
    "Press any button": "Presiona cualquier botón",
    "Settings": "Configuración",
    "Quit Game": "Salir del Juego",
    "Continue": "Continuar",
    "Load": "Cargar",
    "Start": "Iniciar",
    
    # Modes
    "Mode Select": "Selección de Modo",
    "Beginner's Mode": "Modo Principiante",
    "Standard Mode": "Modo Estándar", 
    "Guidance Mode": "Modo Guía",
    
    # Protagonist settings
    "Male": "Masculino",
    "Female": "Femenino",
    "Age.23": "Edad 23",
    "Age.19": "Edad 19",
    "Last-Name": "Apellido",
    "First-Name": "Nombre",
    "Nickname": "Apodo",
    "Birthday": "Cumpleaños",
    "Blood-Type": "Grupo Sanguíneo",
    "End Settings": "Terminar Configuración",
    "GAME START!": "¡INICIAR JUEGO!",
    
    # Characters from screenshot
    "Yamanami": "Yanamimi",
    "Okita": "Okita",
    "Setsuna": "Setsuna",
    "Banjo": "Bánjo",
    "Tobia": "Tobía",
    "Kodai": "Kodai",
    "Akito": "Akitó",
    "Amuro": "Ámuro",
    
    # Dialogues
    "Commander!": "¡Comandante!",
    "Hold.": "Esperar...",
}

print("Buscando strings null-terminated en OP.CPK...\n")

# Encontrar todos los bloques de texto ASCII (entre null terminators o 0x10 boundaries)
ascii_blocks = []
i = 0
while i < len(data):
    # Buscar patrón: bytes imprimibles seguidos de null o 0x10
    j = i
    text_chars = []
    
    while j < len(data) and (
        (32 <= data[j] <= 126) or 
        (data[j] == 0x00) or 
        (data[j] == 0x10)
    ):
        if 32 <= data[j] <= 126:
            text_chars.append(chr(data[j]))
        j += 1
    
    # Ignorar bloques muy cortos o artefactos
    if len(text_chars) >= 5 and any(c.isalpha() for c in ''.join(text_chars)):
        text = ''.join(text_chars).rstrip('\x00').rstrip('\x10')
        
        # Verificar que no es artefacto simple
        cleaned = text.replace(' ', '').upper()
        if len(cleaned) > 15 or not re.match(r'^[A-Z]{2,15}$', cleaned):
            ascii_blocks.append({
                'start': i,
                'end': j - 1,
                'text': text[:100],
                'length': j - i
            })
    
    # Saltar este bloque para no superponer búsquedas
    i = j

print(f"Bloques ASCII encontrados: {len(ascii_blocks)}")

# Buscar coincidencias con traducciones
to_translate = []
for block in ascii_blocks:
    text = block['text'][:80]  # Max 80 chars
    
    for original_key, value in translations.items():
        if original_key.lower() in text.lower():
            to_translate.append({
                'block': block,
                'original': original_key,
                'translated': value,
                'matched_text': text[:60]
            })

print(f"Strings traducibles encontrados: {len(to_translate)}")

# Mostrar coincidencias
if to_translate:
    print("\nCOINCIDENCIAS:")
    for t in sorted(to_translate, key=lambda x: -len(x['original']))[:30]:
        original = repr(t['original'])
        translated = repr(t['translated'])
        block_text = t['matched_text'][:40]
        print(f"  '{block_text}'...")
        print(f"    '{original}' -> '{translated}'")
else:
    print("\nNo se encontraron coincidencias claras. Probando búsqueda aproximada...\n")

    # Búsqueda aproximada - buscar palabras clave
    keywords_to_translate = [k.lower() for k in translations.keys()]
    
    for block in ascii_blocks:
        text_lower = block['text'].lower()
        
        for keyword in keywords_to_translate:
            if keyword.replace("'", '') in text_lower and keyword != text_lower.split()[0] if 'split' in dir(text_lower) else False:
                # Encontrar traducción correspondiente
                for original_key, value in translations.items():
                    if original_key.lower().replace("'", '').replace('"', '') == keyword or \
                       original_key.lower() == keyword.replace("'", '').replace('"', ''):
                        to_translate.append({
                            'block': block,
                            'original': original_key,
                            'translated': value
                        })
                        break
        else:
            continue
        break

# Si aún no hay coincidencias claras, intentar traducción directa por palabras clave específicas
if len(to_translate) < 5:
    print(f"\nTraduciendo nombres de personaje directamente (método aproximado)...")
    
    # Nombres específicos encontrados en el archivo
    character_names = [
        "Ota", "Mori", "Misaki", 
        "Akito", "Amuro", "Banjo", "Setsuna", "Okita", "Yamanami"
    ]
    
    for block in ascii_blocks:
        text_upper = block['text'].upper()
        
        for char_name in character_names:
            if char_name in text_upper:
                # Buscar traducción
                original_key = char_name
                value = translations.get(char_name, char_name + " (no traducido)")
                
                to_translate.append({
                    'block': block,
                    'original': original_key,
                    'translated': value,
                    'matched_text': block['text'][:40]
                })
    
    print(f"Strings traducibles con método aproximado: {len(to_translate)}")

# Mostrar todas las coincidencias finales
print(f"\n{'='*80}")
print("APLICANDO TRADUCCIONES FINALES:")
print(f"{'='*80}\n")

modified_count = 0

for t in sorted(to_translate, key=lambda x: -len(x['original']))[:50]:  # Max 50 traducciones
    original_text = t['original']
    translated = t['translated']
    
    if len(original_text) < 4:
        continue
    
    try:
        # Construir bytes con null terminator
        full_original = original_text + '\x00'
        full_bytes = bytearray(full_original.encode('ascii'))
        
        found_pos = data.find(bytes(full_bytes))
        
        if found_pos >= 0:
            # Verificar coincidencia exacta
            existing_len = len(original_text) + 1  # +1 para null terminator
            existing_text = bytes(data[found_pos:found_pos+existing_len]).decode('ascii', errors='replace')
            
            if original_text.lower() == existing_text[:-1].lower():  # Sin el null final
                new_bytes = translated.encode('ascii')[:len(original_text)]
                data[found_pos:found_pos+len(original_text)] = new_bytes
                modified_count += 1
                print(f"  ✅ '{original_text}' -> '{new_bytes.decode('ascii')}'")
    except Exception as e:
        pass

print(f"\nTotal traducciones aplicadas: {modified_count}")

# Guardar archivo traducido
with open(OUTPUT_PATH, 'wb') as f:
    f.write(data)

print(f"\n✅ Archivo guardado: {OUTPUT_PATH}")
print(f"   Tamaño: {len(data):,} bytes")

# Guardar resumen
summary = r"C:/Dev/Default Project/srwv/outputs/traduction_applied.txt"
with open(summary, 'w', encoding='utf-8') as f:
    f.write("Resumen de traducciones aplicadas a OP_CK_es_real_null.cpk\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Archivo original: {P_ORIGINAL}\n")
    f.write(f"Tamaño original: {len(data):,} bytes\n")
    f.write(f"Traducciones aplicadas: {modified_count}\n\n")
    
    for key, value in sorted(translations.items()):
        if any(t['original'] == key for t in to_translate):
            status = "✅ APLICADO"
        else:
            status = "❌ NO ENCONTRADO"
        
        f.write(f"{key:30} -> {value:40} [{status}]\n")

print(f"\nResumen guardado en: {summary}")
print("\n" + "=" * 80)
print("REINICIA EL JUEGO para ver los cambios!")
print("=" * 80)
