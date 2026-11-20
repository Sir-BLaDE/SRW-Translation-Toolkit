import sys, re, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt
cf=load(r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')
rows={r['id']:r for r in cf.rows}; p3=cf.plain(rows[3]); HDR=40; W=4096; N=(len(p3)-HDR)//36
adv={}
for g in range(N):
    off=HDR+g*36; u=struct.unpack_from('<I',p3,off)[0]; fl=struct.unpack_from('<8f',p3,off+4)
    adv.setdefault(u,fl[5])
def w(s):
    s=re.sub(r'\\c\d|\\a\d\d|\$[A-Za-z]\w*|%[ds]','',s)
    return max(sum(adv.get(ord(c),20.0) for c in p) for p in re.split(r'\r?\n|\\n|\n',s))

orig=r'C:/Dev/Default Project/srwv/backup/SysText_original.cpk'
import os
if not os.path.exists(orig):
    orig=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText - copia.cpk'
a=load(orig); b=load(r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk')
ta=load_lt(a.plain([r for r in a.rows if r['id']==0][0]))
tb=load_lt(b.plain([r for r in b.rows if r['id']==0][0]))
print('counts',ta.count,tb.count)
bad=[]
for i,(x,y) in enumerate(zip(ta.strings,tb.strings)):
    if x==y or not y: continue
    if w(y)>w(x)*1.15 or w(y)>700:
        bad.append((w(y)/max(w(x),1),i,x,y))
bad.sort(reverse=True,key=lambda z:z[0])
print('sospechosos',len(bad))
for r,i,x,y in bad[:40]:
    print(' %.2f [%d] EN=%r ES=%r'%(r,i,x[:60],y[:70]))
