# -*- coding: utf-8 -*-
"""Traduccion in-situ de Prologue.cpk usando las posiciones EXACTAS del JSON.

A diferencia de prologue_inplace_safe.py, no detecta cadenas buscando \x00
(lo cual falla en slots donde el texto empieza en el byte 0, como el slot 5 de
la fila 0). En su lugar usa los 'parts' del JSON con sus offsets reales.
"""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
DATA = r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json'
TRANS = r'C:/Dev/Default Project/srwv/datos/prologue_trans_v7.json'
HEADER = 24
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_es_exact.cpk'

d = json.load(open(DATA, encoding='utf-8'))
T = json.load(open(TRANS, encoding='utf-8'))

def fit(es, maxbytes):
    b = es.encode('utf-8')
    if len(b) <= maxbytes:
        return es
    words = es.split()
    while words and len(' '.join(words).encode('utf-8')) > maxbytes:
        words.pop()
    return ' '.join(words).encode('utf-8')[:maxbytes].decode('utf-8','ignore')

def find_exact(blob, part, start, end):
    """Encontrar la posicion exacta de 'part' dentro de [start,end)."""
    key = part.encode('utf-8') if isinstance(part, str) else part
    idx = blob.find(key, start, end)
    return idx

c = load(ORIG)
newrows = {}
stats = {'ok':0,'shrunk':0,'notfound':0}
for r in c.rows:
    pt = bytearray(c.plain(r))
    before = len(pt)
    rid = str(r['id'])
    rd = d.get(rid)
    if not rd:
        newrows[r['id']] = (c.cipher(r, bytes(pt)), before)
        continue
    slot = rd['slot']
    for row in rd['rows']:
        si = row['i']
        base = HEADER + si*slot
        # el slot va de base a base+slot; los strings estan en parts
        for part in row['parts']:
            if not isinstance(part, str) or not part.strip():
                continue
            pos = find_exact(bytes(pt), part, base, base+slot)
            if pos < 0:
                stats['notfound'] += 1
                continue
            # Si el texto empieza exactamente en el byte 0 del slot, ese primer
            # byte es estructural para el juego (no traducir ese slot).
            if pos == base:
                stats['skip_structural'] = stats.get('skip_structural', 0) + 1
                continue
            key = part.strip()
            if key not in T or not T[key].strip():
                stats['notfound'] += 1
                continue
            # parar antes de la metadata de 22 bytes al final del slot
            meta_start = base + slot - 22
            maxbytes = meta_start - pos - 1
            if maxbytes <= 0:
                stats['nohueco'] = stats.get('nohueco', 0) + 1
                continue
            es = fit(T[key].strip(), maxbytes)
            nb = bytearray(maxbytes+1)
            eb = es.encode('utf-8')
            nb[:len(eb)] = eb
            pt[pos:pos+maxbytes+1] = nb
            stats['ok' if len(eb)<=maxbytes else 'shrunk'] += 1
    assert len(pt) == before
    newrows[r['id']] = (c.cipher(r, bytes(pt)), before)

blob = build_ordered(ORIG, newrows)
open(OUT,'wb').write(blob)
chk = load(OUT)
print('stats',stats)
print(OUT,'ExtractSize OK:',all(r['ex']==len(chk.plain(r)) for r in chk.rows))

# verificar que el byte 374 (slot5 fila0) sigue siendo 'N'
x = chk.plain(next(r for r in chk.rows if r['id']==0))
print('slot5 primer byte:',chr(x[374]),'(debe ser N)')
