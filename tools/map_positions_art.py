"""map_positions_art.py - dibuja los glifos en las posiciones del MAPA donde
estan los caracteres sospechosos (」, ￥, ＼, \), por si el motor usa la
posicion del mapa como indice de glifo.
"""
import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
ORIG=r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
W,HDR=4096,40
cf=load(ORIG); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4])
n=(len(p3)-HDR)//36
data=cf.plain(rows[1]); h=[struct.unpack_from('<I',data,i*4)[0] for i in range(12)]
s=data[h[6]:h[7]].decode('utf-8','ignore')
print('longitud mapa:',len(s))
def art(g):
    if g>=n: return ['(fuera de rango)']
    off=HDR+g*36; fl=struct.unpack_from('<8f',p3,off+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); hh=int(round(fl[3]*W))
    if w<=0 or hh<=0: return ['(w/h=0)']
    o=[]
    for yy in range(min(hh,40)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
for ch in ['」','＼','￥','\\','~','^']:
    if ch not in s: continue
    pos=s.index(ch)
    print('\n=== %r pos=%d -> glifo %d ==='%(ch,pos,pos))
    for ln in art(pos): print(' '+ln)
