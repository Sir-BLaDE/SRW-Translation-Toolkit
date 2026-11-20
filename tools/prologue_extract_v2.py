# -*- coding: utf-8 -*-
"""Extrae cadenas completas de cada slot usando meta = slot - 22 (tamano fijo de cola)."""
import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c = load(p)
META = 22
all_rows = {}
for r in c.rows:
    pt = c.plain(r)
    cnt = struct.unpack_from('<H', pt, 0)[0]
    if cnt == 0 or len(pt) < 24 or (len(pt)-24) % cnt: continue
    slot = (len(pt)-24)//cnt
    meta = slot - META
    rows = []
    for si in range(cnt):
        b = pt[24+si*slot : 24+(si+1)*slot]
        text = b[:meta]
        parts = [s.decode('utf-8','ignore') for s in text.split(b'\x00') if s]
        rows.append({'i':si, 'meta':meta, 'parts':parts})
    all_rows[r['id']] = {'len':len(pt), 'count':cnt, 'slot':slot, 'rows':rows}
json.dump(all_rows, open(r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('filas:',len(all_rows))
for rid,rd in list(all_rows.items())[:8]:
    print('fila %-3s slot=%-4d meta=%-4d cadenas=%d' % (rid, rd['slot'], rd['slot']-META,
          sum(len(x['parts']) for x in rd['rows'])))
