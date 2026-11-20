#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Búsqueda simple de strings en CPK."""

import os

en_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk'
jpn_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/JPN/lega_zkn.cpk'

print("=== BUSQUEDA EN ARCHIVO EN ===")
try:
    with open(en_path, 'rb') as f:
        data = f.read()
    
    # Buscar keywords específicas (strings ASCII exactos)
    keywords = [
        b'Full Metal Panic',
        b'The Second Raid', 
        b'EVANGELION',
        b'Rebuild of'
    ]
    
    for kw in keywords:
        pos = data.find(kw)
        if pos != -1:
            # Leer contexto alrededor
            start = max(0, pos - 50)
            end = min(len(data), pos + len(kw) + 50)
            context = data[start:end]
            try:
                preview = context.decode('utf-8', errors='replace')
                print("ENCONTRADO '" + kw.decode() + "' @ offset " + str(pos))
                print("  Contexto: [" + preview[:150] + "...]")
            except:
                print("  Contexto binario")
        else:
            print("NO ENCONTRADO '" + str(kw) + "'")
            
except Exception as e:
    print("ERROR:", str(e))

print("\n=== COMPARISON JPN vs EN ===")
try:
    with open(jpn_path, 'rb') as f:
        jpn_data = f.read()
    
    for kw in keywords:
        en_pos = data.find(kw) if 'data' in locals() else -1
        jpn_pos = jpn_data.find(kw)
        
        print("Keyword: '" + str(kw[:50]) + "'")
        print("  EN offset: " + str(en_pos))
        print("  JPN offset: " + str(jpn_pos))
        
except Exception as e:
    print("ERROR:", str(e))
