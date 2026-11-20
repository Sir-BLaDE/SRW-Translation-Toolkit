# -*- coding: utf-8 -*-
"""Comparar campos numericos (no texto) original vs traducido."""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

A = load(r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk')
B = load(r'C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_v7.cpk')

for r in A.rows:
    fid = r['id']
    x = A.plain(r)
    y = B.plain(next(q for q in B.rows if q['id']==fid))
    # core 24 bytes
    if x[:24] != y[:24]:
        print('fila %d: CABECERA 24 bytes DIFERENTE' % fid)
        print('  orig', x[:24].hex(' '))
        print('  es  ', y[:24].hex(' '))
    # bytes de metadata al final de cada slot (ultimos 22)
    import json
    d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json', encoding='utf-8'))
    rd = d.get(str(fid))
    if not rd: continue
    cnt, slot = rd['count'], rd['slot']
    for si in range(cnt):
        base = 24 + si*slot
        mx = x[base+slot-22:base+slot]
        my = y[base+slot-22:base+slot]
        if mx != my:
            print('fila %d slot %d: META22 DIFERENTE' % (fid, si))
            print('  orig', mx.hex(' '))
            print('  es  ', my.hex(' '))
            break
