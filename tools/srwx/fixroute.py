import json,os,re
recs=[json.loads(l) for l in open('datos/story_dialogues.jsonl',encoding='utf-8')]
for fn in sorted(os.listdir('datos/es_batches')):
    p='datos/es_batches/'+fn; e=json.load(open(p,encoding='utf-8')); ch=0
    for k,v in e.items():
        r=recs[int(k)]['route']; nv=v
        if recs[int(k)]['pid']!='pid_HOPE': continue
        if r=='F': nv=re.sub(r'\bamo\b','ama',re.sub(r'\bAmo\b','Ama',v))
        if r=='M': nv=re.sub(r'\bama\b','amo',re.sub(r'\bAma\b','Amo',v))
        if nv!=v: e[k]=nv; ch+=1; print('FIX',fn,k,r,nv.replace('\r\n　','/')[:70])
        if r=='N' and re.search(r'\b[Aa]m[oa]\b',v): print('NEUTRO',fn,k,v.replace('\r\n　','/'))
    if ch: json.dump(e,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
