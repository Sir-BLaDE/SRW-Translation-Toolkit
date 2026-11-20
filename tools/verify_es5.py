import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es5.cpk'
cf=load(p)
print('diag', cf.cpk.diagnose() or 'ok')
for r in cf.rows:
    pt=cf.plain(r)
    print('id',r['id'],'table',r['table'],'size',r['size'],'ex',r['ex'],'plain',len(pt),'OK' if r['ex']==len(pt) else 'MISMATCH')
