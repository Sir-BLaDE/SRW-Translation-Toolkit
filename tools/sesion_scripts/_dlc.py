import os,sys,re,glob
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/DLCDIRE/EN/'
tot=0
for f in sorted(glob.glob(D+'dlc*_en.cpk')):
    k=load(f); hits=0;n=0
    for r in k.rows:
        p=k.plain(r)
        n+=len(re.findall(rb'\[\[[^\r\n]*\r\n\xe3\x80\x8c',p))
        if b'stowaway' in p or b'agile fighters' in p: hits+=1; print('  FOUND',os.path.basename(f),r['id'])
    tot+=n
    print(os.path.basename(f),len(k.rows),'lineas',n,flush=True)
print('total',tot)
