import sys, pathlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
for p in [r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/CMN00.CPK',
          r'C:/Dev/Default Project/srwv/backup/CMN00_CPK_original.cpk']:
    c=load(p)
    print(p)
    print(' rows', [(r['id'],r['size'],r['ex']) for r in c.rows])
    for rid in [0,1]:
        if rid in {r['id'] for r in c.rows}:
            a=c.plain([r for r in c.rows if r['id']==rid][0])
            print('  f%d len=%d head=%s'%(rid,len(a),a[:16].hex()))
for f in [r'C:/Dev/Default Project/srwv/outputs/cmn_f1_test.bin',
          r'C:/Dev/Default Project/srwv/outputs/cmn_f1_traducido.bin']:
    b=pathlib.Path(f).read_bytes()
    print(f, len(b), b[:16].hex())
