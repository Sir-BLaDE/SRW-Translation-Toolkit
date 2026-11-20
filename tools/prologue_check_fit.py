# -*- coding: utf-8 -*-
"""prologue_check_fit.py - muestra que traducciones no caben en su espacio."""
import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full.json', encoding='utf-8'))
T = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_trans.json', encoding='utf-8'))

# tamano original de cada cadena unica
sizes = {}
for rid, rd in d.items():
    for row in rd['rows']:
        for s in row['parts']:
            k = s.strip()
            n = len(s.encode('utf-8'))
            if k not in sizes or n > sizes[k]:
                sizes[k] = n

seen = set()
print('%-4s %-4s %-58s %s' % ('ORIG','ES','INGLES','TRADUCCION'))
for k, es in T.items():
    if k in seen: continue
    seen.add(k)
    n = sizes.get(k, len(k.encode()))
    e = es.encode('utf-8')
    flag = 'OK' if len(e) == n else ('CORTO' if len(e) < n else 'LARGO %+d' % (len(e)-n))
    print('%-4d %-4d %-58s %s' % (n, len(e), k[:58], flag))
