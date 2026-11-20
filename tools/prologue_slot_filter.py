# -*- coding: utf-8 -*-
"""Construir Prologue con solo ciertos SLOTS de la fila 0 traducidos."""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
TRAD = r'C:/Dev/Default Project/srwv/outputs/Prologue_es_exact.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_slot_test.cpk'
slots = set(int(x) for x in sys.argv[1:])

a = load(ORIG); b = load(TRAD)
ra = next(r for r in a.rows if r['id']==0)
rb = next(r for r in b.rows if r['id']==0)
pa = bytearray(a.plain(ra)); pb = b.plain(rb)
slot = 70
# copiar solo los slots elegidos desde pb
for si in slots:
    base = 24 + si*slot
    pa[base:base+slot] = pb[base:base+slot]

newrows = {}
for r in a.rows:
    if r['id']==0:
        newrows[r['id']] = (a.cipher(r, bytes(pa)), r['ex'])
    else:
        newrows[r['id']] = (a.cipher(r, a.plain(r)), r['ex'])

blob = build_ordered(ORIG, newrows)
open(OUT,'wb').write(blob)
chk = load(OUT)
print(OUT,'slots',sorted(slots),'ExtractSize OK:',all(r['ex']==len(chk.plain(r)) for r in chk.rows))
