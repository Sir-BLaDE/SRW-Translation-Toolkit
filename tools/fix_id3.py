import sys, io, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
path = r'C:/Dev/Default Project/srwv/datos/ln_id3_descs_es.json'
m = json.load(io.open(path, encoding='utf-8'))
# Source uses literal backslash-n; map currently uses real newlines. Convert both.
new = {}
for k,v in m.items():
    nk = k.replace('\n', '\\n')
    nv = v.replace('\n', '\\n')
    new[nk] = nv
io.open(path, 'w', encoding='utf-8').write(json.dumps(new, ensure_ascii=False, indent=2))
print('converted', len(new))
# verify coverage
from cpk_util import load
import kpack_ln as kln
c = load(r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk')
pt = c.plain([f for f in c.rows if f['id']==3][0])
strs, _ = kln.parse3(pt)
longs = [s.decode('utf-8','replace') for s in strs if len(s.decode('utf-8','replace'))>40]
mm = json.load(io.open(path, encoding='utf-8'))
miss = [s for s in set(longs) if s not in mm]
print('long unique', len(set(longs)), 'miss', len(miss))
