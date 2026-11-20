# -*- coding: utf-8 -*-
"""lib_build.py NAME BASE.cpk OUT.cpk : sustituye DSCR/DSC2 in-situ (mismo tamano de campo, relleno con espacios)."""
import sys,os,re,json,glob,hashlib
sys.path.insert(0,os.path.expanduser('~/mnt/srwv/tools'))
from lib_extract import *
from srwv_cpkbuild2 import build_ordered
name=sys.argv[1];base=sys.argv[2];out=sys.argv[3]
keys={int(k):bytes.fromhex(v) for k,v in json.load(open(S+f'datos/lib/{name.lower()}_keys.json')).items()}
tr={}
for f in sorted(glob.glob(S+f'datos/lib/{name.lower()}_*_es.txt')):
    cur=None;buf=[]
    def put():
        if cur is not None:
            t='\n'.join(buf).rstrip('\n')
            tr[cur]=t
    for line in open(f,encoding='utf-8').read().split('\n'):
        m=re.match(r'### (\d+)( \[\d+\])?$',line)
        if m:
            put();cur=int(m.group(1));buf=[]
        else: buf.append(line)
    put()
bymap={keys[i]:t for i,t in tr.items() if i in keys}
over=[];done=0
o=load(S+f'backup/MtZkn_{name}_original.cpk')
b=load(base)
assert len(o.rows)==len(b.rows)
new={}
for ro,rb in zip(o.rows,b.rows):
    po=bytes(x^0x5E for x in o.plain(ro));pb=bytearray(x^0x5E for x in b.plain(rb))
    assert len(po)==len(pb)
    pr=parse_row(po);ch=False
    for kind,s,ln in pr:
        t=po[s:s+ln]
        if t in bymap:
            es=bymap[t].encode('utf-8')
            if len(es)>ln: continue
            pb[s:s+ln]=es+b' '*(ln-len(es));ch=True;done+=1
    if ch: new[rb['id']]=(b.cipher(rb,bytes(x^0x5E for x in pb)),len(pb))
for i,t in sorted(tr.items()):
    if i in keys and len(t.encode('utf-8'))>len(keys[i]): over.append((i,len(t.encode('utf-8')),len(keys[i])))
print(name,'traducidos',len(tr),'de',len(keys),'campos escritos',done,'exceden',len(over))
open(S+f'datos/lib/{name.lower()}_over.txt','w').write('\n'.join(f'{i} {a}>{b}' for i,a,b in over))
if len(sys.argv)>4 and sys.argv[4]=='dry': sys.exit()
blob=build_ordered(base,new);open(out,'wb').write(blob)
k=load(out)
ok=all(len(k.plain(r))==len(o.plain(q)) and r['ex']==len(k.plain(r)) for r,q in zip(k.rows,o.rows))
print('tamano de fila igual al original:',ok,hashlib.sha256(blob).hexdigest()[:12])
