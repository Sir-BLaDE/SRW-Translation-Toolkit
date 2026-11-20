"""composed_art.py - dibuja las letras acentuadas ya compuestas en es3."""
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
    g=byc.get(ord(ch))
    if g is None: return None
    fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    o=[]
    for yy in range(min(h,40)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
for ch in ['a','á','e','é','A','Á','n','ñ','i','í']:
    o=art(ch)
    print('\n=== %s ==='%ch)
    if o:
        for ln in o: print(' '+ln)
