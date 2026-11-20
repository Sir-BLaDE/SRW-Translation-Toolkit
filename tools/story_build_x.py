"""story_build_x.py - Aplica datos/es_batches/*.json a STGEST002_EN.CPK (SRW X).
Uso: python3 story_build_x.py SALIDA.cpk [--ascii]
"""
import json, os, sys, unicodedata
from cpk_util import load
from story import find_dialogs, rebuild_block
from srwv_cpkbuild2 import build_ordered

GAME = 'orig/Data/STAGE/STGEST002_EN.CPK'
ASCII = '--ascii' in sys.argv
OUT = sys.argv[1]

def deaccent(s):
    s = s.replace('¿', '').replace('¡', '').replace('ñ', 'ny').replace('Ñ', 'NY')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn' or c in '　')

trans = {}
for fn in sorted(os.listdir('datos/es_batches')):
    if fn.endswith('.json'):
        trans.update({int(k): v for k, v in json.load(open('datos/es_batches/' + fn, encoding='utf-8')).items()})
recs = [json.loads(l) for l in open('datos/story_dialogues.jsonl', encoding='utf-8')]
per = {}
for i, d in enumerate(recs):
    if i in trans:
        per.setdefault(d['entry'], []).append((d['start'], trans[i]))

cf = load(GAME)
new = {}
for f in cf.rows:
    if f['id'] not in per:
        continue
    pt = open('stg/%04d.bin' % f['id'], 'rb').read()
    by = {d.start: d for d in find_dialogs(f['id'], pt)}
    out = bytearray(); last = 0
    for st, es in sorted(per[f['id']]):
        d = by[st]
        if ASCII:
            es = deaccent(es)
        out += pt[last:d.start] + rebuild_block(d.speaker, es); last = d.end
    out += pt[last:]
    new[f['id']] = (cf.cipher(f, bytes(out)), len(out))
open(OUT, 'wb').write(build_ordered(GAME, new))
# verificacion completa
c2 = load(OUT); bad = 0
for r in c2.rows:
    p = c2.plain(r)
    if len(p) != r['ex']: bad += 1
    if r['id'] not in new and p != open('stg/%04d.bin' % r['id'], 'rb').read(): bad += 1
print('entradas modificadas', len(new), '| lineas', sum(len(v) for v in per.values()), '| errores', bad, '| magic', open(OUT,'rb').read(4))
