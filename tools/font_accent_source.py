"""font_accent_source.py - compara los acentos de YuGothM/Arial con el juego."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from PIL import Image,ImageDraw,ImageFont
W,HDR=4096,40
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
from cpk_util import load
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
def game_art(ch):
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    o=[]
    for yy in range(min(h,36)):
        row=tex[(y+yy)*W+x:(y+yy)*W+x+w]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
def src_art(ch,fp,size,idx=0):
    f=ImageFont.truetype(fp,size,index=idx)
    im=Image.new('L',(size*3,size*3),0)
    ImageDraw.Draw(im).text((size,size//4),ch,font=f,fill=255)
    bb=im.getbbox(); im=im.crop(bb)
    o=[]
    for yy in range(min(im.height,36)):
        row=[im.getpixel((xx,yy)) for xx in range(im.width)]
        o.append(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))
    return o
SOURCES=[('YuGothM',r'C:/Windows/Fonts/YuGothM.ttc',38,0),
         ('Arial',r'C:/Windows/Fonts/arial.ttf',32,0)]
for label,fp,size,idx in SOURCES:
    for ch in ['á','é','í','ñ','¿','¡']:
        print('\n=== %s %s ==='%(label,ch))
        for ln in src_art(ch,fp,size,idx): print(' '+ln)
print('\n\n######## JUEGO (es5) ########')
for ch in ['á','é','í','ñ','¿','¡']:
    print('\n=== juego %s ==='%ch)
    for ln in game_art(ch): print(' '+ln)
