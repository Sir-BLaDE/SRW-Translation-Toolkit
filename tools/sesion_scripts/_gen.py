import pickle,re,collections,sys
txt=pickle.load(open('/tmp/b/dlc_txt.pkl','rb')) if len(sys.argv)<2 else pickle.load(open(sys.argv[1],'rb'))
F=set('Ange Asuka Beecha Belleza Bernadette Elle Ersha Fa Feldt Hilda Izumi Jasmine Keiko Lacus Lottie Louise Lunamaria Mao Marida Marie Melda Meran Meyrin Mileina Misato Mori Okiku Ple Reika Rosalie Roux Ruri Ryoko Salia Sally Sayaka Sumeragi Tessa Vivian Yurika Kati Mari Peries Kaname'.split())|{'Hou Mei','Ple Two'}
Mset=set('Akito Amuro Athrun Banagher Benkei Hayato Joe Judau Koji Kamille Kodai Ryoma Setsuna Sousuke Kincade Kurz Okita Hathaway Harry Banjo Lockon Saji Shinn Kira Kappei Tobia Velt Gates Allelujah Tieria Bright Otto Tetsuya Maito Saburouta Zinnerman Jerid Riddhe Rakan Hokushin Shima Mondo Yazan Waltfeld Lasse Sanada Graham Clouseau'.split())
adj='listo preparado cansado sorprendido agradecido contento seguro harto tranquilo orgulloso decidido confundido emocionado nervioso asustado enfadado enojado preocupado convencido dispuesto encantado avergonzado perdido herido vivo muerto sano salvo curado bienvenido querido bueno malo solo único último primero nuevo loco tonto idiota ocupado furioso extraño mimado engañado atrapado sorprendido aliviado equivocado sincero honesto fuerte débil cansada'.split()
adjf={a[:-1]+'a' for a in adj if a.endswith('o')}
adjs=set(adj)|adjf
pat=re.compile(r'\b('+'|'.join(sorted(adjs,key=len,reverse=True))+r')s?\b',re.I)
for (f,i),t in txt.items():
    for b in re.finditer(r'(pid_\w+),\s*\r?\n\s*\[\[[　 ]*([^\r\n\]]+)\r?\n(.*?)\]\]',t,flags=re.S):
        pid,sp,body=b.groups()
        if sp=='$n': g='F' if 'FHERO' in pid else ('M' if 'MHERO' in pid else None)
        else: g='F' if sp in F else ('M' if sp in Mset else None)
        if not g: continue
        for m in pat.finditer(body):
            w=m.group(1).lower()
            f_=w in adjf or w=='cansada'
            if (g=='F' and not f_) or (g=='M' and f_):
                print(f[:6],i,sp,g,'|',body[max(0,m.start()-30):m.end()+14].replace('\n','|').replace('　','').replace('\r',''))
