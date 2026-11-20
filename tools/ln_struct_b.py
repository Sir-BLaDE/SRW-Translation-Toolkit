import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}

# --- id2
pt2 = c.plain(rows[2])
print('id2 len', len(pt2), 'hdr', [hex(x) for x in struct.unpack_from('<4I', pt2, 0)])
print('  0x00-0x40', pt2[:0x40].hex(' '))
print('  0x80-0xc0', pt2[0x80:0xc0].hex(' '))
print('  repr 0x8c0', repr(pt2[0x8c0:0x920]))

# --- id3
pt3 = c.plain(rows[3])
pos = 0
strs = []
while pos + 4 <= len(pt3):
    ln = struct.unpack_from('<I', pt3, pos)[0]
    if ln == 0 or pos + 4 + ln > len(pt3):
        break
    raw = pt3[pos + 4:pos + 4 + ln]
    strs.append((pos, ln, raw.split(b'\0')[0].decode('utf-8', 'replace')))
    pos += 4 + ln
print('id3 cadenas', len(strs), 'fin', hex(pos), 'len', hex(len(pt3)), 'resto', pt3[pos:].hex(' ')[:60])
print('  primeras', [s[2] for s in strs[:5]], 'ultimas', [s[2] for s in strs[-5:]])
print('  prefix lens raros', [(hex(o), l, t) for o, l, t in strs if l % 4])

# --- id4
pt4 = c.plain(rows[4])
print('id4 len', len(pt4), 'hdr', [hex(x) for x in struct.unpack_from('<6I', pt4, 0)])
print('  0x00-0x60', pt4[:0x60].hex(' '))
print('  0x40-0x80 repr', repr(pt4[0x40:0x80]))
print('  0x10-0x30', pt4[0x10:0x30].hex(' '))
