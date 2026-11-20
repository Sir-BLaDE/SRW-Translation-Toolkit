import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p = sys.argv[1] if len(sys.argv)>1 else r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
for rid in [1,2]:
    d=cf.plain(rows[rid])
    h=[struct.unpack_from('<I',d,i*4)[0] for i in range(12)]
    print('=== row',rid,'header',h)
    a,b,c,n,e,f=h[6:12]
    print(' offsets: mapstart=%d mapend=%d table=%d n=%d end=%d'%(a,b,c,n,e))
    s=d[a:b].decode('utf-8','ignore')
    print(' map len',len(s),'sample:',repr(s[:120]))
    print(' tail:',repr(s[-80:]))
    chars=['a','á','é','í','ó','ú','ñ','¿','¡','?','!','A','E','O','U','ü','º','ª']
    print(' present:',[(c,c in s) for c in chars])
    tbl=[struct.unpack_from('<I',d,c+i*4)[0] for i in range(n)]
    print(' table:',tbl)
    # show slices by table
    for i,t in enumerate(tbl):
        if t<b-a:
            print('  sec%d @%d:'%(i,t), repr(s[t:t+24]))
