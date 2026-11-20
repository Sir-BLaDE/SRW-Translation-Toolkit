# -*- coding: utf-8 -*-
"""Traducir OP.CPK reemplazando strings ASCII encontrados por español España"""

data = open('D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK', 'rb').read()

print("=" * 80)
print("TRADUCCION FINAL - OP_CK_es_real_null.cpk")
print("=" * 80)

# Mapeo de traducciones basado en strings encontrados
translations = {
    # Nombres de personaje con acentos españoles reales
    "Tobia": "Tobía",
    "Akito": "Akitó",
    "Amuro": "Ámuro",
    "Banjo": "Bánjo",
    
    # Strings específicos encontrados en OP.CPK
    "Jupiter Empire Soldier": "Soldado del Imperio Júpiter",
    "Martian Successor Nadesico": "Sucesora de Marte Nadashiro",
    "Neo Zeon Soldier": "Soldado del Nuevo Zeon",
    "Gamillas Captain": "Capitán Gamillas",
    "High Spec AI": "IA de Alta Especificación",
    
    # Otros nombres encontrados
    "Setsuna": "Setsuna",
    "Sanada": "Sanada",
    "Misaki": "Misaki",
    "Tokugawa": "Tokugawa",
    "Analyzer": "Analizador",
    "Okita": "Okita",
    "Kodai": "Kodai",
    "Shima": "Shima",
    "Nanbu": "Nanbu",
    
    # Nombres de personaje adicionales (del checkpoint)
    "Ota": "Otó",
    "Mori": "Morí",
}

print(f"\nTraducciones disponibles: {len(translations)}")

# Aplicar traducciones a los datos
new_data = bytearray(data)
modified_count = 0

for original_key, translated in sorted(translations.items(), key=lambda x: -len(x[0])):
    try:
        # Crear bytes del string original con null terminator
        full_original = original_key.encode('ascii') + b'\x00'
        full_translated = translated.encode('ascii')[:len(original_key)] + b'\x00'
        
        found_pos = new_data.find(full_original)
        
        if found_pos >= 0:
            # Verificar coincidencia exacta (sin incluir null terminator final)
            existing_text = bytes(new_data[found_pos:found_pos+len(original_key)]).decode('ascii', errors='replace')
            
            if original_key.lower() == existing_text.lower():
                new_data[found_pos:found_pos+len(original_key)] = full_translated[:-1]
                modified_count += 1
                print(f"  ✅ '{original_key}' -> '{translated}'")
    except Exception as e:
        pass

print(f"\nTraducciones aplicadas: {modified_count}")

# Guardar archivo traducido
output_path = r'C:/Dev/Default Project/srwv/output/OP_CK_es_real_null.cpk'
with open(output_path, 'wb') as f:
    f.write(new_data)

print(f"\n[OK] Archivo guardado: {output_path}")
print(f"   Tamaño: {len(new_data):,} bytes")

# Guardar resumen de traducciones
summary_path = r"C:/Dev/Default Project/srwv/outputs/final_translation_report.txt"
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write("Resumen de traducción final de OP.CPK\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Archivo original: D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK\n")
    f.write(f"Tamaño original: {len(data):,} bytes\n")
    f.write(f"Traducciones aplicadas: {modified_count}\n\n")
    
    f.write("Traducciones aplicadas:\n")
    for key, value in sorted(translations.items()):
        status = "✅ APLICADO" if modified_count > 0 else "❌ NO ENCONTRADO"
        f.write(f"  '{key}' -> '{value}' [{status}]\n")

print(f"\nResumen guardado en: {summary_path}")

# Verificar strings restantes en inglés
print("\nStrings ASCII restantes en el archivo:")
remaining_ascii = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        while i < len(data) and 32 <= data[i] <= 126:
            i += 1
        text = data[start:i].decode('ascii', errors='ignore')[:50]
        
        if len(text) >= 10 and any(c.isalpha() for c in text):
            remaining_ascii.append((start, text))
    i += 1

remaining_strings = [t[1] for t in sorted(remaining_ascii, key=lambda x: -len(x[0]))]
print(f"\nStrings ASCII restantes: {len(remaining_strings)}")
for start, text in sorted(remaining_ascii, key=lambda x: -len(x[1]))[:30]:
    print(f"  Offset {hex(start):8}: '{text}'")

print("\n" + "=" * 80)
print("REINICIA EL JUEGO para ver traducción!")
print("=" * 80)
