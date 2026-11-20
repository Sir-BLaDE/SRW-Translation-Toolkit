import os,sys,re,glob,collections,json
sys.path.insert(0,'/tmp/b')
from cpk_util import load
P=os.environ['HOME']+'/mnt/srwv/'
sp=collections.Counter(); gam=collections.Counter(); caps=collections.Counter()
for f in sorted(glob.glob(P+'outputs/dlc_es/dlc*_en.cpk')):
    k=load(f)
    for r in k.rows:
        t=k.plain(r).decode('utf8','replace')
        for m in re.finditer(r'\[\[((?:　)*)([^\r\n]*)\r\n',t): sp[m.group(2)]+=1
        for m in re.finditer(r'\b\w*[Gg]amil\w*\b',t): gam[m.group(0)]+=1
json.dump({'sp':sp,'gam':gam},open('/tmp/dsurvey.json','w'),ensure_ascii=False)
print(gam.most_common(30)); print(len(sp)); print(sp.most_common(400))
