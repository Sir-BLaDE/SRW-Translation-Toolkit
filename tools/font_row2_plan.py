import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); W=4096; HDR=40; N=(len(p3)-HDR)//36
byc={}
for g in range(N):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
need=list('áéíóúñÁÉÍÓÚü¿¡')
print('row3 records:')
for ch in need: print(' ',repr(ch),'U+%04X'%ord(ch),'g=',byc.get(ord(ch)))

d=cf.plain(rows[2]); h=[struct.unpack_from('<I',d,i*4)[0] for i in range(12)]
s=d[h[6]:h[7]].decode('utf-8','ignore')
two=[(i,ch) for i,ch in enumerate(s) if len(ch.encode('utf-8'))==2]
print('row2 2-byte chars:',len(two))
print(''.join(ch for _,ch in two))
print('last 40:', [(hex(ord(c)),c) for c in s[-40:]])
# gap bytes
print('gap row2', d[h[7]:h[8]].hex())
