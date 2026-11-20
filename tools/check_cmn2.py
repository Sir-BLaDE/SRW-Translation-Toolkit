import sys, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/CMN00.CPK'
c = load(p)
acc_re = re.compile(r'[\u00c0-\u00ff\u00a1\u00bf]')
for f in c.rows:
    pt = c.plain(f)
    u = pt.decode('utf-8','ignore')
    toks = re.findall(r'[A-Za-zÁÉÍÓÚáéíóúñÑ¿¡][A-Za-zÁÉÍÓÚáéíóúñÑ¿¡\s\',\.!?-]{4,}', u)
    acc = [t for t in toks if acc_re.search(t)]
    inv = [t for t in toks if '¿' in t or '¡' in t]
    print('file id=%s len=%d tokens=%d accented=%d inv=%d' % (f['id'], len(pt), len(toks), len(acc), len(inv)))
    for t in acc[:8]: print('   ACC', repr(t[:70]))
    for t in inv[:4]: print('   INV', repr(t[:70]))
