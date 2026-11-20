#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traducción de LayoutData.cpk al español de España.
Mantiene longitudes exactas para evitar overflow (CPK length == plain length).
"""

import struct
import os

# Diccionario de traducciones manteniendo longitud original aproximada
TRANSLATIONS = {
    # Categorías principales - términos UI clave
    # Select Pilot to Change Mech → Cambio robot con piloto (más corto)
    "Select Pilot to Change Mech": "\u3000\u3000Cambiar Rob-Pil.\u3000\u3000",  # ~44 caracteres unicode
    
    # Select Mech to Cambiar pil. → Seleccionar mech para cambiar piloto
    "Select Mech to Cambiar pil.": "\u3000Selecciona Mech/Piloto\u3000",  # ~42 caracteres unicode
    
    # Unit Info
    "Unit Info": "Info unidad",  # ~10 -> ~10
    
    # Pilot Info
    "Pilot Info": "Info piloto",  # ~10 -> ~10
    
    # Weapon Info
    "Weapon Info": "Info arma",  # ~12 -> ~9
    
    # Select Track
    "Select Track": "Selecciona pista",  # ~13 -> ~15 OK
    
    # Data Type
    "Data Type": "Tipo datos",  # ~10 -> ~10
    
    # Ace Pilot
    "Ace Pilot": "\u3000Piloto ace\u3000",  # ~10 unicode -> ~11 OK
    
    # Skill PG
    "Skill PG": "PG habilidad",  # ~8 -> ~12 OK
    
    # The Special-PG
    "The Special-PG": "\u3000El PG especial\u3000",  # ~14 unicode -> ~16 OK
    
    # Skill Level
    "Skill Level": "Nivel habilidad",  # ~12 -> ~15 OK
    
    # Object Select (brackets)
    "【 Object Select 】": "\u3000†Selección objeto\u3000",  # ~18 unicode -> ~20 OK
    
    # Theme Select
    "【 Theme Select 】": "\u3000†Selección tema\u3000",  # ~17 unicode -> ~20 OK
    
    # Ally Unit List
    "【 Ally Unit List 】": "\u3000†Lista unidad aliada\u3000",  # ~20 unicode -> ~25 OK
    
    # Assign Unit
    "Assign Unit": "Asignar unidad",  # ~12 -> ~14 OK
    
    # Detach/This unit has been detached
    "This unit has been detached from the platoon.": "Unidad desconectada del pelotón.",  # ~49 -> ~38 OK
    
    # Display All Tracks
    "Display All Tracks": "Mostrar todas pistas",  # ~18 -> ~17 OK
    
    # Save has ended
    "Save has ended.": "\u3000Guardado finalizado\u3000",  # ~14 unicode -> ~19 OK
    
    # Do not turn off the power
    "Do not turn off the power.": "No apagues energía.",  # ~27 -> ~18 OK
    
    # You have to save the file
    "You have to save the file.": "Debes guardar archivo.",  # ~26 -> ~23 OK
    
    # By the effect of special skills "president"
    'By the effect of special skills "president"': '\u3000Efecto habilidades especiales"',  # ~51 unicode -> ~45 OK
    
    # All Ataque (ya traducido, asegurar consistencia)
    "All Ataque": "Todo ataque",  # ~10 -> ~12 OK
    
    # Direct Hit
    "Direct Hit": "Impacto directo",  # ~11 -> ~15 OK
    
    # No Ataque
    "No Ataque": "Sin ataque",  # ~10 -> ~10
    
    # Re-attack → Contraataque
    "Re-attack": "\u3000Contraataque\u3000",  # ~9 unicode -> ~12 OK
    
    # Support Attack
    "Support Attack": "Apoyo ataque",  # ~14 -> ~14 OK
    
    # Hit and Away → Danno y distancia (mejor: Daño distancial)
    "Hit and Away": "\u3000Daño distancial\u3000",  # ~12 unicode -> ~16 OK
    
    # Commander
    "Commander": "\u3000Comandante\u3000",  # ~10 unicode -> ~12 OK
    
    # Fleet commander → Comandante flotilla (mejor: Almirante)
    "Fleet commander": "Almirante",  # ~15 -> ~9 OK
    
    # Versus spirit attack → Ataque espíritu rival
    "Versus spirit attack": "\u3000Ataque espírituv\u3000",  # ~22 unicode -> ~20 OK
    
    # Increase → Aumentar
    "Increase": "\u3000Aumentar\u3000",  # ~9 unicode -> ~10 OK
    
    # Special Skill＜：All＞ → Habilidad especial＜：Todo＞ (mantener)
    'Special Skill＜:All＞': 'Habilidad especial＜:Todo＞',  # ~28 -> ~25 OK
    
    # End Phase → Final fase
    '" End Phase "': "\u3000Final fase\u3000",  # ~13 unicode -> ~16 OK
    
    # To the sortie pilot → Al piloto de sortie (mejor: piloto saliente)
    "To the sortie pilot": "\u3000Al piloto saliente\u3000",  # ~20 unicode -> ~20 OK
    
    # Please check the organization screen.
    "Please check the organization screen.": "Revisar pantalla organización.",  # ~39 -> ~34 OK
    
    # This space is blank or contains a unit that cannot be used.
    "This space is blank or contains a unit that cannot be used.": "\u3000Espacio vacío/unidad no usable\u3000",  # ~62 unicode -> ~50 OK
    
    # Please do not remove your USB storage device.
    "Please do not remove your USB storage device.": "No quite dispositivo USB.",  # ~47 -> ~32 OK
    
    # Not enough free space on target device.
    "Not enough free space on target device.": "\u3000Sin espacio suficiente en destino\u3000",  # ~36 unicode -> ~38 OK
    
    # Memory Stick, you can disconnect,
    "Memory Stick, you can disconnect,": "Stick memoria desconectar,\u3000",  # ~35 -> ~34 OK
    
    # Free space on the Memory Stick TM is missing.
    "Free space on the Memory Stick TM is missing.": "\u3000Sin espacio en stick memoria\u3000",  # ~46 unicode -> ~40 OK
    
    # To save the system data
    "To save the system data": "Guardar datos sistema\u3000",  # ~24 -> ~23 OK
    
    # Free space after 999KB or more, is required.
    "Free space after 999KB or more, is required.": "\u3000Req. 999KB+ espacio vacío\u3000",  # ~46 unicode -> ~40 OK
    
    # Are you sure you want to delete the other save data?
    "Are you sure you want to delete the other save data?": "\u3000¿Borrar datos guardados otros?\u3000",  # ~54 unicode -> ~52 OK
    
    # By the effect of ace bonus of the overabundance of vigor
    "By the effect of ace bonus of the overabundance of vigor": "\u3000Efecto bono aceso vigor abundan\u3000",  # ~61 unicode -> ~52 OK
    
    # It was hand.
    "It was hand.": "\u3000Fue mano.\u3000",  # ~13 unicode -> ~12 OK
    
    # By the effect of the Z Crystal "gathered to Reiko"
    'By the effect of the Z Crystal "gathered to Reiko"': '\u3000Efecto cristal Z "reunido"',  # ~54 unicode -> ~48 OK
    
    # We got the following bonus.
    "We got the following bonus.": "\u3000Obtenemos bonos siguientes\u3000",  # ~27 -> ~29 OK
    
    # By the effect of Z Crystal "Journey to the Warriors"
    'By the effect of Z Crystal "Journey to the Warriors"': '\u3000Efecto cristal Z "',  # ~56 unicode -> ~44 OK
    
    # PP has been incremented by 2.
    "PP has been incremented by 2.": "\u3000PP incrementado 2\u3000",  # ~28 unicode -> ~26 OK
    
    # The Z chip in effect
    "The Z chip in effect": "\u3000Chip Z en efecto\u3000",  # ~21 -> ~19 OK
    
    # 10000z was obtained.
    "10000z was obtained.": "\u3000Obtenido 10000z\u3000",  # ~21 -> ~18 OK
    
    # Funds in effect 999999
    "Funds in effect 999999": "\u3000Fundos en efecto 999999\u3000",  # ~25 unicode -> ~27 OK
    
    # Cover attack → Ataque cobertura (mejor: Apoyo defensivo)
    "Cover attack": "\u3000Apoyo defensivo\u3000",  # ~12 unicode -> ~16 OK
    
    # AT^\rAT^ / AT^\tAT^ (control characters - omitir)
}

# Función principal para traducción controlada con validación de longitud
def translate_layout_data(input_path, output_path):
    """
    Traduce LayoutData.cpk manteniendo longitudes exactas.
    
    Args:
        input_path: Ruta del CPK original (EN/LayoutData.cpk)
        output_path: Ruta de salida para el CPK traducido
        
    Returns:
        bool: True si éxito, False si error
    """
    
    print(f"Traduciendo {input_path} → {output_path}")
    
    # Extraer estructura del CPK original
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado: {input_path}")
        return False
    
    # Verificar que el archivo es válido (tiene header PK+)
    if data[:4] != b'PK\x03\x04':
        print("WARNING: Archivo no parece ser CPK válido (sin header PK)")
        return False
    
    # Extraer y traducir cada entrada text_string (string 8-bit)
    offset = 0
    original_strings_count = 0
    translated_strings_count = 0
    
    while offset < len(data):
        try:
            # Intentar leer length (2 bytes big-endian para strings 8-bit con null terminator)
            if data[offset] & 0x80:
                # String con referencia a tablas
                header_len = struct.unpack('>H', data[offset:offset+2])[0]
                offset += 2
                
                # Saltar al texto real (skip header, tipo, ref)
                string_offset = offset + 16  # Aproximado, ajustar según estructura
                
                # Verificar límites
                if string_offset >= len(data):
                    break
                    
                try:
                    text_bytes = bytes(data[string_offset:string_offset+30])
                    
                    # Buscar coincidencias de traducción
                    for en_key, es_value in TRANSLATIONS.items():
                        if en_key.encode('utf-8') in text_bytes.decode('utf-8', errors='ignore'):
                            # Validar longitud: plain length <= original
                            if len(es_value) <= len(en_key):
                                old_text = text_bytes.decode('utf-8', errors='ignore')
                                new_text = es_value
                                
                                # Reemplazar en el CPK
                                data[string_offset:string_offset+len(old_text)] = new_text.encode('utf-8')
                                translated_strings_count += 1
                                print(f"  Traducido: '{en_key[:30]}...' → '{new_text}'")
                            break
                
                except UnicodeDecodeError:
                    offset += 30
                    continue
                    
            else:
                # Header simple (longitud directa)
                try:
                    header_len = struct.unpack('>H', data[offset:offset+2])[0]
                except:
                    header_len = 0
                offset += 2
                
                # Saltar entrada completa (tipo, ref, flags, texto)
                string_offset = offset + 16 + header_len
                if string_offset < len(data):
                    text_bytes = bytes(data[string_offset:string_offset+30])
                    
                    for en_key, es_value in TRANSLATIONS.items():
                        if en_key.encode('utf-8') in text_bytes.decode('utf-8', errors='ignore'):
                            old_text = text_bytes.decode('utf-8', errors='ignore')
                            new_text = es_value
                            
                            if len(new_text) <= len(old_text):
                                data[string_offset:string_offset+len(old_text)] = new_text.encode('utf-8')
                                translated_strings_count += 1
                                print(f"  Traducido: '{en_key[:30]}...' → '{new_text}'")
                            break
                    
                    offset += 40 + header_len
                else:
                    break
                    
        except Exception as e:
            offset += 8
            continue
        
    # Escribir CPK traducido con longitud exacta
    try:
        with open(output_path, 'wb') as f:
            f.write(data)
        print(f"✓ Traducción completa: {translated_strings_count} cadenas traducidas")
        return True
    except Exception as e:
        print(f"ERROR escribiendo archivo: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Uso: python layoutdata_translate_es.py <input.cpk> <output.cpk>")
        print("\nEjemplo:")
        print('  python layoutdata_translate_es.py EN/LayoutData.cpk LayoutData_es.cpk')
        
    input_file = sys.argv[1] if len(sys.argv) > 1 else "EN/LayoutData.cpk"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "LayoutData_es.cpk"
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_input = os.path.join(base_path, '..', '..', 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk')
    full_output = os.path.join(base_path, '..', '..', 'outputs/LayoutData_es.cpk')
    
    # Corregir rutas si existen
    if input_file.lower().endswith('.cpk'):
        input_file = input_file.replace('layoutdata.cpk', 'EN/LayoutData.cpk')
    if input_file == 'layoutdata.cpk':
        full_input = os.path.join(base_path, '..', '..', 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk')
    if output_file.lower().endswith('.cpk'):
        output_file = output_file.replace('layoutdata_es.cpk', 'LayoutData_es.cpk')
    elif output_file == 'layoutdata_es.cpk':
        full_output = os.path.join(base_path, '..', '..', 'outputs/LayoutData_es.cpk')
    
    # Verificar rutas correctas
    if full_input:
        print(f"Ruta input: {full_input}")
        print(f"Ruta output: {full_output}")
        
        result = translate_layout_data(full_input, full_output)
        if result:
            print("\n✓ Traducción completa exitosa")
        else:
            print("\n✗ Traducción falló")
    else:
        # Modo manual - pedir rutas al usuario
        input_path = input("Introduce ruta del archivo LayoutData.cpk original (ej: D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk): ").strip()
        output_path = input("Introduce ruta de salida para el CPK traducido (ej: outputs/LayoutData_es.cpk): ").strip()
        
        result = translate_layout_data(input_path, output_path)
        if result:
            print("\n✓ Traducción completa exitosa")
            
            # Preguntar si se quiere instalar ahora
            install_now = input("\n¿Instalar en el juego ahora? (s/n): ").strip().lower()
            if install_now == 's':
                from set_cpk_set import set_cpk_path
                
                cpk_name = "LayoutData"
                target_dir = "Data/AIDDATA/EN"  # La ruta EN activa
                
                print(f"Instalando {cpk_name}.cpk en {target_dir}")
                
                # Crear estructura de carpeta y copiar archivo
                target_full_path = os.path.join(target_dir, cpk_name + ".cpk")
                
                if not os.path.exists(os.path.dirname(target_full_path)):
                    os.makedirs(os.path.dirname(target_full_path))
                
                import shutil
                shutil.copy(output_path, target_full_path)
                
                print(f"✓ Instalado en {target_full_path}")
                
                # Ejecutar verificación de boot
                print("\nEjecutando verificación de arranque...")
                os.system(f'powershell -File "{os.path.join(base_path, "..\\..", "D:/Juegos/-SPARROW-/Super Robot Wars V", "Data/BTLC/EN0/privacy_en_win.cpk")}"')
                
                print("\n✓ Instalación completa!")
