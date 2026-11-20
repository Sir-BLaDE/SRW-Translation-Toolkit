#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analizar contenido de LayoutData.cpk para entender formato real."""

import os, struct

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'

print(f"Analizando {INPUT_CPK}...")

with open(INPUT_CPK, 'rb') as f:
    data = f.read()

# Mostrar header
print(f"\nHeader (4 bytes): {data[:4]}")
print(f"  Hex: {data[:4].hex()}")

# Contar entradas string 8-bit simples (header 2-byte + 1-byte type + ref + texto)
offset = 0
entry_count = 0
string_count = 0

while offset < len(data):
    # Intentar leer header de string 8-bit
    try:
        length = struct.unpack('>H', data[offset:offset+2])[0]
    except:
        break
    
    if length == 0 and offset >= 10000:
        break
    
    entry_count += 1
    
    # Calcular posición del texto
    text_offset = offset + 4
    end_offset = min(text_offset + length, len(data))
    
    try:
        text_bytes = data[text_offset:end_offset]
        text = text_bytes.decode('utf-8', errors='replace')
        
        # Filtrar strings legibles (no corruptos)
        if text.strip() and not any(c in text for c in ['~','^`?+\n\x00']):
            string_count += 1
            
            # Mostrar cadenas cortas (< 50 chars) - probablemente texto UI real
            if len(text) < 50:
                print(f"Entry {entry_count:4d} (@{offset:7d}): '{text[:60]}...' (len={len(text)})")
                
    except Exception as e:
        pass
    
    offset += max(length, 8)

print(f"\nTotal entries procesadas: {entry_count}")
print(f"Total strings legibles cortos: {string_count}")
