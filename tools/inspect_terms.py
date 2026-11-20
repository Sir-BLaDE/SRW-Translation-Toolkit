# -*- coding: utf-8 -*-
"""Extrae cadenas con terminos pendientes de los CPK relevantes."""
import sys, os, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
files=[]
for root in [r'D:/Juegos/-SPARROW-/Super Robot Wars V']:
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if f.lower()=='systext.cpk': files.append(os.path.join(dp,f))
for f in files: print('SYSTEXT:',f)
print()
rx=re.compile(r'\b(AI|Soldier|Gamillas|Jupiter Empire Soldier|Neo Zeon Soldier|Medallion)\b',re.I)
for f in files:
    c=load(f); print('\n====',f)
    for r in c.rows:
        pt=c.plain(r)
        for m in re.finditer(rb'[\x20-\x7e]{4,}',pt):
            s=m.group().decode('latin1')
            if rx.search(s):
                print('  id=%-4s %r'%(r['id'],s[:160]))
