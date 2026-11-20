import sys, io
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es.cpk'
MOD = r'C:/Dev/Default Project/srwv/outputs/id4_inplace_on_translated.bin'
OUT = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es2.cpk'

cf = load(SRC)
f4 = [f for f in cf.rows if f['id']==4][0]
plain = open(MOD, 'rb').read()
orig_plain = cf.plain(f4)
assert len(plain) == len(orig_plain), 'size mismatch %d vs %d' % (len(plain), len(orig_plain))
blob = cf.cipher(f4, plain)
new_files = {4: (blob, len(plain))}
out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('written', len(out))

cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    p = cf2.plain(f)
    print(' id', f['id'], 'ex', f['ex'], 'plain', len(p), 'OK' if f['ex']==len(p) else 'BAD')