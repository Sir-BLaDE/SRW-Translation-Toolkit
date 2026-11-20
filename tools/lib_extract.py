# -*- coding: utf-8 -*-
import sys,os,re,struct,json
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'))
import cpk_util,fastinf
cpk_util.inflate=fastinf.inflate
from cpk_util import load
S=os.path.expanduser('~/mnt/srwv/')
def fld(p,tag,pos=0):
    """devuelve (start,len) del primer campo valido tag desde pos"""
    while True:
        i=p.find(tag,pos)
        if i<0: return None
        b=p[i+4:i+8]
        if len(b)<4: return None
        if b[1:4]==b'^^^': ln=b[0]
        elif b[2:4]==b'^^': ln=struct.unpack('<H',b[:2])[0]
        else: pos=i+4; continue
        s=i+8 if b[2:4]==b'^^' and b[1:4]!=b'^^^' else i+8
        return i,s,ln
def parse_row(p):
    out=[]
    pos=0
    while True:
        f=fld(p,b'DSCR',pos)
        if not f: return out
        i,s,ln=f
        if s+ln<=len(p) and p[s+ln:s+ln+4]==b'DSC2':
            out.append(('DSCR',s,ln))
            g=fld(p,b'DSC2',s+ln)
            if g and g[0]==s+ln:
                i2,s2,l2=g
                if s2+l2<=len(p) and p[s2+l2:s2+l2+4]==b'KANA':
                    out.append(('DSC2',s2,l2))
            return out
        pos=i+4
def collect(name):
    o=load(S+f'backup/MtZkn_{name}_original.cpk')
    items={}  # text bytes -> list of (row,kind)
    bad=0
    for r in o.rows:
        p=bytes(b^0x5E for b in o.plain(r))
        pr=parse_row(p)
        if not pr: bad+=1; continue
        for kind,s,ln in pr:
            t=p[s:s+ln]
            if kind=='DSC2' and t.startswith(b'<srw-tag') and ln<40: continue
            items.setdefault(t,[]).append((r['id'],kind))
    return o,items,bad
if __name__=='__main__':
    os.makedirs(S+'datos/lib',exist_ok=True)
    BATCH=26000
    for name in ('Nm','Pt','Rt'):
        o,items,bad=collect(name)
        print(name,'rows sin campos',bad,'textos unicos',len(items),sum(len(t) for t in items))
        order=sorted(items,key=lambda t:(items[t][0][0],items[t][0][1]))
        k=0;cur=[];sz=0
        def flush():
            global k,cur,sz
            if not cur: return
            with open(S+f'datos/lib/{name.lower()}_{k:02d}_in.txt','w',encoding='utf-8') as f:
                for idx,t in cur:
                    f.write(f'### {idx} [{len(t)}]\n'+t.decode('utf-8')+'\n')
            k+=1;cur=[];sz=0
        keys={}
        for n,t in enumerate(order):
            keys[n]=t.hex()
            if sz+len(t)>BATCH: flush()
            cur.append((n,t));sz+=len(t)
        flush()
        json.dump(keys,open(S+f'datos/lib/{name.lower()}_keys.json','w'))
        print(name,'lotes',k)
