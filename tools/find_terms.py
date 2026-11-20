# -*- coding: utf-8 -*-
"""Busca terminos concretos en los CPK pendientes de traduccion."""
import sys, os, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
terms = [b'Jupiter Empire Soldier', b'Gamillas Soldier', b"Soldier's Medallion",
         b'Neo Zeon Soldier', b'AI', b'Gamillas', b'Soldier']
roots = [
 r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData',
 r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data',
]
files=[]
for root in roots:
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if f.lower().endswith('.cpk'): files.append(os.path.join(dp,f))
print('CPKs:',len(files))
# solo los que sabemos que tienen texto EN pendiente
focus=[f for f in files if any(k in f.upper() for k in
    ['CMN00','B_LT00','MTZKN','KPACK_LN','SYSTEXT','LT00','PROLOGUE'])]
print('foco:',len(focus))
for f in focus:
    try:
        c=load(f)
    except Exception as e:
        continue
    hits={}
    for r in c.rows:
        try: pt=c.plain(r)
        except Exception: continue
        for t in terms:
            if t in pt: hits[t.decode('latin1')]=hits.get(t.decode('latin1'),0)+pt.count(t)
    if hits:
        print(os.path.basename(f),hits)
