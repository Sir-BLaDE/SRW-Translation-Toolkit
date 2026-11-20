import os,sys,glob
sys.path.insert(0,os.environ['HOME']+'/mnt/srwv/tools'); sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B, genero_dirigido as D
H=os.environ['HOME']; P=H+'/mnt/srwv/'
def run(src,out,apply=True):
    k=load(src); rows={}
    for r in k.rows:
        try: rows[r['id']]=k.plain(r).decode('utf8')
        except Exception: pass
    tg=D.table_gender_map(rows); names=D.speakers_of(rows); rep=[]; new={}
    byid={r['id']:r for r in k.rows}
    for j in sorted({j for j,_ in tg}):
        t2=D.process_row(rows[j],lambda n,j=j:tg.get((j,n)),names,j,rep)
        if t2!=rows[j]: new[j]=(k.cipher(byid[j],t2.encode()),len(t2.encode()))
    for r in rep: print(os.path.basename(src)[:8],r[0],r[1],r[2],r[3],'|',r[5][:100],'=>',[(a[-20:],b[-18:]) for a,b in r[6]])
    if apply and new:
        open(out,'wb').write(B.build_ordered(src,new))
        k2=load(out); print('bad',[r['id'] for r in k2.rows if r['ex']!=len(k2.plain(r))],len(new),'filas')
    return len(rep)
if __name__=='__main__':
    w=sys.argv[1]; ap=len(sys.argv)>2 and sys.argv[2]=='apply'
    R=H+'/mnt/Super Robot Wars V/Data/'
    if w=='stg': run(R+'STAGE/STGEST_EN.CPK',P+'outputs/STGEST_EN_es_gen3.cpk',ap)
    else:
        os.makedirs(P+'outputs/dlc_es5',exist_ok=True)
        for f in sorted(glob.glob(P+'outputs/dlc_es3/dlc*_en.cpk')): run(f,P+'outputs/dlc_es5/'+os.path.basename(f),ap)
