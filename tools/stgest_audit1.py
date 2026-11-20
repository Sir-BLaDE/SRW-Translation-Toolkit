import os,sys,re,json,time,hashlib,shutil
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util,fastinf; cpk_util.inflate=fastinf.inflate
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME']; P=H+'/mnt/srwv/'
SRC=H+'/mnt/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'; BK=P+'backup/antes_auditoria_20261119/STGEST_EN.CPK'
if not os.path.exists(BK): shutil.copy2(SRC,BK)
SP={e:v[0] for e,v in json.load(open('/tmp/sg/rpwmap.json')).items() if e not in ('Purple','Nuke')}
SP.update({'Gamilas Soldier':'Soldado de Gamilas','Gamilas Captain':'Capitán de Gamilas','Agent':'Agente',"Hokushin's Six":'Los Seis de Hokushin','Garrison':'Guarnición','Beauty':'Belleza','Black Gaine':'Gaine Negro'})
CAP={'Arzenal Cafeteria':'Cafetería de Arzenal','Arzenal Mess Hall':'Comedor de Arzenal','Arzenal Prison Cell':'Celda de Arzenal','Bardos Island Ruins':'Ruinas de la isla Bardos','Colony Laser Dock':'Muelle del láser de la colonia',"Hoi Kow Lou's Hideout":'Escondite de Hoi Kow Lou','Goergametsch Bridge':'Puente del Goergametsch','Holy Misurugi Empire Palace':'Palacio del Sacro Imperio Misurugi','Holy Misurugi Empire Royal Palace':'Palacio real del Sacro Imperio Misurugi','Jasmine Mall Storehouse':'Almacén del centro comercial Jasmine','Jindai High School Playground':'Patio del instituto Jindai','Jupiter Colony Dock':'Muelle de la colonia Júpiter','Kurogane Spa Garden':'Jardín del balneario Kurogane','Megalanica Vist Manor':'Mansión Vist de Megalanica','NERV Facility':'Instalaciones de NERV','NERV HQ Central Dogma':'Dogma Central de la sede de NERV','Nadesico B Bridge':'Puente de la Nadesico B','Nadesico C Bridge':'Puente de la Nadesico C','Nahel Argama Bridge':'Puente de la Nahel Argama','Nahel Argama　Hangar':'Hangar de la Nahel Argama','Natto Quality Assurance':'Control de calidad del natto','Senpuji Residence Garden Area':'Jardín de la residencia Senpuji',"Supreme Leader's Quarters":'Aposentos del líder supremo',"Tatsu's House":'Casa de Tatsu',"Tuatha de Danaan Captain's Quarters":'Camarote del capitán del Tuatha de Danaan','VangRay Cockpit':'Cabina del VangRay','Yamato Bridge':'Puente de la Yamato',"Yamato Commanding Officer's Cabin":'Camarote del capitán de la Yamato','Yamato Cosmo Reverse System':'Sistema Cosmo Reverse de la Yamato','Yamato Engineering Department':'Departamento de ingeniería de la Yamato','Yamato Laboratory':'Laboratorio de la Yamato','Yamato Observation Deck':'Sala de observación de la Yamato','Yamato Passageway':'Pasillo de la Yamato','Yamato Workboat':'Lancha de trabajo de la Yamato'}
rsp=re.compile(rb'(\[\[(?:\xe3\x80\x80)*)('+b'|'.join(re.escape(k.encode()) for k in sorted(SP,key=len,reverse=True))+rb')(\r\n\xe3\x80[\x8c\x8e])')
rcp=re.compile(rb'(\[\[[^\]]*?)-('+b'|'.join(re.escape(k.encode()) for k in sorted(CAP,key=len,reverse=True))+rb')-(\]\])')
c=load(BK); new={}; ns=nc=0
for r in c.rows:
    try:p=c.plain(r)
    except Exception: continue
    q,a=rsp.subn(lambda m:m.group(1)+SP[m.group(2).decode()].encode()+m.group(3),p)
    q,b=rcp.subn(lambda m:m.group(1)+b'-'+CAP[m.group(2).decode()].encode()+b'-'+m.group(3),q)
    if a or b: new[r['id']]=(c.cipher(r,q),len(q)); ns+=a; nc+=b
print('filas',len(new),'hablantes',ns,'rotulos',nc,flush=True)
out=P+'outputs/STGEST_EN_es_v7.cpk'; blob=B.build_ordered(BK,new); open(out,'wb').write(blob)
k=load(out); bad=[r['id'] for r in k.rows if r['ex']!=len(k.plain(r))]
print('ex_mismatch',bad,len(blob),hashlib.sha256(blob).hexdigest()[:12])
