"""font_id0.py - Analiza a fondo id0 (config 32848 bytes) y la relacion con la
tabla de metricas id3. Determina el orden y el enlace codepoint<->registro."""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
p0 = cf.plain([r for r in cf.rows if r['id'] == 0][0])
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])

print('=== id0 len', len(p0), '===')
print('hex primeros 256:')
print(p0[:256].hex(' '))

# metric ids (1041)
HDR = 40
ids = [struct.unpack_from('<I', p3, HDR + g * 36)[0] for g in range(1041)]

# comprobar si ids esta ordenado
asc = all(ids[i] <= ids[i+1] for i in range(len(ids)-1))
desc = all(ids[i] >= ids[i+1] for i in range(len(ids)-1))
print('\nmetric ids[0:30] =', ids[:30])
print('metric ids[100:130] =', ids[100:130])
print('metric ids[200:230] =', ids[200:230])
print('metric ids[260:280] =', ids[260:280])
print('metric ids[900:941] =', ids[900:941])
print('orden ascendente?', asc, ' descendente?', desc)

# buscar el codepoint de 'é' (233), 'ó'(243), etc. en metric table
for ch, cp in [('é',0xE9),('É',0xC9),('ó',0xF3),('ü',0xFC),('¿',0xBF),('¡',0xA1)]:
    pos = [i for i,v in enumerate(ids) if v == cp]
    print('  metric: %r (U+%04X) en registros %s' % (ch, cp, pos))

# --- id0: buscar codepoints de acentos en id0 ---
print('\n=== buscar codepoints en id0 ===')
for ch, cp in [('é',0xE9),('É',0xC9),('ó',0xF3),('á',0xE1),('í',0xED),
               ('ú',0xFA),('ñ',0xF1),('Á',0xC1),('Ó',0xD3),('Ú',0xDA),
               ('ü',0xFC),('¿',0xBF),('¡',0xA1),('«',0xAB),('»',0xBB)]:
    # buscar u16 LE
    pat = struct.pack('<H', cp)
    pos = []
    start = 0
    while True:
        k = p0.find(pat, start)
        if k < 0:
            break
        pos.append(k)
        start = k + 1
    print('  id0: %r (U+%04X) en offsets %s' % (ch, cp, pos[:10]))

# buscar 'é' (0xE9) como byte suelto y contexto
print('\n=== contexto de algunos codepoints en id0 ===')
def ctx(off):
    return p0[off-4:off+12].hex(' ')
for cp in [0xE9, 0xC9, 0xF3]:
    pat = struct.pack('<H', cp)
    k = p0.find(pat)
    if k >= 0:
        print('  U+%04X en offset %d: ...%s...' % (cp, k, ctx(k)))
