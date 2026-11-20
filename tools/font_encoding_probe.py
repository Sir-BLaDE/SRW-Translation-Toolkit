import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(p); rows={r['id']:r for r in cf.rows}
for rid in [0,1,2,3]:
    d = cf.plain(rows[rid])
    print('=== row',rid,'len',len(d))
    for ch in ['a','á','ñ','¿','¡','é','ó','?','!']:
        cp=ord(ch)
        pats = {
          'utf8': ch.encode('utf-8'),
          'utf16le': struct.pack('<H',cp),
          'utf16be': struct.pack('>H',cp),
          'u32le': struct.pack('<I',cp),
        }
        hits=[]
        for nm,pat in pats.items():
            i=0
            while True:
                i=d.find(pat,i)
                if i<0: break
                hits.append((nm,i,d[max(0,i-4):i+12].hex()))
                i+=1
                if len(hits)>12: break
        print(' ',repr(ch),'U+%04X'%cp, hits[:8])

# section headers of row1
d=cf.plain(rows[1])
print('row1 header u32:', [struct.unpack_from('<I',d,i*4)[0] for i in range(12)])
for off in [0x30,0x942,0x978,0x9d0]:
    print('row1 @%x'%off, d[off:off+64].hex())

# row0 as u32 array sample
d=cf.plain(rows[0])
u=[struct.unpack_from('<I',d,i*4)[0] for i in range(len(d)//4)]
print('row0 first 80 u32:', [hex(x) for x in u[:80]])
