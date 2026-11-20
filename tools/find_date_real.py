# -*- coding: utf-8 -*-
"""Buscar 'November 11, 2199' (y variantes) en TODOS los CPK del juego."""
import os, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

G = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
NEEDLES = [b'November 11', b'ovember 11', b'Pluto Airspace', b'2199 NCC']

def strings(b):
    out=[]
    start=0
    for i,c in enumerate(b):
        if c==0:
            if i-start>=6:
                out.append(b[start:i])
            start=i+1
    return out

found=0
for root, dirs, files in os.walk(G):
    for fn in files:
        if not fn.lower().endswith('.cpk'):
            continue
        p=os.path.join(root,fn)
        try:
            c=load(p)
        except Exception:
            continue
        for r in c.rows:
            try:
                pt=c.plain(r)
            except Exception:
                continue
            for nd in NEEDLES:
                if nd in pt:
                    idx=pt.find(nd)
                    # mostrar contexto ASCII imprimible
                    ctx=pt[max(0,idx-30):idx+len(nd)+60]
                    ctx=''.join(chr(x) if 32<=x<127 else '.' for x in ctx)
                    print('%s | fila %d | %s' % (p.replace(G+os.sep,''), r['id'], nd.decode()))
                    print('   ',ctx)
                    found+=1
                    break
print('total coincidencias:',found)
