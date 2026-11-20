"""prologue_slots.py - analiza los slots repetitive de una fila del Prologue."""
import sys, re, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c = load(p)
r = [x for x in c.rows if x['id'] == 0][0]
pt = c.plain(r)
print('len', len(pt))
# buscar todas las apariciones de la cadena conocida
needle = b'November 11, 2199 NCC, Pluto Airspace'
pos = 0
hits = []
while True:
    i = pt.find(needle, pos)
    if i < 0: break
    hits.append(i); pos = i + 1
print('apariciones de cadena completa:', hits)
# trouver todos los trozos imprimibles largos con sus offsets
print('\n-- trozos imprimibles (>=6) con offset --')
for m in re.finditer(rb'[ -~]{6,}', pt):
    print('  0x%04x len=%-3d %r' % (m.start(), len(m.group()), m.group().decode('ascii','ignore')[:80]))
