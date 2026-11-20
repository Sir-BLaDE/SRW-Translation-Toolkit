import os,sys,re,json,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
H=os.environ['HOME']
o=load(H+'/mnt/srwv/backup/STGEST_EN_original.cpk'); n=load(H+'/mnt/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK')
S=re.compile(rb'\[\[((?:\xe3\x80\x80)*)([^\r\n\]]*)\r\n(?=\xe3\x80[\x8c\x8e])')
mp=collections.defaultdict(collections.Counter)
for a,b in zip(o.rows,n.rows):
    x=S.findall(o.plain(a)); y=S.findall(n.plain(b))
    if len(x)!=len(y): continue
    for (_,e),(_,s) in zip(x,y): mp[e.decode('utf8','replace')][s.decode('utf8','replace')]+=1
d={e:c.most_common(1)[0][0] for e,c in mp.items()}
ch={e:s for e,s in d.items() if e!=s}
json.dump(ch,open('/tmp/spmap.json','w'),ensure_ascii=False)
print(len(d),len(ch)); print(ch)
