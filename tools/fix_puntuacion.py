import csv,re,sys
INT=r'(?:Gah|Uh|Vaya|Oh no|Aww|Ja|Jeje|Jaja|Hey|Eh|Uf|Huh|Bueno|Ay|Ah|Bien|Pues|Hum+|Wow|Uwah|Owww|Nuh|Guh|Heh|Hehe|Entonces|Pero|Oh|Hmph|Ceh)'
INTERJ=re.compile(r'^('+INT+r',\s+)',re.I)
def prot(s):
    s=re.sub(r'\b(Dr|Sr|Sra|Cap|Gral|Cmdr|Mr|Mrs)\.',lambda m:m.group(1)+'\x01',s)
    s=re.sub(r'(?<=\d)\.(?=\d)','\x01',s)
    s=re.sub(r'(?<=\b[A-Z])\.(?=[A-Z])','\x01',s)
    s=re.sub(r'(?<=\b[A-Z])\.(?=[\s"]|$)',lambda m:'\x01',s) if False else s
    return s
def fix_sent(body,term,prev=''):
    lead=re.match(r'^((?:\\n|\s|["«|])*)',body).group(1)
    s=body[len(lead):]
    q='?' in term; e='!' in term
    if q and not e and prev.count('¿')>prev.count('?'): return body+term
    if e and not q and prev.count('¡')>prev.count('!'): return body+term
    if not(q or e): return body+term
    m=re.match(r'^([¡¿]+)',s); cur=m.group(1) if m else ''
    rest=s[len(cur):]
    if q and e: need='¡¿'
    elif q: need='¿'
    else: need='¡'
    if cur==need or (set(need)<=set(cur) and len(cur)==len(need)): return body+term
    if q and not e and '¿' in rest and rest.rstrip().endswith('') and cur=='¡':
        return lead+rest+term  # ¡X, pero ¿y...? -> X, pero ¿y...?
    if cur:
        # wrong opener: replace
        return lead+need+rest+term
    if q and '¿' in rest: return body+term
    if e and not q and '¡' in rest: return body+term
    mi=INTERJ.match(rest)
    if mi:
        after=rest[len(mi.group(1)):]
        # vocative like "Ja, Kamille" (single capitalized word) -> opener at start
        if not re.fullmatch(r'[A-ZÁÉÍÓÚÑ][\wáéíóúñ]*',after.strip()):
            return lead+mi.group(1)+need+after+term
    return lead+need+rest+term
def fix(es):
    p=prot(es)
    parts=re.findall(r'[^.!?…]+[.!?…]+|[^.!?…]+$|[.!?…]+',p)
    res=[]
    for x in parts:
        m=re.match(r'^(.*?)([.!?…]+)$',x,re.S)
        if not m or not m.group(1).strip(): res.append(x); continue
        b,t=m.groups()
        res.append(fix_sent(b,t,''.join(res)) if ('?' in t or '!' in t) else x)
    return ''.join(res).replace('\x01','.')
if __name__=='__main__':
    rows=list(csv.DictReader(open('/tmp/w/in.csv',encoding='utf-8-sig')))
    ch=0
    for r in rows:
        n=fix(r['es'])
        if n!=r['es']:
            ch+=1
            if ch<=int(sys.argv[1]) and (ch%int(sys.argv[2])==0): print(repr(r['es']),'->',repr(n))
    print(ch)
