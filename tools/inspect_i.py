"""inspect_i.py - dibuja i, í, j y acentos en es5, y busca fuentes del sistema parecidas."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
W,HDR=4096,40
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
def art(ch):
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    print('\n=== %r g=%d b=%.0f a=%.0f x=%d y=%d w=%d h=%d ==='%(ch,g,fl[4],fl[5],x,y,w,h))
    for yy in range(min(h,36)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        print(' '+''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
for ch in ['i','í','j','a','á','1','l']: art(ch)
