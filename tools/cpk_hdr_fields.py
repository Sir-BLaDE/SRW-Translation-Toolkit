import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_cpk import Cpk
for p in sys.argv[1:]:
    c=Cpk(p)
    h=c.header.row(0)
    print('===',p)
    for k,v in h.items(): print(' ',k,'=',v if not isinstance(v,bytes) else v[:16].hex())
