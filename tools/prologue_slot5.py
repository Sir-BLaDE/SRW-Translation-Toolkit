# -*- coding: utf-8 -*-
"""Traducir el slot 5 de la fila 0 de Prologue (el que muestra la fecha).

El slot 5 es el unico cuyo texto empieza en el byte 0 del slot con 'N'
("November 11, 2199 NCC, Pluto Airspace"); los demas slots tienen 0x00
delante y no se muestran. Escribimos desde el byte 0 del slot, dentro de
los 48 bytes de texto, sin tocar la metadata de 22 bytes final.

Uso: python prologue_slot5.py "texto"
"""
import sys, shutil, hashlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_slot5.cpk'
DST = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
txt = sys.argv[1] if len(sys.argv) > 1 else '11 nov 2199'

c = load(ORIG)
pt = bytearray(c.plain(next(r for r in c.rows if r['id'] == 0)))
base = 24 + 5 * 70          # 374: inicio del slot 5
text_area = 48              # bytes 0..47; metadata en 48..69
eb = txt.encode('utf-8')
if len(eb) >= text_area:
    raise SystemExit('demasiado largo: %d >= %d' % (len(eb), text_area))
block = bytearray(text_area)
block[:len(eb)] = eb
pt[base:base + text_area] = block

newrows = {}
for r in c.rows:
    p = pt if r['id'] == 0 else c.plain(r)
    newrows[r['id']] = (c.cipher(r, bytes(p)), len(p))
blob = build_ordered(ORIG, newrows)
open(OUT, 'wb').write(blob)
chk = load(OUT)
assert all(r['ex'] == len(chk.plain(r)) for r in chk.rows)
shutil.copy2(OUT, DST)
print('instalado slot5:', repr(txt), 'bytes', len(eb))
print('hash', hashlib.sha256(open(DST, 'rb').read()).hexdigest())
