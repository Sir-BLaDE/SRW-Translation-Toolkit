# -*- coding: utf-8 -*-
import os,sys,hashlib,shutil,re,textwrap
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
H=os.environ['HOME']; P=H+'/mnt/srwv/'; G=H+'/mnt/Super Robot Wars V/'
src=G+'Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'; bk=P+'backup/KPACK_P4_LN_instalado_antes_audit2.cpk'
if not os.path.exists(bk): shutil.copy2(src,bk)
D={}
def A(s):
    for l in s.strip().split('\n'):
        k,_,v=l.partition(' => '); D[k]=v.split(' | ')
A("""Galvanizing Hope => Esperanza que enciende | Esperanza viva
A Chilling Reunion => Un reencuentro glacial | Reencuentro glacial
Cosmic Crossroads => Encrucijada cósmica
Calm Seas => Mares en calma
Blood-Splattered Wings => Alas manchadas de sangre | Alas ensangrentadas | Alas de sangre
Island Encounter => Encuentro en la isla | Encuentro isleño
Bonds Renewed => Lazos renovados
Tearing into Space => Rasgando el espacio
An Opened Door => Una puerta abierta | Puerta abierta
Thought Patterns => Patrones de pensamiento | Patrones mentales
Take Flight, Brave Heroes! => ¡Alzad el vuelo, valientes héroes! | ¡Alzad el vuelo, héroes! | ¡Volad, héroes!
Dr. Hell's Final Wager => La apuesta final del Dr. Infierno | Apuesta final del Dr. Infierno | Apuesta del Dr. Infierno
A New Hope Grows => Crece una nueva esperanza | Crece la esperanza | Nueva esperanza
Contact => Contacto
Purple Malice => Malicia púrpura
Space Wolf => Lobo espacial
-Ange's Search => -La búsqueda de Ange | -Búsqueda de Ange | -Ange busca
Calling Londo Bell => La llamada de Londo Bell | Llama Londo Bell | Londo Bell
-Earth Federation => -Federación Terrestre | -Federación
Thrice Divided => Tres bandos | Triple división
-Japan => -Japón
-Space => -Espacio
A Final Choice => Una última elección | Última elección | Elección final
Trial by Fire => Prueba de fuego
A Life's Vow => El voto de una vida | Voto de una vida | Voto vital
A Fight Between Men => Una pelea entre hombres | Pelea entre hombres | Pelea de hombres
Blooming Anew => Florecer de nuevo | Florecer otra vez
A Subtle Difference => Una sutil diferencia | Sutil diferencia
A Disquieting Clash => Un choque inquietante | Choque inquietante
A Grudge Among Men => Rencor entre hombres
G-Hound's Critical Battle => La batalla crítica de G-Hound | Batalla crítica de G-Hound | Batalla de G-Hound
Bellicose Star Sea => Mar de estrellas belicoso | Mar estelar bélico | Mar bélico
A Desperate Battlefield => Un campo de batalla desesperado | Campo desesperado
Another Desperate Battlefield => Otro campo de batalla desesperado | Otro campo desesperado | Otro campo letal
Complete Pack Purchase Gift V => Regalo V por pack completo | Regalo V pack completo | Regalo V pack
DL Version Purchase Gift Ｖ => Regalo V versión digital | Regalo V ver. digital | Regalo V digital
Happy Gift V => Regalo V Alegría | Regalo V Feliz | Regalo V
Lucky Gift V => Regalo V Suerte | Regalo V Fortuna
Wonderful Gift V => Regalo V Maravilla | Regalo V Magia
Dream Gift V => Regalo V Sueño | Regalo V Ilusión
Lovely Gift V => Regalo V Encanto | Regalo V Cariño
Special Starter-Kit Pack => Pack inicial especial | Kit inicial especial | Kit inicial
Impending Departure => Partida inminente | Despedida cercana
Bonus Scenario Full Pack => Pack completo de episodios extra | Pack de episodios extra | Pack episodios extra
Stage Clear => Escenario superado | Escen. superado
Scenario Guidance => Guía de escenarios | Guía de episodios | Guía
The Trick to Activating Destroy Mode => Cómo activar el Modo Destroy | Activar Modo Destroy
Full Frontal's Prediction => La predicción de Full Frontal | Predicción de Frontal
Storm-Braver Maito Senpuji => Maito Senpuji, valiente de la tormenta | Maito Senpuji, Storm Braver | Maito Senpuji
Powering Up Battle Bomber => Mejora del Battle Bomber | Potenciar Battle Bomber
"Tetsuya, Combat Professional" => "Tetsuya, profesional del combate" | "Tetsuya, profesional"
"Farewell, Ange's Knight" => "Adiós, caballero de Ange" | "Adiós, caballero"
I-Field => Campo I | Campo-I
Psycho Field => Campo Psíquico | Campo Psico
Positron Reflector => Reflec. Positrón | Reflector Pos.
VPS Armor => Blind. VPS | Arm. VPS
GN Sword Bits => Bits Espada GN
GN Holster Bits => Bits Funda GN
GN Field => Campo GN
Reflector Bits => Bits Reflector
Wave Motion Barrier => Barrera Onda Mov. | Barr. Onda Mov.
Distortion Field => Campo Distorsión | Campo Distors.
Beam Coat => Capa Beam | Capa Haz
HP Regen (S) => Regen. HP (P)
HP Regen (M) => Regen. HP (M)
HP Regen (L) => Regen. HP (G)
EN Regen (S) => Regen. EN (P)
EN Regen (M) => Regen. EN (M)
EN Regen (L) => Regen. EN (G)
All-Disabler => Anulador Total | Anulador
Bio-Sensor => Biosensor
Psychoframe => Psicomarco
NT-D System => Sist. NT-D | NT-D
System Seizure => Toma Sistema | Toma Sist.
Gravity Wave Beam => Rayo Onda Grav. | Rayo O.Grav.
Gravity Wave Antenna => Antena Onda Grav. | Ant. Onda Grav.
Baptism => Bautizo
Shadow => Sombra
Quantization => Cuantización | Cuantizar
Shin Getter Vision => Visión Shin Getter | Visión Getter
Ariel Mode => Modo Ariel
Barrier/Armor Type => Tipo Barr./Blind. | Barr./Blind.
HP Recovery => Recup. HP
EN Recovery => Recup. EN
Special Evasion Type => Tipo Evasión Esp. | Evasión Esp.
Fairy's Eyes => Ojos de Hada | Ojos Hada
Umbilical Cable => Cable Umbilical | Cable Umbil.
Shield Eqp. => Eqp. Escudo | Escudo
Supply Device => Disp. Reabast. | Reabast.
Repair Device => Disp. Reparar | Reparar
Transform => Transformar | Transf.
Single detach => Desacoplar | Desacop.
Jamming => Interf. | Interf
""")
SUM={}
SUM['Desperate to defeat']="Desesperado por derrotar a Mightgaine, Wolfgang entrega el Hiryu a Joe el As, que reta a Maito a combatir. El Tri Bomber lucha en su lugar y el Hiryu lo destroza. Con la tecnología meganoide, Wolfgang reaparece, pero lo derrotan Daitarn 3 y Gran Mazinger. Aun ganando, pierden el Tri Bomber por los daños sufridos."
SUM['Wolfgang, Vuitton']="Wolfgang, Vuitton, Mifune, Hoi y Joe forman la Alianza DG bajo las órdenes del Sr. X y atacan a la tripulación. Harto de las tretas de Hoi, Joe pacta una tregua con Maito y, junto a Graham, Colasour y Battle Bomber, combate a la Alianza DG. Maito se reafirma en enfrentarse a Joe y Purple expulsa a Hoi del grupo."
SUM['Upset by something']="Molesto por algo que dijo Audrey, Banagher queda atrapado en el NT-D en un combate contra Neo Zeon y el Unicorn se desboca. Con la ayuda de Setsuna y los consejos de Judau, se recupera, controla el NT-D y domina el Modo Destroy. Con Ra Cailum y Ple, la tripulación derrota al comandante de Neo Zeon, Full Frontal."
SUM['Amalgam and Neo']="Amalgam y Neo Zeon atacan a la tripulación en la isla Melida. En plena lucha con Full Frontal, Banagher queda atrapado en el NT-D y el Unicorn se desboca. Con la ayuda de Setsuna y Judau, se recupera, controla el NT-D y domina el Modo Destroy. Pero Riddhe se lleva a Audrey en mitad del combate."
SUM['The crew prepares']="La tripulación se prepara para el ataque del Octavo Ángel. Embryo trae de vuelta a Joe y la Alianza DG desde la dimensión AD, pero Maito los derrota fusionando el Mightgaine y el Might Kaiser en el Gran Mightgaine. Con ayuda de Joe, Maito derriba al Octavo Ángel y los tres Evas destruyen su núcleo."
SUM['The group clashes']="El grupo choca con Neo Zeon por la Caja de Laplace, que puede apagar las llamas de la guerra o avivarlas. En combate, Banagher y Amuro hacen ver a Full Frontal que la maldición de Char lo tiene atrapado. Mineva descubre la verdad sobre la Caja y comprende lo inútil de que el pasado dicte el futuro. Ella y Frontal deciden poner fin a la guerra."
DM={'Activated when Focus is above 130 and New Type level is above 5.\\nAllows you to transform into Destroy Mode.\\nEffective during 5 turns once transformed':["Enfoque >130 y Nuevo Tipo >5.\\nPermite transformarse en Modo Destroy.\\nDura 5 turnos tras transformarse."],
'Activated when Focus is above 130 and New Type level is above 5.\\nAllows you to transform into Destroy Mode.\\nNo turn limit':["Enfoque >130 y Nuevo Tipo >5.\\nPermite transformarse en Modo Destroy.\\nSin límite de turnos en Modo Destroy."],
'Activated when Focus is above 130 and New Type level is above 5.\\nAllows you to transform into Destroy Mode.':["Enfoque >130 y Nuevo Tipo >5.\\nPermite transformarse en Modo Destroy."]}
def wrap(t,w=50): return '\n'.join(textwrap.wrap(t,w,break_long_words=False))
c=load(bk); new={}; miss=[]; done=0
for r in c.rows:
    pt=bytearray(c.plain(r)); n0=len(pt); ch=0
    for m in list(re.finditer(rb'[^\x00]+\x00*',bytes(pt))):
        s=m.group(0); t=s.rstrip(b'\0')
        try:u=t.decode('utf8')
        except Exception: continue
        reg=len(s); cands=None
        if u in D: cands=D[u]
        else:
            for k,v in SUM.items():
                if u.startswith(k): cands=[wrap(v,50),wrap(v,52),wrap(v,56)]
            for k,v in DM.items():
                if u.startswith(k) and (cands is None): cands=v
        if cands is None: continue
        if r['id']==3 and reg<3: continue
        ok=None
        for cnd in cands:
            nb=cnd.encode('utf8')
            if len(nb)+1<=reg: ok=nb;break
        if ok is None: miss.append((r['id'],u[:30],reg,len(cands[0].encode('utf8'))+1));continue
        pt[m.start():m.end()]=ok+b'\x00'*(reg-len(ok)); ch+=1
    assert len(pt)==n0
    if ch: new[r['id']]=(c.cipher(r,bytes(pt)),len(pt)); done+=ch; print('fila',r['id'],ch)
print('hechas',done)
for x in miss: print('NOCABE',x)
out=P+'outputs/KPACK_P4_LN_EN_audit2.cpk'; blob=build_ordered(bk,new); open(out,'wb').write(blob)
k=load(out)
for r in k.rows: assert r['ex']==len(k.plain(r))
print(len(blob),hashlib.sha256(blob).hexdigest()[:12])
