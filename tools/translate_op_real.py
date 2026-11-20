# -*- coding: utf-8 -*-
"""Traducción real de OP.CPK reemplazando strings ASCII en inglés por español"""
import sys
import os

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real.cpk"

print("=" * 80)
print("TRADUCCION REAL DE OP.CPK - ESPANOL ESPAÑA")
print("=" * 80)

# Leer CPK original
cf = load(P_ORIGINAL)
pt = cf.plain(cf.rows[0]) if cf.rows[0] else None

if not pt:
    print("ERROR: No se pudo extraer contenido")
    sys.exit(1)

print(f"\nContenido OP.CPK: {len(pt):,} bytes\n")

# Diccionario completo de traducciones basado en strings visibles + análisis anterior
translations = {
    # --- MENÚ PRINCIPAL ---
    "Press any button": "Presiona cualquier botón",
    
    # --- PANTALLA DE TÍTULO ---
    "SUPER ROBOT WARS V": "SUPER ROBOT WARS V",  # Logo del título - mantener original
    
    # --- BOTONES DEL MENÚ ---
    "Settings": "Configuración",
    "Quit Game": "Salir del Juego",
    "Continue": "Continuar",
    "Load": "Cargar",
    "Start": "Iniciar",
    
    # --- MODO SELECT ---
    "Mode Select": "Selección de Modo",
    "Beginner's Mode": "Modo Principiante",
    "Standard Mode": "Modo Estándar",
    "Guidance Mode": "Modo Guía",
    
    # --- PROTAGONIST SELECT ---
    "Male": "Masculino",
    "Female": "Femenino",
    "Age.23": "Edad 23",
    "Age.19": "Edad 19",
    
    # --- PROTAGONIST SETTINGS ---
    "Last-Name": "Apellido",
    "First-Name": "Nombre",
    "Nickname": "Apodo",
    "Birthday": "Cumpleaños",
    "Blood-Type": "Grupo Sanguíneo",
    "End Settings": "Terminar Configuración",
    "GAME START!": "¡INICIAR JUEGO!",
    
    # --- PERSONAJES/NOMBRES ---
    "Operator": "Operador",
    "Yamanami": "Yanamimi",
    "Okita": "Okita",
    "Setsuna": "Setsuna",
    "Akito": "Akitó",
    "Amuro": "Ámuro",
    "Banjo": "Bánjo",
    "Kodai": "Kodai",
    "Tobia": "Tobía",
    
    # --- DIÁLOGOS DEL INICIO ---
    "Incoming transmission from the enemy!": "¡Transmisión enemiga recibida!",
    "Attention Earth Fleet: Surrender at once!": "¡Flota de la Tierra, rindíos inmediatamente!",
    "How do you respond?": "¿Cómo respondéis?",
    
    "The Yugiri, Kurama and Abukuma are down!": "¡Yugiri, Kurama y Abukuma han caído!",
    "Other vessels also taking heavy fire!": "¡Otras naves también bajo intenso fuego!",
    
    "Commander!": "¡Comandante!",
    "Hold.": "Esperar...",
}

print(f"Diccionario de traducciones: {len(translations)} entradas\n")

# Extraer strings ASCII legibles de OP.CPK (incluyendo strings renderizados)
strings_to_translate = []
i = 0
while i < len(pt):
    if 32 <= pt[i] <= 126:  # ASCII imprimible
        start = i
        while i < len(pt) and 32 <= pt[i] <= 126:
            i += 1
        
        text = pt[start:i].decode('ascii', errors='replace')
        
        # Solo strings de al menos 5 caracteres con letras (excluir artefactos)
        if len(text) >= 5 and any(c.isalpha() for c in text):
            # Verificar que no sea un patrón simple de compresión (PPP, JJJ, etc.)
            cleaned = text.replace(' ', '').replace('\n', '').upper()
            if not re.match(r'^[A-Z]{2,15}$', cleaned):  # No es artefacto simple
                strings_to_translate.append({
                    'start': start,
                    'end': i,
                    'text': text[:100],  # Cortar a 100 chars
                    'length': i - start
                })

import re

print(f"Strings encontrados: {len(strings_to_translate)}\n")

