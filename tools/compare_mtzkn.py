# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

A = load(r'C:/Dev/Default Project/srwv/backup/MtZkn_Pt_original.cpk')
B = load(r'C:/Dev/Default Project/srwv/backup/MtZkn_Pt_antes_revert.cpk')

print('filas', len(A.rows), len(B.rows))
print('HEADER diffs:')
for k in sorted(set(A.cpk.h)|set(B.cpk.h)):
    if A.cpk.h.get(k)!=B.cpk.h.get(k):
        print(' ',k,A.cpk.h.get(k),'->',B.cpk.h.get(k))

changed=0
for r in A.rows:
    x=A.plain(r)
    y=B.plain(next(q for q in B.rows if q['id']==r['id']))
    if x!=y:
        changed+=1
        if changed<=12:
            # mostrar strings ascii
            import re
            sx=[m.group(0).decode('ascii','replace') for m in re.finditer(rb'[ -~]{3,}',x)][:5]
            sy=[m.group(0).decode('ascii','replace') for m in re.finditer(rb'[ -~]{3,}',y)][:5]
            print('\nfila %d len %d->%d'%(r['id'],len(x),len(y)))
            print('  orig',sx)
            print('  trad',sy)
print('\nfilas cambiadas:',changed)
