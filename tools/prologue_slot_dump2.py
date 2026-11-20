"""prologue_slot_dump2.py - volca slots de la fila 1 del Prologue."""
import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c = load(p)
for rid in [1, 3, 7]:
    r = [x for x in c.rows if x['id'] == rid][0]
    pt = c.plain(r)
    cnt = struct.unpack_from('<H', pt, 0)[0]
    slot = (len(pt)-24)//cnt
    print('\n######## FILA %d len=%d count=%d slot=%d (resto=%d) ########' %
          (rid, len(pt), cnt, slot, (len(pt)-24) % cnt))
    for si in [0, 1, 2, 3]:
        b = pt[24+si*slot : 24+(si+1)*slot]
        print('\n === slot %d ===' % si)
        for off in range(0, len(b), 16):
            ch = b[off:off+16]
            txt = ''.join(chr(x) if 32 <= x < 127 else '.' for x in ch)
            print('  +%02x  %-47s %s' % (off, ch.hex(' '), txt))
