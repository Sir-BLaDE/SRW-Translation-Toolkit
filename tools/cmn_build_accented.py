import sys, pathlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_buildbltu import build as build_bltu
from srwv_bltu import load as load_bltu

ORIG = r'C:/Dev/Default Project/srwv/backup/CMN00_CPK_original.cpk'
CSV  = r'C:/Dev/Default Project/srwv/datos/lineas_batalla_final_es6.csv'
BIN  = r'C:/Dev/Default Project/srwv/outputs/cmn_f1_es6.bin'
OUT  = r'C:/Dev/Default Project/srwv/outputs/CMN00_CPK_final_es6.cpk'

cf = load(ORIG)
rows = {r['id']: r for r in cf.rows}
orig_f1 = cf.plain(rows[1])
print('original f1', len(orig_f1))

new_f1 = build_bltu(orig_f1, CSV)
pathlib.Path(BIN).write_bytes(new_f1)
print('new f1', len(new_f1))
t = load_bltu(new_f1)
alls = [x[3] for x in t.all_strings()]
acc = [s for s in alls if any(ord(c) > 127 for c in s)]
print('chunks', len(t.chunks), 'strings', len(alls), 'accented', len(acc))
for s in acc[:5]: print('  ', repr(s[:70]))

new = {1: (cf.cipher(rows[1], new_f1), len(new_f1))}
blob = build_ordered(ORIG, new)
pathlib.Path(OUT).write_bytes(blob)
print('escrito', OUT, len(blob))
# verify
c2 = load(OUT)
for r in c2.rows:
    pt = c2.plain(r)
    print('id', r['id'], 'ex', r['ex'], 'plain', len(pt), 'OK' if r['ex'] == len(pt) else 'FAIL')
c2.cpk.diagnose()
