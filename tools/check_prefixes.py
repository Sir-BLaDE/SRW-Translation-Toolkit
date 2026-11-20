# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

A = load(r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk')
B = load(r'C:/Dev/Default Project/srwv/outputs/Prologue_half_single.cpk')
x = A.plain(next(r for r in A.rows if r['id']==0))
y = B.plain(next(r for r in B.rows if r['id']==0))

# los slots empiezan en 24, tamano 70
for si in range(24):
    base = 24 + si*70
    b = x[base:base+70]
    # encontrar la N de November
    idx = b.find(b'ovember')
    if idx < 0: idx = b.find(b'November')+1
    print('slot %2d @%4d: %s' % (si, base, b[:16].hex(' ')))
