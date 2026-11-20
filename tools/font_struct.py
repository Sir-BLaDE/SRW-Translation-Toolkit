"""font_struct.py - Determina la relacion real entre mapa JAPN y tabla de metricas.
Renderiza rangos de registros de metrica y busca ids coincidentes con codepoints."""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
HDR = 40

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

def art(g, downsample=1):
    u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W)
    w = max(1, int(fl[2] * W)); h = max(1, int(fl[3] * W))
    rows = []
    for yy in range(0, h, downsample):
        row = tex[(y + yy) * W + x:(y + yy) * W + x + w]
        rows.append(''.join('#' if max(row) > 128 else ('.' if max(row) > 0 else ' ') for b in [0]))
    # rebuild properly
    rows = []
    for yy in range(0, h, downsample):
        row = tex[(y + yy) * W + x:(y + yy) * W + x + w]
        rows.append(''.join('#' if b > 128 else ('.' if b > 0 else ' ') for b in row))
    return u32, x, y, w, h, rows

# buscar ids que coinciden con codepoints de acentos latinos que nos interesan
want = {'é': 0xE9, 'É': 0xC9, 'à': 0xE0, 'è': 0xE8, 'á': 0xE1, 'í': 0xED,
        'ó': 0xF3, 'ú': 0xFA, 'ñ': 0xF1, 'Á': 0xC1, 'Ó': 0xD3, 'Ú': 0xDA,
        'ü': 0xFC, '¿': 0xBF, '¡': 0xA1, '«': 0xAB, '»': 0xBB, 'º': 0xBA, 'ª': 0xAA}
print('=== registros cuyo id == codepoint de acentos ===')
found = {}
for g in range(1041):
    u32, fl = rec(g)
    for ch, cp in want.items():
        if u32 == cp:
            found.setdefault(ch, []).append(g)
for ch in sorted(want):
    print('  %r (U+%04X): %s' % (ch, want[ch], found.get(ch, 'NO ESTA')))

# renderizar rango 840..912 (grupo 19 + 20 + inicio LATN) como arte ASCII
print('\n=== render registros 840..912 ===')
for g in range(840, 913):
    u32, x, y, w, h, rows = art(g)
    # mostrar solo una "firma" compacta: primera fila no vacia + id
    nonblank = [r for r in rows if r.strip()]
    first = nonblank[0] if nonblank else '(vacio)'
    print('g%03d id=%-6d pos(%4d,%3d) %s' % (g, u32, x, y, first))
