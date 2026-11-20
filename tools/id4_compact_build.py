import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es4.cpk'
mp = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_compact_es.json', encoding='utf-8'))

cf = load(SRC)
f4 = [f for f in cf.rows if f['id'] == 4][0]
plain = bytearray(cf.plain(f4))
orig = bytes(plain)

# Replace each English literal in-place, padding with zeros to keep exactly the same length.
# Sort by length desc so longer strings are replaced first (avoid partial overlaps).
def replace_literal(buf, en, es):
    eb = en.encode('utf-8')
    zb = es.encode('utf-8')
    count = 0
    pos = 0
    while True:
        i = buf.find(eb, pos)
        if i < 0: break
        # field extends over trailing zero bytes
        j = i + len(eb)
        while j < len(buf) and buf[j] == 0:
            j += 1
        field = j - i
        if len(zb) > field:
            print('  OVER %r -> %r blen=%d field=%d' % (en, es, len(zb), field))
            pos = i + 1
            continue
        buf[i:j] = zb + b'\0'*(field - len(zb))
        count += 1
        pos = i + field
    return count

total = 0
for en, es in sorted(mp.items(), key=lambda x: -len(x[0])):
    n = replace_literal(plain, en, es)
    if n: total += n
    # print('%r -> %r : %d' % (en, es, n))

assert len(plain) == len(orig)
blob = cf.cipher(f4, bytes(plain))
out = build_ordered(SRC, {4: (blob, len(plain))})
open(OUT,'wb').write(out)
print('total replacements', total, 'written', len(out))
cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    p = cf2.plain(f)
    print(' id', f['id'], 'ex', f['ex'], 'plain', len(p), 'OK' if f['ex']==len(p) else 'BAD')
