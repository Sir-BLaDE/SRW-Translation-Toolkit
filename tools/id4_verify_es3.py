import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

for label, path in [('INST', r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
                    ('ES3', r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk')]:
    c = load(path)
    f4 = [f for f in c.rows if f['id'] == 4][0]
    pt = c.plain(f4)
    sh = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es_short.json', encoding='utf-8'))
    es = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es.json', encoding='utf-8'))
    engkeys = set(es.keys())
    def align4(v): return (v+3)&~3
    off = 0x10
    en = []
    n = 0
    while off + 0x40 <= len(pt):
        ln = struct.unpack_from('<I', pt, off+0x3c)[0]
        if not (0 < ln <= 0x1000): break
        txt = pt[off+0x40:off+0x40+ln].split(b'\0')[0].decode('utf-8','replace')
        if txt in engkeys: en.append((n, txt))
        off += 0x48 + align4(ln)
        n += 1
    print(label, 'primary English remaining:', len(en), en[:10])
