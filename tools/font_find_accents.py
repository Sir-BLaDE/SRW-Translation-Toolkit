import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p1=cf.plain(rows[1]); p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); W=4096; HDR=40
N=(len(p3)-HDR)//36
byc={}
for g in range(N):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)

def art(ch):
    g=byc.get(ord(ch))
    if g is None: print('--- %r: sin glifo'%ch); return
    fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    print('--- %r U+%04X g=%d box=(%d,%d,%d,%d) b=%.0f a=%.0f ink=%.0f'%(
        ch,ord(ch),g,x,y,w,h,fl[4],fl[5],fl[7]))
    for yy in range(min(h,44)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        print(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))

for ch in ['´','`','¨','~','^',"'",'‘','’','"','"','«','»']:
    art(ch)
