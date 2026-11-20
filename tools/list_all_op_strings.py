# -*- coding: utf-8 -*-
"""Listar todos los strings de interfaz de usuario en OP.CPK con estructura correcta."""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from srwv_cpk import Cpk

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"

print(f"=== ANALISIS DE {P} ===\n")

c = Cpk(P)

# Obtener lista de todos los archivos
files = c.file_list()
print(f"Total archivos en ITOC: {len(files)}\n")

# Mostrar estadísticas por tipo
l_count = sum(1 for f in files if f['table'] == 'L')
h_count = sum(1 for f in files if f['table'] == 'H')
print(f"  Filas L: {l_count}")
print(f"  Filas H: {h_count}\n")

# Extraer y mostrar strings ASCII de todos los archivos
all_strings = []

for f in sorted(files, key=lambda x: x['id'])[:10]:  # Procesar primeros 10 archivos como muestra
    print(f"=== ARCHIVO ID={f['id']}: Size={f['size']} ExtractSize={f['extract_size']} ===")
    
    try:
        # Leer archivo raw
        raw = c.read_file(f['id'])
        
        # Decodificar (si está cifrado)
        if raw[:8] in (b"\x9c" + b"S\x96\xb4\x07\xf1\xbf+\xc2", b"\xf3K\xc5\xd2\xcbYH"):  # Magic bytes Blowfish
            print(f"    Este archivo está cifrado, no procesaré strings ASCII")
            continue
        
        # Extraer strings ASCII imprimibles (caracteres espacio a tilde ~)
        i = 0
        while i < len(raw):
            if 32 <= raw[i] <= 126:
                start = i
                while i < len(raw) and 32 <= raw[i] <= 126:
                    i += 1
                
                text = raw[start:i].decode('ascii', errors='replace')
                
                # Solo registrar strings de al menos 5 caracteres (evitar ruido)
                if len(text) >= 5 and any(c.isalpha() for c in text):
                    all_strings.append({
                        'file_id': f['id'],
                        'start': start,
                        'text': text[:100]  # Cortar a 100 chars para evitar saturación
                    })
            else:
                i += 1
    
    except Exception as e:
        print(f"    Error procesando: {e}\n")

# Mostrar resultados únicos agrupados por frecuencia
seen = {}
for s in all_strings:
    seen.setdefault(s['text'], []).append({
        'file_id': s['file_id'],
        'start': s['start']
    })

unique_strings = sorted(seen.items(), key=lambda x: len(x[1]), reverse=True)

print(f"\n{'='*80}")
print("STRINGS ASCII ENCONTRADOS ÚNICOS (ordenados por frecuencia):")
print(f"{'='*80}\n")

for text, occurrences in unique_strings[:50]:  # Mostrar primeras 50 únicas
    freq = len(occurrences)
    
    # Saltar artefactos y patrones de compresión comunes
    if re.match(r'^[A-Z]{3}$', text):  # PPP, CCC, etc.
        continue
    
    marker = " [REPETED x{}]".format(freq) if freq > 1 else ""
    
    print(f"{marker} \\\"{text}\\\"")

print(f"\n{'='*80}")
print(f"Total strings únicas con contenido significativo: {len(unique_strings)}")
print(f"Total apariciones de strings: {sum(len(v) for k, v in unique_strings)}")
print(f"{'='*80}\n")
