import json,os,sys
recs=[json.loads(l) for l in open('datos/story_dialogues.jsonl',encoding='utf-8')]
tr={}
for fn in os.listdir('datos/es_batches'):
    tr.update({int(k):v for k,v in json.load(open('datos/es_batches/'+fn,encoding='utf-8')).items()})
tm={}
for k,v in tr.items(): tm.setdefault((recs[k]['text'],recs[k]['speaker'].startswith('$n')),v)
import re
GEN=re.compile(r'(list|segur|sol[oa]\\b|cansad|content|preocupad|sorprendid|encantad|obligad|hechicer|\\bmag[oa]\\b|equivocad|dispuest|convencid|hart[oa]|nervios|tranquil|preparad|decidid|nuev[oa]\\b|amo\\b|ama\\b|señor|chic[oa]\\b|mism[oa]|\\bun[oa]\\b)',re.I)
a,b=int(sys.argv[1]),int(sys.argv[2]); auto={}; seen=set()
for i in range(a,b+1):
    d=recs[i]
    if d['speaker'].startswith('-'): continue
    key=(d['text'],d['speaker'].startswith('$n'))
    if key in tm and (not d['speaker'].startswith('$n') or not GEN.search(tm[key])):
        auto[str(i)]=tm[key]; continue
    kk=(d['text'],d['speaker'],d['pid'][:6])
    if kk in seen: continue
    seen.add(kk)
    if set(d['text'])<=set('!?！？ '): continue
    print(i, d['route'], d['speaker'].strip(), d['pid'][4:] ,'|',d['text'].replace('\r\n　','/').replace('\r\n','//'), ('  [TM: '+tm[key].replace('\r\n　','/')+']' if key in tm else ''))
def route(i): return recs[i]['route']
for k in list(auto):
    r=route(int(k)); v=auto[k]
    if r=='F': v=re.sub(r'\bamo\b','ama',v)
    if r=='M': v=re.sub(r'\bama\b','amo',v)
    auto[k]=v
    if re.search(r'hechicer|\bmag[oa]\b|señorit|chic[oa]\b',v): print('REVISAR',k,r,v.replace('\r\n\u3000','/'))
json.dump(auto,open('/tmp/auto.json','w',encoding='utf-8'),ensure_ascii=False)
print('auto TM',len(auto))
