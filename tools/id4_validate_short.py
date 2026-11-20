import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
sh = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es_short.json', encoding='utf-8'))

def align4(v): return (v+3)&~3
off = 0x10
slots = {}
while off + 0x40 <= len(pt):
    ln = struct.unpack_from('<I', pt, off+0x3c)[0]
    if not (0 < ln <= 0x1000): break
    txt = pt[off+0x40:off+0x40+ln].split(b'\0')[0].decode('utf-8','replace')
    if txt in sh and txt not in slots: slots[txt] = ln
    off += 0x48 + align4(ln)

print('English present:', len(slots), 'in short map:', len(sh))
problems = []
for en, ln in slots.items():
    tr = sh.get(en)
    if tr is None:
        problems.append((en, ln, 'MISSING', None, None)); continue
    blen = len(tr.encode('utf-8'))
    if blen + 1 > ln:
        problems.append((en, ln, 'OVER', blen, tr))
print('problems:', len(problems))
for p in problems:
    print('  %-45s ln=%2d %s blen=%s %s' % (p[0][:45], p[1], p[2], p[3], p[4] or ''))
