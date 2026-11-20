import sys,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c=load(p)
for r in c.rows:
    pt=c.plain(r)
    ss=re.findall(rb'[ -~]{6,}',pt)
    if ss:
        print('id',r['id'],'size',r['size'],'strings',len(ss))
        for s in ss[:8]: print('  ',repr(s[:100].decode('ascii','ignore')))
