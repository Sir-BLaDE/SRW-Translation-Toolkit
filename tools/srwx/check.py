import json,re,os,sys
en=[json.loads(l) for l in open('datos/story_dialogues.jsonl',encoding='utf-8')]
tok=re.compile(r'\$kwb|\$kwe|\$[nlrfFc]|%[ds]')
for fn in sorted(os.listdir('datos/es_batches')):
    es=json.load(open('datos/es_batches/'+fn,encoding='utf-8'))
    for k,v in es.items():
        a=sorted(tok.findall(en[int(k)]['text'])); b=sorted(tok.findall(v))
        if a.count('$kwb')!=b.count('$kwb') or [x for x in a if x not in('$kwb','$kwe')]!=[x for x in b if x not in('$kwb','$kwe')]: print('TOK',fn,k,a,b)
        if b.count('$kwb')!=b.count('$kwe'): print('KW',fn,k)
        nl_en=en[int(k)]['text'].count('\r\n'); nl_es=v.count('\r\n')
        if nl_es>3: print('LINEAS',fn,k,nl_es+1)
        for ln in v.split('\r\n'):
            if len(re.sub(r'\$kw[be]','',ln.lstrip('　')))>50: print('LARGA',fn,k,len(ln),ln[:50])
    print(fn,len(es))
