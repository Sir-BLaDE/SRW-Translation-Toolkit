import re
FS=set('Tessa Ange Ruri Kaname Melda Sally Hilda Lacus Salia Sumeragi Ryoko Mori Yurika Jill Bernadette Lottie Asuka Mari Ersha Rosalie Marida Jasmine Mao Vivian Misato Elle Beecha Izumi Roux Sayaka Lunamaria Feldt Keiko Momoka Rei Audrey Yurisha Starsha Martha Celestella Mineva Ple Kati Peries Meyrin Reika Mileina Marie Cagalli Hoshina Salamandinay Chitose Misaki Nevanlinna Niimi Marina Sophia Inez Sylvia Riza Angelise Emma Pamela Maggie'.split())|{'Ple Two','Ple Twelve'}
ADJ=set('seguro listo contento preocupado cansado ocupado acostumbrado impresionado dispuesto obligado destinado encargado orgulloso nervioso asustado harto convencido agradecido confundido sorprendido emocionado avergonzado decidido tranquilo curioso perdido herido vivo loco tonto denso novato agotado enfadado enojado satisfecho aliviado equivocado sincero honesto engañado atrapado ansioso desesperado entusiasmado animado inquieto enamorado mareado preparado cuidadoso furioso mimado triste capaz'.split())-{'triste','capaz'}
NOUN={'novato':'novata','chico':'chica','hombre':'mujer','humano':'humana','amigo':'amiga','hijo':'hija','hermano':'hermana','único':'única','primero':'primera'}
V=r'(?:estoy|soy|estuve|fui|me siento|me sentía|me quedé|me veo|me encuentro|sigo|estaré|seré|me puse|vengo|quedo|me quedo|he estado|he sido)'
ADV=r'(?:(?:muy|tan|un poco|bastante|totalmente|completamente|demasiado|casi|ya|todavía|aún|nada|realmente|de verdad|siempre|solo|tan solo)\s+)*'
pat=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])('+V+r'\s+'+ADV+r')([a-záéíóúñ]+)(?![A-Za-zñáéíóú])',re.I)
patN=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])(soy|era|fui|seré|sigo siendo|como)\s+un\s+([a-záéíóúñ]+)',re.I)
def conv(w,g):
    lw=w.lower()
    if g=='F':
        if lw in ADJ: return w[:-1]+'a'
        if re.fullmatch(r'[a-záéíóúñ]+(ado|ido)',lw): return w[:-1]+'a'
    else:
        if lw.endswith('a') and lw[:-1]+'o' in ADJ: return w[:-1]+'o'
        if re.fullmatch(r'[a-záéíóúñ]+(ada|ida)',lw): return w[:-1]+'o'
    return w
patR=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])((?:yo|mí|me)\s+)(mism[oa]|sol[oa](?=\s*[.,!?」）…])|mism[oa])(?![A-Za-zñáéíóú])',re.I)
patE=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])(Encantad|Agradecid|Orgullos|Honrad)([oa])(?![A-Za-zñáéíóú])')
patU=re.compile(r'(?<![A-Za-zñáéíóúÁÉÍÓÚ])(fui|soy|era|seré)\s+(la|el)\s+(única|único)\s+(superviviente)',re.I)
def fixbody(body,g):
    out=[]
    def r1(m):
        n=conv(m.group(2),g)
        if n!=m.group(2): out.append((m.group(0),m.group(1)+n))
        return m.group(1)+n
    b=pat.sub(r1,body)
    def r3(m):
        w=m.group(2); t=w[:-1]+('a' if g=='F' else 'o')
        if t!=w: out.append((m.group(0),m.group(1)+t)); 
        return m.group(1)+t
    b=patR.sub(r3,b)
    def r4(m):
        t=m.group(1)+('a' if g=='F' else 'o')
        if m.group(2)!=t[-1]: out.append((m.group(0),t))
        return t
    b=patE.sub(r4,b)
    def r5(m):
        a,u=('la','única') if g=='F' else ('el','único')
        n=m.group(1)+' '+a+' '+u+' '+m.group(4)
        if n!=m.group(0): out.append((m.group(0),n))
        return n
    b=patU.sub(r5,b)
    if g=='F':
        def r2(m):
            n=NOUN.get(m.group(2).lower())
            if n and m.group(2).lower() in ('novato','chico','hombre'):
                out.append((m.group(0),m.group(1)+' una '+n)); return m.group(1)+' una '+n
            return m.group(0)
        b=patN.sub(r2,b)
    return b,out
def process(t):
    changes=[]
    def blk(m):
        head,sp,body,tail=m.group(1),m.group(2).strip('　 '),m.group(3),m.group(4)
        pid=re.search(r'(pid_\w+)\s*,\s*\r?\n\s*\[\[$',head)
        g=None
        if sp=='$n':
            if pid:
                g='F' if 'pid_FHERO' in pid.group(1) else ('M' if 'pid_MHERO' in pid.group(1) else None)
        elif sp in FS: g='F'
        if not g: return m.group(0)
        nb,ch=fixbody(body,g)
        changes.extend((sp,g)+c for c in ch)
        return head+m.group(2)+'\r\n'+nb+tail if '\r\n' in m.group(0)[len(head)+len(m.group(2)):len(head)+len(m.group(2))+2] else head+m.group(2)+'\n'+nb+tail
    t2=re.sub(r'((?:pid_\w+)\s*,\s*\r?\n\s*\[\[)([^\r\n\]]+)\r?\n(.*?)(\]\])',blk,t,flags=re.S)
    return t2,changes
