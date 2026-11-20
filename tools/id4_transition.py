import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
c = load(r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk')
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
for i in range(0x2a50, 0x2bc0, 16):
    chunk = pt[i:i+16]
    pr = ''.join(chr(x) if 32<=x<127 else '.' for x in chunk)
    print('%s  %s  %s' % (hex(i), chunk.hex(' '), pr))
