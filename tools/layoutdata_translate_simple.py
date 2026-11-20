#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traducción simple de LayoutData.cpk al español de España.
Mantiene longitudes exactas para evitar overflow (CPK length == plain length).
"""

import os, shutil, struct

GAME_ROOT = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
INPUT_CPK = os.path.join(GAME_ROOT, 'Data/AIDDATA/EN/LayoutData.cpk')
OUTPUT_CPK = 'C:/Dev/Default Project/srwv/outputs/LayoutData_es.cpk'

# Diccionario de traducciones - formato (texto_ingles: texto_espanol_corto)
TRANSLATIONS = {
    "Select Pilot to Change Mech": "Cambiar Rob-Pil.",
    "Select Mech to Cambiar pil.": "Selecciona Mech/Piloto", 
    "Unit Info": "Info unidad",
    "Pilot Info": "Info piloto",
    "Weapon Info": "Info arma",
    "Select Track": "Selecciona pista",
    "Data Type": "Tipo datos",
    "Ace Pilot": "Piloto ace",
    "Skill PG": "PG habilidad",
    "The Special-PG": "El PG especial",
    "Skill Level": "Nivel habilidad",
    "【 Object Select 】": "Seleccion objeto",
    "【 Theme Select 】": "Seleccion tema",
    "【 Ally Unit List 】": "Lista unidad aliada",
    "Assign Unit": "Asignar unidad",
    "Display All Tracks": "Mostrar todas pistas",
    "Save has ended.": "Guardado finalizado",
    "Do not turn off the power.": "No apagues energia",
    "You have to save the file.": "Debes guardar archivo",
    "All Ataque": "Todo ataque",
    "Direct Hit": "Impacto directo",
    "No Ataque": "Sin ataque",
    "Re-attack": "Contraataque",
    "Support Attack": "Apoyo ataque",
    "Hit and Away": "Danno distancial",
    "Commander": "Comandante",
    "Fleet commander": "Almirante",
    "Versus spirit attack": "Ataque espiritu",
    "Increase": "Aumentar",
    '" End Phase "': "Final fase",
    "To the sortie pilot": "Al piloto saliente",
    "Please check the organization screen.": "Revisar pantalla organizacion",
    "This space is blank or contains a unit that cannot be used.": "Espacio vacio/unidad no usable",
    "Please do not remove your USB storage device.": "No quite dispositivo USB",
    "Not enough free space on target device.": "Sin espacio suficiente en destino",
    "Memory Stick, you can disconnect,": "Stick memoria desconectar,",
    "Free space on the Memory Stick TM is missing.": "Sin espacio en stick memoria",
    "To save the system data": "Guardar datos sistema",
    "Free space after 999KB or more, is required.": "Req. 999KB+ espacio vacio",
    "Are you sure you want to delete the other save data?": "Borrar datos guardados otros?",
    "By the effect of ace bonus of the overabundance of vigor": "Efecto bono aceso vigor abundan",
    "It was hand.": "Fue mano.",
    'By the effect of the Z Crystal "gathered to Reiko"': "Efecto cristal Z reunion",
    "We got the following bonus.": "Obtenemos bonos siguientes",
    'By the effect of Z Crystal "Journey to the Warriors"': "Efecto cristal Z ",
    "PP has been incremented by 2.": "PP incrementado 2",
    "The Z chip in effect": "Chip Z en efecto",
    "10000z was obtained.": "Obtenido 10000z",
    "Funds in effect 999999": "Fundos en efecto 999999",
    "Cover attack": "Apoyo defensivo",
}

def translate_cpk(input_path, output_path):
    """Traduce CPK manteniendo longitudes exactas."""
    
    print(f"Traduciendo {input_path} -> {output_path}")
    
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"ERROR leyendo archivo: {e}")
        return False
    
    offset = 0
    translated_count = 0
    
    while offset < len(data):
        # Leer header (2 bytes para string 8-bit)
        try:
            length = struct.unpack('>H', data[offset:offset+2])[0]
        except:
            break
        
        if length == 0 and offset >= 10:
            break
            
        # Calcular offset del texto
        text_offset = offset + 4  # Header + flags/tipo
        end_offset = min(text_offset + length, len(data))
        
        try:
            text_bytes = data[text_offset:end_offset]
            text = text_bytes.decode('utf-8', errors='ignore')
            
            # Buscar traducción
            for en_key, es_value in TRANSLATIONS.items():
                if en_key in text:
                    old_len = len(en_key)
                    new_len = len(es_value)
                    
                    # Validar longitud
                    if new_len <= old_len:
                        data[text_offset:text_offset+old_len] = es_value.encode('utf-8')
                        translated_count += 1
                        print(f"  Traducido (len {old_len}->{new_len}): '{en_key}' -> '{es_value}'")
                    break
            
            # Avanzar offset
            if length > 0:
                offset = text_offset + length
            else:
                offset += 8
                
        except Exception as e:
            offset += 8
            continue
    
    try:
        with open(output_path, 'wb') as f:
            f.write(data)
        print(f"Traducción completa: {translated_count} cadenas traducidas")
        return True
        
    except Exception as e:
        print(f"ERROR escribiendo archivo: {e}")
        return False

if __name__ == "__main__":
    result = translate_cpk(INPUT_CPK, OUTPUT_CPK)
    
    if result:
        # Preguntar si instalar
        try:
            install_now = input("Instalar en el juego ahora? (s/n): ").strip().lower()
            if install_now == 's':
                target_dir = os.path.join(GAME_ROOT, 'Data/AIDDATA/EN')
                target_path = os.path.join(target_dir, 'LayoutData.cpk')
                
                if not os.path.exists(os.path.dirname(target_path)):
                    os.makedirs(os.path.dirname(target_path))
                
                shutil.copy(OUTPUT_CPK, target_path)
                print(f"Instalado en {target_path}")
            else:
                print("No instalado. Mover manualmente si lo deseas.")
        except:
            print("Operacion de instalacion omitida.")
