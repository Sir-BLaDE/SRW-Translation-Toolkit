# -*- coding: utf-8 -*-
"""Muestra el tamano maximo disponible para cada cadena unica (primera aparicion)."""
import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full.json', encoding='utf-8'))
seen = {}
for rid, rd in d.items():
    cnt=rd['count']; slot=rd['slot']
    for si in range(cnt):
        sinfo=rd['rows'][si]
        ms = sinfo['meta'] if 0 < sinfo['meta'] <= slot else slot-22
        bparts = sinfo['parts']
        for idx, txt in enumerate(bparts):
            k = txt.strip()
            if len(k) < 4 or k in seen: continue
            n = len(txt.encode('utf-8'))
            seen[k] = n
for k,n in seen.items():
    print('%3d|%s' % (n, k))
