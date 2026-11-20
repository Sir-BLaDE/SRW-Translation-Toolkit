# -*- coding: utf-8 -*-
"""Analizar la estructura binaria de Prologue.cpk: slots y su metadata."""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
DATA = r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json'
d = json.load(open(DATA, encoding='utf-8'))
c = load(ORIG)

for r in c.rows[:4]:
    pt = c.plain(r)
    rd = d.get(str(r['id']))
    if not rd:
        print('fila', r['id'], 'sin datos'); continue
    cnt, slot = rd['count'], rd['slot']
    print('\n=== fila %d  count=%d slot=%d total=%d ===' % (r['id'], cnt, slot, len(pt)))
    print('primeros 32 bytes:', pt[:32].hex(' '))
    for si in range(min(cnt, 3)):
        base = 24 + si * slot
        b = pt[base:base+slot]
        print(' slot %d @%d: %s' % (si, base, b[:64].hex(' ')))
        # strings
        strings=[]
        i=0
        while i < slot-22:
            j = b.find(b'\x00', i, slot-22)
            if j < 0: break
            if j > i:
                strings.append((i, b[i:j].decode('utf-8','replace')[:70]))
            i = j+1
        print('   strings:', strings[:8])
        print('   meta22:', b[-22:].hex(' '))
