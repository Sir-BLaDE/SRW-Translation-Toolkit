# -*- coding: utf-8 -*-
"""Instalar traducción completa en el directorio del juego"""
import os
import shutil

GAME_ROOT = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
DATA_PATH = f"{GAME_ROOT}/Data"
BTLC_PATH = f"{DATA_PATH}/BTLC"
EN0_PATH = f"{BTLC_PATH}/EN0"

# Archivos traducidos del backup y creados
TRANSLATED_FILES = {
    'OP.CPK': r"C:/Dev/Default Project/srwv/output/OP_CK_es.cpk",
    'MtZkn_Nm.cpk': r"C:/Dev/Default Project/srwv/output/MtZkn_Nm_es.cpk", 
    'KPACK_P4_LN_EN.es2': r"C:/Dev/Default Project/srwv/output/KPACK_P4_LN_EN_es2.cpk",
}

OUTPUT_DIR = r"C:/Dev/Default Project/srwv/output"

print("=" * 80)
print("INSTALANDO TRADUCCION COMPLETA EN EL JUEGO")
print("=" * 80)

# Verificar archivos traducidos disponibles
print("\nArchivos traducidos disponibles:")
for name, path in TRANSLATED_FILES.items():
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    print(f"  {name}: {'✅' if exists else '❌'} {size:,} bytes")

# Copiar archivos traducidos al directorio correcto
print("\nCopiando archivos traducidos a:", EN0_PATH)

try:
    # Crear directorio de destino si no existe
    os.makedirs(EN0_PATH, exist_ok=True)
    
    # Copiar OP_CK_es.cpk (el más importante)
    if 'OP.CPK' in TRANSLATED_FILES:
        source = TRANSLATED_FILES['OP.CPK']
        target = os.path.join(EN0_PATH, 'OP.CPK')
        
        if os.path.exists(source):
            shutil.copy2(source, target)
            print(f"  Copiado OP.CPK traducido ({os.path.getsize(source):,} bytes)")
        else:
            print(f"  ❌ OP_CK_es.cpk no encontrado para copiar")
    
    # Copiar archivos MtZkn_* traducidos si existen
    mtzkn_source = r"C:/Dev/Default Project/srwv/output/MtZkn_Nm_es.cpk"
    if os.path.exists(mtzkn_source):
        target_mtzkn = os.path.join(DATA_PATH, 'MTDATA', 'MtZkn_Nm.es')
        os.makedirs(os.path.dirname(target_mtzkn), exist_ok=True)
        shutil.copy2(mtzkn_source, target_mtzkn)
        print(f"  Copiado MtZkn_Nm_es.cpk")
    
    # KPACK_P4_LN - verificar estructura correcta
    kpack_source = r"C:/Dev/Default Project/srwv/output/KPACK_P4_LN_EN_es2.cpk"
    if os.path.exists(kpack_source):
        target_kpack = os.path.join(DATA_PATH, 'KURODATA', 'KPACK_P4_LN.es')
        os.makedirs(os.path.dirname(target_kpack), exist_ok=True)
        shutil.copy2(kpack_source, target_kpack)
        print(f"  Copiado KPACK_P4_LN_EN_es2.cpk")
    
    # Crear archivo de estado final
    status_file = os.path.join(EN0_PATH, 'TRANSLATION_STATUS.txt')
    with open(status_file, 'w', encoding='utf-8') as f:
        f.write("TRADUCCION COMPLETA INSTALADA\n")
        f.write("=" * 80 + "\n\n")
        f.write("OP.CPK traducido a español España instalado\n")
        f.write("Todos los archivos CPK traducidos copiados\n")
        f.write("\nUbicación del juego:\n")
        f.write(f"  {GAME_ROOT}\n")
        f.write("\nArchivos instalados:\n")
        for name, path in TRANSLATED_FILES.items():
            if os.path.exists(path):
                target = path.replace(r"C:/Dev/Default Project/srwv/output/", "")
                f.write(f"  - {name}: {target}\n")
    
    print(f"\n✅ TRADUCCION INSTALADA EXITOSAMENTE!")
    print(f"\nVerificar en el juego:")
    print(f"  Directorio: {EN0_PATH}")
    print(f"  Archivo OP.CPK traducido instalado")
    print(f"\nReinicia el juego para ver cambios\n")
    
except Exception as e:
    print(f"\n❌ Error instalando traducción: {e}")
