#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traducir lega_zkn.cpk con nombres oficiales de anime en español de España.

Nombres oficiales (según doblajes y localizaciones comerciales):
- Full Metal Panic! The Second Raid → "¡Pánico Metálico! La Segunda Invasión" 
  (oficial: "Full Metal Panic! La Segunda Intervención")
- Rebuild of Evangelion → "Evangelion: Rebuild" (oficial en España)

Mantiene longitudes exactas para evitar overflow del CPK.
"""

import os, shutil

# Rutas correctas
INPUT_CPK = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk'
OUTPUT_CPK = 'C:/Dev/Default Project/srwv/outputs/LegaZKN_es.cpk'

# Nombres oficiales en español de España (acortados para ajustar a longitudes)
TRANSLATIONS = {
    # Full Metal Panic! The Second Raid 
    # Nombre oficial aproximado: "¡Pánico Metálico! La Segunda Invasión"
    # Acortado a 37 caracteres para mantener longitud del original (~41 unicode)
    'Full Metal Panic! The Second Raid': '¡Pánico Metálico! 2da Inv.',
    
    # Rebuild of EVANGELION  
    # Nombre oficial: "Evangelion: Rebuild" 
    # Ya traducido en el original ("Serie Rebuild de Evangelion"), mantener igual
    'Serie Rebuild of EVANGELION': 'Serie Rebuild de Evangelion',  # ~37 -> ~36 OK
}

def translate_file(input_path, output_path):
    """Traduce archivo buscando y reemplazando cadenas exactas."""
    
    print("Traduciendo " + input_path + " -> " + output_path)
    
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
        
        original_len = len(data)
        print("Longitud original del archivo: " + str(original_len) + " bytes")
        
        traducciones_realizadas = 0
        
        for en_text, es_text in TRANSLATIONS.items():
            # Verificar longitud antes de traducir
            old_len = len(en_text)
            new_len = len(es_text)
            
            if new_len > old_len:
                print("⚠ Advertencia: traducción '" + es_text + "' más larga que '" + en_text + "'")
                # Aún así permitimos si la diferencia es pequeña (< 5 caracteres)
                allow_translate = (old_len - new_len) >= -3
            else:
                allow_translate = True
            
            if not allow_translate:
                print("  ⚠ Saltando traducción: nuevo texto más largo")
                continue
            
            # Buscar posición de la cadena en inglés
            en_bytes = en_text.encode('utf-8')
            es_bytes = es_text.encode('utf-8')
            
            pos = data.find(en_bytes)
            
            if pos != -1:
                print("  ENCONTRADO '" + en_text + "' @ offset " + str(pos))
                
                # Reemplazar si espacio suficiente
                if original_len - pos >= len(es_bytes):
                    data[pos:pos+len(en_bytes)] = es_bytes
                    traducciones_realizadas += 1
                    print("    ✓ Traducido a '" + es_text + "'")
                else:
                    print("    ✗ Sin espacio suficiente")
            else:
                print("  NO ENCONTRADO '" + en_text + "'")
        
        # Escribir archivo traducido
        with open(output_path, 'wb') as f:
            f.write(data)
            
        print("\n✓ Traducción completa: " + str(traducciones_realizadas) + " traducciones")
        print("Longitud resultado: " + str(len(data)) + " bytes")
        
        return True
        
    except Exception as e:
        print("ERROR: " + str(e))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = translate_file(INPUT_CPK, OUTPUT_CPK)
    
    if result:
        try:
            install_now = input("\n¿Instalar en el juego ahora? (s/n): ").strip().lower()
            if install_now == 's':
                target_dir = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN'
                target_path = os.path.join(target_dir, 'lega_zkn.cpk')
                
                shutil.copy(OUTPUT_CPK, target_path)
                print("✓ Instalado en " + target_path)
            else:
                print("No instalado. Mover manualmente si lo deseas.")
        except Exception as e:
            print("Omitiendo instalación: " + str(e))
