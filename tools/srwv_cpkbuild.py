"""
srwv_cpkbuild.py - Constructor/parcheador de CPK para Super Robot Wars V.

Replica exactamente la disposicion de los CPK originales:

    +0x000  "CPK " + u32 version + u32 tamaño tabla cabecera + u32 0
    +0x010  @UTF  CpkHeader
    ...     relleno con ceros hasta 0x800
    +0x800  frame ITOC:  "ITOC" + u32 0xFF + u32 tamaño @UTF + u32 0 + @UTF
    ...     relleno con ceros hasta ContentOffset = align16(fin ITOC + 0x20)
    +ContentOffset  contenido: ficheros concatenados y alineados a `Align`

Para reconstruir un CPK se parte del original y se cambian:
  * el contenido de los ficheros,
  * los campos ContentSize / EnabledPackedSize / EnabledDataSize de la cabecera,
  * los campos FileSize / ExtractSize de las filas del ITOC.

Los ficheros NO comprimidos/cifrados se dejan tal cual.
"""

import struct

from cri_utf import UtfTable
from srwv_cpk import Cpk


def _align(v, a):
    return (v + a - 1) & ~(a - 1)


def build_cpk(original: Cpk, new_files: dict, extract_sizes: dict = None):
    """
    original : instancia de Cpk del fichero original
    new_files: {id: bytes} contenido nuevo (sin cifrar) de cada fichero
    extract_sizes: {id: int} tamaño descomprimido de cada fichero

    Devuelve los bytes del CPK reconstruido.
    """
    if extract_sizes is None:
        extract_sizes = {}

    raw = bytearray(original.raw)
    files = original.file_list()
    align = original.align or 16

    # --- 1.ITOC: actualizar FileSize / ExtractSize --------------------
    info = original.itoc_info
    for tab_name in ("CpkItocL", "CpkItocH"):
        tab = info.get(tab_name)
        if tab is None:
            continue
        for r in range(tab.rows_count):
            row = tab.row(r)
            fid = row["ID"]
            if fid not in new_files:
                continue
            size = len(new_files[fid])
            ex = extract_sizes.get(fid, size)
            for col, value in (("FileSize", size), ("ExtractSize", ex)):
                c = tab.column(col)
                off = original.cell_offset(tab, col, r)
                if c.type == 0x02:      # u16
                    struct.pack_into(">H", raw, off, value)
                else:                   # u32
                    struct.pack_into(">I", raw, off, value)

    # --- 2. cabecera: ContentSize / EnabledPackedSize / EnabledDataSize -
    #     Se ajustan respecto a los valores originales para conservar las
    #     rarezas del fichero original (redondeos, tamaños declarados...).
    delta_content = 0
    delta_data = 0
    delta_packed = 0
    for f in files:
        fid = f["id"]
        if fid not in new_files:
            continue
        new_size = len(new_files[fid])
        new_ex = extract_sizes.get(fid, new_size)
        delta_content += _align(new_size, align) - _align(f["size"], align)
        delta_data += new_size - f["size"]
        delta_packed += new_ex - f["extract_size"]

    for col, delta in (("ContentSize", delta_content),
                       ("EnabledPackedSize", delta_packed),
                       ("EnabledDataSize", delta_data)):
        try:
            off = original.cell_offset(original.header, col)
        except KeyError:
            continue
        old = struct.unpack_from(">Q", raw, off)[0]
        struct.pack_into(">Q", raw, off, old + delta)

    # --- 3. reconstruir el area de contenido ---------------------------
    content = bytearray()
    for i, f in enumerate(files):
        fid = f["id"]
        blob = new_files[fid] if fid in new_files else raw[f["offset"]:f["offset"] + f["size"]]
        content += blob
        if i < len(files) - 1:          # el ultimo fichero no lleva relleno
            pad = _align(len(content), align) - len(content)
            content += b"\0" * pad
    content_offset = original.content_offset
    out = bytearray(raw[:content_offset])
    out += content
    return bytes(out)


def rebuild_from_original(path, new_files, extract_sizes=None):
    cpk = Cpk(path)
    return build_cpk(cpk, new_files, extract_sizes)


if __name__ == "__main__":
    import sys
    # prueba: reconstruir un fichero sin cambios y comparar
    src = sys.argv[1]
    cpk = Cpk(src)
    files = {f["id"]: cpk.raw[f["offset"]:f["offset"] + f["size"]] for f in cpk.file_list()}
    ex = {f["id"]: f["extract_size"] for f in cpk.file_list()}
    out = build_cpk(cpk, files, ex)
    same = out == cpk.raw
    print("reconstruccion identica:", same)
    if not same:
        print("longitudes:", len(out), len(cpk.raw))
        for i in range(min(len(out), len(cpk.raw))):
            if out[i] != cpk.raw[i]:
                print("primera diferencia en 0x%X" % i)
                print("  orig:", cpk.raw[i:i+32].hex())
                print("  nuevo:", out[i:i+32].hex())
                break
