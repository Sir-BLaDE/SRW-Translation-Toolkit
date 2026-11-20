"""
srwv_buildbltu.py - Constructor de ficheros BLTU a partir de un CSV de traducciones.

Lee un fichero BLTU original (descifrado), aplica las traducciones del CSV
(clave: texto ingles -> texto espanol) y devuelve los bytes del BLTU nuevo.

Uso:
    python srwv_buildbltu.py original.bin traducciones.csv salida.bin
"""
import sys, csv, struct

sys.path.insert(0, r"C:\Dev\Default Project\srwv\tools")
from srwv_bltu import load as load_bltu


def build(original_bytes, csv_path):
    t = load_bltu(original_bytes)

    # Cargar traducciones: en -> es
    trans = {}
    with open(csv_path, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            en = row["en"]
            es = row["es"]
            if es.strip():
                trans[en] = es

    out = bytearray()

    # Cabecera: copiar tal cual (12 u32)
    header = t.header
    for v in header:
        out += struct.pack("<I", v)

    # Ajustar [10] al final: se rellenara despues
    # Por ahora, copiar
    header_off_10 = 10 * 4

    # Reconstruir cada bloque
    new_chunks = []
    for ch in t.chunks:
        new_strings = []
        for s in ch.strings:
            if s in trans:
                new_strings.append(trans[s])
            else:
                new_strings.append(s)

        # Construir el blob
        blob = bytearray()
        offsets = []
        for s in new_strings:
            offsets.append(len(blob))
            blob += s.encode("utf-8") + b"\x00"

        # Construir el bloque
        block = bytearray()
        block += struct.pack("<I", len(new_strings))
        for off in offsets:
            block += struct.pack("<I", off)
        block += blob

        # Alinear a 16 bytes
        while len(block) % 16:
            block += b"\x00"

        new_chunks.append(block)

    # Posicion de inicio del primer bloque
    start = header[2] if header[2] else 0x30
    # Rellenar hasta start
    while len(out) < start:
        out += b"\x00"

    # Escribir los bloques
    for block in new_chunks:
        out += block

    # Actualizar [10] = offset del final del ultimo bloque
    out[header_off_10:header_off_10 + 4] = struct.pack("<I", len(out))

    return bytes(out)


def main():
    if len(sys.argv) < 4:
        print("uso: python srwv_buildbltu.py original.bin csv salida.bin")
        sys.exit(1)
    original = open(sys.argv[1], "rb").read()
    csv_path = sys.argv[2]
    salida = sys.argv[3]
    result = build(original, csv_path)
    open(salida, "wb").write(result)
    print(f"escrito {len(result)} bytes en {salida}")

    # Verificar
    t = load_bltu(result)
    print(f"bloques: {len(t.chunks)}, cadenas: {len(t)}")
    print(f"cabecera [10]: 0x{t.header[10]:X}")


if __name__ == "__main__":
    main()
