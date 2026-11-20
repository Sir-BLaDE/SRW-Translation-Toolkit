import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

c = load(r'C:/Dev/Default Project/srwv/backup/LT00_EN_instalado_antes.cpk')
f = c.rows[0]
pt = c.plain(f)
open(r'C:/Dev/Default Project/srwv/outputs/lt00_plain.bin', 'wb').write(pt)
print('plain len', len(pt), 'id', f['id'], f['table'])
print(pt[:96].hex(' '))
print(repr(pt[:200]))
# buscar cadenas
import re
strs = [(m.start(), m.group()) for m in re.finditer(rb'[\x20-\x7e]{4,}', pt)]
print('num cadenas', len(strs))
for s in strs[:15]:
    print(s)
