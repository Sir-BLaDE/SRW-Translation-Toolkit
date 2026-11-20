# -*- coding: utf-8 -*-
"""Buscar cualquier texto ASCII en LayoutImage.cpk"""

input_path = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutImage.cpk'

print("=== BUSCANDO TEXTO EN LayoutImage.cpk ===\n")

try:
    with open(input_path, 'rb') as f:
        data = f.read()
    
    # Convertir a string buscando secuencias ASCII imprimibles
    text_regions = []
    
    pos = 0
    while True:
        # Buscar inicio de texto ASCII
        match = None
        for i in range(pos, min(pos + 1000, len(data))):
            if 32 <= data[i] <= 126:  # Character imprimible
                try:
                    c = chr(data[i])
                    if c.isalnum() or c in ' .-_:!?@#$%&*':
                        match = i
                        break
                except:
                    pass
            else:
                break
        
        if match is not None:
            # Leer hasta fin del texto o salto de linea
            end = match + 1
            while end < min(len(data), match + 200):
                c = chr(data[end])
                try:
                    if c.isalnum() or c in ' .-_:!?@#$%&*()[]{}<>':
                        end += 1
                    elif c == '\r' and data[end:end+1] == b'\n':
                        break
                    else:
                        break
                except:
                    break
            
            text_bytes = data[match:end]
            
            # Verificar si tiene longitud razonable (>= 10 caracteres)
            if len(text_bytes) >= 10 and not text_bytes.startswith(b'CPK'):
                try:
                    text_preview = text_bytes.decode('utf-8', errors='ignore')[:150]
                    clean_text = ' '.join(filter(lambda c: c.isalnum() or c in ' ._:-@#()', text_preview.strip()))
                    
                    if len(text_preview.strip()) > 2 and not text_preview.startswith('Layout'):
                        region_name = text_preview.split()[0] + '...'
                        text_regions.append((match, clean_text))
                except:
                    pass
        
        if match is None:
            break
        
        pos = match + 1
    
    print(f"Encontradas {len(text_regions)} regiones de texto")
    
    # Mostrar las primeras 20 por region
    for offset, text in sorted(text_regions)[:20]:
        print(f"\nOffset {offset}:")
        print(f"  Longitud: {len(text)} bytes")
        try:
            decoded = text.decode('utf-8', errors='ignore')[:100]
            clean = ' '.join(filter(lambda c: c.isalnum() or c in ' ._:-@#()', decoded.strip()))
            print(f"  Texto: {clean}")
        except:
            print("  Binario")

except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
