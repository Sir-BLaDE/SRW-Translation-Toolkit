import os,sys,struct,hashlib,glob,shutil
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'))
import cpk_util as U,fastinf
U.inflate=fastinf.inflate
from cpk_util import load
G=os.path.expanduser('~/mnt/Super Robot Wars V');S=os.path.expanduser('~/mnt/srwv/')
SRC=G+'/Data/ANIME/effwin.cpk';OUT=S+'outputs/effwin_es_v1.cpk'
c=load(SRC);cpk=c.cpk;raw=bytearray(cpk.raw);toc=cpk.toc
new={}
for f in glob.glob(os.path.expanduser('~/blobs/eff_*.bin')):
    new[int(os.path.basename(f)[4:-4])]=open(f,'rb').read()
for rid,blob in sorted(new.items()):
    f=[x for x in c.rows if x['id']==rid][0]
    while len(raw)%2048: raw+=b'\0'
    off=len(raw)-cpk.toc_offset;raw+=blob
    struct.pack_into('>Q',raw,cpk.cell_offset(toc,'FileOffset',f['row']),off)
    struct.pack_into('>I',raw,cpk.cell_offset(toc,'FileSize',f['row']),len(blob))
open(OUT,'wb').write(bytes(raw))
print(len(new),len(raw),hashlib.sha256(bytes(raw)).hexdigest()[:12],flush=True)
k=load(OUT);ok=True
for rid in sorted(new):
    r=[x for x in k.rows if x['id']==rid][0]
    p=k.plain(r)
    good=(len(p)==r['ex'] and p==open(os.path.expanduser(f'~/blobs/eff_{rid}.raw'),'rb').read())
    ok&=good
    if not good: print('BAD',rid)
print('verify',ok,'rows',len(k.rows)==len(c.rows))
