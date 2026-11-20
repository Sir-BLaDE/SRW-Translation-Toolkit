"""prologue_jp_dump.py - compara slots EN vs JP para entender los fragmentos."""
import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
for lang in ['EN','JP']:
    p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/%s/Prologue.cpk' % lang
    c = load(p)
    r = [x for x in c.rows if x['id'] == 1][0]
    pt = c.plain(r)
    cnt = struct.unpack_from('<H', pt, 0)[0]
    slot = (len(pt)-24)//cnt
    print('\n##### %s fila1 len=%d count=%d slot=%d #####' % (lang, len(pt), cnt, slot))
    for si in range(min(6,cnt)):
        b = pt[24+si*slot : 24+(si+1)*slot]
        # mostrar como texto utf-8, sustituyendo no-imprimibles
        s = ''.join(chr(x) if 32 <= x < 127 else ('·' if x==0 else '.') for x in b[:60])
        print(' slot %d: %s' % (si, s))
