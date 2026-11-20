"""yen_deep.py - busca ¥ (y variantes) en TODOS los CPK del juego, decodificando
con utf-8, shift-jis y utf-16, y comprueba si la fuente tiene el glifo."""
import sys, os, re, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

# 1) fuente: esta ¥ en los mapas? tiene glifo?
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); HDR=40; W=4096; N=(len(p3)-HDR)//36
byc={}
for g in range(N): byc.setdefault(struct.unpack_from('<I',p3,HDR+g*36)[0],g)
for rid in (1,2):
    d=cf.plain(rows[rid]); h=[struct.unpack_from('<I',d,i*4)[0] for i in range(12)]
    s=d[h[6]:h[7]].decode('utf-8','ignore')
    print('fila %d: ¥ en mapa=%s | ￥ en mapa=%s | 円 en mapa=%s' % (
        rid, '¥' in s, '￥' in s, '円' in s))
for cp in (0xA5,0xFFE5,0x56E3):
    print('U+%04X en fuente: %s' % (cp, byc.get(cp)))

# 2) buscar en TODOS los cpk del juego
G=r'D:/Juegos/-SPARROW-/Super Robot Wars V'
hits=[]
for root,dirs,files in os.walk(G):
    for f in files:
        if not f.lower().endswith(('.cpk',)): continue
        p=os.path.join(root,f)
        try: c=load(p)
        except Exception: continue
        for r in c.rows:
            try: pt=c.plain(r)
            except Exception: continue
            for enc in ('utf-8','shift-jis','utf-16-le'):
                try: s=pt.decode(enc)
                except Exception: continue
                for y in ('¥','￥','円'):
                    for m in re.finditer(re.escape(y),s):
                        ctx=s[max(0,m.start()-40):m.end()+40].replace('\n',' ').replace('\r',' ').replace('\x00','')
                        hits.append((f,r['id'],enc,y,ctx))
print('\ntotal hits:',len(hits))
seen=set()
for f,rid,enc,y,ctx in hits[:80]:
    k=(f,rid,ctx)
    if k in seen: continue
    seen.add(k)
    print(' %-24s r%-3d %-9s %r : %r'%(f,rid,enc,y,ctx[:90]))
