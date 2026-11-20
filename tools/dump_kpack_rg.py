import sys, io, json, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
c = load(P)
t = load_lt(c.plain(c.rows[0]))
print('count', t.count, 'ids', t.id_count)
print('first ids', t.ids[:4], 'last', t.ids[-3:])
groups = [(t.strings[a], list(range(cc, cc + n))) for a, n, cc in t.ids]
with io.open(r'C:/Dev/Default Project/srwv/datos/kpack_rg_groups.txt', 'w', encoding='utf-8', newline='\n') as fh:
    for k, idxs in groups:
        fh.write(f'### {k}  ({len(idxs)})\n')
        for i in idxs:
            fh.write(f'{i}\t{json.dumps(t.strings[i], ensure_ascii=False)}\n')
        fh.write('\n')
print('grupos', len(groups))
# textos con letras reales
real = [(i, t.strings[i]) for i in range(t.count)
        if i not in {a for a, b, cc in t.ids}
        and len(t.strings[i].strip()) > 2]
print('valores con texto', len(real))
