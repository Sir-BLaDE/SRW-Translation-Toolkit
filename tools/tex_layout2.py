import os,sys
sys.path.insert(0,'/tmp/b')
import tex_layout as T
import numpy as np
from tex_layout import A,box_of,render,find,TR,P
# (nombre,atlas,modo,ventana/semilla,texto)
W3=[('Song','Canción',(655,8,790,58)),('MAP','MAPA',(870,232,1016,284)),('ALL','TODO',(878,298,1016,346)),('Assi','Asist.',(878,360,1016,412)),
 ('Score1','PUNTOS',(20,458,238,506)),('Score2','PUNTOS',(403,358,590,408)),('Boosted','Mejorado',(356,455,572,512)),('UP','SUBE',(260,455,347,508)),
 ('HitAway','¡ATACA Y HUYE!',(365,520,718,572)),('NewV','¡NUEVO! V.',(497,583,736,634)),('Unit','Unidad',(18,648,136,694)),('COMMAND','COMANDO',(303,646,622,700)),
 ('SIZE','TAMAÑO',(843,648,982,696)),('Key','Tecla',(493,714,596,762)),('Help','Ayuda',(493,774,617,822)),('OPTIONS','OPCIONES',(203,903,407,952)),
 ('Lv','Nv',(395,968,475,1018)),('Ace','As',(627,966,748,1016))]
for n,t,w in W3: T.LABELS.append((n,3,'win',w,t))
T.LABELS+= [('Free0',0,'win',(136,4,240,92),'Reparar'),('START0',0,'win',(283,183,487,237),'INICIO'),
 ('Tag1',1,'win',(5,868,105,912),'Dúo-'),('Tension1',1,'win',(5,934,205,978),'Moral.'),('Command1',1,'win',(5,980,252,1022),'Órdenes.'),
 ('Char2',2,'win',(560,958,1022,992),'PERSONAJES-REFERENCIA'),('Rob2',2,'win',(560,992,1022,1024),'ROBOTS-ESPECIFICACIONES')]
T.LABELS+=[('HitMiss',0,'bg',(404,262,398,256,688,320),'ACIERTO FALLO'),('FreeY',0,'bg',(916,390,912,384,1023,480),'Reparar'),
 ('CmdC',0,'bg',(253,205,0,196,258,241),'Órdenes.'),('TenC',0,'bg',(205,250,0,242,210,289),'Moral.'),('TagC',0,'bg',(108,296,0,290,114,349),'Dúo-')]
T.LABELS+=[('ExC2',2,'win',(905,859,980,889),'ExC.'),('ExCnt2',2,'win',(848,891,980,920),'Ex-Cuenta'),('Grade2',2,'win',(830,922,970,958),'RANGO')]
PLATES=[('SupDef',0,(12,590,100,620),'Apoyo def.'),('SupAtk',0,(14,648,99,677),'Apoyo atq.'),('Second',0,(16,702,120,728),'2.º ataque'),('PilotX',0,(50,56,112,78),'Piloto',(33,0,0,255)),('Max0',0,(884,336,1018,382),'¡MÁX!',(255,0,255,255))]
def plate_patch(k,box,txt,fix=None):
    x0,y0,x1,y1=box;a=A[k];w,h=x1-x0,y1-y0
    ring=np.concatenate([a[y0-2,x0:x1],a[y1+1,x0:x1],a[y0:y1,x0-2],a[y0:y1,x1+1]]);ring=ring[ring[:,3]>0]
    vals,cnt=np.unique(ring.reshape(-1,4),axis=0,return_counts=True);col=vals[cnt.argmax()]
    if fix: col=np.array(fix,np.uint8)
    return render(w,h,txt,col,'bg')
def main():
    B,log=T.main(False)
    for n,k,box,txt,*fx in PLATES:
        x0,y0,x1,y1=box;patch=A[k][y0:y1,x0:x1].copy();new=plate_patch(k,box,txt,fx[0] if fx else None);m=find(patch);print(n,m)
        assert any(r[:2]==(k,0) and r[2:]==(x0,y0) for r in m)
        for (kk,ti,x,y) in m: B[kk][y:y+y1-y0,x:x+x1-x0]=TR[ti](new)
    return B
if __name__=='__main__':
    B=main()
    from PIL import Image
    for k in (0,1,2,3):
        im=Image.frombuffer('RGBA',(1024,1024),B[k].tobytes(),'raw','BGRA',0,1);bg=Image.new('RGBA',im.size,(70,70,90,255));bg.alpha_composite(im);bg.convert('RGB').save(P+f'tmp_vis/lo_{k}.png')
    os.makedirs('/tmp/tx',exist_ok=True);np.save('/tmp/tx/B.npy',np.stack([B[i] for i in range(8)]))
