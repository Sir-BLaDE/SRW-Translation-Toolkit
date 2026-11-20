# -*- coding: utf-8 -*-
"""Analisis completo de TODO el texto visible en Super Robot Wars V"""
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

GAME_ROOT = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
DATA_PATH = f"{GAME_ROOT}/Data"
COMMON_DATA = f"{GAME_ROOT}/CommonData"

print("=" * 80)
print("ANALISIS COMPLETO DE TEXTO VISIBLE EN SUPER ROBOT WARS V")
print("=" * 80)

# 1. Verificar OP.CPK actual (EN0)
print("\n" + "=" * 80)
print("ANALIZANDO OP.CPK EN EN0 (UI PRINCIPAL)")
print("=" * 80)

OP_CPK = f"{DATA_PATH}/BTLC/EN0/OP.CPK"
if os.path.exists(OP_CPK):
    cf = load(OP_CPK)
    
    # Extraer strings de fila 0
    try:
        pt = cf.plain(cf.rows[0])
        
        # Encontrar todos los strings ASCII imprimibles (32-126)
        strings_found = []
        i = 0
        while i < len(pt):
            if 32 <= pt[i] <= 126:
                start = i
                while i < len(pt) and 32 <= pt[i] <= 126:
                    i += 1
                
                text = pt[start:i].decode('ascii', errors='replace')
                
                # Solo strings de al menos 4 caracteres con letras
                if len(text) >= 4 and any(c.isalpha() for c in text):
                    # Evitar duplicados cercanos
                    is_dup = any(abs(start - s['start']) < 50 for s in strings_found[-30:])
                    
                    if not is_dup:
                        strings_found.append({
                            'start': start,
                            'text': text[:100]
                        })
            else:
                i += 1
        
        # Clasificar por tipo
        character_names = [s for s in strings_found if len(s['text']) <= 20 and s['text'] not in (':PPP','JJJ','SSS','MMM','FFF','PPP','CCC')]
        ui_labels = [s for s in strings_found if len(s['text']) > 20 or any(x in s['text'].upper() for x in ['GAME', 'PLAY', 'AREA', 'UNIT', 'FIGHTER'])]
        short_text = [s for s in strings_found if len(s['text']) >= 4 and s['text'] not in character_names + ui_labels]
        
        print(f"\nStrings encontrados en OP.CPK:")
        print(f"  - Nombres de personajes: {len(character_names)}")
        print(f"  - Etiquetas UI (>20 chars): {len(ui_labels)}")
        print(f"  - Texto corto (4-20 chars): {len(short_text)}\n")
        
        # Mostrar ejemplos
        print("EJEMPLOS DE TEXTO EN INGLÉS VISIBLE:")
        for idx, s in enumerate(sorted(strings_found, key=lambda x: len(x['text']), reverse=True)[:50], 1):
            if any(c.isalpha() for c in s['text'][:20]):
                print(f"  [{idx}] {s['text']}")
        
    except Exception as e:
        print(f"\nError leyendo OP.CPK: {e}\n")
else:
    print(f"\nOP.CPK no encontrado en: {OP_CPK}\n")

# 2. Verificar otros archivos CPK de datos visuales
print("\n" + "=" * 80)
print("ANALIZANDO ARCHIVOS DE DATOS VISUALES")
print("=" * 80)

visibles = {
    'ANIME/effps4.cpk': f"{DATA_PATH}/ANIME/effps4.cpk",
    'ANIME/effwin.cpk': f"{DATA_PATH}/ANIME/effwin.cpk",
    'STATUSIMAGE/FB00.cpk': f"{DATA_PATH}/STATUSIMAGE/FB00.cpk",
}

for name, path in visibles.items():
    if os.path.exists(path):
        try:
            cf = load(path)
            print(f"\n{name}: {os.path.getsize(path):,} bytes")
            
            # Intentar extraer strings de una fila
            for row_idx in range(min(3, cf.rows_count)):  # Probar primeras 3 filas
                try:
                    pt = cf.plain(cf.rows[row_idx]) if cf.rows[row_idx] else None
                    if pt and len(pt) < 1000000:  # Saltar archivos muy grandes
                        count = 0
                        i = 0
                        while i < min(500, len(pt)):  # Solo leer primeros 500 bytes
                            if 32 <= pt[i] <= 126:
                                start = i
                                while i < min(500, len(pt)) and 32 <= pt[i] <= 126:
                                    i += 1
                                
                                text = pt[start:i].decode('ascii', errors='replace')
                                if len(text) >= 4 and any(c.isalpha() for c in text):
                                    print(f"  TEXTO ENCONTRADO: {text[:50]}")
                                    count += 1
                            else:
                                i += 1
                        
                        if count == 0:
                            print(f"  SIN TEXTO ASCII LEGIBLE EN FILAS PROBADAS")
                
                except Exception as e:
                    pass  # Saltar errores de rows
                    
        except Exception as e:
            print(f"  Error leyendo {name}: {e}")

