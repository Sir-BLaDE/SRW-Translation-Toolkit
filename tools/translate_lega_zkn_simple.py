#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traducir lega_zkn.cpk buscando y reemplazando cadenas exactas.
Mantiene longitudes para evitar overflow del CPK.
"""

import os, shutil

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/CommonData/MtData/EN/lega_zkn.cpk'
OUTPUT_CPK = 'C:/Dev/Default Project/srwv/outputs/LegaZKN_es.cpk'

# Diccionario de traducciones exactas - formato (texto_iningles: texto_espanol)
# Acortado para mantener longitudes
TRANSLATIONS = {
    # Full Metal Panic! The Second Raid -> ¡Pánico Metálico: Segunda Inv. (acortado)
    'Full Metal Panic! The Second Raid': '¡Pánico Metálico: Segunda Inv.',  # ~41 unicode -> ~37 OK
    
    # Serie Rebuild of EVANGELION -> ya está traducido, mantener igual
    'Serie Rebuild of EVANGELION': 'Serie Rebuild de Evangelion',  # ~37 unicode -> ~36 OK
}

def translate_file(input_path, output_path):
    """Traduce archivo buscando y reemplazando cadenas exactas."""
    
    print("Traduciendo " + input_path + " -> " + output_path)
    
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
        
        # Total original para verificación
        original_len = len(data)
        print("Longitud original del archivo: " + str(original_len) + " bytes")
        
        traducciones_realizadas = 0
        
        for en_text, es_text in TRANSLATIONS.items():
            # Buscar la cadena en inglés
            en_bytes = en_text.encode('utf-8')
            es_bytes = es_text.encode('utf-8')
            
            if len(es_bytes) > len(en_bytes):
                print("  ⚠ Advertencia: traducción '" + es_text + "' más larga que original")
            
            # Buscar posición de la cadena en inglés
            pos = data.find(en_bytes)
            
            if pos != -1:
                # Encontrado - reemplazar si longitud permite
                if len(es_bytes) <= len(en_bytes):
                    # Reemplazar con acortamiento seguro
                    old_len = len(en_bytes)
                    new_len = len(es_bytes)
                    
                    # Mantener espacios alrededor (bytes antes y después)
                    space_before = 10
                    space_after = 5
                    total_old_space = space_before + space_after
                    
                    if original_len - pos >= old_len + total_old_space:
                        data[pos:pos+old_len] = es_bytes
                        
                        # Ajustar espacio (opcional - mantener padding)
                        data[pos+old_len:pos+old_len+total_old_space] = b'\x04' * total_old_space
                        
                        traducciones_realizadas += 1
                        print("  Traducido: '" + en_text + "' -> '" + es_text + "' @ offset " + str(pos))
                    else:
                        print("  ⚠ No hay suficiente espacio para reemplazar completo")
                        
                elif len(es_bytes) <= old_len:  # Verificación de longitud
                    data[pos:pos+old_len] = es_bytes
                    traducciones_realizadas += 1
                    print("  Traducido: '" + en_text + "' -> '" + es_text + "' @ offset " + str(pos))
            else:
                print("  NO ENCONTRADO: '" + en_text + "'")
        
        # Escribir archivo traducido
        with open(output_path, 'wb') as f:
            f.write(data)
            
        print("\n✓ Traducción completa: " + str(traducciones_realizadas) + " traducciones realizadas")
        print("Longitud resultado: " + str(len(data)) + " bytes (original: " + str(original_len) + ")")
        
        return True
        
    except Exception as e:
        print("ERROR: " + str(e))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = translate_file(INPUT_CPK, OUTPUT_CPK)
    
    if result:
        # Preguntar si instalar
        try:
            install_now = input("\n¿Instalar en el juego ahora? (s/n): ").strip().lower()
            if install_now == 's':
                target_dir = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/CommonData/MtData'
                target_path = os.path.join(target_dir, 'lega_zkn.cpk')
                
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                shutil.copy(OUTPUT_CPK, target_path)
                print("✓ Instalado en " + target_path)
            else:
                print("No instalado. Mover manualmente si lo deseas.")
        except Exception as e:
            print("Omitiendo instalación: " + str(e))
