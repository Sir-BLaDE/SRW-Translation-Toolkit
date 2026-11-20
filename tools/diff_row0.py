# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

A = load(r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk')
B = load(r'C:/Dev/Default Project/srwv/outputs/Prologue_half_single.cpk')
x = A.plain(next(r for r in A.rows if r['id']==0))
y = B.plain(next(r for r in B.rows if r['id']==0))
print('len', len(x), len(y))
diffs = [i for i in range(len(x)) if x[i]!=y[i]]
print('bytes distintos:', len(diffs))
# agrupar
ranges=[]
s=p=diffs[0]
for i in diffs[1:]:
    if i==p+1: p=i
    else: ranges.append((s,p)); s=p=i
ranges.append((s,p))
print('rangos:',len(ranges))
for s,e in ranges:
    print('@%d-%d (%d bytes)'%(s,e,e-s+1))
    print('  ORIG:',repr(x[max(0,s-5):min(len(x),e+6)]))
    print('  ES  :',repr(y[max(0,s-5):min(len(y),e+6)]))