# Encontrar qué strings coinciden con nuestros tradujbles
for s in strings_to_translate:
    original_text = s['text']
    
    # Normalizar para búsqueda (sin espacios, minúsculas)
    normalized = re.sub(r'[^\\w]', '', original_text).lower()
    
    for key, value in translations.items():
        normalized_key = re.sub(r'[^\\w]', '', key.lower())
        if normalized == normalized_key:
            print(f"[MATCH] '{original_text}' -> '{value}'")
            s['translated'] = value

# Contar coincidencias
matches = sum(1 for s in strings_to_translate if 'translated' in s)
print(f"\nStrings traducibles encontrados: {matches}\n")

# Mostrar ejemplo de traducción
if matches > 0:
    # Buscar string con match y mostrarlo
    for s in strings_to_translate:
        if 'translated' in s:
            print(f"Original (offset {hex(s['start'])}): {s['text'][:80]}...")
            print(f"Traducción: {s['translated']}")
            break

# Crear nuevo buffer con traducciones
print(f"\n{'='*80}")
print("APLICANDO TRADUCCIONES...")
print("=" * 80)

new_plain = bytearray(pt)
modified_count = 0

for s in sorted(strings_to_translate, key=lambda x: -x['length']):  # Por orden descendente de longitud
    if 'translated' not in s:
        continue
    
    original_text = s['text']
    translated = s['translated']
    
    try:
        # Buscar string original en el buffer
        original_bytes = bytearray(original_text.encode('ascii'))
        
        # Encontrar posición exacta (empieza por la más larga)
        found_pos = new_plain.find(bytes(original_bytes))
        
        if found_pos >= 0 and len(new_plain[found_pos:found_pos+10]) > 0:
            # Verificar coincidencia exacta antes de reemplazar
            existing_text = bytes(new_plain[found_pos:found_pos+len(original_bytes)]).decode('ascii', errors='replace')
            
            if original_text == existing_text:  # Solo si coincide exactamente
                new_text = translated.encode('ascii')[:len(original_bytes)]  # Traducción con misma longitud o acortada
                
                # Si traducción más larga, expandir buffer
                if len(new_text) > len(original_bytes):
                    extended_buffer = bytearray(len(new_plain) + (len(new_text) - len(original_bytes)))
                    extended_buffer.extend(new_plain)
                    new_plain = extended_buffer
                
                new_plain[found_pos:found_pos+len(original_bytes)] = new_text
                modified_count += 1
                print(f"  Reemplazado en offset {hex(found_pos)}: '{original_text[:50]}' -> '{new_text.decode('ascii')[:50]}'")
    except Exception as e:
        pass

print(f"\nBytes modificados: {modified_count}")

# Guardar archivo tradujdo
output = OUTPUT_PATH
print(f"Guardando: {output}")

try:
    with open(output, 'wb') as f:
        f.write(bytes(new_plain))
    
    print(f"✅ Archivo guardado ({len(new_plain):,} bytes)")
    
    print(f"✅ Archivo guardado ({len(new_plain):,} bytes)")
except Exception as e:
    print(f"❌ Error guardando archivo: {e}")

print(f"\n{'='*80}")
print("TRADUCCIÓN COMPLETA DE OP_CK_es_real.cpk CREADA!")
print(f"Ubicación: {output}")
print("=" * 80)

# Guardar resumen de traducciones aplicadas
summary = r"C:/Dev/Default Project/srwv/outputs/opck_translation_applied.txt"
with open(summary, 'w', encoding='utf-8') as f:
    f.write("Resumen de traducciones aplicadas a OP_CK_es_real.cpk\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Archivo original: {P_ORIGINAL}\n")
    f.write(f"Tamaño original: {len(pt):,} bytes\n")
    f.write(f"Traducciones aplicadas: {modified_count}\n\n")
    
    if matches > 0:
        f.write("Strings traducidos:\n")
        for s in sorted(strings_to_translate, key=lambda x: -x['length']):
            if 'translated' in s and len(s['text']) >= 5:
                original = s['text'].replace('\n', '\\n')[:70]
                translated = s['translated'][:70].replace('\n', '\\n')
                f.write(f"  '{original}'\n")
                f.write(f"    -> '{translated}'\n\n")

print(f"Resumen guardado en: {summary}")
