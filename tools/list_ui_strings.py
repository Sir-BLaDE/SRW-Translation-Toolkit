# -*- coding: utf-8 -*-
"""Listar todas las strings de interfaz de usuario legibles en OP.CPK"""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
pt = cf.plain(cf.rows[0])  # Fila 0 de OP.CPK (datos UI editables)

print("=" * 80)
print("STRINGS UI DE INTERFAZ EN OP.CPK")
print("=" * 80)
print(f"\nArchivo: {P}")
print(f"Contenido total extraible: {len(pt)} bytes\n")

# Encontrar todas las secuencias ASCII imprimibles de al menos 4 caracteres
strings_found = []
i = 0
while i < len(pt):
    byte = pt[i]
    
    # Caracteres imprimibles ASCII (espacio a ~)
    if 32 <= byte <= 126:
        start = i
        while i < len(pt) and 32 <= pt[i] <= 126:
            i += 1
        
        text = pt[start:i].decode('ascii', errors='replace')
        
        # Solo registrar strings de al menos 5 caracteres (evitar ruido)
        if len(text) >= 5:
            # Evitar duplicados cercanos
            is_dup = any(abs(start - m['start']) < 40 for m in strings_found[-15:])
            
            if not is_dup:
                strings_found.append({
                    'start': start,
                    'end': i,
                    'text': text[:200],  # Cortar a 200 chars
                    'length': i - start
                })
    else:
        i += 1

# Filtrar solo strings con contenido de texto UI real (no artefactos)
ui_strings = [s for s in strings_found 
              if any(c.isalpha() for c in text) or ' ' in text]

print(f"Total secuencias ASCII: {len(strings_found)}")
print(f"String con contenido legible: {len(ui_strings)}\n")

# Mostrar resultados agrupados por tipo
ui_samples = []
for s in ui_strings[:300]:  # Mostrar primeras 300 muestras
    text_upper = s['text'].upper()
    
    # Categorizar por tipo
    if len(s['text']) > 10 and any(word in text_upper for word in 
                                    ['THE', 'AND', 'OR', 'TO', 'OF', 'IS', 'A', 'IN', 'IT', 'HE', 'SHE',
                                     'PLAYER', 'GAME', 'WORLD', 'AREA', 'MAP', 'LEVEL', 'MISSION']):
        category = "NARRATION/TEXT"
    elif len(s['text']) > 20:
        category = "LONG TEXT"
    elif s['length'] < 30:
        category = "SHORT TEXT/DIALOGUE"
    else:
        category = "MEDIUM TEXT"
    
    # Extraer contexto (bytes antes y después)
    before = pt[max(0, s['start']-20):s['start']].decode('ascii', errors='replace').strip()
    after = pt[s['end']:min(len(pt), s['end']+15)].decode('ascii', errors='replace').strip()
    
    ui_samples.append({
        'category': category,
        'start': s['start'],
        'hex_start': f"{s['start']:04x}",
        'context_before': before,
        'text': s['text'],
        'context_after': after,
        'length': s['length']
    })

# Mostrar resultados
print(f"{'='*80}")
print("MUESTRAS DE STRINGS UI (primeras 300):")
print(f"{'='*80}\n")

for item in sorted(ui_samples, key=lambda x: x['category']):
    if not item.get('text'):
        continue
    
    marker = "[UI TEXT] " if len(item.get('text', '')) >= 10 else ""
    hex_pos = f"@{item['hex_start']}:"
    
    # Mostrar con contexto limitado para evitar saturación
    display_text = item['text'][:80].replace('\n', '\\n')
    
    print(f"{marker}{display_text}")
    print("-" * 60)

# Contar por categoría
category_counts = {}
for s in ui_samples:
    cat = s.get('category', 'UNKNOWN')
    category_counts[cat] = category_counts.get(cat, 0) + 1

print(f"\n{'='*80}")
print("RESUMEN POR CATEGORÍA:")
print(f"{'='*80}\n")

for cat, count in sorted(category_counts.items()):
    print(f"{cat:30s}: {count}")
