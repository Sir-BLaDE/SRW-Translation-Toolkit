# -*- coding: utf-8 -*-
"""zkn_rt2_build.py NAME OUT.cpk [dry] : DSC2 traducido in-situ. Modos: (defecto) solapa->es1+cuerpo, cont->tag+cuerpo; !FULL; !COPY."""
import os,re,sys,json,textwrap,hashlib
from zkn_dsc2_scan import *
from srwv_cpkbuild2 import build_ordered
NAME=sys.argv[1]; W=int(os.environ.get('W','68'))
D=os.path.expanduser('~/mnt/srwv/datos/lib/')
P=json.load(open(D+NAME.lower()+'2_plan.json')) if os.path.exists(D+NAME.lower()+'2_plan.json') else {}; tr={};mode={};cur=None
for line in open(D+NAME.lower()+'2_es.txt',encoding='utf8').read().split('\n'):
    m=re.match(r'### (\d+)$',line)
    if m: cur=int(m.group(1));tr[cur]=[];mode[cur]=''
    elif line.startswith('!') and cur is not None and not tr[cur]: mode[cur]=line
    elif cur is not None and line.strip(): tr[cur].append(line)
def wrap(paras): return '\n'.join('\n'.join(textwrap.wrap(p,W,break_long_words=False)) for p in paras)
c=load(G+f'MtZkn_{NAME}.cpk'); new={}; over=[]
for r in c.rows:
    i=r['id']
    if i not in tr: continue
    v=P.get(str(i)) or {'tag':'<srw-tag=before-clear-text-here>\n','overlap':False,'es1':''}; q=bytearray(X(c.plain(r))); f=fields(bytes(q)); s,l=f[b'DSC2']; l=min(l,len(q)-s)
    es1=v['es1'].split('DSC2')[0].rstrip()
    if mode[i]=='!COPY': txt=es1
    elif mode[i]=='!FULL': txt=v['tag']+wrap(tr[i])
    else: txt=v['tag']+((es1+'\n') if v['overlap'] else '')+wrap(tr[i])
    b=txt.encode('utf8')
    if len(b)>l: over.append((i,len(b),l)); continue
    q[s:s+l]=b+b' '*(l-len(b))
    new[i]=(c.cipher(r,bytes(x^0x5E for x in q)),len(q))
DS={};cur=None
if os.path.exists(D+NAME.lower()+'2_dscr_es.txt'):
    for line in open(D+NAME.lower()+'2_dscr_es.txt',encoding='utf8').read().split('\n'):
        m=re.match(r'### (\d+)$',line)
        if m: cur=int(m.group(1));DS[cur]=[]
        elif cur is not None and line.strip(): DS[cur].append(line)
for r in c.rows:
    i=r['id']
    if i not in DS: continue
    q=bytearray(X(c.plain(new[i][0] and r))) if False else bytearray(X(c.plain(r))) if i not in new else bytearray(X(c.plain(r)))
    # partir de la version ya modificada si existe
    if i in new: q=bytearray(x^0x5E for x in c.plain_from(new[i][0],r)) if hasattr(c,'plain_from') else q
    f=fields(bytes(q)); s,l=f[b'DSCR']; tagpos=f[b'DSC2'][0]-8; avail=tagpos-s; lim=min(l,avail)
    b=wrap(DS[i]).encode('utf8')
    if len(b)>lim: over.append(('DSCR',i,len(b),lim)); continue
    q[s:s+avail]=b+b' '*(avail-len(b))
    new[i]=(c.cipher(r,bytes(x^0x5E for x in q)),len(q))
print('listas',len(new),'exceden',over)
if len(sys.argv)>3: sys.exit()
blob=build_ordered(G+f'MtZkn_{NAME}.cpk',new); open(sys.argv[2],'wb').write(blob)
k=load(sys.argv[2]); o=load(B+f'MtZkn_{NAME}_original.cpk')
print('filas igual tamano:',all(len(k.plain(a))==len(o.plain(b)) for a,b in zip(k.rows,o.rows)),hashlib.sha256(blob).hexdigest()[:12])
