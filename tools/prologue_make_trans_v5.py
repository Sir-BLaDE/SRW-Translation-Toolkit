# -*- coding: utf-8 -*-
"""v5: anade traducciones de filas 4-6 y 8-30 a partir del mapa v4."""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
T = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_trans_v4.json', encoding='utf-8'))

NEW = {
# ---- filas 4-6 cierre ----
"The fates of three dimensions rest upon their shoulders.": "Los destinos de tres dimensiones pesan sobre sus hombros.",
"We join them as they begin their journey toward Iscandar.": "Nos unimos a ellos al iniciar su viaje a Iscandar.",
"With the Cosmo Reverse System in hand, the crew puts": "Con el Sistema Inversor Cósmico, la tripulación",
"Iscandar behind them, using the remaining warp gate on": "deja atrás Iscandar y usa la última puerta de salto",
"causing all the Earths to repeat their various histories.": "haciendo que todas las Tierras repitan su historia.",
"ausing all the Earths to repeat their various histories.": "aciendo que todas las Tierras repitan su historia.",
# ---- fila 8 ----
"n Mars, readies itself for the first warp in human history.": "n Marte, se prepara para el primer salto de la humanidad.",
"The Yamato, having halted the Jupiter Empire's development": "El Yamato, tras frenar el desarrollo del Imperio de Júpiter",
"on Mars, readies itself for the first warp in human history.": "en Marte, se prepara para el primer salto de la humanidad.",
# ---- fila 9 ----
"he tactical maneuvers to be used in the": "las maniobras tácticas que se usarán en el",
"New Correct Century, Year 2199.": "Nuevo Siglo Correcto, Año 2199.",
"vers to be used in the": "ras que se usarán en el",
"The Yamato launches from Earth, charting a course for Mars.": "El Yamato zarpa de la Tierra rumbo a Marte.",
"Inside, the three pilots of humanoid mobile weapons attend": "A bordo, los tres pilotos de armas móviles humanoides asisten",
"a briefing on the tactical maneuvers to be used in the": "a un briefing sobre las maniobras tácticas que se usarán en el",
"battles ahead.": "las batallas venideras.",
# ---- fila 10 ----
"we-inducing sea of stars that is the Milky Way.": "ante el mar de estrellas que es la Vía Láctea.",
"g into t": "do en",
"g into the": "do en el",
"Having succeeded in destroying the Gamillas' Pluto Frontline": "Tras destruir la Base Frontal de Plutón de los gamillanos,",
"Base, the Yamato leaves the Solar System, plunging into the": "el Yamato deja el Sistema Solar y se adentra",
"awe-inducing sea of stars that is the Milky Way.": "en el sobrecogedor mar de estrellas de la Vía Láctea.",
# ---- fila 11 ----
"scape by single-handedly keeping the enemy forces at bay.": "scape en solitario manteniendo a raya al enemigo.",
"As the Jupiter War drew to a close, a group of space pirates": "Al terminar la Guerra de Júpiter, un grupo de piratas espaciales",
"known as the Crossbone Vanguard vowed to continue fighting": "la Vanguardia Crossbone juró seguir luchando",
"the remnants of the Empire. It is here we find Tobia, pilot": "contra los restos del Imperio. Aquí encontramos a Tobia, piloto",
"of the Crossbone Gundam X-1, buying time for his allies to": "del Crossbone Gundam X-1, ganando tiempo para sus aliados",
"escape by single-handedly keeping the enemy forces at bay.": "manteniendo a raya al enemigo él solo.",
# ---- fila 12 ----
"isits Commander Okita to try and ease his troubled mind.": "isita al comandante Okita para calmar su agitada mente.",
"As the crew prepares to venture into the unknown, Kodai": "Cuando la tripulación se prepara para lo desconocido, Kodai",
"visits Commander Okita to try and ease his troubled mind.": "visita al comandante Okita para calmar su agitada mente.",
# ---- fila 13 ----
"ingering doubts about the others.": "dudas persistentes sobre los demás.",
"eing, he cannot shake": "iendo, no puede quitarse",
"eing, he cannot shake his": "iendo, no puede quitarse sus",
"Tobia, fresh from warping through the dimensional rift,": "Tobia, recién salido del salto por la grieta dimensional,",
"has the good fortune of reuniting with Setsuna and crew in": "tiene la suerte de reunirse con Setsuna y su tripulación",
"short order. Though it is through their guidance that he": "poco después. Aunque gracias a ellos",
"came to be protected by Celestial Being, he cannot shake": "llegó a estar protegido por Celestial Being, no puede quitarse",
"lingering doubts about the others.": "dudas persistentes sobre los demás.",
# ---- fila 14 ----
"rmy Commander Misumaru's demands and enlist.": "mandante Misumaru y alistarse.",
"Federation": "Federación",
"Ruri is stunned by the accident that killed Akito and Yurika": "Ruri queda consternada por el accidente que mató a Akito y Yurika",
"during their honeymoon. With time and the help of those": "en su luna de miel. Con el tiempo y la ayuda de quienes",
"around her, however, life gradually returns to normal.": "la rodean, la vida vuelve poco a poco a la normalidad.",
"round her, however, life gradually returns to normal.": "la rodean, la vida vuelve poco a poco a la normalidad.",
"Eventually, Ruri decides to comply with Earth Federation": "Finalmente, Ruri decide acceder a la petición del Ejército de la",
"Army Commander Misumaru's demands and enlist.": "Federación Terrestre y alistarse.",
# ---- fila 15 ----
"nd briefly return to Arzenal.": "y regresar brevemente a Arzenal.",
"e a request from Jasmine,": "a una petición de Jasmine,",
"Having evaded the DG Alliance's attacks, the Nadesico Squad": "Tras evadir los ataques de la Alianza DG, el Escuadrón Nadesico",
"prepares to launch an all-out assault on the frontline base": "se prepara para lanzar un asalto total contra la base frontal",
"of the Martian Successors.": "de los Sucesores Marciales.",
"ut assault on the frontline base": "tal contra la base frontal",
"Meanwhile, Ange and crew receive a request from Jasmine,": "Mientras, Ange y su tripulación reciben una petición de Jasmine,",
"and briefly return to Arzenal.": "y regresan brevemente a Arzenal.",
# ---- fila 16 ----
"n anticipation of his showdown with Maito.": "a la espera de su enfrentamiento con Maito.",
"ining simula": "miento simul",
"ining simulator": "miento de simulación",
"The Nadesico Squad, having taken in Kodai and the other": "El Escuadrón Nadesico, tras acoger a Kodai y los demás",
"fugitives from the Yamato, make final preparations to": "fugitivos del Yamato, hace los últimos preparativos para",
"capture the Terminal Colony Amaterasu.": "capturar la Colonia Terminal Amaterasu.",
"reparations to": "parativos para",
"Meanwhile, Kappei puts some time in on a training simulator": "Mientras, Kappei entrena en un simulador",
"in anticipation of his showdown with Maito.": "en previsión de su enfrentamiento con Maito.",
# ---- fila 17 ----
"rustrations bubble up to the surface.": "ustraciones afloran.",
"es, the more his": "a, más sus",
"rder": "den",
"Hathaway, the test pilot for the cutting-edge Ξ Gundam,": "Hathaway, piloto de pruebas del novísimo Gundam Ξ,",
"is pressed into service aboard the Tuatha de Danaan in or": "es reclutado a bordo del Tuatha de Danaan para",
"to collect operation data from Minovsky Craft.": "recoger datos de operación del Minovsky Craft.",
"naan in or": "aan para",
"o collect operation data from Minovsky Craft.": "recoger datos del Minovsky Craft.",
"The longer the submarine voyage continues, the more his": "Cuanto más dura el viaje en submarino, más sus",
"frustrations bubble up to the surface.": "frustraciones afloran.",
# ---- fila 18 ----
"erself seized by profound uneasiness.": "esa presa de una profunda inquietud.",
"yst, Nine, find": "ta, Nine, se",
"yst, Nine, finds": "ta, Nine, se encuentra",
"Our heroes have been transported to the Universal Cent": "Nuestros héroes han sido transportados al siglo universal,",
"dimension, and their only tactical analyst, Nine, find": "una dimensión, y su única analista táctica, Nine, se",
"herself seized by profound uneasiness.": "encuentra presa de una profunda inquietud.",
# ---- fila 19 ----
"ut ends up inciting an incident...": "pero acaba provocando un incidente...",
"th solo guard duty,": "con la guardia en solitario,",
"Surrounded on all sides by Neo Zeon, G-Hound, Dr. Hell,": "Rodeados por Neo Zeon, G-Hound, el Dr. Hell y",
"the Angels, our intrepid heroes hunker down in Japan whi": "los Ángeles, nuestros héroes se atrincheran en Japón",
"waiting for the opportunity to launch a counterattack.": "esperando la ocasión de lanzar un contraataque.",
"Elsewhere, Nahel Argama is tasked with solo guard duty,": "En otro lugar, el Nahel Argama recibe la guardia en solitario,",
"but ends up inciting an incident...": "pero acaba provocando un incidente...",
# ---- fila 20 ----
"hese tense times and cause some chaos.": "estos tiempos tensos y causar algo de caos.",
"to capitalize on": "para aprovecharse de",
"Meanwhile, a criminal element conspires to capitalize on": "Mientras, un elemento criminal conspira para aprovecharse de",
"these tense times and cause some chaos.": "estos tiempos tensos y causar algo de caos.",
# ---- fila 21 ----
"top in Japan to grant Ruri and her crew a much-needed re": "ada en Japón para dar a Ruri y su tripulación un merecido des",
"top in Japan to grant Ruri and her crew a much-needed rest.": "ada en Japón para dar a Ruri y su tripulación un merecido descanso.",
"Our heroes have rescued Ange from the clutches of the": "Nuestros héroes han rescatado a Ange de las garras del",
"Holy Misurugi Empire, and the Ptolemaios 2 Custom carries": "Sacro Imperio de Misurugi, y el Ptolemaios 2 Custom la lleva",
"her toward Arzenal. Elsewhere, the Nadesico C makes a bri": "hacia Arzenal. En otro lugar, el Nadesico C hace una bre",
"stop in Japan to grant Ruri and her crew a much-needed re": "ve parada en Japón para dar a Ruri y su tripulación un merecido des",
"stop in Japan to grant Ruri and her crew a much-needed rest.": "ve parada en Japón para dar a Ruri y su tripulación un merecido descanso.",
# ---- fila 22 ----
"ill soon see that now is not the time for such festiviti": "n pronto verán que ahora no es momento de tales fiestas.",
"ill soon see that now is not the time for such festivities.": "n pronto verán que ahora no es momento de tales fiestas.",
"Shinji's team of Eva pilots have successfully executed th": "El equipo de pilotos de Eva de Shinji ha ejecutado con éxito el",
"battle plan, and the Eighth Angel has been vanquished.": "plan de batalla, y el Octavo Ángel ha sido vencido.",
"The group takes the opportunity to celebrate, though they": "El grupo aprovecha para celebrarlo, aunque",
"will soon see that now is not the time for such festiviti": "pronto verán que ahora no es momento de tales fiestas",
"will soon see that now is not the time for such festivities.": "pronto verán que ahora no es momento de tales fiestas.",
# ---- fila 23 ----
"alactic war being waged.": "láctica que se libra.",
"to put a definitive end to": "para poner fin definitivo a",
"to put a definitive end to the": "para poner fin definitivo a la",
"Under orders from the Earth Federation Army HQ,": "Por orden del Cuartel General del Ejército de la Federación,",
"d to": "do a",
"the heavily outnumbered G-Hound launches into space.": "el G-Hound, en clara minoría, se lanza al espacio.",
"Their plan? To turn the tables by taking control of t": "¿Su plan? Dar la vuelta a la situación tomando el control del",
"Colony Laser and using it to put a definitive end to": "Láser de Colonia y usarlo para poner fin definitivo a",
"galactic war being waged.": "la guerra galáctica que se libra.",
# ---- fila 24 ----
"espite from the fray.": "nes de la refriega.",
"a are reunited, and enjoy a brief": "e重新"  # placeholder
}
# corregir placeholder
NEW["a are reunited, and enjoy a brief"] = "se reúnen y disfrutan de un breve"
NEW.update({
"Laplace, a cooperative organization formed by the Earth": "Laplace, organización cooperativa formada por la Federación",
"Federation and Neo Zeon, has been entrusted with the pow": "y Neo Zeon, ha recibido el encargo de poner",
"to put an end to the war.": "fin a la guerra.",
"as been entrusted with the pow": "ha recibido el encargo de",
"As they carefully consider the course of the battles ahe": "Mientras consideran el rumbo de las batallas venideras,",
"Ple, Ple Two, and Marida are reunited, and enjoy a brief": "Ple, Ple Two y Marida se reúnen y disfrutan de un breve",
"respite from the fray.": "respiro en la refriega.",
# ---- fila 25 ----
"recious enterprise.": "preciada empresa.",
"w creeps ever closer to his": "que se acerca sigilosamente a su",
"he k": "l",
"he know": "No",
"The AD dimension crew say final goodbyes to their": "La tripulación de la dimensión AD se despide de sus",
"friends and loved ones as they prepare to depart for": "amigos y seres queridos antes de partir hacia",
"Iscandar and attempt to stop the space-time fusion.": "Iscandar para intentar detener la fusión espacio-temporal.",
"Uribatake calls Saji Crossroad, who is managing": "Uribatake llama a Saji Crossroad, que gestiona",
"Uribatake's factories in his absence. Little does he k": "las fábricas de Uribatake en su ausencia. No sabe que",
"that an ominous shadow creeps ever closer to his": "que una sombra ominosa se acerca a su",
"precious enterprise.": "preciada empresa.",
# ---- fila 26 ----
"heir mission: prevent the space-time fusion from occurri": "u misión: evitar que se produzca la fusión espacio-temporal",
"heir mission: prevent the space-time fusion from occurring.": "u misión: evitar que se produzca la fusión espacio-temporal.",
"The captains of each ship in the fleet listen intently to": "Los capitanes de cada nave de la flota escuchan atentamente",
"Okita's briefing ahead of their departure for Iscandar.": "el briefing de Okita antes de partir hacia Iscandar.",
"Their mission: prevent the space-time fusion from occurri": "Su misión: evitar que se produzca la fusión espacio-temporal",
"Their mission: prevent the space-time fusion from occurring.": "Su misión: evitar que se produzca la fusión espacio-temporal.",
# ---- fila 27 ----
"oji—having made his decision—pays Tetsuya a visit.": "oji, tras tomar su decisión, visita a Tetsuya.",
"Passing through the Balun gate, the fleet reaches the": "Al cruzar la puerta de Balun, la flota llega a la",
"Large Magellanic Cloud on the other side, where they pa": "Gran Nube de Magallanes, donde se",
"to survey the landscape and draw up new battle plans.": "para inspeccionar el terreno y trazar nuevos planes de batalla.",
"Koji—having made his decision—pays Tetsuya a visit.": "Koji, tras tomar su decisión, visita a Tetsuya.",
# ---- fila 28 ----
"er, Nine is overcome with a deeply unsettling feeling.": "er, Nine se apodera una sensación profundamente inquietante.",
"Passing through the Balun gate, the fleet reaches the La": "Al cruzar la puerta de Balun, la flota llega a la Gran",
"Magellanic Cloud on the other side.": "Nube de Magallanes.",
"fleet reaches the La": "flota llega a la Gran",
"As multiple paths stretch out into the sea of stars befo": "Múltiples caminos se abren ante ella en el mar de estrellas",
"her, Nine is overcome with a deeply unsettling feeling.": "y Nine se ve presa de una sensación inquietante.",
# ---- fila 29 ----
"rupt at any moment as the crew makes final preparations": "estallar en cualquier momento mientras la tripulación ultima",
"rupt at any moment as the crew makes final preparations.": "estallar en cualquier momento mientras la tripulación ultima los preparativos.",
"With Iscandar and Gamillas' home planet right before": "Con Iscandar y el planeta natal de los gamillanos ante",
"their eyes, tensions are running high throughout the fle": "sus ojos, la tensión crece en toda la flota.",
"With a decisive battle looming, a series of squabbles mi": "Con una batalla decisiva en perspectiva, una serie de disputas",
"erupt at any moment as the crew makes final preparations": "pueden estallar en cualquier momento mientras se ultiman los preparativos",
# ---- fila 30 ----
"ecisive battle, Nine is once again overcome by uncertainty": "batalla decisiva, Nine vuelve a verse presa de la incertidumbre",
"ecisive battle, Nine is once again overcome by uncertainty.": "batalla decisiva, Nine vuelve a verse presa de la incertidumbre.",
"With Iscandar and the Gamillas' home planet right before": "Con Iscandar y el planeta natal de los gamillanos ante",
"their eyes, tensions are running high throughout the flee": "sus ojos, la tensión crece en toda la flota.",
"As the fleet pauses to make final preparations ahead of t": "Cuando la flota se detiene para ultimar los preparativos antes de la",
"decisive battle, Nine is once again overcome by uncertainty": "batalla decisiva, Nine vuelve a verse presa de la incertidumbre",
"decisive battle, Nine is once again overcome by uncertainty.": "batalla decisiva, Nine vuelve a verse presa de la incertidumbre.",
})
for k,v in NEW.items(): T[k]=v
json.dump(T, open(r'C:/Dev/Default Project/srwv/datos/prologue_trans_v5.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('claves v5:',len(T))
