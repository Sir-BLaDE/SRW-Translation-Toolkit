# -*- coding: utf-8 -*-
"""Script simple para encontrar texturas en LayoutImage.cpk"""

input_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutImage.cpk'

print("=== ANALIZANDO LayoutImage.cpk ===\n")

try:
    with open(input_path, 'rb') as f:
        data = f.read()
    
    original_len = len(data)
    print(f"Longitud total: {original_len:,} bytes")
    print(f"Header (4 bytes): {data[:4]}")
    
    # Buscar texturas conocidas
    keywords = [
        b'OP_PC_titles',
        b'CMN00_PC_rows', 
        b'OP_1st_place',
        b'title_bg_op'
    ]
    
    print("\n=== BUSQUEDA DE TEXTURAS ===")
    for kw in keywords:
        pos = data.find(kw)
        if pos != -1:
            start = max(0, pos - 40)
            end = min(len(data), pos + len(kw) + 60)
            context = data[start:end]
            try:
                preview = context.decode('utf-8', errors='replace')
                print(f"\n[OK] '{kw.decode()}' @ offset {pos}")
                clean_text = ' '.join(filter(lambda c: c.isalnum() or c in ' ._:-@#()', preview.strip()))
                print(f"      Contexto: ...{clean_text[:150]}...")
            except Exception as e:
                print(f"\n[ERROR] '{kw.decode()}' - Decodificacion fallida: {str(e)}")
        else:
            print(f"[NO ENCONTRADO] {kw}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
