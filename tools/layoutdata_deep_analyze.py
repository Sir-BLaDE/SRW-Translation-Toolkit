#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analizar profundamente LayoutData.cpk - formato CPK real."""

import os
import re

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'

with open(INPUT_CPK, 'rb') as f:
    data = f.read()

print("Archivo total: " + str(len(data)) + " bytes")
print("Header (16 bytes): " + repr(data[:16]))
print("  Hex: " + data[:16].hex())

# Buscar cadenas de texto legibles buscando patrones comunes
pattern = rb'["\x27][^\x00\x27"\x5c]{1,80}["\x27]'
matches = list(re.finditer(pattern, data))

print("\nEncontradas " + str(len(matches)) + " coincidencias de cadenas")

# Mostrar las primeras 30 coincidencias
for i, match in enumerate(matches[:30]):
    text_bytes = match.group()
    try:
        text = text_bytes.decode('utf-8')
        text_preview = text[:60] if len(text) > 60 else text
        print(str(i+1).rjust(2) + ". '" + str(match.start()).rjust(5) + ": " + text_preview + "... (len=" + str(len(text)) + ")")
    except:
        print(str(i+1).rjust(2) + ". '" + str(match.start()).rjust(5) + ": <binary/corrupt>... (len=" + str(len(text_bytes)) + ")")
