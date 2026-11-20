# -*- coding: utf-8 -*-
"""Prologue reconstruido con la fila 0 byte-a-byte IDENTICA al original.

Sirve para comprobar si el crash viene de la traduccion o de que
srwv_cpkbuild2/build_ordered cambie algo en la estructura del contenedor.
"""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_rebuild_identical.cpk'

c = load(ORIG)
newrows = {}
for r in c.rows:
    p = c.plain(r)
    newrows[r['id']] = (c.cipher(r, p), len(p))
blob = build_ordered(ORIG, newrows)
open(OUT, 'wb').write(blob)
chk = load(OUT)
print('magic', chk.cpk.raw[:4], 'filas', len(chk.rows))
print('todas las filas identicas:',
      all(chk.plain(r) == c.plain(next(q for q in c.rows if q['id']==r['id'])) for r in chk.rows))
print('ExtractSize OK:', all(r['ex'] == len(chk.plain(r)) for r in chk.rows))
import hashlib
print('hash original:', hashlib.sha256(open(ORIG,'rb').read()).hexdigest()[:16])
print('hash rebuild :', hashlib.sha256(open(OUT,'rb').read()).hexdigest()[:16])
