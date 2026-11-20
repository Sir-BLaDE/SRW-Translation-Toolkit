import json,os,re
N='\r\n　'
def vis(s): return len(re.sub(r'\$kw[be]','',s))
def wrap(t,width=46):
    words=t.replace(N,' ').split(' ')
    for w in range(width,60):
        lines=[];cur=''
        for x in words:
            if cur and vis(cur+' '+x)>w: lines.append(cur); cur=x
            else: cur=(cur+' '+x) if cur else x
        lines.append(cur)
        if len(lines)<=3 or w>=50: return N.join(lines)
def run():
    for fn in sorted(os.listdir('datos/es_batches')):
        p='datos/es_batches/'+fn; e=json.load(open(p,encoding='utf-8')); ch=0
        for k,v in e.items():
            if any(vis(l.lstrip('　'))>50 for l in v.split('\r\n')):
                e[k]=wrap(v); ch+=1
        if ch: json.dump(e,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=0); print(fn,'rewrap',ch)
if __name__=='__main__': run()
