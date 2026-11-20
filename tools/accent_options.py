"""accent_options.py - muestra todas las opciones de glifo 'acento agudo'
disponibles en la fuente original, para elegir la que mejor se vea."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
W=4096;HDR=40
cf=load(r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk')
rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
def art(g):
    if g is None: return []
    fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    o=[]
    for yy in range(min(h,16)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
# codepoints que suelen ser marcas de acento/acento agudo en fuentes japonesas
for cp,name in [(0xB4,'´ U+00B4 acute (usado)'),(0x60,'` U+0060 grave'),
                (0xA8,'¨ U+00A8 dieresis'),(0x7E,'~ U+007E tilde'),
                (0x2032,'′ U+2032 prime'),(0x00B7,'· U+00B7 middle dot'),
                (0x3099,'゙ U+3099 dakuten'),(0x309A,'゚ U+309A handakuten'),
                (0x02B9,'ʹ U+02B9 modifier letter prime'),(0x02BA,'ʺ U+02BA')]:
    g=byc.get(cp)
    print('\n=== %s g=%s ==='%(name,g))
    if g is not None:
        for ln in art(g): print('  '+ln)
