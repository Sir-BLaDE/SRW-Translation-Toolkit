import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

c = load(r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es4.cpk')
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
mp = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_compact_es.json', encoding='utf-8'))
sh = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es_short.json', encoding='utf-8'))
es = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es.json', encoding='utf-8'))
eng = set(list(mp.keys()) + list(sh.keys()) + list(es.keys()))

base = 0x2bb0
left = []
i = base
while i < len(pt):
    if 32 <= pt[i] < 127:
        j = i
        while j < len(pt) and 32 <= pt[j] < 127:
            j += 1
        s = pt[i:j].decode('ascii','replace')
        if len(s) >= 3 and s in eng:
            left.append((hex(i), s))
        i = j
    else:
        i += 1
print('English strings remaining in compact:', len(left), left)
