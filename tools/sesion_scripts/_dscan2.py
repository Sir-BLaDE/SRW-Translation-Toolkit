import os,sys,re,glob,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from nombres_ataques import R
from glosario_nombres3 import R3
M=dict(R);M.update(R3);M.pop('Full Cross',None)
P=os.environ['HOME']+'/mnt/srwv/'
pat=re.compile(r'(?<![\wáéíóúñÁÉÍÓÚÑ])('+'|'.join(re.escape(k) for k in sorted(M,key=len,reverse=True))+r')(?![\wáéíóúñ])')
cnt=collections.Counter()
ter=re.compile(r'\b(SP|ExC|Tac Pts|Spirit Commands|Support Attack|Support Defense|Boost Dash|Great Ace|Focus|Armor|Targeting|Newtype|ExC\.)\b')
tc=collections.Counter()
for f in sorted(glob.glob(P+'outputs/dlc_es/dlc*_en.cpk')):
    k=load(f)
    for r in k.rows:
        t=k.plain(r).decode('utf8','replace')
        for m in pat.finditer(t): cnt[m.group(1)]+=1
        for m in re.finditer(r'\[\[.*?\]\]',t,re.S):
            for x in ter.finditer(m.group(0)): tc[x.group(0)]+=1
print(sum(cnt.values()),cnt.most_common(40)); print(tc)
