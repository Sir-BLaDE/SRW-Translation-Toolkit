"""Reconstruye KPACK_P4_RG_EN.CPK en espanol (fichero 0 = textos BLTU)."""
import io
import json
import sys

sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')

from cpk_util import load
from lt00 import load as load_lt
from srwv_cpkbuild2 import build_ordered

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
MAP = r'C:/Dev/Default Project/srwv/datos/kpack_rg_es.json'
OUT = r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_RG_EN_es.cpk'

# el mismo texto en ingles se usa en dos mensajes con final distinto
OVERRIDES = {
    501: 'El Programa de Habilidad usado en [PILOT]',
}

trans = json.load(io.open(MAP, encoding='utf-8'))

cf = load(SRC)
print('ficheros', len(cf.rows), 'diag', cf.cpk.diagnose() or 'ok')

row = [r for r in cf.rows if r['id'] == 0][0]
pt = cf.plain(row)
t = load_lt(pt)
print('roundtrip base identico', t.build(list(t.strings)) == pt)

key_idx = {a for a, b, cc in t.ids}
strings = list(t.strings)
changed = 0
for i in range(t.count):
    if i in key_idx:
        continue
    s = strings[i]
    if s in trans and trans[s] != s:
        strings[i] = trans[s]
        changed += 1
for i, v in OVERRIDES.items():
    strings[i] = v
    changed += 1
print('cadenas cambiadas', changed)

plain = t.build(strings)
chk = load_lt(plain)
assert chk.strings == strings, 'roundtrip de cadenas'
assert chk.ids == t.ids, 'tabla de ids alterada'
print('plain nuevo', len(plain), 'ids', chk.id_count)

blob = cf.cipher(row, plain)
new_files = {0: (blob, len(plain))}
out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('escrito', len(out), '->', OUT)

cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    p2 = cf2.plain(f)
    ok = f['ex'] == len(p2)
    print(' id', f['id'], f['table'], 'size', f['size'], 'ex', f['ex'],
          'plain', len(p2), 'OK' if ok else 'MISMATCH')
f0 = [f for f in cf2.rows if f['id'] == 0][0]
p0 = cf2.plain(f0)
t2 = load_lt(p0)
print('row0 identico', p0 == plain, 'cadenas', t2.count)
for i in (210, 212, 216, 330, 407, 500, 501, 502, 516):
    print('  ', i, repr(t2.strings[i]))
