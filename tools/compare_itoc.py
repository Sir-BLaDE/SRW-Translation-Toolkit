# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_cpk import Cpk

A = Cpk(r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk')
B = Cpk(r'C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_v7.cpk')

print('=== HEADER diffs ===')
for k in sorted(set(A.h) | set(B.h)):
    if A.h.get(k) != B.h.get(k):
        print('  %-24s %r -> %r' % (k, A.h.get(k), B.h.get(k)))

print('\n=== ITOC info row diffs ===')
ra, rb = A.itoc_info['row'], B.itoc_info['row']
for k in sorted(set(ra) | set(rb)):
    if ra.get(k) != rb.get(k):
        print('  %-24s %r -> %r' % (k, ra.get(k), rb.get(k)))

print('\n=== CpkItocL columnas ===')
for name in ('CpkItocL', 'CpkItocH'):
    ta = A.itoc_info.get(name)
    tb = B.itoc_info.get(name)
    if not ta or not tb:
        continue
    print(' ', name, 'cols A:', [c.name for c in ta.columns])
    print(' ', name, 'cols B:', [c.name for c in tb.columns])
    for r in range(min(ta.rows_count, 3)):
        print('   fila', r)
        for k in sorted(set(ta.row(r)) | set(tb.row(r))):
            va, vb = ta.row(r).get(k), tb.row(r).get(k)
            if isinstance(va, (bytes, bytearray)):
                va = '<bytes %d>' % len(va)
            if isinstance(vb, (bytes, bytearray)):
                vb = '<bytes %d>' % len(vb)
            if va != vb:
                print('      %-16s %r -> %r' % (k, va, vb))
