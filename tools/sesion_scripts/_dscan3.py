import os,sys,re,glob,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from nombres_ataques import R
from glosario_nombres3 import R3
M=dict(R);M.update(R3);M.pop('Full Cross',None)
P=os.environ['HOME']+'/mnt/srwv/'
pat=re.compile(r'(?<![\w])('+'|'.join(re.escape(k) for k in sorted(M,key=len,reverse=True))+r')(?![\w])')
B=re.compile(r'\[\[(.*?)\]\]',re.S)
ok=0;miss=[]
for f in sorted(glob.glob(P+'outputs/dlc_es/dlc*_en.cpk')):
    n=os.path.basename(f); k=load(f); o=load(P+'backup/dlc_en/'+n)
    for r,ro in zip(k.rows,o.rows):
        te=B.findall(k.plain(r).decode('utf8','replace')); to=B.findall(ro and o.plain(ro).decode('utf8','replace'))
        if len(te)!=len(to): print('DESALINEADO',n,r['id'],len(te),len(to)); continue
        for a,b in zip(to,te):
            for m in pat.finditer(a):
                if M[m.group(1)] in b: ok+=1
                else: miss.append((n,m.group(1),b.replace('\r\n',' / ')[:160]))
print(ok,len(miss))
c=collections.Counter(x[1] for x in miss); print(c.most_common(40))
for x in miss[:25]: print(x)
