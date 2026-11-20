R={
'High Mega Cannon':'Cañón de Alta Mega',
'Gravity Blast':'Explosión Gravitatoria','Boost Knuckle':'Puño Turbo','Booster Knuckle':'Puño Turbo','Big Bang Punch':'Puño Big Bang',
'Rocket Punch':'Puños fuera','Breast Fire':'Fuego de pecho','Rust Hurricane':'Huracán corrosivo','Rust Typhoon':'Tifón corrosivo',
'Mighty Vulcan':'Vulcan Poderoso','Drill Missile':'Misil Taladro','Cañón Fire':'Cañón de Fuego','Bomber Break':'Bombardero Destructor',
'Bomber Gauntlet':'Guantelete Bombardero','Battle Launcher':'Lanzador de Combate','Kaiser Hurricane':'Huracán Kaiser','Wing Gust':'Ráfaga de Alas',
'Daitarn Hammer':'Martillo Daitarn','Buster Missile':'Misil Buster','Moon Attack':'Ataque Lunar','Cyclone Fire':'Fuego Ciclón','Battle Wing':'Ala de Combate',
'Sukiure Cannon':'Cañón Sukiure','Final Breast Nova':'Nova de Pecho Final','Breast Burn Up':'Llama de Pecho Total','Breast Burn':'Llama de Pecho','Breast Nova':'Nova de Pecho',
'Thunder Break':'Trueno Destructor','Bomber Crash':'Choque Bombardero','Kaiser Vulcan':'Vulcan Kaiser','Drill Crusher':'Triturador Taladro',
'Positron Buster':'Cañón de Positrones','Zambot Buster':'Cañón Zambot','Zambot Cutter':'Cortador Zambot','Zambot Moon Attack':'Ataque Lunar Zambot','Zambot Lunar Special':'Especial Lunar Zambot',
'Daitarn Fan':'Abanico Daitarn','Daitarn Missile':'Misil Daitarn','Daitarn Cannon':'Cañón Daitarn','Leg Cannon':'Cañón de Pierna','Deuterion Beam':'Rayo de Deuterión',
'Getter Battle Wing':'Ala de Combate Getter','Getter Beam':'Rayo Getter','Getter Missile':'Misil Getter','Photonic Power Beam':'Rayo Fotónico','Machine God':'Dios Mecánico',
'Muramasa Blaster':'Cañón Muramasa','Missile Storm':'Tormenta de Misiles','Drill Hurricane':'Huracán Taladro','Gaine Shot':'Disparo Gaine','Vivian Boomerang':'Bumerán de Vivian',
'Boomerang Blade':'Cuchilla Bumerán','Full Burst':'Ráfaga Total','Feather Funnels':'Funnels de Plumas','Beam Saber':'Sable de Haz','Beam Magnum':'Magnum de Haz',
'Beam Confuse':'Haz de Confusión','Destroy Mode':'Modo Destroy','Great Mazin Emperador':'Gran Emperador Mazin','Great Mazin Emperor':'Gran Emperador Mazin',
'Wave Motion Gun':'Cañón de Ondas de Movimiento','Hyper Mega Launcher':'Hiper Lanzador Mega','High Mega Launcher':'Lanzador de Alta Mega','Sun Attack':'Ataque Solar',
'Gordon Cyclone':'Ciclón Gordon','Full Cross':'Full Cross',
}
R.update({'Drive Wheel Sword':'Espada Rueda Motriz','Horn Bomber':'Bombardero de Cuerno','Perfect Cannon':'Cañón Perfecto','Signal Beam':'Rayo Señal','Beam Gatling Guns':'Metralletas de Haz','Beam Gatling Gun':'Metralleta de Haz',
'GN Rifle Bits II':'Bit Rifle GN II','GN Claw':'Garra GN','GN Bazooka':'Bazuca GN','GN Buster Gun':'Cañón Buster GN','GN Big Cannon':'Gran Cañón GN','GN Cannon':'Cañón GN','GN Sword Rifles':'Rifles Espada GN','GN Sword Rifle':'Rifle Espada GN','GN Buster Rifle':'Rifle Buster GN','GN Buster Sword':'Espada Buster GN','GN Sword V':'Espada GN V','GN Sword Bits':'Bit Espada GN','GN Holster Bits':'Bit Funda GN','GN Rifle':'Rifle GN',
'Quantum Burst':'Ráfaga Cuántica','Drill Grenade':'Granada Taladro','Hyper Bazooka':'Hiper Bazuca','Mega Beam Launcher':'Lanzador de Mega Haz','Mega Bazooka Launcher':'Lanzabazucas Mega','Hyper Knuckle Buster':'Hiper Puño Destructor','Knuckle Buster':'Puño Destructor','Bomber Missiles':'Misiles Bombarderos','Battle Burst':'Ráfaga de Combate','Goryu Cannon':'Cañón Goryu','Drill Attack':'Ataque Taladro','Special Diamond Attack':'Ataque Especial Diamante','Plasma Drill Hurricane':'Huracán Taladro de Plasma','Smasher Punch':'Puño Aplastador','Great Blaster':'Gran Cañón','Gordon Fire':'Fuego Gordon','Beam Gun':'Pistola de Haz','Beam Shields':'Escudos de Haz','Beam Cloak':'Capa de Haz','Great Fire':'Gran Fuego','Psycho Field':'Campo Psíquico'})
import re
keys=sorted(R,key=len,reverse=True)
PAT=re.compile(r'(?<![\wáéíóúñÁÉÍÓÚÑ])('+'|'.join(re.escape(k) for k in keys)+r')(?![\wáéíóúñ])')
def apply(s): return PAT.sub(lambda m:R[m.group(1)],s)
