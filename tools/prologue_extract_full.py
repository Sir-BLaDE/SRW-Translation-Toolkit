"""prologue_extract_full.py - extrae las cadenas completas de cada slot del Prologue.

Cada fila: header 24 bytes + N slots de tamano fijo.
Dentro de cada slot: cadenas terminadas en 0x00, y una cola de metadatos.
La cola de metadatos se detecta buscando el patron comun que termina en '78 00 00 00'.
"""
import sys, struct, re, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c = load(p)
META_TAIL = bytes.fromhex('9402100078000000')

def split_slot(b):
    # encontrar donde empiezan los metadatos: buscar la cola conocida
    tail = b.rfind(META_TAIL)
    if tail < 0:
        tail = len(b) - 22
    # los metadatos suelen empezar 14 bytes antes de la cola
    meta_start = max(0, tail - 14)
    text = b[:meta_start]
    parts = [s.decode('utf-8','ignore') for s in text.split(b'\x00') if s]
    return parts, meta_start

all_rows = {}
for r in c.rows:
    pt = c.plain(r)
    cnt = struct.unpack_from('<H', pt, 0)[0]
    if cnt == 0 or len(pt) < 24: continue
    slot = (len(pt)-24)//cnt
    if (len(pt)-24) % cnt: continue
    rows = []
    for si in range(cnt):
        b = pt[24+si*slot : 24+(si+1)*slot]
        parts, ms = split_slot(b)
        rows.append({'i':si, 'meta':ms, 'parts':parts})
    all_rows[r['id']] = {'len':len(pt), 'count':cnt, 'slot':slot, 'rows':rows}

# resumen
for rid,rd in all_rows.items():
    tot = sum(len(x['parts']) for x in rd['rows'])
    print('fila %-3d len=%-7d slots=%-4d slot=%-4d cadenas=%d' %
          (rid, rd['len'], rd['count'], rd['slot'], tot))

json.dump(all_rows, open(r'C:/Dev/Default Project/srwv/datos/prologue_full.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('\nvolcado -> prologue_full.json')
