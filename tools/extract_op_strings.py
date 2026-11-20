# -*- coding: utf-8 -*-
"""Extraer todos los strings ASCII legibles de OP.CPK EN0 para traducción"""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
pt = cf.plain(cf.rows[0])  # Extraer contenido descifrado de fila 0

print(f"Archivo: {P}")
print(f"Contenido total extraible: {len(pt):,} bytes\n")

# Encontrar todos los strings ASCII imprimibles (bytes 32-126)
i = 0
strings = []
while i < len(pt):
    if 32 <= pt[i] <= 126:
        start = i
        while i < len(pt) and 32 <= pt[i] <= 126:
            i += 1
        text = pt[start:i].decode('ascii', errors='replace')
        # Solo strings de al menos 4 caracteres
        if len(text) >= 4:
            strings.append({
                'start': start,
                'text': text[:200]  # Cortar a 200 chars máximo
            })
    else:
        i += 1

# Evitar duplicados cercanos (mismas ~30 bytes)
unique_strings = []
for s in strings:
    is_dup = any(abs(s['start'] - u['start']) < 30 for u in unique_strings[-10:])
    if not is_dup:
        unique_strings.append(s)

print(f"Total strings ASCII encontrados: {len(unique_strings)}")

# Categorizar por tipo
categorized = {'text': [], 'short': [], 'artifact': []}

for s in unique_strings:
    text = s['text'].upper()
    
    # Artefactos comunes de compresión (saltarlos)
    if re.match(r'^[A-Z]{3}$', text):  # PPP, CCC, FFF, etc.
        categorized['artifact'].append(s)
        continue
    
    # Patrones binarios/artefactos (saltarlos)
    if any(c in text for c in ['`', '@', '[', ']', '\\']):
        categorized['artifact'].append(s)
        continue
    
    # Texto real con letras y espacios
    if re.search(r'[A-Za-z]{2,}.*[A-Za-z ]', text):
        if len(text) > 30:
            categorized['text'].append(s)
        else:
            categorized['short'].append(s)

print(f"  - Texto largo (>30 chars): {len(categorized['text'])}")
print(f"  - Corto/etiqueta (2-30 chars): {len(categorized['short'])}")
print(f"  - Artefactos binarios: {len(categorized['artifact'])}\n")

# Mostrar todos los strings de texto real únicos ordenados alfabéticamente
text_dict = {}
for s in categorized['text'] + categorized['short']:
    text_lower = s['text'].lower().strip()
    if text_lower and not text_lower.startswith(('!', '+', '.', '>', '=', '\\')):
        # Solo incluir strings con contenido relevante
        if any(c.isalpha() for c in s['text']):
            if text_lower not in text_dict:
                text_dict[text_lower] = s

print(f"{'='*80}")
print("LISTADO COMPLETO DE STRINGS UI POR TRADUCIR:")
print("=" * 80)

# Ordenar strings por longitud descendente (strings largos primero)
sorted_strings = sorted(text_dict.values(), key=lambda x: len(x['text']), reverse=True)

for idx, s in enumerate(sorted_strings[:500], 1):  # Mostrar primeros 500
    marker = "[LONG] " if len(s['text']) > 30 else "[SHORT]"
    text_preview = s['text'][:80].replace('\n', '\\n').replace('\r', '\\r')
    
    print(f"{marker} [{idx:4d}] {len(s['text']):3d} bytes @ 0x{s['start']:04x}")
    print(f"      \\\"{text_preview}\\\"")

print(f"\n{'='*80}")
print(f"Total strings UI a traducir: {len(text_dict)}")
print("=" * 80)

# Guardar en archivo para traducción posterior
output = r"C:/Dev/Default Project/srwv/outputs/op_strings_to_translate.txt"
with open(output, 'w', encoding='utf-8') as f:
    f.write("# OP.CPK strings a traducir - Extraído de BTLC\\EN0\\OP.CPK\n")
    f.write("# Formato: ORIGIN_ENGLISH\n")
    f.write("#\n")
    
    for idx, s in enumerate(sorted_strings[:200], 1):  # Guardar primeros 200 para empezar
        text_preview = s['text'][:80]
        line = f"{idx}: {text_preview}\n"
        f.write(line)

print(f"\nStrings guardados en: {output}")
print("Listo para traducir a español España!")
