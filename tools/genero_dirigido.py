import re,collections
# --- género de cada tabla de mensajes (t_NNN) según las ramas MHERO/FHERO del script de eventos
def branch_genders(script):
    """devuelve {n: 'M'|'F'|None} para cada SC_MESS_B(n)"""
    res={}
    stack=[]  # elementos: ['M',state] o ['x']
    for line in script.replace('\r','').split('\n'):
        s=line.strip()
        if s.startswith('--'): continue
        s=re.sub(r'--.*$','',s).strip()
        if re.match(r'if\b.*\bthen\s*$',s):
            if 'MHERO_scenario_flag' in s and '== SC_TRUE' in s: stack.append(['M','M'])
            elif 'MHERO_scenario_flag' in s: stack.append(['M','F'])
            else: stack.append(['x',None])
        elif re.match(r'(elseif\b.*\bthen|else)\s*$',s):
            if stack and stack[-1][0]=='M' and s=='else': stack[-1][1]='F' if stack[-1][1]=='M' else 'M'
        elif re.match(r'(function\b|for\b.*\bdo|while\b.*\bdo)',s): stack.append(['x',None])
        elif re.match(r'end\b',s):
            if stack: stack.pop()
        m=re.search(r'SC_MESS_B\(\s*(\d+)',s)
        if m:
            g=None
            for fr in reversed(stack):
                if fr[0]=='M': g=fr[1]; break
            n=int(m.group(1)); res.setdefault(n,set()).add(g)
    return {n:(next(iter(v)) if len(v)==1 else None) for n,v in res.items()}
def table_gender_map(rows):
    """rows: {id:text}. devuelve {(msgrow,tablename):'M'|'F'}"""
    out={}
    for i,t in rows.items():
        if 'SC_MESS_B' not in t: continue
        bg=branch_genders(t)
        for j in range(i+1,i+6):
            if j in rows and re.search(r'\nt_\d{3} = \{',rows[j]):
                for n,g in bg.items():
                    if g and re.search(r'\nt_%03d = \{'%n,rows[j]): out[(j,'t_%03d'%n)]=g
                break
    return out
ADJ=set('seguro listo contento preocupado cansado ocupado acostumbrado impresionado dispuesto obligado destinado encargado orgulloso nervioso asustado harto convencido agradecido confundido sorprendido emocionado avergonzado decidido tranquilo curioso perdido herido vivo loco tonto novato agotado enfadado enojado satisfecho aliviado equivocado sincero honesto engañado atrapado ansioso desesperado entusiasmado animado inquieto enamorado mareado preparado cuidadoso furioso mimado fuerte lleno bueno malo ocupado débil capaz tímido valiente cobarde amable cruel egoísta joven nuevo único mismo solo hermoso guapo'.split())
ADJ-= {'fuerte','débil','capaz','amable','cruel','egoísta','joven','valiente','cobarde'}
VERB=r'(?:estás|eres|te ves|te veo|te vi|te encuentro|te noto|pareces|te sientes|te sentías|te has vuelto|te quedaste|te quedas|estabas|fuiste|serás|estarás|sigues|andas|vienes|has estado|has sido|seas|estés|te pones|te pusiste|no estás|no eres|ya estás|ya eres|estás tan|resultas|resultaste|estuviste)'
ADV=r'(?:(?:muy|tan|un poco|bastante|totalmente|completamente|demasiado|casi|ya|todavía|aún|nada|realmente|de verdad|siempre|tan solo)\s+)*'
pat=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])('+VERB+r'\s+'+ADV+r')([a-záéíóúñ]+)(?![A-Za-zñáéíóú])',re.I)
NOUN={'novato':'novata','chico':'chica','amigo':'amiga','compañero':'compañera','jovencito':'jovencita','muchacho':'muchacha','niño':'niña','tonto':'tonta','idiota':'idiota','listillo':'listilla','novatillo':'novatilla'}
patV=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])(Novato|novato|Chico|chico|Amigo|amigo|Compañero|compañero|Jovencito|jovencito|Muchacho|muchacho|Tonto|tonto|Listillo|listillo)(?=\s*[,.!?」）…])')
patT=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])(tú\s+)(mism[oa]|sol[oa](?=\s*[.,!?」）…]))',re.I)
def conv(w,g):
    lw=w.lower()
    if g=='F':
        if lw in ADJ and lw.endswith('o'): return w[:-1]+'a'
        if re.fullmatch(r'[a-záéíóúñ]+(ado|ido)',lw): return w[:-1]+'a'
    else:
        if lw.endswith('a') and lw[:-1]+'o' in ADJ: return w[:-1]+'o'
        if re.fullmatch(r'[a-záéíóúñ]+(ada|ida)',lw): return w[:-1]+'o'
    return w
