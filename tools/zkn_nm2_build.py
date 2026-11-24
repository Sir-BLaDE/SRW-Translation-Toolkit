# -*- coding: utf-8 -*-
"""Construye MtZkn_Nm con DSC2 traducido (in-situ, relleno con espacios). Uso: zkn_nm2_build.py OUT.cpk [dry]"""
import os,re,sys,json,textwrap,hashlib
from zkn_dsc2_scan import *
from srwv_cpkbuild2 import build_ordered
W=int(os.environ.get('W','68'))
P=json.load(open(os.path.expanduser('~/mnt/srwv/datos/lib/nm2_plan.json')))
tr={};cur=None
for line in open(os.path.expanduser('~/mnt/srwv/datos/lib/nm2_es.txt'),encoding='utf8').read().split('\n'):
    m=re.match(r'### (\d+)$',line)
    if m: cur=int(m.group(1));tr[cur]=[]
    elif cur is not None and line.strip(): tr[cur].append(line)
def wrap(paras): return '\n'.join('\n'.join(textwrap.wrap(p,W,break_long_words=False)) for p in paras)
c=load(G+'MtZkn_Nm.cpk'); new={}; over=[]
for r in c.rows:
    i=r['id']
    if str(i) not in P or i not in tr: continue
    v=P[str(i)]; q=bytearray(X(c.plain(r))); f=fields(bytes(q)); s,l=f[b"DSC2"]; l=min(l,len(q)-s)
    body=wrap(tr[i])
    txt=(v['es1']+'\n' if v['overlap'] else '')+body
    txt=v['tag']+txt
    b=txt.encode('utf8')
    if len(b)>l: over.append((i,len(b),l)); continue
    q[s:s+l]=b+b' '*(l-len(b))
    new[i]=(c.cipher(r,bytes(v^0x5E for v in q)),len(q))
print('listas',len(new),'exceden',over)
if len(sys.argv)>2: sys.exit()
blob=build_ordered(G+'MtZkn_Nm.cpk',new); open(sys.argv[1],'wb').write(blob)
k=load(sys.argv[1]); o=load(B+'MtZkn_Nm_original.cpk')
print('filas igual tamano:',all(len(k.plain(a))==len(o.plain(b)) for a,b in zip(k.rows,o.rows)),hashlib.sha256(blob).hexdigest()[:12])
