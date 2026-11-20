# -*- coding: utf-8 -*-
"""Traducción simple: buscar y traducir strings ASCII en OP.CPK"""
import os

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real.cpk"

print("=" * 80)
print("TRADUCCION SIMPLE - ESPANOL ESPAÑA")
print("=" * 80)

# Leer archivo
with open(P_ORIGINAL, 'rb') as f:
    data = bytearray(f.read())

print(f"Tamaño OP.CPK: {len(data):,} bytes\n")

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
    "Commander!": "¡Comandante!",
    "Hold.": "Esperar...",
    "Incoming transmission from the enemy!": "¡Transmisión enemiga recibida!",
    "Attention Earth Fleet: Surrender at once!": "¡Flota de la Tierra, rindíos inmediatamente!",
    "How do you respond?": "¿Cómo respondéis?",
}

# Aplicar traducciones directamente a los bytes
print("Aplicando traducciones...\n")

modified_count = 0
for original_text, translated in sorted(translations.items(), key=lambda x: -len(x[0])):
    try:
        original_bytes = bytearray(original_text.encode('ascii'))
        
        # Buscar string original (empieza por los más largos para evitar parciales)
        found_pos = data.find(bytes(original_bytes))
        
        if found_pos >= 0:
            # Verificar coincidencia exacta
            existing_len = len(data[found_pos:])
            existing_text = bytes(data[found_pos:found_pos+len(original_bytes)]).decode('ascii', errors='replace')
            
            if original_text == existing_text[:len(original_text)]:
                # Reemplazar
                translated_bytes = translated.encode('ascii')[:len(original_bytes)]
                data[found_pos:found_pos+len(original_bytes)] = translated_bytes
                modified_count += 1
                print(f"  ✅ '{original_text}' -> '{translated_bytes.decode('ascii')}'")
    except Exception as e:
        pass

print(f"\nTotal traducciones aplicadas: {modified_count}")

# Guardar archivo
with open(OUTPUT_PATH, 'wb') as f:
    f.write(data)

print(f"\n✅ Archivo guardado: {OUTPUT_PATH}")
print(f"   Tamaño: {len(data):,} bytes")
print()
print("REINICIA EL JUEGO para ver cambios!")
