# -*- coding: utf-8 -*-
"""Crear OP_CK_es_real.cpk con traducción real basada en reemplazo de strings ASCII"""
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real.cpk"

print("=" * 80)
print("CREANDO OP_CK_es_real.cpk - TRADUCCION REAL ESPANOL ESPAÑA")
print("=" * 80)

# Leer CPK original
cf = load(P_ORIGINAL)
pt = cf.plain(cf.rows[0]) if cf.rows[0] else None

if not pt:
    print("ERROR: No se pudo extraer contenido")
    sys.exit(1)

print(f"\nContenido OP.CPK: {len(pt):,} bytes\n")

# Diccionario de traducciones español España
translations = {
    # --- MENÚ PRINCIPAL ---
    "Press any button": "Presiona cualquier botón",
    
    # --- BOTONES MENÚ ---
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
    
    # --- PERSONAJES ---
    "Operator": "Operador",
    "Yamanami": "Yanamimi",
    
    # --- DIÁLOGOS INICIO ---
    "Incoming transmission from the enemy!": "¡Transmisión enemiga recibida!",
    "Attention Earth Fleet: Surrender at once!": "¡Flota de la Tierra, rindíos inmediatamente!",
    "How do you respond?": "¿Cómo respondéis?",
    "The Yugiri, Kurama and Abukuma are down!": "¡Yugiri, Kurama y Abukuma han caído!",
    "Other vessels also taking heavy fire!": "¡Otras naves bajo intenso fuego!",
    
    # --- OTROS ---
    "Commander!": "¡Comandante!",
    "Hold.": "Esperar...",
}

# Extraer strings ASCII de OP.CPK y traducir
strings_found = []
i = 0
while i < len(pt):
    if 32 <= pt[i] <= 126:
        start = i
        while i < len(pt) and 32 <= pt[i] <= 126:
            i += 1
        text = pt[start:i].decode('ascii', errors='replace')
        if len(text) >= 5 and any(c.isalpha() for c in text):
            cleaned = text.replace(' ', '').upper()
            if not re.match(r'^[A-Z]{2,15}$', cleaned):
                strings_found.append({
                    'start': start,
                    'text': text[:20],  # Cortar a 20 chars para evitar duplicados
                    'length': i - start
                })

import re

# Buscar coincidencias con diccionario
to_translate = []
for s in strings_found:
    for key in translations.keys():
        if key.lower() in s['text'].lower():
            to_translate.append((s['start'], key, translations[key]))

print(f"Strings traducibles encontrados: {len(to_translate)}\n")

# Mostrar ejemplos
for start, key, value in to_translate[:10]:
    original = pt[start:start+min(40, len(pt)-start)].decode('ascii', errors='replace')
    print(f"Offset {hex(start):10}: '{original}' -> '{value}'")

# Crear nuevo buffer con traducciones
new_plain = bytearray(pt)
modified_count = 0

for start, key, value in sorted(to_translate, key=lambda x: -len(key)):
    original_text = key
    translated = value
    
    try:
        original_bytes = bytearray(original_text.encode('ascii'))
        found_pos = new_plain.find(bytes(original_bytes))
        
        if found_pos >= 0:
            # Expandir buffer si traducción es más larga
            if len(translated) > len(original_text):
                extra_len = len(translated) - len(original_text)
                new_plain.extend(b'\x00' * extra_len)
            
            new_plain[found_pos:found_pos+len(original_text)] = translated.encode('ascii')[:len(original_text)]
            modified_count += 1
            
    except Exception as e:
        pass

print(f"\nBytes modificados: {modified_count}")

# Guardar archivo
with open(OUTPUT_PATH, 'wb') as f:
    f.write(bytes(new_plain))

print(f"✅ Archivo creado: {OUTPUT_PATH}")
print(f"   Tamaño: {len(new_plain):,} bytes\n")

# Guardar resumen
summary = r"C:/Dev/Default Project/srwv/outputs/traduction_applied.txt"
with open(summary, 'w', encoding='utf-8') as f:
    f.write(f"Traducciones aplicadas: {modified_count}\n\n")
    for start, key, value in sorted(to_translate, key=lambda x: -len(key))[:50]:
        original = repr(pt[start:start+len(key)]) if len(key) < 20 else repr(pt[start:start+20])
        f.write(f"{key:40} -> {value}\n")

print(f"Resumen guardado en: {summary}")
