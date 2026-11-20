import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

c = load(r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk')
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)

def align4(v): return (v+3)&~3

# Region 1: type-5 with subtitle, 0x2bb0 .. 0x305c
print('=== REGION 1: type5 + subtitle ===')
off = 0x2bb0
while off < 0x305c:
    typ, tlen = struct.unpack_from('<2I', pt, off)
    title = pt[off+8:off+8+tlen].split(b'\0')[0].decode('utf-8','replace')
    p = off + 8 + align4(tlen)
    slen = struct.unpack_from('<I', pt, p)[0]; p += 4
    sub = pt[p:p+slen].split(b'\0')[0].decode('utf-8','replace')
    p += align4(slen)
    p += 4  # pad
    scen = pt[p:p+8].split(b'\0')[0].decode('ascii','replace')
    print('%s typ=%d tlen=%2d slen=%2d scen=%-5s title=%r sub=%r' % (hex(off), typ, tlen, slen, scen, title, sub))
    # determine size: find next type5 start
    nxt = p + 8 + 4 + 8  # after scen + offset + v1v2
    while nxt + 8 <= len(pt):
        if pt[nxt:nxt+4] == b'\x05\x00\x00\x00':
            nl = struct.unpack_from('<I', pt, nxt+4)[0]
            if 4 <= nl <= 0x80: break
        nxt += 4
    off = nxt

# Region 2: type-B, 0x3060 .. 0x41dc
print('\n=== REGION 2: type-B (direct len) ===')
off = 0x3060
while off < 0x41dc:
    tlen = struct.unpack_from('<I', pt, off)[0]
    if not (4 <= tlen <= 0x80):
        print('STOP at', hex(off), 'tlen', tlen); break
    title = pt[off+4:off+4+tlen].split(b'\0')[0].decode('utf-8','replace')
    scen = pt[off+0x1c:off+0x24].split(b'\0')[0].decode('ascii','replace')
    size = 72 + align4(tlen)
    print('%s tlen=%2d scen=%-5s size=%d title=%r' % (hex(off), tlen, scen, size, title))
    off += size

# Region 3: type5 simple, 0x41e0 .. end
print('\n=== REGION 3: type5 simple ===')
off = 0x41e0
while off + 8 <= len(pt):
    typ, tlen = struct.unpack_from('<2I', pt, off)
    if typ != 5 or not (0 <= tlen <= 0x80):
        print('STOP at', hex(off), 'typ', typ, 'tlen', tlen); break
    title = pt[off+8:off+8+tlen].split(b'\0')[0].decode('utf-8','replace')
    scen = pt[off+0x1c:off+0x24].split(b'\0')[0].decode('ascii','replace')
    print('%s tlen=%2d scen=%-5s title=%r' % (hex(off), tlen, scen, title))
    off += 72 + align4(tlen)
