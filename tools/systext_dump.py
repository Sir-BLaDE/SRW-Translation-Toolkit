# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c=load(p)
for r in c.rows:
    pt=c.plain(r)
    print('\n==== id=%s len=%d'%(r['id'],len(pt)))
    for m in re.finditer(rb'[\x20-\x7e]{3,}',pt):
        print(' 0x%04x %r'%(m.start(),m.group().decode('latin1')[:200]))
