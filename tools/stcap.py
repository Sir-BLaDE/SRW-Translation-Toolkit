# -*- coding: utf-8 -*-
import os,sys,re,hashlib
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'))
import cpk_util,fastinf,srwv_cpkbuild2 as B
cpk_util.inflate=fastinf.inflate
from cpk_util import load
S=os.path.expanduser('~/mnt/srwv/')
SRC=os.path.expanduser('~/mnt/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK')
OUT=S+'outputs/STGEST_EN_es_v5.cpk'
M={
"-Secret Underground Base, Bono-Misaki, Kyushu, Japan-":"-Base secreta subterránea, Bono-Misaki, Kyushu, Japón-",
"-Federation Far East Headquarters, Japan-":"-Cuartel de la Federación en Oriente, Japón-",
"-Yamato Hangar-":"-Hangar de la Yamato-",
"-Earth Federation Forces Far East Headquarters-":"-Cuartel general de la Federación en Extremo Oriente-",
"-Yamato Reception Room-":"-Sala de recepción de la Yamato-",
"-Yamato Central War Room-":"-Sala central de estrategia de la Yamato-",
"-Factory-":"-Fábrica-",
"-Jupiter Empire Base-":"-Base del Imperio de Júpiter-",
"-Yamato Aircraft Squad Briefing Room-":"-Sala de espera del escuadrón aéreo de la Yamato-",
"-Gamilas Pluto Frontline Base-":"-Base gamilas de primera línea en Plutón-",
"-Great Gamilas Empire Supreme Leader's Office-":"-Despacho del líder supremo gamilas-",
"-Yamato Observation Room-":"-Sala de observación de la Yamato-",
"-Nubel Tokio City Central Park-":"-Parque central de Nueva Tokio-",
"-Police Station Reception Room-":"-Recepción de la comisaría-",
"-Brave Express Base Might Station Hangar-":"-Hangar de la estación Might, base Brave Express-",
"-Brave Express Base Might Station Control Room-":"-Sala de control de la estación Might, Brave Express-",
"-Aoto Factory Underground Secret Factory-":"-Fábrica secreta bajo la Fábrica Aoto-",
"-Brave Express Corps Base Might Station Control Room-":"-Sala de control de la estación Might, Brave Express-",
"-Brave Express Corps Base Might Station Hangar-":"-Hangar de la estación Might, Cuerpo Brave Express-",
"-Brave Express Corps Base Might Station Hanger-":"-Hangar de la estación Might, Cuerpo Brave Express-",
"-Hangar de la estación Might del Cuerpo Brave Express-":"-Hangar de la estación Might, Cuerpo Brave Express-",
"-Nouvelle Tokyo City Jewelry Store-":"-Joyería de Nueva Tokio-",
"-Ptolemaios 2 Custom Briefing Room-":"-Sala de reuniones de la Ptolemaios 2 modificada-",
"-Tuatha de Danaan Command Center-":"-Centro de mando del Tuatha de Danaan-",
"-Tuatha de Danaan Hangar-":"-Hangar del Tuatha de Danaan-",
"-Arzenal Ange's Room-":"-Habitación de Ange en Arzenal-",
"-Arzenal Locker Room-":"-Vestuario de Arzenal-",
"-Ange's Room-":"-Habitación de Ange-",
"-Nouvelle Tokyo City-":"-Nueva Tokio-",
"-Aoto Factory Underground Hangar-":"-Hangar subterráneo de la Fábrica Aoto-",
"-Nahel Argama Hangar-":"-Hangar de la Nahel Argama-",
"-Nahel Argama Communication Room-":"-Sala de comunicaciones de la Nahel Argama-",
"-NERV Command Center-":"-Centro de mando de NERV-",
"-Ra Cailum Briefing Room-":"-Sala de reuniones de la Ra Cailum-",
"-Earth Federation Forces Base VIP Lounge-":"-Sala VIP de la base de la Federación-",
"-Senpuji Heavy Industries Aoto Factory-":"-Fábrica Aoto de Industrias Pesadas Senpuji-",
"—Martian Successor Provisional Headquarters—":"—Cuartel provisional de los Sucesores Marcianos—",
"—Arzenal Command Center—":"—Centro de mando de Arzenal—",
"-Inside Dragon Barrier Near Temple-":"-Barrera del Dragón, cerca del templo-",
"-Inside Dragon Barrier-":"-Dentro de la Barrera del Dragón-",
"—Yamato Hangar—":"—Hangar de la Yamato—",
"—Yamato Air Corps Briefing Room—":"—Sala de reuniones del Cuerpo Aéreo Yamato—",
"-NERV Hangar-":"-Hangar de NERV-",
"-True Science Fortress Laboratory Command Center-":"-Centro de mando, Fortaleza de la Verdadera Ciencia-",
"-Subspace Submarine UX-01 Interior-":"-Interior del submarino subespacial UX-01-",
"-Yamato Wave Motion Gun Control Room-":"-Control del cañón de onda motriz de la Yamato-",
"-Planet Leptaporda 17th Detention Center-":"-Centro de detención n.º 17 del planeta Leptaporda-",
"-Planet Leptaporda Detention Center Interior-":"-Interior del centro de detención de Leptaporda-",
"-Supreme Leader's Office-":"-Despacho del líder supremo-",
"-Gamilas Executive VIP Room-":"-Sala VIP de los ejecutivos gamilas-",
"-Baleras II Central Control Room-":"-Sala de control central de la Baleras II-",
"-Baleras II Interior-":"-Interior de la Baleras II-",
"-Earth Federation Base-":"-Base de la Federación Terrestre-",
"-Colony Laser Control Room-":"-Sala de control del láser de la colonia-",
# acortar desbordantes
"-Lugar del accidente de la cápsula de escape de la Scheherazade-":"-Accidente de la cápsula de la Scheherazade-",
"-Ruinas de la Cal Polar Marciana, Fortaleza de los Sucesores Marcianos-":"-Ruinas polares de Marte, fortaleza de los Sucesores-",
"-Centro de Mando del Instituto de Investigación de Energía Fotónica-":"-Centro de mando del Instituto de Energía Fotónica-",
"-Cerca del Sistema de Navegación Automática de la Yamato-":"-Cerca del navegador automático de la Yamato-",
"-Cerca del Instituto de Investigación de Energía Fotónica-":"-Cerca del Instituto de Energía Fotónica-",
"-Sala de mando del cuartel de los Sucesores Marcianos-":"-Sala de mando de los Sucesores Marcianos-",
"-Puente de la nave de espacio profundo Celestial Being-":"-Puente de la nave espacial Celestial Being-",
"-Sala de reuniones del Cuerpo Aéreo de la Yamato-":"-Sala de reuniones del Cuerpo Aéreo Yamato-",
}
c=load(SRC);new={};n=0
for r in c.rows:
    p=c.plain(r);q=p
    for k,v in M.items():
        kb=k.encode();vb=v.encode()
        if kb in q:
            n+=q.count(kb);q=q.replace(kb,vb)
    if q!=p: new[r['id']]=(c.cipher(r,q),len(q));
print('reemplazos',n,'filas',len(new),flush=True)
blob=B.build_ordered(SRC,new);open(OUT,'wb').write(blob)
k=load(OUT);ok=True
for r in k.rows:
    p=k.plain(r);ok&=(r['ex']==len(p))
print('verify',ok,len(blob),hashlib.sha256(blob).hexdigest()[:12])
# caption widths
mx=[]
for r in k.rows:
    t=k.plain(r).decode('utf-8','replace')
    for m in re.finditer(r'\[\[(　[^\]]*?)\]\]',t,re.S):
        ls=m.group(1).split('\r\n')
        u=max(sum(2 if ch=='　' else 1 for ch in l) for l in ls)
        mx.append((u,r['id'],m.group(1).replace('　','').replace('\r\n','')))
mx=sorted(set(mx),reverse=True)
for u,i,s in mx[:8]: print(u,i,s)
EN=re.compile(r"\b(the|of|Base|Room|Station|Center|Headquarters|Office|Factory|Interior|Hangar|Squad)\b")
print('inglés restante:',[s for u,i,s in mx if EN.search(s)][:10])
