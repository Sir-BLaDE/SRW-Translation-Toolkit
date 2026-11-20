"""fontmap_diff.py - diff caracter a caracter de los mapas de fuente original
vs instalado, mostrando que codepoint habia y cual hay ahora en cada posicion."""
import sys
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
ORIG=r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
INST=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
import struct
def maps(p):
    cf=load(p); rows={r['id']:r for r in cf.rows}; out={}
    for rid in (1,2):
        d=cf.plain(rows[rid]); h=[struct.unpack_from('<I',d,i*4)[0] for i in range(12)]
        out[rid]=d[h[6]:h[7]].decode('utf-8','ignore')
    return out
a,b=maps(ORIG),maps(INST)
for rid in (1,2):
    x,y=a[rid],b[rid]
    print('=== MAPA %d  orig=%d inst=%d ==='%(rid,len(x),len(y)))
    if len(x)!=len(y):
        print('  LONGITUDES DISTINTAS')
    n=min(len(x),len(y))
    for i in range(n):
        if x[i]!=y[i]:
            print('  pos %-4d  %s U+%04X  ->  %s U+%04X'%(
                i,repr(x[i]),ord(x[i]),repr(y[i]),ord(y[i])))
