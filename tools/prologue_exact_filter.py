# -*- coding: utf-8 -*-
"""Construir Prologue_es_exact.cpk filtrado a ciertas filas (para prueba)."""
import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
TRAD = r'C:/Dev/Default Project/srwv/outputs/Prologue_es_exact.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_exact_row0.cpk'
allowed = {0} if len(sys.argv) < 2 else set(int(x) for x in sys.argv[1:])

a = load(ORIG)
b = load(TRAD)
newrows = {}
for r in a.rows:
    if r['id'] in allowed:
        src = b
    else:
        src = a
    p = src.plain(next(q for q in src.rows if q['id']==r['id']))
    newrows[r['id']] = (src.cipher(next(q for q in src.rows if q['id']==r['id']), p), r['ex'])

blob = build_ordered(ORIG, newrows)
open(OUT,'wb').write(blob)
chk = load(OUT)
print(OUT,'filas',len(allowed),'ExtractSize OK:',all(r['ex']==len(chk.plain(r)) for r in chk.rows))
