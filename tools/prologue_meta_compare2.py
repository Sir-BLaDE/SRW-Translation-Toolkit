"""Compara la cola de metadatos (ultimos 22 bytes) de slots EN vs JP."""
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
    print('\n%s slot=%d' % (lang, slot))
    for si in range(6):
        b = pt[24+si*slot:24+(si+1)*slot]
        print(' slot %d cola22=%s' % (si, b[-22:].hex(' ')))
