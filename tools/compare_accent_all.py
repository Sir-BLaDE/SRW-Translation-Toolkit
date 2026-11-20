"""compare_accent_all.py - dibuja á/é/Á en es3, es4 y es5."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
W,HDR=4096,40
FILES=[('es3',r'C:/Dev/Default Project/srwv/outputs/FontInfo_es3.cpk'),
       ('es4',r'C:/Dev/Default Project/srwv/outputs/FontInfo_es4.cpk'),
       ('es5',r'C:/Dev/Default Project/srwv/outputs/FontInfo_es5.cpk'),
       ('es6',r'C:/Dev/Default Project/srwv/outputs/FontInfo_es6.cpk')]
def render(cf,ch,nrows=14):
    rows={r['id']:r for r in cf.rows}
    p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
    byc={}
    for g in range(n):
        u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    o=[]
    for yy in range(min(h,nrows)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
for tag,p in FILES:
    cf=load(p)
    for ch in ['á','é','Á']:
        print('\n=== %s %s ==='%(tag,ch))
        for ln in render(cf,ch): print(' '+ln)
