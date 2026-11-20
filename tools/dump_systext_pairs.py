import sys, io, json, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c = load(P)
f = c.rows[0]
t = load_lt(c.plain(f))

print('count', t.count, 'ids', t.id_count)
print('ids[:5]', t.ids[:5], 'ids[-5:]', t.ids[-5:])
print('keys max', max(a for a, b, cc in t.ids), 'values min', min(cc for a, b, cc in t.ids),
      'values max', max(cc for a, b, cc in t.ids))
# comprobar que todos los indices de clave son 0..711 y valores 712..3290
print('claves consecutivas', all(a == i for i, (a, b, cc) in enumerate(t.ids)))
print('vals unicos', len(set(cc for a, b, cc in t.ids)))
print('flags', sorted(set(b for a, b, cc in t.ids)))

# volcar pares
pairs = [(t.strings[a], t.strings[cc]) for a, b, cc in t.ids]
with io.open(r'C:/Dev/Default Project/srwv/datos/systext_pairs.txt', 'w', encoding='utf-8', newline='\n') as fh:
    for k, v in pairs:
        fh.write(k + '\t' + json.dumps(v, ensure_ascii=False) + '\n')

# estadisticas
real = [(k, v) for k, v in pairs if re.search(r'[A-Za-z]', v) and not re.match(r'^[A-Z0-9_]+$', v)]
print('pares con texto real', len(real))
print('identicos clave', sum(1 for k, v in pairs if k == v))
print('vacios', sum(1 for k, v in pairs if not v.strip()))
