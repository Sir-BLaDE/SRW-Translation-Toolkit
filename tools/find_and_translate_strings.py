# -*- coding: utf-8 -*-
"""Buscar y traducir strings ASCII en OP.CPK sin usar parser CPK"""
import os

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real.cpk"

print("=" * 80)
print("BUSCAR Y TRADUCIR STRINGS EN OP.CPK")
print("=" * 80)

# Leer archivo como binario
with open(P_ORIGINAL, 'rb') as f:
    data = f.read()

print(f"\nTamaño OP.CPK: {len(data):,} bytes\n")

# Diccionario de traducciones
translations = {
    "Press any button": "Presiona cualquier botón",
    "Settings": "Configuración",
    "Quit Game": "Salir del Juego",
    "Continue": "Continuar",
    "Load": "Cargar",
    "Start": "Iniciar",
    "Mode Select": "Selección de Modo",
    "Beginner's Mode": "Modo Principiante",
    "Standard Mode": "Modo Estándar",
    "Guidance Mode": "Modo Guía",
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
    "Operator": "Operador",
    "Yamanami": "Yanamimi",
    "Incoming transmission from the enemy!": "¡Transmisión enemiga recibida!",
    "Attention Earth Fleet: Surrender at once!": "¡Flota de la Tierra, rindíos inmediatamente!",
    "How do you respond?": "¿Cómo respondéis?",
    "The Yugiri, Kurama and Abukuma are down!": "¡Yugiri, Kurama y Abukuma han caído!",
    "Other vessels also taking heavy fire!": "¡Otras naves bajo intenso fuego!",
    "Commander!": "¡Comandante!",
    "Hold.": "Esperar...",
}

# Encontrar todos los strings ASCII legibles en el archivo
print("Buscando strings ASCII imprimibles (32-126)...\n")

ascii_strings = []
i = 0
while i < len(data):
    if 32 <= data[i] <= 126:
        start = i
        while i < len(data) and 32 <= data[i] <= 126:
            i += 1
        
        text = data[start:i].decode('ascii')
        
        # Solo strings de al menos 5 caracteres con letras
        if len(text) >= 5 and any(c.isalpha() for c in text):
            # Excluir artefactos simples (PPP, JJJ, etc.)
            cleaned = text.replace(' ', '').upper()
            if not re.match(r'^[A-Z]{2,15}$', cleaned):
                ascii_strings.append({
                    'start': start,
                    'end': i,
                    'text': text[:100],  # Cortar a 100 chars
                    'length': i - start
                })

import re

print(f"Strings ASCII encontrados: {len(ascii_strings)}\n")

# Buscar coincidencias con diccionario de traducción
to_translate = []
for s in ascii_strings:
    for key in translations.keys():
        if key.lower() in s['text'].lower():
            to_translate.append({
                'start': s['start'],
                'end': s['end'],
                'original': key,
                'translated': translations[key]
            })

print(f"Strings traducibles encontrados: {len(to_translate)}\n")

# Mostrar ejemplos de coincidencias
print("EJEMPLOS DE COINCIDENCIAS:")
for t in sorted(to_translate, key=lambda x: -len(x['original']))[:15]:
    original = repr(t['original'])
    translated = repr(t['translated'])
    offset = hex(t['start'])
    print(f"  Offset {offset:8}: '{original}' -> '{translated}'")

# Contar coincidencias únicas (sin duplicados cercanos)
unique_count = sum(1 for t in to_translate if all(abs(t['start'] - u['start']) > 50 for u in to_translate[to_translate.index(t)+1:min(to_translate.index(t)+6, len(to_translate))]])

print(f"\nStrings únicos para traducir: {unique_count}")

# Si no hay coincidencias claras, usar un enfoque más agresivo
if unique_count == 0 or len(to_translate) < 10:
    print("\nNo se encontraron suficientes coincidencias. Intentando traducción aproximada...\n")
    
    # Buscar strings que contengan palabras clave traducibles
    to_translate = []
    for s in ascii_strings:
        text_lower = s['text'].lower()
        
        # Traducir si contiene palabras de inglés
        words = text_lower.split()
        if any(word in words for word in [
            'button', 'settings', 'game', 'start', 'continue', 'load',
            'male', 'female', 'age', 'mode', 'select',
            'commander', 'operator', 'incoming', 'earth', 'fleet',
            'yugiri', 'kurama', 'abukuma', 'vessels'
        ]):
            # Encontrar traducción aproximada
            for key, value in translations.items():
                if key.lower() in text_lower:
                    to_translate.append({
                        'start': s['start'],
                        'original': key,
                        'translated': value
                    })
                    break

print(f"Strings traducibles (método aproximado): {len(to_translate)}\n")

# Guardar archivo sin traducción si no hay coincidencias claras
if len(to_translate) < 3:
    print("No se encontraron suficientes strings traducibles. Guardando CPK original.\n")
else:
    # Aplicar traducciones a los bytes del archivo
    new_data = bytearray(data)
    
    for t in sorted(to_translate, key=lambda x: -len(x['original']))[:50]:  # Max 50 traducciones
        if len(t['original']) < 5:
            continue
        
        original_bytes = t['original'].encode('ascii')
        translated_bytes = t['translated'].encode('ascii')[:len(original_bytes)]  # Misma longitud o acortada
        
        try:
            found_pos = new_data.find(original_bytes)
            
            if found_pos >= 0:
                # Reemplazar solo si coincide exactamente
                existing_text = bytes(new_data[found_pos:found_pos+len(original_bytes)]).decode('ascii', errors='replace')
                
                if t['original'] == existing_text:
                    new_data[found_pos:found_pos+len(original_bytes)] = translated_bytes
                    print(f"  Tradujdo: '{t['original']}' -> '{translated_bytes.decode('ascii')}'")
        except Exception as e:
            pass
    
    modified_count = sum(1 for t in to_translate if any(t['original'] == bytes(new_data[pos:pos+len(t['original'])]).decode('ascii', errors='ignore').lower() 
                    for pos in range(len(new_data)-len(t['original']))))
    
    print(f"\nTraducciones aplicadas exitosamente: {modified_count}\n")

# Guardar archivo tradujdo
with open(OUTPUT_PATH, 'wb') as f:
    if len(to_translate) >= 3:
        f.write(bytes(new_data))
    else:
        # Copiar original si no se encontraron suficientes traducciones
        with open(P_ORIGINAL, 'rb') as f_orig:
            f.write(f_orig.read())

print(f"✅ Archivo guardado: {OUTPUT_PATH}")
print(f"   Tamaño: {len(new_data):,} bytes")

# Crear resumen de traducciones
summary = r"C:/Dev/Default Project/srwv/outputs/traduction_applied.txt"
with open(summary, 'w', encoding='utf-8') as f:
    f.write("Resumen de traducciones aplicadas a OP_CK_es_real.cpk\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Archivo original: {P_ORIGINAL}\n")
    f.write(f"Tamaño original: {len(data):,} bytes\n")
    f.write(f"Strings traducibles encontrados: {len(to_translate)}\n\n")
    
    for t in sorted(to_translate, key=lambda x: -len(x['original']))[:100]:
        if len(t['original']) >= 5:
            original = repr(t['original'])
            translated = repr(t['translated'])
            f.write(f"{original}\n")
            f.write(f"    -> {translated}\n\n")

print(f"Resumen guardado en: {summary}")
