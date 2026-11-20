# -*- coding: utf-8 -*-
"""Traduce CommonData/hiyama/defaultSS_E.cpk (textos de lugar del mapa, USB, etc.).
Estructura: cabecera 48 bytes; pool de cadenas (48..hdr[7]); tabla de 150 offsets u32 (relativos a 48) en hdr[8];
hdr[10] = fin de la tabla; el resto (registros) se copia sin cambios. Cadenas 0..74 = claves, 75..149 = textos EN."""
import os,sys,struct,hashlib
sys.path.insert(0,os.path.expanduser('~/tools_vm'))
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
ROOT=os.path.expanduser('~/mnt/srwv/')
G=os.path.expanduser('~/mnt/Super Robot Wars V/')
SRC=ROOT+'backup/defaultSS_E_original.cpk'
if not os.path.exists(SRC):
    import shutil; shutil.copy(G+'CommonData/hiyama/defaultSS_E.cpk',SRC)
OUT=ROOT+'outputs/defaultSS_E_es.cpk'
ES={
 ':OK':':Aceptar',':Back':':Volver','Title':'Título',
 'Mars, Solar System':'Marte, Sistema Solar',
 'Earth to Mars, Solar System':'De la Tierra a Marte, Sistema Solar',
 "Jupiter's Satellite Orbit, Solar System":'Orbita de satélites de Júpiter, Sistema Solar',
 'Gamillas Frontline Base, Pluto, Solar System':'Base avanzada gamila, Plutón, Sistema Solar',
 'Jupiter Sphere, Solar System':'Esfera de Júpiter, Sistema Solar',
 "Saturn's Satellite Orbit, Solar System":'Orbita de satélites de Saturno, Sistema Solar',
 'Near Pluto, Solar System':'Cerca de Plutón, Sistema Solar',
 'Outer Solar System':'Sistema Solar exterior','Milky Way Galaxy':'Vía Láctea',
 'Near Gliese 581, Milky Way Galaxy':'Cerca de Gliese 581, Vía Láctea',
 'Subspace Gate, Intergalactic space':'Puerta del subespacio, espacio intergaláctico',
 'Large Magellanic Cloud':'Gran Nube de Magallanes',
 'Great Gamillas Empire, Salezar System, Large Magellanic Cloud':'Gran Imperio Gamilas, sistema Salezar, Gran Nube de Magallanes',
 'Feldina, Uranometria Nebula, Large Magellanic Cloud':'Feldina, Nebulosa Uranometria, Gran Nube de Magallanes',
 'Planet Leptaporda, Large Magellanic Cloud':'Planeta Leptaporda, Gran Nube de Magallanes',
 'Near Great Gamillas Empire, Large Magellanic Cloud':'Cerca del Gran Imperio Gamilas, Gran Nube de Magallanes',
 'Old Tokyo, Japan':'Antigua Tokio, Japón','Nubel Tokio City, Japan':'Ciudad de Nubel Tokio, Japón','Japan':'Japón',
 'Tokyo Bay, Japan':'Bahía de Tokio, Japón','Arzenal, Area D, Pacific Ocean':'Arsenal, Zona D, océano Pacífico',
 'Pacific Ocean':'Océano Pacífico','Martian Successor Headquarters':'Cuartel general de los Sucesores de Marte',
 'Aprilius City, PLANT':'Ciudad Aprilius, PLANT','Near Earth':'Cerca de la Tierra',
 'Amaterasu, Terminal Colony':'Amaterasu, colonia terminal','Holy Misurugi Empire':'Sacro Imperio Misurugi',
 'Colony Laser':'Láser colonial','Near Japan':'Cerca de Japón','Melida Island':'Isla Melida',
 'Tokyo-3, Japan':'Tokio-3, Japón','Tokyo, Japan':'Tokio, Japón',
 'Photonic Power Research Institute, Japan':'Instituto de Energía Fotónica, Japón',
 'Augusta, North America':'Augusta, Norteamérica','Indian Ocean':'Océano Indico','Mediterranean Sea':'Mar Mediterráneo',
 'Morón Base, Spain':'Base de Morón, España',"Dragon's Barrier":'Barrera del Dragón','GeoFront, Japan':'GeoFrente, Japón',
 'Science Fortress Laboratory, Japan':'Laboratorio Fortaleza de la Ciencia, Japón',
 'True Science Fortress Laboratory, Japan':'Verdadero Laboratorio Fortaleza de la Ciencia, Japón',
 'New Correct Century Dimension':'Dimensión del Nuevo Siglo Correcto','AD Dimension':'Dimensión AD',
 'Universal Century Dimension':'Dimensión del Siglo Universal','Pluto, Solar System':'Plutón, Sistema Solar',
 'Last Name':'Apellido','First Name':'Nombre','Nickname':'Apodo','Squad Name':'Escuadrón',
 'A tough guy who lives in the fast lane.':'Un tipo duro que vive al límite.',
 'A positive rookie who never loses hope.':'Un novato optimista que nunca pierde la esperanza.',
 "A member of the Earth Federation Forces' Lunar Special Tactical Lab Defense Force.":'Miembro de la Fuerza de Defensa del Laboratorio Táctico Especial Lunar de las Fuerzas de la Federación Terrestre.',
 'Formerly a mobile weaponry pilot with the Lunar Aviation Wing.':'Antes piloto de armamento móvil del Ala Aérea Lunar.',
 "A member of the Earth Federation Forces' 3rd Special Tactical Lab Defense Force.":'Miembro de la 3.ª Fuerza de Defensa del Laboratorio Táctico Especial de las Fuerzas de la Federación Terrestre.',
 'Has almost no combat experience and has been entrusted with odd jobs as a result.':'Casi sin experiencia en combate, por lo que le encargan trabajos menores.',
 'This space is blank or contains a unit that cannot be used.':'Este hueco está vacío o contiene una unidad inutilizable.',
 'Please do not remove your USB storage device.':'No retires el dispositivo USB.',
 'Not enough free space on target device.':'No hay espacio libre suficiente en el dispositivo.',
 'USB storage device removed.':'Dispositivo USB retirado.',
 'Updateable MP3 file not found.':'No se encontró un archivo MP3 actualizable.',
}
c=load(SRC);r=c.rows[0];p=c.plain(r)
h=list(struct.unpack_from('<12I',p,0));POOL=h[6];TAB=h[8];N=h[9];REC=h[10]
assert POOL==48 and N==150 and REC==TAB+N*4
offs=struct.unpack_from('<%dI'%N,p,TAB);S=[]
for o in offs:
    a=POOL+o;S.append(p[a:p.index(b'\0',a)].decode('utf8'))
new=[]
for i,s in enumerate(S):
    new.append(ES.get(s,s) if i>=75 else s)
miss=[s for s in S[75:] if s not in ES and s not in (':','/')]
print('sin traducir:',miss)
pool=bytearray();no=[]
for s in new:
    no.append(len(pool));pool+=s.encode('utf8')+b'\0'
end=POOL+len(pool)
tab=((end+15)//16)*16+48
gap=tab-end
h2=h[:];h2[7]=end;h2[8]=tab;h2[10]=tab+N*4
out=bytearray(struct.pack('<12I',*h2))+pool+b'\0'*gap+struct.pack('<%dI'%N,*no)+p[REC:]
assert len(out)==tab+N*4+len(p)-REC
# comprobacion de relectura
q=bytes(out);o2=struct.unpack_from('<%dI'%N,q,tab)
chk=[q[POOL+o:q.index(b'\0',POOL+o)].decode('utf8') for o in o2]
assert chk==new
nf={0:(c.cipher(r,q),len(q))}
open(OUT,'wb').write(build_ordered(SRC,nf))
k=load(OUT);print('ok',len(k.plain(k.rows[0]))==len(q),k.plain(k.rows[0])==q,hashlib.sha256(open(OUT,'rb').read()).hexdigest()[:12])
