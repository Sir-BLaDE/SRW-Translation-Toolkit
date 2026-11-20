import json,sys,re
GEN=re.compile(r'(list[oa]|segur[oa]\b|sol[oa]\b|cansad|content|preocupad|sorprendid|encantad|obligad|hechicer|\bmag[oa]\b|equivocad|dispuest|convencid|hart[oa]|nervios|tranquil|preparad|decidid|\bamo\b|\bama\b|señor|chic[oa]\b|mism[oa]|\bun[oa]?\b|desertor|\bél\b|[^\s]+d[oa]\b)',re.I)
def fill(T,a,b):
    recs=[json.loads(l) for l in open('/home/claude/srwx/datos/story_dialogues.jsonl',encoding='utf-8')]
    by={}
    for k,v in T.items():
        d=recs[k]; by.setdefault((d['text'],d['speaker'],d['pid'][:6]),v)
    n=0
    for i in range(a,b+1):
        d=recs[i]
        if i in T or d['speaker'].startswith('-'): continue
        key=(d['text'],d['speaker'],d['pid'][:6])
        if key in by: T[i]=by[key]; n+=1; continue
        if d['speaker'].startswith('$n'):
            for (t,sp,pp),v in by.items():
                if t==d['text'] and sp.startswith('$n') and not GEN.search(v):
                    T[i]=v; n+=1; break
    miss=[i for i in range(a,b+1) if i not in T and not recs[i]['speaker'].startswith('-') and not set(recs[i]['text'])<=set('!?！？')]
    print('dups',n,'faltan',miss)
    return T
