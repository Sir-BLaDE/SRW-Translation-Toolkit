import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

c = load(r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk')
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
es = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es.json', encoding='utf-8'))

base = 0x2bb0
def align4(v): return (v+3)&~3

# Dump every ASCII-ish run in compact region to find titles
print('=== printable strings in compact region ===')
i = base
while i < len(pt):
    if 32 <= pt[i] < 127:
        j = i
        while j < len(pt) and 32 <= pt[j] < 127:
            j += 1
        s = pt[i:j].decode('ascii','replace')
        if len(s) >= 3:
            print('%s %r %s' % (hex(i), s, 'EN' if s in es else ''))
        i = j
    else:
        i += 1
