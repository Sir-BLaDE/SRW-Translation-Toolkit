"""space3000_check.py - comprueba el glifo de U+3000 (espacio ideografico)
en la fuente instalada y su presencia en los mapas."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
for tag,p in [('ORIG',r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'),
              ('INST',r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')]:
    cf=load(p); rows={r['id']:r for r in cf.rows}
    p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36 if False else (len(p3)-40)//36
    byc={}
    for g in range(n):
        u=struct.unpack_from('<I',p3,40+g*36)[0]; byc.setdefault(u,g)
    print('\n===',tag)
    for cp,name in [(0x3000,'U+3000 ideographic space'),(0x20,'U+0020 space'),(0xA5,'yen')]:
        g=byc.get(cp)
        print(' %-26s g=%s'%(name,g))
        if g is not None:
            fl=struct.unpack_from('<8f',p3,40+g*36+4)
            x=int(round(fl[0]*4096)); y=int(round(fl[1]*4096)); w=int(round(fl[2]*4096)); h=int(round(fl[3]*4096))
            print('    b=%.0f a=%.0f x=%d y=%d w=%d h=%d'%(fl[4],fl[5],x,y,w,h))
            for yy in range(min(h,40)):
                row=tex[(y+yy)*4096+x:(y+yy)*4096+x+w]
                print('    '+''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    for rid in (1,2):
        d=cf.plain(rows[rid]); h=[struct.unpack_from('<I',d,i*4)[0] for i in range(12)]
        s=d[h[6]:h[7]].decode('utf-8','ignore')
        print(' mapa%d: U+3000 en mapa=%s'%(rid,'　' in s))
