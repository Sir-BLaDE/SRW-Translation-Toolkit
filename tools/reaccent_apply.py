import sys, json, pathlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import reaccent
R=r'C:/Dev/Default Project/srwv/datos/'
for name in ['mtzkn_nm_es.json','mtzkn_pt_es.json','mtzkn_rt_es.json']:
    p=R+name
    d=json.load(open(p,encoding='utf-8'))
    changed=[0]
    def walk(x):
        if isinstance(x,str):
            y=reaccent.restore_text(x)
            if y!=x: changed[0]+=1
            return y
        if isinstance(x,dict): return {k:walk(v) for k,v in x.items()}
        if isinstance(x,list): return [walk(v) for v in x]
        return x
    nd=walk(d)
    out=p.replace('.json','_accent.json')
    json.dump(nd,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    import re
    s=pathlib.Path(out).read_text(encoding='utf-8')
    print(name,'changed',changed[0],'accents',len(re.findall(r'[áéíóúñÁÉÍÓÚü¿¡]',s)),'->',out)
