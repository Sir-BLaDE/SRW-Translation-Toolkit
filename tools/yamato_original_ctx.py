"""yamato_original_ctx.py - contexto de 'Yamato' en la historia ORIGINAL (backup)."""
import sys,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import glob,os
for p in glob.glob(r'C:/Dev/Default Project/srwv/backup/*STGEST*'):
    print('ARCHIVO:',p)
    c=load(p)
    for r in c.rows:
        pt=c.plain(r); s=pt.decode('utf-8','ignore')
        for m in re.finditer('Yamato',s):
            a=s[max(0,m.start()-30):m.start()]
            b=s[m.end():m.end()+30]
            print(' r%-3d ..%r  YAMATO  %r..'%(r['id'],a,b))
