import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt
G=r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/'
a=load(G+'LT00_EN.cpk'); b=load(G+'B_LT00_EN.cpk')
sa=set(load_lt(a.plain(a.rows[0])).strings)
sb=load_lt(b.plain(b.rows[0])).strings
uniq=[s for s in sb if s not in sa]
print('unique',len(uniq))
for s in uniq[:80]: print(repr(s[:100]))
