"""prologue_yamato.py - busca Yamato, ¥, U+FFE5, 円 en Prologue.cpk (EN/JP)."""
import sys,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
for lang in ['EN','JP']:
    p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/%s/Prologue.cpk'%lang
    c=load(p)
    print('\n########',lang,'filas',len(c.rows))
    for r in c.rows:
        pt=c.plain(r)
        s=pt.decode('utf-8','ignore')
        hits=[]
        for pat,name in [('Yamato','Yamato'),('ヤマト','ヤマト'),('¥','yen'),('￥','fwyen'),('円','円'),('\\','barra')]:
            for m in re.finditer(re.escape(pat),s):
                hits.append((m.start(),name,s[max(0,m.start()-40):m.end()+40]))
        for off,name,ctx in hits[:12]:
            print(' r%-3d %-8s @%-6d %r'%(r['id'],name,off,ctx))
