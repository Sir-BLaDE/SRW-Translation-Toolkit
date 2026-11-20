"""prologue_compare.py - compara estructura EN vs JP del Prologue para entender longitudes."""
import sys,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
for lang in ['EN','JP']:
    p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/%s/Prologue.cpk'%lang
    c=load(p)
    print('\n#####',lang)
    for r in c.rows[:4]:
        pt=c.plain(r)
        print(' fila %-3d len=%-7d head=%s'%(r['id'],len(pt),pt[:24].hex(' ')))
        # mostrar primeras cadenas legibles
        ss=[m.group().decode('utf-8','ignore') for m in re.finditer(rb'[\x20-\x7e]{8,}',pt)]
        for s in ss[:4]: print('    '+repr(s[:70]))
