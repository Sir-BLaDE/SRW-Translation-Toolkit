import sys, struct
from PIL import Image
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); W=4096; HDR=40; N=(len(p3)-HDR)//36
f=[]
for g in range(N):
    off=HDR+g*36; u=struct.unpack_from('<I',p3,off)[0]
    fl=struct.unpack_from('<8f',p3,off+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    if (w,h)!=(40,44): continue
    px=tex[(y+4)*W+x:(y+4)*W+x+w]
    # detect filler: pixels only in x 0..5, y 15..20
    found=[]
    for yy in range(h):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        for xx,v in enumerate(row):
            if v>30: found.append((xx,yy))
    if found and all(0<=xx<=5 and 15<=yy<=20 for xx,yy in found):
        f.append((g,u))
print('fillers',len(f),f[:60])
