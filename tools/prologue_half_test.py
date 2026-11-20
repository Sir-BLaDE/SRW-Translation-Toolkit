# -*- coding: utf-8 -*-
"""Construir variantes de Prologue con solo algunas filas traducidas.
Uso: python prologue_half_test.py <mitad: first|second|all>
"""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
DATA = r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json'
TRANS = r'C:/Dev/Default Project/srwv/datos/prologue_trans_v7.json'
META = 22
mode = sys.argv[1] if len(sys.argv) > 1 else 'first'
OUT = r'C:/Dev/Default Project/srwv/outputs/Prologue_half_%s.cpk' % mode

d = json.load(open(DATA, encoding='utf-8'))
T = json.load(open(TRANS, encoding='utf-8'))
ids = sorted(int(k) for k in d)
half = len(ids) // 2
if mode == 'first':
    allowed = set(ids[:half])
elif mode == 'second':
    allowed = set(ids[half:])
elif mode == 'q1':
    allowed = set(ids[:7])
elif mode == 'q2':
    allowed = set(ids[7:15])
elif mode == 'a':
    allowed = set(ids[:4])
elif mode == 'b':
    allowed = set(ids[4:7])
elif mode == 'single':
    allowed = set([int(sys.argv[2])])
else:
    allowed = set(ids)

def fit(es, maxbytes):
    b = es.encode('utf-8')
    if len(b) <= maxbytes:
        return es
    words = es.split()
    while words and len(' '.join(words).encode('utf-8')) > maxbytes:
        words.pop()
    out = ' '.join(words)
    return out.encode('utf-8')[:maxbytes].decode('utf-8', 'ignore')

def slot_strings(b, meta_start):
    out = []
    i = 0
    while i < meta_start:
        j = b.find(b'\x00', i, meta_start)
        if j < 0: break
        if j > i: out.append((i, j, b[i:j].decode('utf-8','ignore')))
        i = j + 1
    return out

c = load(ORIG)
newrows = {}
for r in c.rows:
    pt = bytearray(c.plain(r))
    before = len(pt)
    rid = r['id']
    rd = d.get(str(rid))
    if not rd or rid not in allowed:
        newrows[rid] = (c.cipher(r, bytes(pt)), before)
        continue
    cnt, slot = rd['count'], rd['slot']
    meta = slot - META
    for si in range(cnt):
        base = 24 + si*slot
        b = bytes(pt[base:base+slot])
        spans = slot_strings(b, meta)
        for idx, (a, z, txt) in enumerate(spans):
            key = txt.strip()
            if key not in T or not T[key].strip():
                continue
            nxt = spans[idx+1][0] if idx+1 < len(spans) else meta
            mb = nxt - a - 1
            es = fit(T[key].strip(), mb)
            nb = bytearray(mb+1)
            eb = es.encode('utf-8')
            nb[:len(eb)] = eb
            pt[base+a:base+nxt] = nb
    assert len(pt) == before
    newrows[rid] = (c.cipher(r, bytes(pt)), before)

blob = build_ordered(ORIG, newrows)
open(OUT, 'wb').write(blob)
chk = load(OUT)
print(OUT, 'filas traducidas:', len([i for i in allowed if i in [r['id'] for r in c.rows]]),
      'ExtractSize OK:', all(r['ex']==len(chk.plain(r)) for r in chk.rows))
