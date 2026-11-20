# -*- coding: utf-8 -*-
"""prologue_rebuild.py - reconstruye el Prologue con slots mas grandes para el espanol.

El juego calcula slot = (len(fila)-24)/count, igual que hace con la version JP
(slots de 105 bytes). Aqui agrandamos los slots lo necesario para que quepan
las traducciones, manteniendo la cola de metadatos de 22 bytes intacta.
"""
import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_EN_original.cpk'
OUT  = r'C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk'
DATA = r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json'
TRANS= r'C:/Dev/Default Project/srwv/datos/prologue_trans_v7.json'
META = 22
d = json.load(open(DATA, encoding='utf-8'))
T = json.load(open(TRANS, encoding='utf-8'))

c = load(ORIG)
newrows = {}
report = []
for r in c.rows:
    pt = c.plain(r); rid = str(r['id']); rd = d.get(rid)
    if not rd:
        newrows[r['id']] = (c.cipher(r, pt), len(pt)); continue
    cnt = rd['count']; oldslot = rd['slot']
    # primero calcular las traducciones de todos los slots
    all_trans = []
    for si in range(cnt):
        parts = rd['rows'][si]['parts']
        translated = []
        for s in parts:
            k = s.strip()
            es = T.get(k, '') if k in T else s
            if not es.strip(): es = s
            translated.append(es.encode('utf-8'))
        all_trans.append(translated)
    # tamano unico por fila = maximo necesario
    need_max = max(sum(len(x)+1 for x in tr) + META for tr in all_trans)
    newslot_size = max(oldslot, need_max)
    # construir slots nuevos con ese tamano
    newslots = []
    for si in range(cnt):
        b = pt[24+si*oldslot : 24+(si+1)*oldslot]
        meta = b[-META:]
        translated = all_trans[si]
        buf = bytearray()
        for x in translated:
            buf += x + b'\x00'
        buf += b'\x00' * (newslot_size - META - len(buf))
        buf += meta
        assert len(buf) == newslot_size, (len(buf), newslot_size)
        newslots.append(bytes(buf))
    newpt = bytearray(pt[:24] + b''.join(newslots))
    # el campo u16 del offset 2 cambia con el tamano del slot (EN->JP: +12 cuando slot +12)
    delta = newslot_size - oldslot
    if delta:
        f2 = struct.unpack_from('<H', newpt, 2)[0]
        struct.pack_into('<H', newpt, 2, f2 + delta)
    newrows[r['id']] = (c.cipher(r, bytes(newpt)), len(newpt))
    if newslot_size != oldslot:
        report.append((rid, oldslot, newslot_size, cnt))

blob = build_ordered(ORIG, newrows)
open(OUT,'wb').write(blob)
c2 = load(OUT)
for rr in c2.rows: assert rr['ex']==len(c2.plain(rr)), rr
print('escrito', OUT, len(blob), 'verificado')
print('filas con slot agrandado:', len(report))
for x in report: print('  fila %-3s slot %d -> %d (slots=%d)'%x)
