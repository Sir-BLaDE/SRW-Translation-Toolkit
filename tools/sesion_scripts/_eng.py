import os,sys,re,json
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/STAGE/'
k=load(D+'STGEST_EN.CPK')
a,b=int(sys.argv[1]),int(sys.argv[2])
EN=re.compile(rb'\[\[[^\r\n]*\r\n\xe3\x80\x8c((?:[^\]]|\](?!\]))*?)\xe3\x80\x8d\]\]',re.S)
COMMON=re.compile(rb'\b(the|and|with|that|have|this|you|are|was|for|not|but|they|what|from|will|can)\b')
out={}
for r in k.rows[a:b]:
    try:p=k.plain(r)
    except Exception: continue
    n=0;t=0
    for m in EN.finditer(p):
        t+=1
        if len(COMMON.findall(m.group(1)))>=1 and not re.search(rb'[\xc3][\xa0-\xbf]|\xc2[\xa1\xbf]',m.group(1)): n+=1
    if t: out[r['id']]=(n,t)
json.dump(out,open(f'/tmp/eng_{a}.json','w'))