def fixsent(s,g,ch):
    def r1(m):
        n=conv(m.group(2),g)
        if n!=m.group(2): ch.append((m.group(0),m.group(1)+n))
        return m.group(1)+n
    s=pat.sub(r1,s)
    def r2(m):
        w=m.group(1); lw=w.lower()
        tgt=NOUN.get(lw) if g=='F' else None
        if g=='M':
            inv={v:k for k,v in NOUN.items() if v!=k}; tgt=inv.get(lw)
        if not tgt: return w
        tgt=tgt.capitalize() if w[0].isupper() else tgt
        ch.append((w,tgt)); return tgt
    s=patV.sub(r2,s)
    def rb(m):
        t=m.group(1)+('a' if g=='F' else 'o')
        if t!=m.group(0): ch.append((m.group(0),t))
        return t
    s=re.sub(r'(?<![A-Za-zñáéíóú])(Bienvenid)[oa](?![A-Za-zñáéíóú])',rb,s)
    def r3(m):
        w=m.group(2); t=w[:-1]+('a' if g=='F' else 'o')
        if t!=w: ch.append((m.group(0),m.group(1)+t))
        return m.group(1)+t
    s=patT.sub(r3,s)
    return s

BLK=re.compile(r'(\[\[)([^\r\n\]]+)(\r?\n)(.*?)(\]\])',re.S)
def speakers_of(rows):
    s=set()
    for t in rows.values():
        for m in BLK.finditer(t): s.add(m.group(2).strip('　 '))
    return {x for x in s if re.fullmatch(r"[A-Z][A-Za-z]+( [A-Z][A-Za-z]+)?",x)}
def process_row(t,gender_of_table,names,rowid,report):
    """t: texto de la fila de mensajes. gender_of_table(tname)->g. Devuelve texto nuevo."""
    out=[];pos=0
    tabs=[(m.start(),m.group(1)) for m in re.finditer(r'\n(t_\d{3}) = \{',t)]
    if not tabs: return t
    tabs.append((len(t),None))
    res=t[:tabs[0][0]]
    for (a,name),(b,_) in zip(tabs,tabs[1:]):
        seg=t[a:b]; g=gender_of_table(name)
        if not g: res+=seg; continue
        blocks=list(BLK.finditer(seg)); prev=None; new=seg; delta=0
        for idx,m in enumerate(blocks):
            sp=m.group(2).strip('　 ')
            body=m.group(4)
            nxt=blocks[idx+1].group(2).strip('　 ') if idx+1<len(blocks) else None
            if sp!='$n' and sp in names:
                present=[n for n in names if re.search(r'(?<![A-Za-z])'+re.escape(n)+r'(?![A-Za-z])',body)]
                hero_addr=('$n' in body) or (not present and ('$n' in (prev,nxt)))
                if hero_addr:
                    ch=[]; nb=fixsent(body,g,ch)
                    if nb!=body:
                        report.append((rowid,name,g,sp,prev,body.replace('\n','|').replace('　','')[:150],ch))
                        s0=m.start(4)+delta; e0=m.end(4)+delta
                        new=new[:s0]+nb+new[e0:]; delta+=len(nb)-len(body)
            prev=sp
        res+=new
    return res
