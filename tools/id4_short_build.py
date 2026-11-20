import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K
from srwv_cpkbuild2 import build_ordered

SRC = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es2.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk'
sh = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es_short.json', encoding='utf-8'))

cf = load(SRC)
f4 = [f for f in cf.rows if f['id'] == 4][0]
plain = bytearray(cf.plain(f4))
orig_len = len(plain)

def align4(v): return (v+3)&~3

off = 0x10
changed = 0
while off + 0x40 <= len(plain):
    ln = struct.unpack_from('<I', plain, off+0x3c)[0]
    if not (0 < ln <= 0x1000): break
    txt = bytes(plain[off+0x40:off+0x40+ln]).split(b'\0')[0].decode('utf-8','replace')
    if txt in sh:
        tr = sh[txt].encode('utf-8')
        assert len(tr) <= ln, 'overflow %r %d > %d' % (txt, len(tr), ln)
        plain[off+0x40:off+0x40+ln] = tr + b'\0'*(ln-len(tr))
        changed += 1
    off += 0x48 + align4(ln)

assert len(plain) == orig_len
blob = cf.cipher(f4, bytes(plain))
out = build_ordered(SRC, {4: (blob, len(plain))})
open(OUT,'wb').write(out)
print('changed', changed, 'written', len(out))
cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    p = cf2.plain(f)
    print(' id', f['id'], 'ex', f['ex'], 'plain', len(p), 'OK' if f['ex']==len(p) else 'BAD')
