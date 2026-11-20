import json,sys
R=r'C:/Dev/Default Project/srwv/datos/'
for name in ['mtzkn_nm_es.json','mtzkn_pt_es.json','mtzkn_rt_es.json']:
    a=json.load(open(R+name,encoding='utf-8')); b=json.load(open(R+name.replace('.json','_accent.json'),encoding='utf-8'))
    print('===',name)
    n=0
    def walk(x,y,path=''):
        global n
        if isinstance(x,str):
            if x!=y and n<8:
                print(' ',path); print('  ANTES',repr(x[:140])); print('  AHORA',repr(y[:140])); n+=1
        elif isinstance(x,dict):
            for k in x:
                if k in y: walk(x[k],y[k],path+'/'+str(k))
        elif isinstance(x,list):
            for i,(p,q) in enumerate(zip(x,y)): walk(p,q,path+'/'+str(i))
    walk(a,b)
