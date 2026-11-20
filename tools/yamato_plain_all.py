"""yamato_plain_all.py - busca 'Yamato' en el TEXTO DECODEADO de todos los
CPK instalados, mostrando los bytes delante/detras."""
import os, re, sys
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
G=r'D:/Juegos/-SPARROW-/Super Robot Wars V'
pat=re.compile('Yamato')
count=0
for root,dirs,files in os.walk(G):
    for f in files:
        if not f.lower().endswith('.cpk'): continue
        p=os.path.join(root,f)
        try: c=load(p)
        except Exception: continue
        for r in c.rows:
            try: pt=c.plain(r)
            except Exception: continue
            s=pt.decode('utf-8','ignore')
            for m in pat.finditer(s):
                count+=1
                before=s[max(0,m.start()-20):m.start()]
                after=s[m.end():m.end()+20]
                if count<=80:
                    print('%-30s r%-4d ..%r Yamato %r..'%(os.path.relpath(p,G)[:30],r['id'],before,after))
print('TOTAL Yamato en texto decodeado:',count)