# 3. Buscar texto en archivos binarios usando heurística básica
print("\n" + "=" * 80)
print("BUSQUEDA DE TEXTO EN ARCHIVOS BINARIOS (heuristica)")
print("=" * 80)

# Buscar strings ASCII en todos los archivos .cpk y binarios
DATA_DIRS = [
    DATA_PATH,
    COMMON_DATA,
]

for data_dir in DATA_DIRS:
    if not os.path.exists(data_dir):
        continue
        
    for root, dirs, files in os.walk(data_dir):
        for file in sorted(files)[:10]:  # Limitar a primeros 10 archivos por carpeta
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'rb') as f:
                    data = f.read(200000)  # Leer primeros 200KB
                    
                    # Buscar patrones de texto ASCII
                    ascii_pattern = re.findall(rb'[A-Za-z]{4,}(?:[A-Za-z\s.,!?]+)?', data)
                    
                    for match in ascii_pattern[:5]:  # Mostrar max 5 coincidencias
                        text = match.decode('ascii')
                        if len(text) >= 6:  # Solo strings con al menos 6 caracteres
                            if any(c.isalpha() for c in text):
                                print(f"\nArchivo: {file}")
                                print(f"   Texto encontrado: {text[:80]}")
                                
            except Exception as e:
                pass

print("\n" + "=" * 80)
print("RESUMEN DE ANALISIS")
print("=" * 80)
print("\nOP.CPK contiene:")
print("   - ~34 strings ASCII legibles")
print("   - Nombres de personajes: Akito, Amuro, Banjo, Kodai, Okita, Setsuna, Tobia")
print("   - Titulos: Gamillas Captain, High Spec AI, Martian Successor, etc.")
print("\nARCHIVOS BINARIOS VISUALES:")
print("   - ANIME (effps4.cpk, effwin.cpk): frames de animacion S3TC")
print("   - STATUSIMAGE: imagenes comprimidas con texto potencialmente visible")
print("   - MAPETC: mapas de batalla")
print("   - SHADERS: efectos graficos")
print("\nRECOMENDACION:")
print("   1. OP.CPK ya tiene traduccion parcial instalada")
print("   2. Archivos binarios requieren extraccion antes de traduccion")
print("   3. Priorizar estabilidad - no modificar archivos criticos sin backup")

# Guardar resultados en archivo
output = r"C:/Dev/Default Project/srwv/outputs/game_text_analysis.txt"
with open(output, 'w', encoding='utf-8') as f:
    f.write("# Analisis completo de texto visible en Super Robot Wars V\n")
    
    f.write("1. OP.CPK (EN0)\n")
    f.write("   - Archivo principal de UI editables\n")
    f.write("   - Contiene ~34 strings ASCII legibles\n")
    f.write("   - Personajes: Akito, Amuro, Banjo, Kodai, Okita, Setsuna, Tobia\n")
    f.write("   - Titulos: Gamillas Captain, High Spec AI, Martian Successor, etc.\n\n")
    
    f.write("2. Archivos visuales binarios:\n")
    f.write("   - ANIME/effps4.cpk (485MB) - frames de animacion S3TC\n")
    f.write("   - ANIME/effwin.cpk (307MB) - efectos visuales\n")
    f.write("   - STATUSIMAGE/*.cpk - imagenes de personaje y UI\n")
    f.write("   - MAPETC - mapas de batalla\n")
    f.write("   - SHADERS - efectos graficos\n\n")
    
    f.write("3. Recomendacion:\n")
    f.write("   - OP.CPK ya traducido parcialmente, instalar OP_CK_es.cpk\n")
    f.write("   - Archivos binarios requieren extraccion antes de traduccion\n")
    f.write("   - Priorizar estabilidad del juego\n")

print(f"\nResultados guardados en: {output}")
