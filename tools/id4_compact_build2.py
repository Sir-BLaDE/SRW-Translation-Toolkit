import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es5.cpk'
tmap = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_compact_es.json', encoding='utf-8'))

cf = load(SRC)
f4 = [f for f in cf.rows if f['id'] == 4][0]
plain = bytearray(cf.plain(f4))
orig = bytes(plain)

def align4(v): return (v+3)&~3

def put(buf, off, ln, en, es):
    """Write es into a known title field of length ln, padded with zeros."""
    cur = bytes(buf[off:off+ln]).split(b'\0')[0].decode('utf-8','replace')
    if cur != en:
        print('  MISMATCH at %s expected %r got %r' % (hex(off), en, cur))
        return False
    zb = es.encode('utf-8')
    if len(zb) > ln:
        print('  OVER %r -> %r blen=%d ln=%d' % (en, es, len(zb), ln))
        return False
    buf[off:off+ln] = zb + b'\0'*(ln-len(zb))
    return True

changed = 0

# Region 1: type5 + subtitle, 0x2b54 .. 0x305c
# (0x2b54 is a type5 record in the transition zone, before the main 0x2bb0 block)
off = 0x2b54
while off < 0x305c:
    typ, tlen = struct.unpack_from('<2I', plain, off)
    if typ != 5 or not (4 <= tlen <= 0x80):
        print('REG1 STOP', hex(off), typ, tlen); break
    title = bytes(plain[off+8:off+8+tlen]).split(b'\0')[0].decode('utf-8','replace')
    if title in tmap and put(plain, off+8, tlen, title, tmap[title]): changed += 1
    p = off + 8 + align4(tlen)
    slen = struct.unpack_from('<I', plain, p)[0]
    if 4 <= slen <= 0x80:
        sub = bytes(plain[p+4:p+4+slen]).split(b'\0')[0].decode('utf-8','replace')
        if sub in tmap and put(plain, p+4, slen, sub, tmap[sub]): changed += 1
    # advance: find next type5
    q = p + 4 + align4(slen)
    # pad u32 + scen 8 + offset 4 + v1v2 8 = 24; then search
    q += 24
    while q + 8 <= len(plain):
        if plain[q:q+4] == b'\x05\x00\x00\x00':
            nl = struct.unpack_from('<I', plain, q+4)[0]
            if 4 <= nl <= 0x80: break
        q += 4
    if q >= 0x305c: break
    off = q

# Region 2: type-B, 0x3060 .. 0x3c28 (has titles), then 0x4180..0x41dc
for start, end in [(0x3060, 0x3c28), (0x4180, 0x41dc)]:
    off = start
    while off < end:
        tlen = struct.unpack_from('<I', plain, off)[0]
        if not (4 <= tlen <= 0x80):
            print('REG2 STOP', hex(off), 'tlen', tlen); break
        title = bytes(plain[off+4:off+4+tlen]).split(b'\0')[0].decode('utf-8','replace')
        if title in tmap and put(plain, off+4, tlen, title, tmap[title]): changed += 1
        off += 72 + align4(tlen)

# Region 3: type5 simple, 0x41e0 onward (Stage Clear, 500), plus Scenario Guidance at 0x42d0
# handle 0x41e0, 0x4234 manually via type5; 0x42d0 via type-B
for off in [0x41e0, 0x4234]:
    typ, tlen = struct.unpack_from('<2I', plain, off)
    title = bytes(plain[off+8:off+8+tlen]).split(b'\0')[0].decode('utf-8','replace')
    if title in tmap and put(plain, off+8, tlen, title, tmap[title]): changed += 1
# Scenario Guidance at 0x42d0 is type-16: typ at +0, tlen at +4, title at +8
off = 0x42d0
typ, tlen = struct.unpack_from('<2I', plain, off)
title = bytes(plain[off+8:off+8+tlen]).split(b'\0')[0].decode('utf-8','replace')
if title in tmap and put(plain, off+8, tlen, title, tmap[title]): changed += 1

# Manual: type-B record at 0x2af0 (tlen=12 at +0, title at +4) in transition zone
if put(plain, 0x2af4, 12, 'Stay or Go?', '¿Vas o no?'): changed += 1

assert len(plain) == len(orig)
blob = cf.cipher(f4, bytes(plain))
out = build_ordered(SRC, {4: (blob, len(plain))})
open(OUT,'wb').write(out)
print('changed', changed, 'written', len(out))
cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    p = cf2.plain(f)
    print(' id', f['id'], 'ex', f['ex'], 'plain', len(p), 'OK' if f['ex']==len(p) else 'BAD')
