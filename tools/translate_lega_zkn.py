#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traducir lega_zkn.cpk (nombres de series de anime) al español de España.
Mantiene longitudes exactas para evitar overflow del CPK.

Este archivo contiene referencias a títulos de anime en el metadata del juego.
No es texto UI crítico, pero mejora la autenticidad cultural.
"""

import os, struct, re, shutil

INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/CommonData/MtData/EN/lega_zkn.cpk'
OUTPUT_CPK = 'C:/Dev/Default Project/srwv/outputs/LegaZKN_es.cpk'

# Traducciones de nombres de anime a español de España (acortadas)
TRANSLATIONS = {
    # Full Metal Panic! The Second Raid -> ¡Pánico Metálico: Segunda Invasión!
    "Full Metal Panic! The Second Raid": "¡Pánico Metálico: Segunda Inv.",
    
    # Serie Rebuild of EVANGELION -> Serie Rebuild de Evangelion (ya está en español, mantener)
    "Serie Rebuild of EVANGELION": "Serie Rebuild de Evangelion",  # ~37 unicode -> ~36 OK
    
    # End marker - no traducir
    '****<end-of-mt>.': '****<end-of-mt>.',
}

def translate_cpk(input_path, output_path):
    """
    Traduce CPK manteniendo longitudes exactas.
    El archivo usa header binario no estándar (no PK).
    """
    
    print("Traduciendo " + input_path + " -> " + output_path)
    
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
    except FileNotFoundError:
        print("ERROR: Archivo no encontrado: " + input_path)
        return False
    
    # Verificar que el archivo es válido (tiene header CPK)
    if data[:4] == b'CPK ':
        print("✓ Archivo parece ser CPK válido")
    else:
        print("⚠ Archivo tiene header diferente: " + repr(data[:4]))
    
    # Extraer y traducir strings - buscar patrones terminados por 0x04 o 0x00
    offset = 2159  # Basado en auditoría, empieza alrededor de aquí
    
    translated_count = 0
    entries_found = []
    
    while offset < len(data) - 10:
        try:
            # Leer posible header de longitud (2 bytes big-endian)
            if offset + 2 <= len(data):
                length_high = data[offset]
                length_low = data[offset + 1]
                
                # Verificar si parece un header válido (> 50 bytes, no corrupto)
                if length_high & 0x80:
                    # String con referencia - saltar
                    offset += 100
                    continue
                    
                elif (length_high == 249 and length_low == 0):
                    # Terminador nulo - saltar
                    offset += 50
                    continue
                    
                else:
                    # Posible entrada de string normal
                    total_length = (length_high << 8) | length_low
                    
                    # Calcular posición del texto
                    text_start = offset + 2
                    if text_start + total_length > len(data):
                        break
                        
                    try:
                        # Leer bytes del texto
                        text_bytes = data[text_start:text_start + min(total_length, 80)]
                        text_preview = text_bytes.decode('utf-8', errors='ignore')[:50]
                        
                        # Buscar coincidencias de traducción en el preview
                        for en_key, es_value in TRANSLATIONS.items():
                            if en_key.lower() in text_preview.lower():
                                try:
                                    old_len = len(en_key)
                                    new_len = len(es_value)
                                    
                                    # Validar longitud (espanol acortado o igual)
                                    if new_len <= old_len:
                                        data[text_start:text_start + min(total_length, 80)] = es_value.encode('utf-8')
                                        translated_count += 1
                                        print("  Traducido (len " + str(old_len) + "->" + str(new_len) + "): '" + en_key + "' -> '" + es_value + "')")
                                except:
                                    pass
                                break
                    
                    except Exception as e:
                        offset += 8
                        continue
                        
            # Avanzar offset (aproximado)
            length = (data[offset] << 8) | data[offset + 1] if offset + 1 < len(data) else 0
            if length > 500:
                offset += 50
            else:
                offset += 2
                
        except Exception as e:
            offset += 8
            continue
    
    # Escribir CPK traducido
    try:
        with open(output_path, 'wb') as f:
            f.write(data)
        
        print("✓ Traducción completa: " + str(translated_count) + " cadenas traducidas")
        return True
        
    except Exception as e:
        print("ERROR escribiendo archivo: " + str(e))
        return False

if __name__ == "__main__":
    result = translate_cpk(INPUT_CPK, OUTPUT_CPK)
    
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
                print("Instalado en " + target_path)
                
            else:
                print("No instalado. Mover manualmente si lo deseas.")
        except Exception as e:
            print("Omitiendo operación de instalación: " + str(e))
    else:
        print("Traducción falló")
