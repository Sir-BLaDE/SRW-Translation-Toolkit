import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt
G=r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/'
a=load(G+'LT00_EN.cpk'); b=load(G+'B_LT00_EN.cpk')
for name,c in [('LT00',a),('B_LT00',b)]:
    r=c.rows[0]; pt=c.plain(r); t=load_lt(pt)
    print(name,'plain',len(pt),'count',t.count,'strings',len(t.strings))
    print(' sample', [repr(s[:60]) for s in t.strings[:8]])
sa=set(load_lt(a.plain(a.rows[0])).strings)
sb=load_lt(b.plain(b.rows[0])).strings
print('B strings in LT00:',sum(1 for s in sb if s in sa),'/',len(sb))
print('B unique not in LT00:',sum(1 for s in sb if s not in sa))
