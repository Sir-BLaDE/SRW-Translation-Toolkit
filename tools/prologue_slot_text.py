# -*- coding: utf-8 -*-
"""Instalar un texto arbitrario en el slot 0 de la fila 0 de Prologue.

Uso: python prologue_slot_text.py "texto"
"""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
import shutil, hashlib

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_slot_text.cpk'
DST = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
txt = sys.argv[1]

c = load(ORIG)
pt = bytearray(c.plain(next(r for r in c.rows if r['id']==0)))
pos = 25
maxb = (24+48) - pos - 1
eb = txt.encode('utf-8')
if len(eb) > maxb:
    raise SystemExit('demasiado largo: %d > %d' % (len(eb), maxb))
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
assert all(r['ex']==len(chk.plain(r)) for r in chk.rows)
shutil.copy2(OUT, DST)
print('instalado:', repr(txt), 'bytes', len(eb))
print('hash', hashlib.sha256(open(DST,'rb').read()).hexdigest())
