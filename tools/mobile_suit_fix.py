import os,sys,re,glob,shutil
sys.path.insert(0,os.environ['HOME']+'/mnt/srwv/tools'); sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME']; P=H+'/mnt/srwv/'; R=H+'/mnt/Super Robot Wars V/'
SUBS=[(r'[Tt]rajes móviles','Mobile Suits'),(r'[Tt]raje móvil','Mobile Suit')]
ROBOT=[(r'\b(ese|este|ese|ese) traje(?!s)',r'\1 robot'),(r'un traje fascinante','un robot fascinante'),(r'traje de Crux Dogatie','robot de Crux Dogatie')]
def fix(t,robot):
    n=0
    for a,b in SUBS: t,c=re.subn(a,b,t); n+=c
    if robot:
        # solo las frases revisadas a mano (ver informe): no tocar 'traje' como ropa
        for rid in ():
            pass
    return t,n
def run(src,out,robot_rows=()):
    k=load(src); new={}; n=0
    for r in k.rows:
        try:t=k.plain(r).decode('utf8','surrogateescape')
        except Exception: continue
        t2,c=fix(t,False)
        if r['id'] in robot_rows:
            for a,b in robot_rows[r['id']]:
                t2,c2=re.subn(a,b,t2); c+=c2
        if t2!=t: new[r['id']]=(k.cipher(r,t2.encode('utf8','surrogateescape')),len(t2.encode('utf8','surrogateescape'))); n+=c
    blob=B.build_ordered(src,new) if new else open(src,'rb').read()
    open(out,'wb').write(blob)
    k2=load(out); bad=[x['id'] for x in k2.rows if x['ex']!=len(k2.plain(x))]
    print(os.path.basename(src),n,'cambios',len(new),'filas bad',bad,flush=True)
    return new
if __name__=='__main__':
    w=sys.argv[1]
    if w=='small':
        os.makedirs(P+'outputs/ms',exist_ok=True)
        # SysText/rpw_jstr: títulos 'Traje móvil Gundam…' sin holgura en el pool -> no se tocan.
        SUBS=[(r'[Tt]raje móvil','Mobile Suit ')]   # mismos bytes (ó=2 bytes)
        run(R+'Data/KURODATA/EN/KPACK_P4_LN_EN.CPK',P+'outputs/ms/KPACK_P4_LN_EN.CPK')
    elif w=='stg':
        rr={}
        for (rid,subs) in [(404,[('ese traje','ese robot')]),(339,[('este traje','este robot')]),(477,[('ese traje','ese robot')]),(625,[('un traje fascinante','un robot fascinante')]),(459,[('ese traje','ese robot')])]: rr.setdefault(rid,[]).extend(subs)
        run(R+'Data/STAGE/STGEST_EN.CPK',P+'outputs/ms/STGEST_EN.cpk',rr)
    else:
        os.makedirs(P+'outputs/ms/dlc',exist_ok=True)
        for f in sorted(glob.glob(R+'Data/DLCDIRE/EN/dlc*_en.cpk')): run(f,P+'outputs/ms/dlc/'+os.path.basename(f))
