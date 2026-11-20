"""accent_glyphs_art.py - dibuja los glifos de acento de la fuente original."""
import sys, struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
ORIG=r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
W,HDR=4096,40
cf=load(ORIG); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4])
n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
def art(cp):
    g=byc.get(cp)
    if g is None: return None,[]
    off=HDR+g*36; fl=struct.unpack_from('<8f',p3,off+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    o=[]
    for yy in range(min(h,40)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return g,o
for cp,name in [(0xB4,'acute ´'),(0x7E,'tilde ~'),(0xA8,'dia ¨'),(0xA5,'yen ¥'),(0x5C,'backslash \\'),(0xA1,'inverted !'),(0xBF,'inverted ?'),(0x21,'!'),(0x3F,'?')]:
    g,o=art(cp)
    print('\n=== U+%04X %s g=%s ==='%(cp,name,g))
    for ln in o: print(' '+ln)
