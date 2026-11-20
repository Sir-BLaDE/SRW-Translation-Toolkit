"""prologue_image_probe.py - lista el contenido de PrologueImage.cpk."""
import sys
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/COMMON/PrologueImage.cpk'
c=load(p)
print('filas:',len(c.rows))
for r in c.rows[:60]:
    pt=c.plain(r)
    print('id=%-5s ex=%-9s len=%-9s head=%s'%(r['id'],r['ex'],len(pt),pt[:20].hex(' ')))
