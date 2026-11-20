"""Reconstruye KPACK_P4_LN_EN.CPK en espanol (ids 0,1,3,4)."""
import io
import json
import sys

sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')

from cpk_util import load
import kpack_ln as kln
from srwv_cpkbuild2 import build_ordered

SRC = r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk'
# Actually original is KPACK_P4_LN_EN.CPK in game dir? check
OUT = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es.cpk'

# load maps
m0 = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/ln_id0_es.json', encoding='utf-8'))
m1 = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/ln_id1_es.json', encoding='utf-8'))
m3 = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/ln_id3_descs_es.json', encoding='utf-8'))
m4 = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es.json', encoding='utf-8'))

cf = load(SRC)
print('ficheros', len(cf.rows), 'diag', cf.cpk.diagnose() or 'ok')

new_files = {}

# id0
f0 = [f for f in cf.rows if f['id'] == 0][0]
pt0 = cf.plain(f0)
recs0 = kln.parse0(pt0)
# verify roundtrip
rb0 = kln.build0(recs0)
assert len(rb0) <= len(pt0)
changed0 = 0
for r in recs0:
    s = r['text'].decode('utf-8', 'replace')
    if s in m0 and m0[s] != s:
        r['text'] = m0[s].encode('utf-8')
        changed0 += 1
plain0 = kln.build0(recs0)
plain0 = plain0 + b'\x00'*(len(pt0)-len(plain0))
chk0 = kln.parse0(plain0)
assert len(chk0) == len(recs0)
print('id0 changed', changed0, 'plain', len(plain0))
blob0 = cf.cipher(f0, plain0)
new_files[0] = (blob0, len(plain0))

# id1
f1 = [f for f in cf.rows if f['id'] == 1][0]
pt1 = cf.plain(f1)
d1 = kln.parse1(pt1)
rb1 = kln.build1(d1)
assert len(rb1) <= len(pt1)
changed1 = 0
for i, s in enumerate(d1['strs']):
    t = s.decode('utf-8', 'replace')
    if t in m1 and m1[t] != t:
        d1['strs'][i] = m1[t].encode('utf-8')
        changed1 += 1
plain1 = kln.build1(d1)
plain1 = plain1 + b'\x00'*(len(pt1)-len(plain1))
print('id1 changed', changed1, 'plain', len(plain1))
blob1 = cf.cipher(f1, plain1)
new_files[1] = (blob1, len(plain1))

# id3
f3 = [f for f in cf.rows if f['id'] == 3][0]
pt3 = cf.plain(f3)
strs3, pos3 = kln.parse3(pt3)
rb3 = kln.build3(strs3)
assert len(rb3) <= len(pt3)
changed3 = 0
new_strs3 = []
for s in strs3:
    t = s.decode('utf-8', 'replace')
    if t in m3 and m3[t] != t:
        new_strs3.append(m3[t].encode('utf-8'))
        changed3 += 1
    else:
        new_strs3.append(s)
plain3 = kln.build3(new_strs3)
plain3 = plain3 + b'\x00'*(len(pt3)-len(plain3))
chk3, _ = kln.parse3(plain3)
assert len(chk3) == len(strs3)
print('id3 changed', changed3, 'plain', len(plain3))
blob3 = cf.cipher(f3, plain3)
new_files[3] = (blob3, len(plain3))

# id4: dejar sin traducir por ahora (formato complejo con seccion compacta);
# se mantiene el original ingles.
print('id4: omitido (original ingles conservado)')

out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('escrito', len(out), '->', OUT)

# verify
cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    p2 = cf2.plain(f)
    ok = f['ex'] == len(p2)
    print(' id', f['id'], f['table'], 'size', f['size'], 'ex', f['ex'],
          'plain', len(p2), 'OK' if ok else 'MISMATCH')
