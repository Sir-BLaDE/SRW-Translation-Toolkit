# -*- coding: utf-8 -*-
"""Traducciones de SysText fila 2 (nombres de piloto, unidad, arma, habilidad)."""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
items=json.load(open(r'C:/Dev/Default Project/srwv/datos/systext_row2.json',encoding='utf-8'))
T={}
def add(s,es):
    if s: T[s]=es
# nombres de piloto / fuerza
add('Artificial Newtype','Nuevo Tipo Artificial')
add('Jupiter Empire Soldier','Soldado del Imperio de Júpiter')
add('ECOAS Squad Member','Miembro del Escuadrón ECOAS')
add('Wolfgang Subordinate','Subalterno de Wolfgang')
add('Emperor of Darkness','Emperador de la Oscuridad')
add('Great General of Darkness','Gran General de la Oscuridad')
add('Artificial Intelligence','Inteligencia Artificial (IA)')
# habilidades de terreno
add('Terrain Handling Up: Air','Manejo en terreno aéreo +')
add('Terrain Handling Up: Grd','Manejo en terreno terrestre +')
add('Terrain Handling Up: Wtr','Manejo en terreno acuático +')
add('Terrain Handling Up: Spc','Manejo en el espacio +')
# Evangelion: nombres completos de unidad
evas={
'All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Production Model (Wille Custom) Unit-08':
 'Arma Humanoi de Combate Decisivo Polivalente, Humano Artificial Evangelion, Modelo de Producción (Personalizado por Wille), Unidad-08',
'All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Production Model Unit-02 (First Production Model)':
 'Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Modelo de Producción Unidad-02 (Primer Modelo de Producción)',
'All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-00':
 'Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-00',
'All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-00 (Mod)':
 'Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-00 (Modificado)',
'All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-01':
 'Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-01',
'All-purpose Humanoid Decisive Battle Weapon Artificial Human Evangelion Prototype Unit-01 Pseudo-Evolution Initial Arousal Phase':
 'Arma Humanoide de Combate Decisivo Polivalente, Humano Artificial Evangelion, Prototipo Unidad-01, Fase de Despertar Inicial de Pseudoevolución',
}
for s,es in evas.items(): add(s,es)
# unidades y equipos
add(' High-Mobility Unit Black Selena','Unidad de Alta Movilidad Black Selena')
add('Aestivalis Custom Hikaru Unit','Aestivalis Personalizado de Hikaru')
add('Baron Ashura Mechanical Beast','Bestia Mecánica Baron Ashura')
add('Gundam F91 Mass Production Type','Gundam F91 de Producción en Masa')
add('Interstellar Ballistic Munitions','Municiones Balísticas Interestelares')
add('Mobile Suit Gundam 00 the Movie: A Wakening of the Trailblazer',
    'Mobile Suit Gundam 00: La Película - El Despertar del Sendero')
add('Martian Successor Nadesico: The Motion Picture – Prince of Darkness',
    'Martian Successor Nadesico: La Película - Príncipe de la Oscuridad')
# armas
w={
'Seward Arsenal 165mm Multi-purpose Destructive Howitzer "Demolition Gun" Gun-Howitzer Mode':
 'Obús Destructor Multiusos de 165 mm del Arsenal Seward "Cañón de Demolición", modo obús',
'Devastation Particle Convergence Cannon "Seiran" (Anti-Armor Bayonet "Shinden"-Equipped)':
 'Cañón de Convergencia de Partículas Devastadoras "Seiran" (con bayoneta antiblindaje "Shinden")',
'330mm 3-barrel Positron Beam Turret': 'Torreta de Rayos de Positrones de 3 cañones de 330 mm',
'330mm 3-barrel Positron Cannon Turret': 'Torreta de Cañones de Positrones de 3 cañones de 330 mm',
'33mm 4-barrel Positron Rapid-fire Cannon': 'Cañón Rápido de Positrones de 4 cañones de 33 mm',
'490mm 4-barrel Positron Beam Cannon': 'Cañón de Rayos de Positrones de 4 cañones de 490 mm',
'Black Drive Wheel Sword Vertical Slice': 'Espada de Rueda Motriz Negra, Corte Vertical',
'Boomerang Blade "Bunbunmaru"': 'Hoja Bumerán "Bunbunmaru"',
'Calidus Multi-phase Beam Cannon': 'Cañón de Rayos Multifásico Calidus',
'Decisive Cannon Fire Mode Koga': 'Modo de Disparo Decisivo Koga',
'Devastation Particle Convergence Cannon "Seiran"': 'Cañón de Convergencia de Partículas Devastadoras "Seiran"',
'Great Drive Wheel Sword Bamboo Splitter': 'Gran Espada de Rueda Motriz, Corte de Bambú',
'High Energy Beam Rifle Successive Fire': 'Fusil de Rayos de Alta Energía, Disparo Sucesivo',
'High Energy Long-range Beam Cannon': 'Cañón de Rayos de Largo Alcance y Alta Energía',
'Joint Tactical Information Control System': 'Sistema Conjunto de Control de Información Táctica',
'Kurogane Five Certain Death Attack': 'Ataque Mortal Quíntuple de Kurogane',
'Large Caliber Shoulder Revolver-Cannon': 'Revólver-Cañón de Gran Calibre en el Hombro',
'Layer Forged Photon Sword "Tenrai"': 'Espada Fotónica Forjada en Capas "Tenrai"',
'Main Cannon (Type 3 Fusion Munitions)': 'Cañón Principal (Municiones de Fusión Tipo 3)',
'Positron Convergence Cannon Gorai': 'Cañón de Convergencia de Positrones Gorai',
'Positron Convergence Cannon Shunrai': 'Cañón de Convergencia de Positrones Shunrai',
'Space-time Convergence Cannon': 'Cañón de Convergencia Espaciotemporal',
'Standalone Particle Cannon Seiran': 'Cañón de Partículas Independiente Seiran',
'Super Large Mega Beam Cannon': 'Super Cañón de Rayos Mega de Gran Tamaño',
'Super-electromagnetic Crossbow': 'Ballesta Super-electromagnética',
'Type Zero Super Density Blade "Raziel"': 'Hoja de Superdensidad Tipo Cero "Raziel"',
'Variable Strike Lance "Patlocross"': 'Lanza de Ataque Variable "Patlocross"',
'Wire-guided Psycommu Mega Arm Cannon': 'Cañón de Mega Brazo Psicommu Guiado por Cable',
'Boomerang Blade "Bunbunmaru': 'Hoja Bumerán "Bunbunmaru',
'Devastation Particle Convergence Cannon "Seiran': 'Cañón de Convergencia de Partículas Devastadoras "Seiran',
'Layer Forged Photon Sword "Tenrai': 'Espada Fotónica Forjada en Capas "Tenrai',
'Type Zero Super Density Blade "Raziel': 'Hoja de Superdensidad Tipo Cero "Raziel',
'Variable Strike Lance "Patlocross': 'Lanza de Ataque Variable "Patlocross',
}
for s,es in w.items(): add(s,es)
# soporte R2 (las claves japonesas se dejan; solo se anaden las traducciones utiles)
for i in range(10):
    add('R2=%dに対応'%i, 'Compatible con R2=%d'%i)
json.dump(T,open(r'C:/Dev/Default Project/srwv/datos/systext_trans.json','w',encoding='utf-8'),
          ensure_ascii=False,indent=1)
print('traducciones:',len(T))
# cobertura
n=sum(1 for x in items if T.get(x['s'],'').strip())
print('cadenas cubiertas:',n,'de',len(items))
