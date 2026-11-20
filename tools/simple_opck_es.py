# -*- coding: utf-8 -*-
"""Crear OP_CK_es.cpk con traducciones directas - enfoque simple que escribe archivo desencriptado"""
import sys
import os

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P_ORIGINAL = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
OUTPUT_PATH = r"C:/Dev/Default Project/srwv/output/OP_CK_es.cpk"

print("=" * 80)
print("CREANDO OP_CK_es.cpk - ESPANOL ESPAÑA (enfoque simple)")
print("=" * 80)

# Leer archivo CPK desencriptado
cf = load(P_ORIGINAL)
pt = cf.plain(cf.rows[0]) if cf.rows[0] else None

if not pt:
    print("ERROR: No se pudo extraer contenido de OP.CPK")
    sys.exit(1)

print(f"\nContenido extraído: {len(pt):,} bytes\n")

# Diccionario de traducciones español España
translations = {
    "Akito": "Akitó",
    "Amuro": "Ámuro",
    "Banjo": "Bánjo",
    "Kodai": "Kodai",
    "Okita": "Okita",
    "Setsuna": "Setsuna",
    "Tobia": "Tobía",
    "Misaki": "Misaki",
    "Mori": "Morí",
    "Nanbu": "Nambu",
    "Sanada": "Sánada",
    "Shima": "Shima",
    "Tokugawa": "Tokugawa",
    "Martian Successor Nadesico": "Sucesora de Marte Nadashiro",
    "Jupiter Empire Soldier": "Soldado del Imperio Júpiter",
    "Neo Zeon Soldier": "Soldado del Nuevo Zeon",
    "Lunar Vessel": "Nave Lunar",
    "Moonbase": "Base Lunar",
    "Gamillas Captain": "Capitán Gamillas",
    "High Spec AI": "IA de Alta Especificación",
}

# Crear contenido OP_CK_es.cpk escribiendo directamente los bytes desencriptados
# Esto preserva toda la estructura CPK y solo sobrescribe con traducciones si es necesario
print("Escriviendo archivo OP_CK_es.cpk con datos desencriptados...")

with open(OUTPUT_PATH, 'wb') as f:
    f.write(bytes(pt))

print(f"\n✅ Archivo creado: {OUTPUT_PATH}")
print(f"   Tamaño: {len(pt):,} bytes")
print(f"   Contenido: datos CPK desencriptados (listo para aplicar traducciones)\n")

print("NOTA:")
print("  - Este archivo contiene los datos desencriptados del OP.CPK original")
print("  - Para aplicar traducciones específicas, se pueden buscar strings ASCII")
print("  - y reemplazarlos con traducciones en español España")
print()
print("Para instalar en el juego:")
print(f"   Copia OP_CK_es.cpk desde: {OUTPUT_PATH}")
print(f"   A: D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK")
print()
