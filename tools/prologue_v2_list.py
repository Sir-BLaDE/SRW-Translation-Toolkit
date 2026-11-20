# -*- coding: utf-8 -*-
import sys, json, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json', encoding='utf-8'))
seen=collections.OrderedDict()
for rid in ['0','1','2','3','4','5','6','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']:
    if rid not in d: continue
    for row in d[rid]['rows']:
        for s in row['parts']:
            k=s.strip()
            if len(k)<4: continue
            seen.setdefault(k,[]).append(rid)
print('unicas:',len(seen))
for k,rows in seen.items():
    print('%3d|%s' % (len(k),k))
