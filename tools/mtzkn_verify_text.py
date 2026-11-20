import sys, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
ACC = re.compile(r'[áéíóúñÁÉÍÓÚü]')
for name, p in [
 ('NM', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Nm.cpk'),
 ('PT', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Pt.cpk'),
 ('RT', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk'),
]:
    c = load(p)
    hits = []
    for r in c.rows:
        pt = c.plain(r)
        s = pt.decode('utf-8', 'ignore')
        for m in ACC.finditer(s):
            i = m.start()
            hits.append(s[max(0,i-25):i+25].replace('\n',' '))
    print('=== MtZkn_%s: %d acentos' % (name, len(hits)))
    for h in hits[:6]:
        print('   ', repr(h))
