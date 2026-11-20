import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
c = load(r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk')
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)

# dump u32 fields around several record starts found from strings
for base in [0x2bb0, 0x3060, 0x30b8, 0x3880, 0x41e0, 0x4250, 0x42d0, 0x4338]:
    print('=== base %s ===' % hex(base))
    for o in range(base, min(base+0x50, len(pt)), 4):
        v = struct.unpack_from('<I', pt, o)[0]
        b = pt[o:o+16]
        pr = ''.join(chr(x) if 32<=x<127 else '.' for x in b)
        print('  +%02x %08x %s' % (o-base, v, pr))
