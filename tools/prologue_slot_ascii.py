# -*- coding: utf-8 -*-
"""Slot 0 de la fila 0 con traduccion ASCII pura."""
import sys, unicodedata
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_slot_ascii.cpk'
TXT = sys.argv[1] if len(sys.argv)>1 else '1 nov 2199, NCC, espacio aereo de Pluton'

a = load(ORIG)
ra = next(r for r in a.rows if r['id']==0)
pa = bytearray(a.plain(ra))
eb = TXT.encode('ascii')
# slot 0: byte0=0x00, texto desde 25, metadata desde 24+48=72
pos = 25
maxb = (24+48) - pos - 1
nb = bytearray(maxb+1)
nb[:len(eb)] = eb
pa[pos:pos+maxb+1] = nb

newrows={}
for r in a.rows:
    if r['id']==0:
        newrows[r['id']]=(a.cipher(r,bytes(pa)),r['ex'])
    else:
        newrows[r['id']]=(a.cipher(r,a.plain(r)),r['ex'])
blob=build_ordered(ORIG,newrows)
open(OUT,'wb').write(blob)
chk=load(OUT)
print(OUT,'slot0:',repr(chk.plain(next(q for q in chk.rows if q['id']==0))[24:94]))
print('ExtractSize OK:',all(r['ex']==len(chk.plain(r)) for r in chk.rows))
