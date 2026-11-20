"""font_map.py - Estructura de id1 (mapa de caracteres) e id3 (metricas) de la
fuente EN, y medidas de tinta de los glifos base para componer acentos."""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
rows = {r['id']: r for r in cf.rows}

for fid in (0, 1, 2, 3):
    pt = cf.plain(rows[fid])
    print('---- id%d  %d bytes ----' % (fid, len(pt)))
    print('  primeros 64:', pt[:64].hex())
    print('  u32[:12]:', struct.unpack_from('<12I', pt, 0))
    print('  u16[:20]:', struct.unpack_from('<20H', pt, 0))
    print()

p1 = cf.plain(rows[1])
print('=== id1 completo como u16 y como u8 ===')
h = struct.unpack_from('<16H', p1, 0)
print('u16:', h)
print('bytes 0..40:', p1[:40])
# interpretar como: count + pares?
for guess in ('count_then_pairs',):
    pass
print('total u8 distintos:', len(set(p1)))
# imprimir como lista de rangos si parece (start,end) consecutivos
print('tail:', p1[-32:])

p3 = cf.plain(rows[3])
print()
print('=== id3 header (40 bytes) ===')
print('  bytes:', p3[:40])
print('  u32:', struct.unpack_from('<10I', p3, 0))
print('  f32:', [round(v, 4) for v in struct.unpack_from('<10f', p3, 0)])
print('  registros:', (len(p3) - 40) // 36)
