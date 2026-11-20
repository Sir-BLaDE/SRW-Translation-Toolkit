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

import re as _re
_TRAIL = _re.compile(rb'^(\s*[^\s].*?[},])\s*--[^\[\]"\']*$')
def strip_lua_comments(b):
    """Quita comentarios '--' de línea completa y finales, solo fuera de cadenas [[ ]].
    Necesario cuando una entrada supera 65535 bytes (columna u16 del CPK)."""
    out = []; depth = 0
    for line in b.split(b'\n'):
        if depth == 0:
            st = line.lstrip()
            if st.startswith(b'--') and not st.startswith(b'--[['):
                continue
            m = _TRAIL.match(line)
            if m and b'[[' not in line and b']]' not in line:
                line = m.group(1)
        depth += line.count(b'[[') - line.count(b']]')
        if depth < 0: depth = 0
        out.append(line)
    return b'\n'.join(out)

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
    if f['ex'] <= 0xFFFF < len(out):  # fila de la tabla pequeña (u16)
        out = bytearray(strip_lua_comments(bytes(out)))
        print('entrada %d: comentarios Lua eliminados -> %d bytes' % (f['id'], len(out)))
        assert len(out) <= 0xFFFF, f['id']
    new[f['id']] = (cf.cipher(f, bytes(out)), len(out))
open(OUT, 'wb').write(build_ordered(GAME, new))
# las entradas modificadas deben seguir siendo Lua válido
try:
    from lupa import LuaRuntime
    _load = LuaRuntime(unpack_returned_tuples=True).eval('load')
    for fid, (_, ln) in new.items():
        src = load(OUT).plain([r for r in load(OUT).rows if r['id'] == fid][0]) if False else None
except ImportError:
    _load = None
# verificacion completa
c2 = load(OUT); bad = 0
for r in c2.rows:
    p = c2.plain(r)
    if len(p) != r['ex']: bad += 1
    if _load and r['id'] in new:
        res = _load(p.decode('utf-8'))
        if isinstance(res, tuple) and res[0] is None:
            print('LUA ERROR', r['id'], res[1]); bad += 1
    if r['id'] not in new and p != open('stg/%04d.bin' % r['id'], 'rb').read(): bad += 1
print('entradas modificadas', len(new), '| lineas', sum(len(v) for v in per.values()), '| errores', bad, '| magic', open(OUT,'rb').read(4))
