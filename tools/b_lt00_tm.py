import sys,difflib,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt
import json
G=r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/'
a=load(G+'LT00_EN.cpk'); b=load(G+'B_LT00_EN.cpk')
ta=load_lt(a.plain(a.rows[0])); tb=load_lt(b.plain(b.rows[0]))
# TM from LT00 translations: need original EN strings. Use backup original.
orig=load(r'C:/Dev/Default Project/srwv/backup/LT00_EN_antes_es2.cpk')
to=load_lt(orig.plain(orig.rows[0]))
trans={e:s for e,s in zip(to.strings,ta.strings) if e!=s and len(e)>12}
uniq=[]
for s in tb.strings:
    if s not in uniq: uniq.append(s)
print('unicas B',len(uniq),'TM',len(trans))
exact=sum(1 for s in uniq if s in trans)
print('exactos',exact)
fuzzy=0; samples=[]
for s in uniq:
    if s in trans or len(s)<15: continue
    m=difflib.get_close_matches(s,trans.keys(),n=1,cutoff=0.82)
    if m:
        fuzzy+=1
        if len(samples)<15: samples.append((s,trans[m[0]]))
print('fuzzy',fuzzy)
for x,y in samples: print(' EN',repr(x[:80]),'-> ES',repr(y[:80]))
