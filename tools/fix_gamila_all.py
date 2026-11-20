import os,sys,hashlib,shutil
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
H=os.environ['HOME']; P=H+'/mnt/srwv/'; G=H+'/mnt/Super Robot Wars V/'
JOBS=[
 ('CommonData/MtData/EN/rpw_jstr.cpk',{0:[(b'Capit\xc3\xa1n de Gamillas\x00',b'Capit\xc3\xa1n de Gamilas\x00'),(b'Soldado de Gamillas\x00',b'Soldado de Gamilas\x00')]}),
 ('Data/BTLC/EN0/OP.CPK',{0:[(b'Capit\xc3\xa1n Gamillas\x00',b'Capit\xc3\xa1n Gamilas\x00')]}),
 ('Data/AIDDATA/EN/Prologue.cpk',{1:[(b'ambled on a last stand with the Gamillans near Pluto.\x00',b' \x00')],2:[(b'ambled on a last stand with the Gamillans near Pluto.\x00',b' \x00')]}),
]
for rel,rows in JOBS:
    src=G+rel; bk=P+'backup/antes_auditoria_20261119/'+os.path.basename(rel)
    if not os.path.exists(bk): shutil.copy2(src,bk)
    c=load(bk); new={}
    for rid,subs in rows.items():
        row=[r for r in c.rows if r['id']==rid][0]; pt=c.plain(row)
        for o,n in subs:
            assert pt.count(o)>=1,(rel,o); 
            nn=n+b'\x00'*(len(o)-len(n)); assert len(nn)==len(o); pt=pt.replace(o,nn)
        new[rid]=(c.cipher(row,pt),len(pt)); 
    out=P+'outputs/'+os.path.basename(rel)+'.auditoria1'
    blob=build_ordered(bk,new); open(out,'wb').write(blob)
    k=load(out)
    for r in k.rows: assert r['ex']==len(k.plain(r))
    print(rel,len(blob),hashlib.sha256(blob).hexdigest()[:12])
