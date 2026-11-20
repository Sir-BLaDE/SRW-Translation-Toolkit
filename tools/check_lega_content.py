#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificar contenido real de lega_zkn.cpk EN vs JPN."""

import os, re

jpn_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/JPN/lega_zkn.cpk'
en_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk'

print("=== LEGA_ZKN.JPN (original) ===")
try:
    with open(jpn_path, 'rb') as f:
        jpn_data = f.read()
    
    # Buscar texto ASCII imprimible
    ascii_pattern = rb'[a-zA-Z\s!.,-]{1,60}'
    matches = list(re.finditer(ascii_pattern, jpn_data))
    
    print("Encontradas", len(matches), "coincidencias ASCII")
    
    # Mostrar primeras coincidencias que parezcan ser texto de anime
    for i, match in enumerate(matches[:20]):
        text_bytes = match.group()
        try:
            text = text_bytes.decode('ascii')
            if any(kw in text for kw in ['Metal Panic', 'EVANGELION', 'Full Metal']):
                preview = text[:60]
                print("MATCH " + str(i).rjust(2) + ": '" + preview.replace('\n', '\\n').replace('\r', '\\r') + "')")
        except:
            pass
            
except Exception as e:
    print("ERROR leyendo JPN:", str(e))

print("\n=== LEGA_ZKN.EN (actual) ===")
try:
    with open(en_path, 'rb') as f:
        en_data = f.read()
    
    ascii_pattern = rb'[a-zA-Z\s!.,-]{1,60}'
    matches = list(re.finditer(ascii_pattern, en_data))
    
    print("Encontradas", len(matches), "coincidencias ASCII")
    
    # Mostrar primeras coincidencias
    for i, match in enumerate(matches[:20]):
        text_bytes = match.group()
        try:
            text = text_bytes.decode('ascii')
            preview = text[:60]
            if len(text.strip()) > 3 and not text.startswith('CPK'):
                print("MATCH " + str(i).rjust(2) + ": '" + preview.replace('\n', '\\n').replace('\r', '\\r') + "')")
        except:
            pass
            
except Exception as e:
    print("ERROR leyendo EN:", str(e))
