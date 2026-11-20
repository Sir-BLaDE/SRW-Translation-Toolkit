"""Reconstruye SysText.cpk en espanol (fichero 0 = textos de sistema)."""
import io
import json
import sys

sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')

from cpk_util import load
from lt00 import load as load_lt
from srwv_cpkbuild2 import build_ordered

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
P1 = r'C:/Dev/Default Project/srwv/datos/systext_es_1.json'
P2 = r'C:/Dev/Default Project/srwv/datos/systext_es_2.json'
OUT = r'C:/Dev/Default Project/srwv/outputs/SysText_es.cpk'

# el mismo texto en ingles aparece dos veces con sentido distinto (PE de Gran As)
OVERRIDES = {
    795: '　Si un piloto es Gran As (más de 80 puntos), sus PE son',
}

trans = {}
for p in (P1, P2):
    trans.update(json.load(io.open(p, encoding='utf-8')))

cf = load(SRC)
print('ficheros', len(cf.rows), 'diag', cf.cpk.diagnose() or 'ok')

row = [r for r in cf.rows if r['id'] == 0][0]
t = load_lt(cf.plain(row))
strings = list(t.strings)

changed = 0
for i in range(712, t.count):
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
print('plain nuevo', len(plain))

blob = cf.cipher(row, plain)
new_files = {0: (blob, len(plain))}
out = build_ordered(SRC, new_files)
open(OUT, 'wb').write(out)
print('escrito', len(out), '->', OUT)

cf2 = load(OUT)
print('diag', cf2.cpk.diagnose() or 'ok')
for f in cf2.rows:
    pt = cf2.plain(f)
    ok = f['ex'] == len(pt)
    print(' id', f['id'], f['table'], 'size', f['size'], 'ex', f['ex'],
          'plain', len(pt), 'OK' if ok else 'MISMATCH')
f0 = [f for f in cf2.rows if f['id'] == 0][0]
pt0 = cf2.plain(f0)
t2 = load_lt(pt0)
print('row0 identico', pt0 == plain, 'cadenas', t2.count)
print('muestra:', [t2.strings[i][:48] for i in (712, 713, 737, 1055, 3157)])
