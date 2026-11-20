"""yen_glyph_map.py - investiga por que aparece un yen tras 'Yamato'.

Comprueba que glifo tiene el codepoint del yen (U+00A5), de la barra
invertida (U+005C) y del corchete de cierre de dialogo (U+300D), tanto en
la fuente original como en la instalada, y que codepoints del MAPA apuntan
a ese glifo.
"""
import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

ORIG = r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
INST = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
W, HDR = 4096, 40

class F:
    def __init__(self, p, tag):
        self.tag=tag
        self.cf=load(p); rows={r['id']:r for r in self.cf.rows}
        self.p3=self.cf.plain(rows[3]); self.tex=self.cf.plain(rows[4])
        self.n=(len(self.p3)-HDR)//36
        self.byc={}
        for g in range(self.n):
            u=struct.unpack_from('<I',self.p3,HDR+g*36)[0]
            self.byc.setdefault(u,g)
        # mapas fila 1 y 2
        self.maps={}
        for rid in (1,2):
            data=self.cf.plain(rows[rid])
            h=[struct.unpack_from('<I',data,i*4)[0] for i in range(12)]
            a,b=h[6],h[7]
            self.maps[rid]=data[a:b].decode('utf-8','ignore')
    def glyph(self, cp):
        return self.byc.get(cp)
    def art(self, g, maxh=40):
        if g is None: return ['(sin glifo)']
        off=HDR+g*36; fl=struct.unpack_from('<8f',self.p3,off+4)
        x=int(round(fl[0]*W)); y=int(round(fl[1]*W))
        w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
        if w<=0 or h<=0: return ['(w/h=0)']
        out=[]
        for yy in range(min(h,maxh)):
            row=self.tex[(y+yy)*W+x:(y+yy)*W+x+w]
            out.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
        return out

fo,fi=F(ORIG,'ORIG'),F(INST,'INST')
CPS={'yen':0xA5,'backslash':0x5C,'fullwidth_yen':0xFFE5,
     'close_br':0x300D,'open_br':0x300C,'circum':0x5E,'tilde':0x7E}

print('=== glifos por codepoint ===')
for name,cp in CPS.items():
    print('\n-- %s U+%04X --'%(name,cp))
    for f in (fo,fi):
        g=f.glyph(cp)
        print(' %s g=%s'%(f.tag,g))
        if g is not None:
            for ln in f.art(g): print('   '+ln)

# Encontrar que glifo es "yen" visualmente: buscar codepoints cuyo glifo tiene
# la misma firma de bits que el yen de la fuente original
def sig(f,g):
    return '\n'.join(f.art(g,maxh=64))
yen_g=fo.glyph(0xA5)
print('\n=== codepoints que comparten el glifo del yen (g=%s) ==='%yen_g)
for f in (fo,fi):
    cps=[cp for cp,g in f.byc.items() if g==yen_g]
    print(' %s codepoints: %s'%(f.tag,[hex(c) for c in sorted(cps)]))

print('\n=== posicion del yen en los MAPAS (fila1/fila2) ===')
for f in (fo,fi):
    for rid,s in f.maps.items():
        for c in ['¥','\\','」','＼','￥','~','^']:
            if c in s:
                i=s.index(c)
                print(' %s mapa%d %r en posicion %d'%(f.tag,rid,c,i))
