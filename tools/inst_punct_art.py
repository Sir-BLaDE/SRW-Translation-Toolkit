"""inst_punct_art.py - dibuja ¿ y ¡ en la fuente instalada (es2) y en es3."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
W,HDR=4096,40
FILES=[('es2 instalada',r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'),
       ('es3 build',r'C:/Dev/Default Project/srwv/outputs/FontInfo_es3.cpk')]
for tag,p in FILES:
    cf=load(p); rows={r['id']:r for r in cf.rows}
    p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
    byc={}
    for g in range(n):
        u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
    for cp,name in [(0xBF,'¿'),(0xA1,'¡')]:
        g=byc.get(cp)
        print('\n=== %s %s g=%s ==='%(tag,name,g))
        if g is None: continue
        fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
        x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
        print('   b=%.0f a=%.0f w=%d h=%d'%(fl[4],fl[5],w,h))
        for yy in range(min(h,40)):
            row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
            print('   '+''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
