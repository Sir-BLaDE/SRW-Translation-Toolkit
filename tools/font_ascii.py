import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p = sys.argv[1] if len(sys.argv)>1 else r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); W=4096; HDR=40; N=(len(p3)-HDR)//36
byc={}
for g in range(N):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]
    byc.setdefault(u,g)
def art(ch):
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    print('--- %r U+%04X g=%d box=(%d,%d,%d,%d)'%(ch,ord(ch),g,x,y,w,h))
    for yy in range(h):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        print(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
for ch in sys.argv[2:] or ['?','¿','!','¡','a','á','n','ñ','o','ó']:
    art(ch)
