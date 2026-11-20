# -*- coding: utf-8 -*-
"""Buscar TODOS los strings ASCII legibles en todos los archivos .cpk del juego para traducción"""
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

# Directorios de archivos CPK a buscar
GAME_PATHS = [
    r"D:\Juegos\*-SPARROW-\Super Robot Wars V\Data",
    r"D:\Juegos\*-SPARROW-\Super Robot Wars V\CommonData"
]

print("=" * 80)
print("BUSCANDO STRINGS ASCII EN TODOS LOS ARCHIVOS .CPK DEL JUEGO")
print("=" * 80)

all_strings = []
total_strings = 0

for game_path in GAME_PATHS:
    if "*" in game_path:
        # Expandir patrón de comodín
        import fnmatch
        base_dir = r"D:\Juegos"
        for name in os.listdir(base_dir):
            full_path = os.path.join(base_dir, name)
            if "SPARROW" in name:
                srwv_path = os.path.join(full_path, "Super Robot Wars V")
                
                if os.path.isdir(srwv_path):
                    print(f"\nEscaneando: {srwv_path}")
                    
                    # Buscar todos los archivos .cpk
                    for root, dirs, files in os.walk(srwv_path):
                        for file in sorted(files):
                            if file.lower().endswith('.cpk'):
                                filepath = os.path.join(root, file)
                                
                                try:
                                    # Intentar cargar archivo CPK
                                    cf = load(filepath)
                                    
                                    # Extraer strings de cada fila del CPK
                                    for row_idx in range(cf.rows_count):
                                        try:
                                            pt = cf.plain(cf.rows[row_idx]) if cf.rows[row_idx] else None
                                            
                                            if not pt:
                                                continue
                                            
                                            i = 0
                                            while i < len(pt):
                                                if 32 <= pt[i] <= 126:
                                                    start = i
                                                    while i < len(pt) and 32 <= pt[i] <= 126:
                                                        i += 1
                                                    
                                                    text = pt[start:i].decode('ascii', errors='replace')
                                                    
                                                    # Solo strings de al menos 4 caracteres con letras
                                                    if len(text) >= 4 and any(c.isalpha() for c in text):
                                                        # Evitar duplicados (misma línea + texto similar)
                                                        is_dup = False
                                                        for prev_text, prev_row in all_strings[-100:]:
                                                            if abs(prev_row) < row_idx:  # Mismo archivo/área
                                                                if text.lower() == prev_text.lower():
                                                                    is_dup = True
                                                                    break
                                                        
                                                        if not is_dup:
                                                            all_strings.append({
                                                                'file': filepath,
                                                                'row': row_idx,
                                                                'start': start,
                                                                'text': text[:100],  # Cortar a 100 chars
                                                                'length': i - start
                                                            })
                                                            
                                                            total_strings += 1
                                                    
                                                    if len(text) > 80:  # Evitar bucles infinitos en strings muy largos
                                                        break
                                                        
                                                else:
                                                    i += 1
                                                    
                                        except Exception as e:
                                            pass  # Saltar errores de filas individuales
                                
                                except Exception as e:
                                    print(f"  Error leyendo {file}: {e}")
    
    if total_strings > 500:  # Limitar búsqueda para evitar tiempo excesivo
        break

# Eliminar duplicados y artefactos
unique_strings = {}
for s in all_strings:
    text_lower = s['text'].lower().strip()
    file_name = os.path.basename(s['file'])
    
    if not re.match(r'^[A-Za-z]{3,}$', text_lower):  # Excluir artefactos puros como PPP, JJJ
        if len(text) < 40:  # Saltar strings muy largos (probablemente diálogos enteros)
            key = f"{file_name}:{text_lower[:50]}"
            unique_strings[key] = s

print(f"\n{'='*80}")
print(f"Total strings únicos encontrados: {len(unique_strings)}")

# Mostrar resumen por tipo de string
character_names = [s for s in unique_strings.values() if len(s['text']) <= 20 and not any(x in s['text'] for x in ['THE', 'AND', 'OF', 'IN', 'IS', 'A'])]
ui_labels = [s for s in unique_strings.values() if any(x in s['text'].upper() for x in ['GAME', 'PLAY', 'AREA', 'MAP', 'LEVEL', 'FIGHTER', 'UNIT'])]
other_text = [s for s in unique_strings.values() if len(s['text']) > 20 or s['text'] not in character_names + ui_labels]

print(f"  - Nombres de personajes (<20 chars): {len(character_names)}")
print(f"  - Etiquetas UI/etiquetas: {len(ui_labels)}")
print(f"  - Otro texto/diálogos: {len(other_text)}\n")

# Mostrar todas las strings únicas por orden alfabético (para facilitar traducción)
print("=" * 80)
print("LISTADO COMPLETO DE STRINGS POR TRADUCIR:")
print("=" * 80)

sorted_strings = sorted(unique_strings.values(), key=lambda x: x['text'].lower())

for idx, s in enumerate(sorted_strings[:200], 1):  # Mostrar primeros 200
    print(f"{idx:3d}: \\\"{s['text']}\\\"")

print(f"\n{'='*80}")
print(f"Total strings a traducir: {len(unique_strings)}")
print("=" * 80)

# Guardar en archivo de traducción
output = r"C:/Dev/Default Project/srwv/outputs/all_translateable_strings.txt"
with open(output, 'w', encoding='utf-8') as f:
    f.write("# Strings ASCII legibles encontrados en todos los archivos CPK\n")
    f.write("# Para traducción a español España\n# Formato: NÚMERO: TEXTO_ORIGINAL\n#\n")
    
    for idx, s in enumerate(sorted_strings[:500], 1):  # Guardar primeros 500
        line = f"{idx}: {s['text']}\n"
        f.write(line)

print(f"\nStrings guardados en: {output}")
