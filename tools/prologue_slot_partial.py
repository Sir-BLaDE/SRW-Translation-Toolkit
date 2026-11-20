# -*- coding: utf-8 -*-
"""Slot 0 de la fila 0 con una porcion controlada de la traduccion.

Uso: python prologue_slot_partial.py <modo>
 modos: original | same_len | short | trad
"""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_slot_partial.cpk'
mode = sys.argv[1] if len(sys.argv) > 1 else 'original'

TEXTS = {
 'original': 'ovember 11, 2199 NCC, Pluto Airspace',
 'same_len': 'noviembre 11, 2199 NCC, Espacio A',  # misma longitud que el original (36)
 'short': '1 nov 2199',
 'trad': '1 nov 2199, NCC, espacio aereo de Pluton',
 'trim': '1 nov 2199, NCC, espacio a',
}
txt = TEXTS[mode]

c = load(ORIG)
pt = bytearray(c.plain(next(r for r in c.rows if r['id']==0)))
pos = 25
maxb = (24+48) - pos - 1  # 46 bytes
eb = txt.encode('utf-8')
assert len(eb) <= maxb, (len(eb), maxb)
block = bytearray(maxb+1)
block[:len(eb)] = eb
pt[pos:pos+maxb+1] = block

newrows = {}
for r in c.rows:
    p = pt if r['id']==0 else c.plain(r)
    newrows[r['id']] = (c.cipher(r, bytes(p)), len(p))
blob = build_ordered(ORIG, newrows)
open(OUT,'wb').write(blob)
chk = load(OUT)
print(mode, repr(txt), 'len', len(eb), 'ExtractSize OK',
      all(r['ex']==len(chk.plain(r)) for r in chk.rows))
