import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
H=os.environ['HOME']+'/mnt/Super Robot Wars V/'
pats=[x.encode() for x in sys.argv[1:]]
import glob
fs=[H+'Data/AIDDATA/EN/SysText.cpk',H+'Data/AIDDATA/EN/LayoutData.cpk',H+'Data/KURODATA/EN/KPACK_P4_LN_EN.CPK',H+'Data/KURODATA/EN/KPACK_P4_RG_EN.CPK',H+'Data/KURODATA/CMN/KPACK_PC_CMN.cpk']
fs+=glob.glob(H+'CommonData/hiyama/defaultSS_E.cpk')
for f in fs:
    k=load(f)
    for r in k.rows:
        p=k.plain(r)
        for pt in pats:
            for m in list(re.finditer(re.escape(pt),p))[:6]:
                print(os.path.basename(f),r['id'],hex(m.start()),p[max(0,m.start()-30):m.start()+50])
