"""font_diag_visual.py - compara metricas y dibuja los glifos problematicos
de la fuente original vs la instalada."""
import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

ORIG = r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
INST = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
W = 4096; HDR = 40

class F:
    def __init__(self, p):
        self.cf = load(p); rows = {r['id']: r for r in self.cf.rows}
        self.p3 = self.cf.plain(rows[3]); self.tex = self.cf.plain(rows[4])
        self.n = (len(self.p3)-HDR)//36
        self.byc = {}
        for g in range(self.n):
            u = struct.unpack_from('<I', self.p3, HDR+g*36)[0]
            self.byc.setdefault(u, g)
    def info(self, ch):
        g = self.byc.get(ord(ch))
        if g is None: return None
        off = HDR+g*36
        fl = struct.unpack_from('<8f', self.p3, off+4)
        x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
        bb=(x,y,w,h)
        px=img=None
        for yy in range(h):
            row=self.tex[(y+yy)*W+x:(y+yy)*W+x+w]
            for xx,v in enumerate(row):
                if v>30:
                    if px is None: px=[xx,yy,xx,yy]
                    else: px[0]=min(px[0],xx); px[1]=min(px[1],yy); px[2]=max(px[2],xx); px[3]=max(px[3],yy)
        return g, fl, bb, px
    def art(self, ch, maxh=44):
        g=self.byc.get(ord(ch))
        if g is None: return ['(sin glifo)']
        off=HDR+g*36; fl=struct.unpack_from('<8f', self.p3, off+4)
        x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
        out=[]
        for yy in range(min(h,maxh)):
            row=self.tex[(y+yy)*W+x:(y+yy)*W+x+w]
            out.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
        return out

chars = ['a','á','e','é','i','í','o','ó','u','ú','n','ñ','A','Á','E','É','O','Ó','U','Ú','?','¿','!','¡']
fo, fi = F(ORIG), F(INST)
def fmt(v):
    if not v: return '(none)'
    g,fl,bb,px=v
    return 'g%-4d b=%-3.0f a=%-3.0f i=%-3.0f bb=%s' % (g,fl[4],fl[5],fl[7],px)
print('%-5s %-28s %-28s' % ('CH','ORIGINAL (g,bear,adv,ink,bb)','INSTALADA (g,bear,adv,ink,bb)'))
for ch in chars:
    print('%-5s %-28s %-28s' % (repr(ch), fmt(fo.info(ch)), fmt(fi.info(ch))))
