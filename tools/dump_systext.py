import sys, io
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c = load(P)
f = c.rows[0]
pt = c.plain(f)
open(r'C:/Dev/Default Project/srwv/outputs/systext_row0.bin', 'wb').write(pt)
t = load_lt(pt)
with io.open(r'C:/Dev/Default Project/srwv/datos/systext_strings.txt', 'w', encoding='utf-8', newline='\n') as fh:
    for i, s in enumerate(t.strings):
        fh.write(f'{i}\t{s!r}\n')
print('escrito', t.count, 'cadenas')
