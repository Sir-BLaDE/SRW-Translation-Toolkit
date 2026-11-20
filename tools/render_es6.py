"""render_es6.py - dibuja los glifos acentuados de es6."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
W,HDR=4096,40
p=r'C:/Dev/Default Project/srwv/outputs/FontInfo_es6.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
def art(ch):
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    o=[]
    for yy in range(min(h,36)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
for ch in ['a','á','i','í','e','é','A','Á','I','Í','ñ','¿']:
    print('\n=== es6 %s ==='%ch)
    for ln in art(ch): print(' '+ln)
