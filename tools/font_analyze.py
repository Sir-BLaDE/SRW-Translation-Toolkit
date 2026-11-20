"""font_analyze.py - Entiende la estructura completa de FontInfo.cpk (EN):
relacion entre mapa JAPN (id1), mapa LATN (id2), tabla de metricas (id3) y textura (id4).
Determina que es el campo 'id' de cada registro de metricas."""
from cpk_util import load
import struct, zlib, binascii

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096

def parse_bltu(pt):
    """Devuelve (magic, grupos_real, lista_completa, colas)."""
    magic = pt[:8].decode('latin1')
    fixoff = struct.unpack_from('<I', pt, 0x18)[0]
    end = struct.unpack_from('<I', pt, 0x1C)[0]
    i = fixoff
    groups = []
    while i < end:
        j = pt.index(b'\x00', i)
        groups.append(pt[i:j].decode('utf-8', 'replace'))
        i = j + 1
    return magic, groups

# ---- id1 JAPN ----
p1 = cf.plain([r for r in cf.rows if r['id'] == 1][0])
magic1, g1 = parse_bltu(p1)
assert g1[0] == 'Fix'
japn = ''.join(g1[1:])
print('JAPN: grupos=%d chars=%d' % (len(g1) - 1, len(japn)))

# ---- id2 LATN ----
p2 = cf.plain([r for r in cf.rows if r['id'] == 2][0])
magic2, g2 = parse_bltu(p2)
print('LATN magic=%s grupos=%d' % (magic2, len(g2)))
if g2 and g2[0] == 'Fix':
    latn = ''.join(g2[1:])
else:
    latn = ''.join(g2)
print('LATN chars=%d' % len(latn))
print('LATN lista (primeros 120):', latn[:120])

# ---- id3 metrics ----
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])
HDR = 40
nrec = (len(p3) - HDR) // 36
print('metricas nrec=%d' % nrec)

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

# ---- hipotesis: los ultimos len(latn) registros = LATN en orden inverso ----
ids = [rec(g)[0] for g in range(nrec)]
print('\nultimos 140 ids:', ids[-140:])

# comparar con codepoints de LATN en orden inverso
latn_rev = latn[::-1]
match = 0
for k in range(min(len(latn_rev), 140)):
    cp = ord(latn_rev[k])
    if ids[-(k+1)] == cp:
        match += 1
print('coincidencias id==codepoint (LATN inverso):', match, '/', min(len(latn_rev),140))

# ---- test hash para los primeros registros (JAPN) ----
print('\n=== test de hash para ids JAPN ===')
pairs = [(japn[i], ids[i]) for i in range(20)]  # '0'..'i'
for ch, want in pairs[:10]:
    print('  %r -> id %d' % (ch, want))

def test_hashes(ch):
    c = ord(ch)
    u8 = ch.encode('utf-8')
    u16 = ch.encode('utf-16-le')
    u16b = ch.encode('utf-16-be')
    c4 = struct.pack('<I', c)
    c4b = struct.pack('>I', c)
    out = {}
    out['crc32_u8'] = zlib.crc32(u8)
    out['crc32_u16'] = zlib.crc32(u16)
    out['crc32_u16b'] = zlib.crc32(u16b)
    out['crc32_c4'] = zlib.crc32(c4)
    out['crc_hqx_u8'] = binascii.crc_hqx(u8, 0)
    out['adler32_u8'] = zlib.adler32(u8)
    # fnv1a 32
    h = 2166136261
    for b in u8:
        h ^= b; h = (h * 16777619) & 0xFFFFFFFF
    out['fnv1a32_u8'] = h
    h = 2166136261
    for b in u16:
        h ^= b; h = (h * 16777619) & 0xFFFFFFFF
    out['fnv1a32_u16'] = h
    # djb2
    h = 5381
    for b in u8:
        h = ((h * 33) + b) & 0xFFFFFFFF
    out['djb2_u8'] = h
    h = 5381
    for b in u16:
        h = ((h * 33) + b) & 0xFFFFFFFF
    out['djb2_u16'] = h
    # sdbm
    h = 0
    for b in u8:
        h = (ord(ch) + (h << 6) + (h << 16) - h) & 0xFFFFFFFF
    out['sdbm_u8'] = h
    return out

# probar si algun hash (mod 65536) coincide con los ids
def match_hash(ch, want):
    for name, val in test_hashes(ch).items():
        if (val & 0xFFFF) == want:
            return name, val
        if val == want:
            return name + '=full', val
    return None, None

print('\n--- buscar hash que case con id (mod 65536) ---')
for ch, want in pairs:
    name, val = match_hash(ch, want)
    print('  %r id=%d -> %s' % (ch, want, (name, val) if name else 'NINGUNO'))
