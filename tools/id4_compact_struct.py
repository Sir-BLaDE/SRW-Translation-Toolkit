import sys, struct, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
base = 0x2bb0

# Find all record starts: pattern 05 00 00 00 followed by a small length u32
starts = []
for m in re.finditer(b'\x05\x00\x00\x00', pt[base:]):
    s = base + m.start()
    if s + 8 <= len(pt):
        ln = struct.unpack_from('<I', pt, s + 4)[0]
        if 4 <= ln <= 0x40:
            starts.append(s)
print('records found:', len(starts))
deltas = [starts[i+1]-starts[i] for i in range(len(starts)-1)]
from collections import Counter
print('deltas distribution:', Counter(deltas).most_common(10))
print('first starts:', [hex(s) for s in starts[:5]])
print('last starts:', [hex(s) for s in starts[-5:]])
print('tail after last:', len(pt) - starts[-1])

# Dump one record as u32 fields
s = starts[0]
size = deltas[0] if deltas else 0x68
print('\nrecord size', size)
for off in range(0, size, 4):
    v = struct.unpack_from('<I', pt, s + off)[0]
    b = pt[s+off:s+off+16]
    printable = ''.join(chr(x) if 32 <= x < 127 else '.' for x in b)
    print('  +%02x: %08x  %s' % (off, v, printable))
