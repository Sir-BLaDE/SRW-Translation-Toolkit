"""prologue_slot_dump.py - volca slots completos del Prologue para ver la estructura."""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c = load(p)
r = [x for x in c.rows if x['id'] == 0][0]
pt = c.plain(r)
hdr = 24; slot = 70
print('len=%d hdr=%d slot=%d count=%d (24*70=%d, sobran %d)' %
      (len(pt), hdr, slot, (len(pt)-hdr)//slot, (len(pt)-hdr)//slot*slot, (len(pt)-hdr)%slot))
for si in [0, 1, 4, 5, 6, 23]:
    b = pt[hdr+si*slot : hdr+(si+1)*slot]
    print('\n=== slot %d (offset 0x%04x) ===' % (si, hdr+si*slot))
    for off in range(0, len(b), 16):
        ch = b[off:off+16]
        txt = ''.join(chr(x) if 32 <= x < 127 else '.' for x in ch)
        print('  +%02x  %-47s %s' % (off, ch.hex(' '), txt))
