"""prologue_structure.py - analiza la estructura de Prologue.cpk para poder
reemplazar el texto manteniendo los bytes de longitud/control."""
import sys, struct, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c=load(p)
for r in c.rows:
    pt=c.plain(r)
    # contar cadenas ASCII imprimibles largas
    ss=[m.group().decode('ascii','ignore') for m in re.finditer(rb'[ -~]{8,}',pt)]
    print('fila %-3d len=%-7d cadenas>=8: %d'%(r['id'],len(pt),len(ss)))
