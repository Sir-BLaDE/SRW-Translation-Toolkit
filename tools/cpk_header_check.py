"""cpk_header_check.py - Compara cabeceras e invariantes del CPK original y el
reconstruido."""
import sys

from srwv_cpk import Cpk

orig = 'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
for p in [orig] + sys.argv[1:]:
    c = Cpk(p)
    print('====', p)
    print('  FileSize        ', c.h.get('FileSize'), '| real', __import__('os').path.getsize(p))
    print('  ContentOffset   ', c.h.get('ContentOffset'))
    print('  ContentSize     ', c.h.get('ContentSize'))
    print('  EnabledDataSize ', c.h.get('EnabledDataSize'))
    print('  EnabledPackedSize', c.h.get('EnabledPackedSize'))
    print('  Align           ', c.align)
    tot = 0
    totex = 0
    for tn in ('CpkItocL', 'CpkItocH'):
        t = c.itoc_info.get(tn)
        if not t:
            continue
        for r in range(t.rows_count):
            d = t.row(r)
            a = c.align
            tot += (d['FileSize'] + a - 1) & ~(a - 1)
            tot += 0
            tot -= (d['FileSize'] + a - 1) & ~(a - 1)
            tot += (d['FileSize'] + a - 1) & ~(a - 1)
            tot -= (d['FileSize'] + a - 1) & ~(a - 1)
        print('  tabla', tn, 'filas', t.rows_count)
    # sumas correctas
    s_stored = 0
    s_ex = 0
    n = 0
    for tn in ('CpkItocL', 'CpkItocH'):
        t = c.itoc_info.get(tn)
        if not t:
            continue
        for r in range(t.rows_count):
            d = t.row(r)
            s_stored += (d['FileSize'] + c.align - 1) & ~(c.align - 1)
            s_ex += d['ExtractSize']
            n += 1
    print('  n entradas      ', n)
    print('  suma alineada   ', s_stored)
    print('  suma extract    ', s_ex)
    print('  filesize-content', __import__('os').path.getsize(p) - c.h.get('ContentOffset'))
    print()
