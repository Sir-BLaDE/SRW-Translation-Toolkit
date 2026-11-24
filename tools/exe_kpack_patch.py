"""exe_kpack_patch.py - Parchea en el EXE la tabla de tamanos de las filas KPACK.

PROBLEMA (SRW X y, casi seguro, SRW V)
  El EXE lleva una tabla por cada KPACK_*_<IDIOMA>.CPK con pares (fila, tamano
  descomprimido) por recurso. Al cargar un recurso el juego reserva y copia
  EXACTAMENTE ese tamano, ignorando el tamano real de la fila en el CPK.
  Si una fila traducida crece, se trunca: la parte final queda con basura y el
  juego se cuelga o no segun lo que haya en memoria. Sintomas tipicos:
    * "modificar KPACK RG impide arrancar" aunque se recomprima sin cambios
      (en realidad la fila truncada es otra, p. ej. LN fila 3, y al cambiar RG
      solo cambia la disposicion de la memoria);
    * "la fila 4 de KPACK LN impide arrancar".
  En SRW X el crash esta en SRWX.EXE+0x260c1b (recorre una cadena de 142
  registros [int32 desplazamiento][datos] de LN fila 3 y sale del bufer).

COMO LO ENCUENTRA (sin offsets fijos, valido para cualquier EXE del motor)
  1. Busca en el EXE la cadena del nombre del CPK (p. ej. KPACK_P4_LN_EST002_EN.CPK).
  2. Busca una estructura {char *nombre; int32 (*entradas)[2]} que apunte a ella.
  3. Lee las entradas (fila, tamano) hasta la primera que no sea valida.
  4. Comprueba que los tamanos coinciden con el CPK ORIGINAL y escribe los del
     CPK traducido.

USO
  python exe_kpack_patch.py EXE_ORIG EXE_SALIDA ORIG.CPK NUEVO.CPK [ORIG2.CPK NUEVO2.CPK ...]
  Ej. SRW X:
    python exe_kpack_patch.py SRWX.EXE SRWX_es.EXE \
        orig/KPACK_P4_LN_EST002_EN.CPK out/KPACK_P4_LN_EST002_EN.CPK \
        orig/KPACK_P4_RG_EST002_EN.CPK out/KPACK_P4_RG_EST002_EN.CPK
  Requiere SRW_GAME / SRW_EXE configurados para cpk_util (clave Blowfish).

Ojo: si Steam actualiza o verifica el juego, restaura el EXE original y hay que
volver a parchear.
"""
import os
import struct
import sys

import pefile

from cpk_util import load


def _rows(path):
    return {r['id']: r['ex'] for r in load(path).rows}


def find_table(pe, img, name):
    """Devuelve [(rva_de_la_entrada, fila, tamano), ...] de la tabla de `name`."""
    ib = pe.OPTIONAL_HEADER.ImageBase
    hits = []
    key = name.encode() + b'\0'
    i = img.find(key)
    while i >= 0:
        if i == 0 or img[i - 1] == 0:          # inicio de cadena
            hits.append(i)
        i = img.find(key, i + 1)
    if not hits:
        raise SystemExit('no encuentro %s en el EXE' % name)
    for srva in hits:
        ptr = struct.pack('<Q', ib + srva)
        j = img.find(ptr)
        while j >= 0:
            if j % 8 == 0:
                ent_va = struct.unpack_from('<Q', img, j + 8)[0]
                ent = ent_va - ib
                if 0 < ent < len(img):
                    out = []
                    for k in range(64):
                        row, size = struct.unpack_from('<ii', img, ent + 8 * k)
                        if row == -1 and size == 0:
                            out.append((ent + 8 * k, row, size))
                            continue
                        if 0 <= row < 64 and 0 < size < 0x4000000:
                            out.append((ent + 8 * k, row, size))
                            continue
                        break
                    if any(r >= 0 for _, r, _ in out):
                        return out
            j = img.find(ptr, j + 1)
    raise SystemExit('no encuentro la tabla de %s' % name)


def patch(exe_in, exe_out, pairs):
    """pairs: [(cpk_original, cpk_nuevo), ...]. El nombre del CPK original da la tabla."""
    pe = pefile.PE(exe_in)
    img = pe.get_memory_mapped_image()
    data = bytearray(open(exe_in, 'rb').read())
    log = []
    for orig, new in pairs:
        name = os.path.basename(orig)
        o, n = _rows(orig), _rows(new)
        for rva, row, size in find_table(pe, img, name):
            if row < 0:
                continue
            # SRW V: el EXE puede llevar un tamano algo MENOR que el de la fila del CPK
            # original (relleno final que el juego no usa). Se conserva esa holgura.
            delta = o.get(row, -1) - size
            if not 0 <= delta < 1024:
                raise SystemExit('%s fila %d: el EXE dice %d y el CPK original %s; '
                                 '¿EXE o CPK que no son los originales?' % (name, row, size, o.get(row)))
            want = n[row] - delta
            if want != size:
                off = pe.get_offset_from_rva(rva + 4)
                struct.pack_into('<i', data, off, want)
                log.append('%s fila %d: %d -> %d (offset 0x%X, holgura %d)' % (name, row, size, want, off, delta))
    open(exe_out, 'wb').write(data)
    return log


def main():
    a = sys.argv[1:]
    if len(a) < 4 or len(a) % 2:
        raise SystemExit(__doc__)
    pairs = list(zip(a[2::2], a[3::2]))
    log = patch(a[0], a[1], pairs)
    print('\n'.join(log) if log else 'sin cambios: ninguna fila cambia de tamano')
    print('escrito', a[1])


if __name__ == '__main__':
    main()
