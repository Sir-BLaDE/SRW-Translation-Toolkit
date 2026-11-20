"""reaccent.py - restaura acentos en textos que fueron desacentuados.
Aprende de los corpus de espanol correcto ya existentes en el proyecto.
"""
import sys, os, re, json, csv, pathlib, unicodedata, collections
ROOT = r'C:/Dev/Default Project/srwv'
WORD = re.compile(r"[A-Za-zÁÉÍÓÚáéíóúñÑüÜ']+")
ACC = re.compile(r'[áéíóúñÁÉÍÓÚüÜ]')

def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

def corpus_strings():
    out=[]
    # batalla
    with open(ROOT + r'/datos/lineas_batalla_final.csv', encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            if r['es']: out.append(r['es'])
    # historia
    for p in pathlib.Path(ROOT + '/datos/es_batches').glob('*.json'):
        try: d=json.load(open(p,encoding='utf-8'))
        except Exception: continue
        out += [v for v in d.values() if isinstance(v,str)]
    # systext y otros
    for name in ['systext_es_1.json','systext_es_2.json','kpack_rg_es.json',
                 'ln_id0_es.json','ln_id1_es.json','ln_id3_descs_es.json',
                 'ln_id4_es_short.json','ln_id4_compact_es.json']:
        p=ROOT+'/datos/'+name
        if not os.path.exists(p): continue
        try: d=json.load(open(p,encoding='utf-8'))
        except Exception: continue
        def walk(x):
            if isinstance(x,str): out.append(x)
            elif isinstance(x,dict):
                for v in x.values(): walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(d)
    return out

def build_map():
    # contamos TODAS las apariciones (acentuadas y sin acentuar) para no
    # convertir palabras que son validas sin acento, p.ej. "piloto" -> "pilotó"
    counters=collections.defaultdict(collections.Counter)
    for s in corpus_strings():
        for w in WORD.findall(s):
            if "'" in w: continue
            counters[fold(w).lower()][w.lower()]+=1
    amap={}
    for k,c in counters.items():
        total=sum(c.values())
        accs=[(v,n) for v,n in c.items() if ACC.search(v)]
        if not accs: continue
        best,n=max(accs,key=lambda x:x[1])
        if n/total>=0.95 and n>=3:
            amap[k]=best
    return amap

AMAP=build_map()
print('mapa aprendido:',len(AMAP),'palabras')

# palabras ambiguas: nunca tocar automaticamente
QW={'Que':'Qué','Como':'Cómo','Cuando':'Cuándo','Donde':'Dónde','Quien':'Quién',
    'Cual':'Cuál','Cuanto':'Cuánto','Cuanta':'Cuánta','Cuantos':'Cuántos','Cuantas':'Cuántas'}
SKIP={'si','el','tu','mas','aun','solo','este','esta','estos','estas','ese','esa',
      'eso','los','las','un','una','como','cuando','donde','quien','que','porque'}

def restore_word(w, amap=AMAP):
    if ACC.search(w): return w
    low=fold(w).lower()
    if low in SKIP: return w
    rep=amap.get(low)
    if not rep: return w
    if w.isupper(): return rep.upper()
    if w[:1].isupper(): return rep[:1].upper()+rep[1:]
    return rep

def restore_text(s):
    if not isinstance(s,str): return s
    out=WORD.sub(lambda m: restore_word(m.group(0)), s)
    # signos de apertura: se parte conservando TODO el whitespace original
    # (los saltos de linea son significativos en estos textos)
    parts=re.split(r'(?<=[.!?])(\s+)', out)
    for i in range(0,len(parts),2):
        p=parts[i]
        if not p: continue
        st=p.lstrip(); pre=p[:len(p)-len(st)]
        if st.endswith('?') and '¿' not in p:
            st='¿'+st
            st=re.sub(r'^¿(Que|Como|Cuando|Donde|Quien|Cual|Cuanto|Cuanta|Cuantos|Cuantas)\b',
                      lambda m:'¿'+QW[m.group(1)], st)
            parts[i]=pre+st
        elif st.endswith('!') and '¡' not in p:
            st='¡'+st
            st=re.sub(r'^¡(Que|Como|Cuando|Donde|Quien|Cual|Cuanto|Cuanta|Cuantos|Cuantas)\b',
                      lambda m:'¡'+QW[m.group(1)], st)
            parts[i]=pre+st
    return ''.join(parts)

if __name__=='__main__':
    for s in sys.argv[1:]:
        print(repr(s),'->',repr(restore_text(s)))
