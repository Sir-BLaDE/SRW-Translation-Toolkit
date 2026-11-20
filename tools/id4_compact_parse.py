import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
base = 0x2bb0

def align4(v):
    return (v + 3) & ~3

off = base
recs = []
while off + 8 <= len(pt):
    typ, tlen = struct.unpack_from('<2I', pt, off)
    if typ != 5 or not (0 <= tlen <= 0x80):
        print('STOP at', hex(off), 'typ', typ, 'tlen', tlen,
              'bytes', pt[off:off+16].hex(' '))
        break
    title = pt[off+8:off+8+tlen].split(b'\0')[0].decode('utf-8', 'replace')
    p = off + 8 + align4(tlen)
    slen = struct.unpack_from('<I', pt, p)[0]
    if slen > 0x80:
        print('BAD slen at', hex(p), slen)
        break
    p += 4
    sub = pt[p:p+slen].split(b'\0')[0].decode('utf-8', 'replace')
    p += align4(slen)
    pad = struct.unpack_from('<I', pt, p)[0]
    p += 4
    scen = pt[p:p+8].split(b'\0')[0].decode('ascii', 'replace')
    p += 8
    offset = struct.unpack_from('<I', pt, p)[0]
    p += 4
    v1, v2 = struct.unpack_from('<2I', pt, p)
    p += 8
    recs.append({'off': off, 'title': title, 'sub': sub, 'scen': scen,
                 'offset': offset, 'v1': v1, 'v2': v2, 'pad': pad,
                 'tlen': tlen, 'slen': slen})
    off = p + 0x24   # 0x24 bytes from v2 end to next record

print('parsed', len(recs), 'compact records; end', hex(off), 'len', hex(len(pt)))
for i, r in enumerate(recs):
    print('%3d off=%s scen=%-6s offval=%s v1=%3d v2=%3d tlen=%2d slen=%2d title=%r sub=%r' % (
        i, hex(r['off']), r['scen'], hex(r['offset']), r['v1'], r['v2'],
        r['tlen'], r['slen'], r['title'][:42], r['sub'][:26]))
