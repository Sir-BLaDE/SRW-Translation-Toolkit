"""
srwv_cpkbuild2.py - Constructor de CPK que respeta el orden real del contenido
(IDs ascendentes mezclando CpkItocL y CpkItocH).

Uso:
    out = build_ordered('juego.cpk', {id: (blob_almacenado, tam_descomprimido)})
"""
import struct

from srwv_cpk import Cpk
from cpk_util import CpkFiles


def _align(v, a):
    return (v + a - 1) & ~(a - 1)


def build_ordered(path, new_files):
    cf = CpkFiles(path)
    cpk = cf.cpk
    raw = bytearray(cpk.raw)
    align = cpk.align

    old_span = 0
    new_span = 0
    delta_data = 0
    delta_packed = 0

    blobs = []
    for f in cf.rows:
        fid = f['id']
        old = bytes(raw[f['offset']:f['offset'] + f['size']])
        if fid in new_files:
            blob, ex = new_files[fid]
        else:
            blob, ex = old, f['ex']
        blobs.append(blob)
        old_span += _align(f['size'], align)
        new_span += _align(len(blob), align)
        delta_data += len(blob) - f['size']
        delta_packed += ex - f['ex']

    # ITOC
    info = cpk.itoc_info
    for f, blob in zip(cf.rows, blobs):
        tab = info[f['table']]
        ex = new_files[f['id']][1] if f['id'] in new_files else f['ex']
        for col, value in (('FileSize', len(blob)), ('ExtractSize', ex)):
            c = tab.column(col)
            off = cpk.cell_offset(tab, col, f['row'])
            if c.type == 0x02:
                if value > 0xFFFF:
                    raise ValueError('columna u16 desbordada: id=%s col=%s value=%s old_size=%s old_ex=%s'
                                     % (f['id'], col, value, f['size'], f['ex']))
                struct.pack_into('>H', raw, off, value)
            else:
                struct.pack_into('>I', raw, off, value)

    # cabecera
    for col, delta in (('ContentSize', new_span - old_span),
                       ('EnabledDataSize', delta_data),
                       ('EnabledPackedSize', delta_packed)):
        try:
            off = cpk.cell_offset(cpk.header, col)
        except KeyError:
            continue
        old = struct.unpack_from('>Q', raw, off)[0]
        struct.pack_into('>Q', raw, off, old + delta)

    # contenido
    content = bytearray()
    for i, blob in enumerate(blobs):
        content += blob
        if i < len(blobs) - 1:
            content += b'\0' * (_align(len(content), align) - len(content))
    out = bytes(raw[:cpk.content_offset]) + bytes(content)

    if 'FileSize' in cpk.h and cpk.h['FileSize'] is not None:
        buf = bytearray(out)
        off = cpk.cell_offset(cpk.header, 'FileSize')
        struct.pack_into('>Q', buf, off, len(buf))
        out = bytes(buf)
    return out


if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv) > 1 else \
        'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
    out = build_ordered(p, {})
    orig = open(p, 'rb').read()
    print('identico:', out == orig, '| len', len(out), len(orig))
    if out != orig:
        for i in range(min(len(out), len(orig))):
            if out[i] != orig[i]:
                print('primera diferencia 0x%X' % i, orig[i:i+16].hex(), out[i:i+16].hex())
                break
        print('colas iguales:', out[-16:] == orig[-16:], len(out) - len(orig))
