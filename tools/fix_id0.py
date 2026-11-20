import sys, io, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as kln

c = load(r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk')
pt = c.plain([f for f in c.rows if f['id']==0][0])
recs = kln.parse0(pt)
m0 = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/ln_id0_es.json', encoding='utf-8'))

def norm(s): return s.replace('\u2014','-').replace('\u2013','-')

normmap = {}
for k,v in m0.items():
    normmap[norm(k)] = (k,v)

seen=set()
new_entries = {}
unmatched = []
for r in recs:
    t = r['text'].decode('utf-8','replace')
    if t in seen: continue
    seen.add(t)
    if t in m0:
        new_entries[t] = m0[t]
        continue
    nt = norm(t)
    if nt in normmap:
        new_entries[t] = normmap[nt][1]
    else:
        unmatched.append(t)

for t in unmatched:
    new_entries[t] = t

io.open(r'C:/Dev/Default Project/srwv/datos/ln_id0_es.json','w',encoding='utf-8').write(
    json.dumps(new_entries, ensure_ascii=False, indent=2))
print('total entries', len(new_entries), 'unmatched(fallback)', len(unmatched))
for u in unmatched:
    print('  UNMATCHED:', repr(u[:60]))