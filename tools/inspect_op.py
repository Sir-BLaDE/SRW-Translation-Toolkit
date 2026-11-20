# -*- coding: utf-8 -*-
"""Inspeccionar estructura de OP.CPK"""
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from srwv_cpk import Cpk

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
print(f"=== ANALISIS DE {P} ===\n")

c = Cpk(P)

print("HEADER:")
print(f"  rows_count: {c.header.rows_count}")
print(f"  content_offset: {hex(c.content_offset)}\n")

if c.itoc_offset:
    print(f"ITOC encontrado @ offset {hex(c.itoc_offset)}\n")
    
    info = c.itoc_info
    
    if 'CpkItocL' in info and 'CpkItocH' in info:
        rows_l_count = info['CpkItocL'].rows_count
        rows_h_count = info['CpkItocH'].rows_count
        print(f"CpkItocL: {rows_l_count} filas")
        print(f"CpkItocH: {rows_h_count} filas\n")
        
        # Obtener todas las entradas de la tabla ITOC
        all_rows = []
        
        if rows_l_count > 0:
            print("Obteniendo filas L...")
            for r in range(rows_l_count):
                row_data = c.itoc['CpkItocL'].row(r)
                all_rows.append({
                    'id': row_data['ID'],
                    'size': row_data['FileSize'],
                    'ex': row_data['ExtractSize'],
                    'table': 'L',
                    'row': r
                })
        
        if rows_h_count > 0:
            print("Obteniendo filas H...")
            for r in range(rows_h_count):
                row_data = c.itoc['CpkItocH'].row(r)
                all_rows.append({
                    'id': row_data['ID'],
                    'size': row_data['FileSize'],
                    'ex': row_data['ExtractSize'],
                    'table': 'H',
                    'row': r
                })
        
        # Ordenar por ID para ver la estructura real
        all_rows.sort(key=lambda x: x['id'])
        
        print(f"\n=== ENTRADAS ITOC ORDENADAS (primeras 50) ===\n")
        for item in all_rows[:50]:
            marker = "[L]" if item['table'] == 'L' else "[H]"
            print(f"{marker} ID={item['id']:4d} Size={item['size']:6d} ExtractSize={item['ex']:6d}")
        
        # Mostrar estadísticas de IDs
        ids_l = [r['id'] for r in all_rows if r['table'] == 'L']
        ids_h = [r['id'] for r in all_rows if r['table'] == 'H']
        
        print(f"\n=== ESTADÍSTICAS ===")
        print(f"  Filas L: {len(ids_l)} entradas, IDs: {min(ids_l)} - {max(ids_l)}")
        print(f"  Filas H: {len(ids_h)} entradas, IDs: {min(ids_h)} - {max(ids_h)}")
        
else:
    print("No hay ITOC encontrado. Verificando TOC...")

print("\n=== PRIMEROS 10 BYTES DEL HEADER ===")
with open(P, 'rb') as f:
    header_bytes = f.read(32)
    print(f"Header hex: {header_bytes.hex()}")
    print(f"Primeros bytes (ASCII): {header_bytes[:32]}")
