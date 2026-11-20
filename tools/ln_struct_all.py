import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)

# --- id0 cola
pt0 = c.plain(c.rows[0])
off = 0
last = None
n = 0
while off + 16 <= len(pt0):
    key = pt0[off:off + 4]
    a, nxt, d = struct.unpack_from('<3I', pt0, off + 4)
    last = (off, key, a, nxt, d)
    n += 1
    if nxt <= off or nxt > len(pt0):
        break
    off = nxt
print('id0 registros', n, 'ultimo', last, 'len', hex(len(pt0)))
print('   cola', pt0[-32:].hex(' '))

# --- id1
pt1 = c.plain(c.rows[1])
count, os_, ss = struct.unpack_from('<3I', pt1, 4)
print('id1 count', count, 'offs', hex(os_), 'strs', hex(ss), 'len', len(pt1))
offs = struct.unpack_from('<%dI' % count, pt1, os_)
print('   offsets crecientes', all(offs[i] < offs[i+1] for i in range(count - 1)),
      'primero', offs[0], 'ultimo', offs[-1])
end = len(pt1)
lasts = pt1[ss + offs[-1]:end]
print('   ultima cadena repr', repr(lasts[:80]))
print('   bytes tras ultima cadena', lasts.count(0), 'de', len(lasts))

# --- id3
pt3 = c.plain(c.rows[2])
pos = 0
strs = []
while pos + 4 <= len(pt3):
    ln = struct.unpack_from('<I', pt3, pos)[0]
    if ln == 0 or pos + 4 + ln > len(pt3):
        break
    raw = pt3[pos + 4:pos + 4 + ln]
    strs.append(raw.split(b'\0')[0].decode('utf-8', 'replace'))
    pos += 4 + ln
print('id3 cadenas', len(strs), 'fin', hex(pos), 'len', hex(len(pt3)), 'cola', pt3[pos:pos+16].hex(' '))
print('   primeras', strs[:6], 'ultimas', strs[-4:])

# --- id4
pt4 = c.plain(c.rows[3])
print('id4 len', len(pt4), 'hdr', [hex(x) for x in struct.unpack_from('<8I', pt4, 0)])
for o in range(0x10, 0x120, 8):
    print('  ', hex(o), pt4[o:o + 8].hex(' '), repr(pt4[o:o + 8]))
