import sys, pathlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_bltu import load
for f in [r'C:/Dev/Default Project/srwv/outputs/cmn_f1_test.bin',
          r'C:/Dev/Default Project/srwv/outputs/cmn_f1_traducido.bin']:
    b=pathlib.Path(f).read_bytes()
    t=load(b)
    alls=[x[3] for x in t.all_strings()]
    acc=[s for s in alls if any(ord(c)>127 and c not in '¡¿' for c in s)]
    inv=[s for s in alls if '¿' in s or '¡' in s]
    print(f,'chunks',len(t.chunks),'strings',len(alls),'acc',len(acc),'inv',len(inv))
    for s in acc[:3]: print('  ACC',repr(s[:70]))
    for s in inv[:3]: print('  INV',repr(s[:70]))
