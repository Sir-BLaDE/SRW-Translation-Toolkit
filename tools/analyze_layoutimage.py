#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analizar estructura de LayoutImage.cpk para identificar texturas OP_PC y CMN00.
"""

import os, struct, zlib

input_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutImage.cpk'

print("=== ANALIZANDO LayoutImage.cpk ===\n")

try:
    with open(input_path, 'rb') as f:
        data = f.read()
    
    # Header
    header_bytes = data[:4]
    
    original_len = len(data)
    print(f"Longitud total: {original_len:,} bytes ({original_len / 1024:.1f} KB)")
    print(f"Header: {data[:4].decode('ascii', errors='replace')}")
    \n
    
    # Buscar texturas con nombres conocidos (OP_PC, CMN00)
    keywords = [
        b'OP_PC_titles',
        b'CMN00_PC_rows',
        b'OP_1st_place',
        b'OP_backstage_pass',
        b'title_bg_op'
    ]
    
    print("\n=== BUSCANDO TEXTURAS CONOCIDAS ===")
    for kw in keywords:
        pos = data.find(kw)
        if pos != -1:
            # Leer contexto
            start = max(0, pos - 40)
            end = min(len(data), pos + len(kw) + 60)
            context = data[start:end]
            try:
                preview = context.decode('utf-8', errors='replace')
                print(f"\n✓ ENCONTRADO '{kw.decode()}' @ offset {pos}")
                print(f"  Contexto (limpio): ...{preview.strip()[:200]}...")
            except Exception as e:
                print(f"\n✗ '{kw.decode()}' - Error decodificando")
                print(f"  Bytes brutos: {data[pos:pos+50].hex()}")
        else:
            print(f"\n✗ NO ENCONTRADO: {kw.decode()!r}")
    
    # También buscar patrones binarios (texturas ZIP/S3TC)
    print("\n=== BUSCANDO PATRONES DE TEXTURA ===")
    s3tc_pattern = b'\x05\x49'  # Patrón típico de texturas S3TC/DXT5
    
    count = 0
    pos = 0
    while (pos := data.find(s3tc_pattern, pos)) != -1:
        # Leer posible header ZIP alrededor
        try:
            zip_start = pos - 8
            if zip_start >= 0 and len(data) > zip_start + 40:
                header_bytes = data[zip_start:zip_start+40]
                header_preview = header_bytes[:30].decode('utf-8', errors='replace')
                
                # Verificar si parece inicio de ZIP o datos comprimidos
                if b'PK\x03' in header_bytes or len(set(header_bytes)) < 20:
                    print(f"✓ Posible textura comprimida @ offset {zip_start}")
                    count += 1
                    if count >= 5:
                        break  # Limite para no saturar consola
        
        except:
            pass
        
        pos += 4
    
    print(f"\nTotal patrones S3TC encontrados: ~{count}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== PRÓXIMOS PASOS ===")
print("1. Identificar texturas OP_PC y CMN00 por posición")
print("2. Preparar versiones acortadas con texto español")
print("3. Validar flags DDS (0x2100f)")
