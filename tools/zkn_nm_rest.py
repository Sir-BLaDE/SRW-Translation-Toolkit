# -*- coding: utf-8 -*-
import os,re,json
from zkn_dsc2_scan import *
o=load(B+'MtZkn_Nm_original.cpk'); c=load(G+'MtZkn_Nm.cpk'); ci={r['id']:r for r in c.rows}
def norm(s): return re.sub(r'\s+','',s)
out={}
for r in o.rows:
    q=X(o.plain(r)); f=fields(q)
    if b'DSC2' not in f: continue
    s,l=f[b'DSC2']; d2=q[s:s+l].decode('utf8').rstrip()
    if len(d2)<200 and d2.startswith('<srw'): continue
    sd,ld=f[b'DSCR']; d1=q[sd:sd+ld].decode('utf8').rstrip()
    qc=X(c.plain(ci[r['id']])); es1=qc[sd:sd+ld].decode('utf8').rstrip()
    tag=''
    body=d2
    if body.startswith('<srw-tag=before-clear-text-here>\n'): tag='<srw-tag=before-clear-text-here>\n'; body=body[len(tag):]
    overlap = norm(body).startswith(norm(d1)[:60])
    rest=body
    if overlap:
        # buscar corte: consumir caracteres de body hasta cubrir norm(d1)
        n1=norm(d1); k=0;i=0
        while k<len(n1) and i<len(body):
            if not body[i].isspace(): k+=1
            i+=1
        rest=body[i:].lstrip('\n ')
    out[r['id']]=dict(l=l,tag=tag,overlap=overlap,es1=es1,rest=rest,es1b=len(es1.encode()))
json.dump(out,open(os.path.expanduser('~/mnt/srwv/datos/lib/nm2_plan.json'),'w'),ensure_ascii=False,indent=1)
for i,v in out.items():
    print('###',i,'l=%d'%v['l'],'overlap' if v['overlap'] else 'solo-continuacion','es1=%dB'%v['es1b'],'presupuesto=%d'%(v['l']-len(v['tag'])-(v['es1b']+1 if v['overlap'] else 0)),'rest_en=%d'%len(v['rest']))
