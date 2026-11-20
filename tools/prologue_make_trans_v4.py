# -*- coding: utf-8 -*-
"""Traducciones concisas v4 que caben en el espacio disponible."""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
d = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json', encoding='utf-8'))
old = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_trans_v3.json', encoding='utf-8'))

# Tamano maximo por clave (primera aparicion)
sizes={}
for rid,rd in d.items():
    if rid=='7': continue
    for row in rd['rows']:
        for s in row['parts']:
            k=s.strip()
            if len(k)>=4 and k not in sizes: sizes[k]=len(s.encode('utf-8'))

T = {
"ovember 11, 2199 NCC, Pluto Airspace": "1 nov 2199, NCC, espacio aéreo de Plutón",
"November 11, 2199 NCC, Pluto Airspace": "11 nov 2199, NCC, espacio aéreo de Plutón",
"ith another symbol of hope.": "tra símbolo de esperanza.",
"the moon returns to Earth,": "Luna regresa a la Tierra,",
"p of": "de",
"ace.": "cio.",
"The Earth Federation, the first unifying body for all of": "La Federación Terrestre, primer organismo unificador de",
"humanity, marks the beginning of the New Correct Century in": "la humanidad, marca el inicio del Nuevo Siglo Correcto en",
"2000, and the beginning of humankind's expansion into space.": "2000, y el inicio de la expansión humana al espacio.",
"000, and the beginning of humankind's expansion into space.": "000, y el inicio de la expansión humana al espacio.",
"Some say it was also the beginning of a new era of war.": "Algunos dicen que también empezó una nueva era de guerra",
"The battle between the Earthnoids and Spacenoids that began": "La lucha entre terrícolas y espaciales que empezó",
"with the One Year War raged on through Char's Rebellion,": "con la Guerra de Un Año siguió con la Rebelión de Char,",
"giving way to the so-called 10 Year Void.": "dando paso al llamado Vacío de los 10 Años.",
"r's Rebellion,": "Rebelión,",
"iving way to the so-called 10 Year Void.": "ando paso al Vacío de los 10 Años.",
"Now, 100 years later, humans have become a truly": "Ahora, 100 años después, los humanos son una verdadera",
"ellion,": "belión,",
"interstellar species, and it feels as though yet another new": "especie interestelar, y parece que otra nueva era",
"era is approaching.": "se acerca.",
", and it feels as though yet another new": ", y parece que otra nueva era",
"ra is approaching.": "ra se acerca.",
"For years, humankind knew of a race of intelligent": "Durante años, la humanidad conoció una raza de seres",
"other new": "otra",
"ther new": "tra",
"extraterrestrial life forms known as the Gamillans.": "extraterrestres inteligentes llamados gamillanos.",
"The Federation was in shambles, despite having rebuffed the": "La Federación estaba en ruinas, pese a rechazar al",
"Jupiter Empire in the Jupiter War.": "Imperio de Júpiter en la Guerra de Júpiter.",
"pite having rebuffed the": "ese a rechazar al",
"Once the Gamillans invaded, it seemed the Federation would": "Al invadir los gamillanos, la Federación parecía",
"be destroyed for good. The Gamillan Pluto Frontline Base": "condenada a ser destruida. La Base de Plutón gamillana",
"then fired a Planet Bomb at Earth, with devastating": "lanzó una Bomba Planetaria a la Tierra, con efectos",
"Base": "Base",
"consequences. Its back against the wall, the Federation": "devastadores. Acorralada, la Federación",
"gambled on a last stand with the Gamillans near Pluto.": "se jugó todo en una última resistencia cerca de Plutón.",
"ambled on a last stand with the Gamillans near Pluto.": "jugó todo en una última resistencia cerca de Plutón.",
"In the midst of the M Operation, an escape pod containing": "En plena Operación M, una cápsula con",
"one of Earth's last hopes lands on Mars...": "una de las últimas esperanzas de la Tierra aterriza en Marte...",
"pod containing": "psula con",
"ne of Earth's last hopes lands on Mars...": "na de las últimas esperanzas de la Tierra en Marte...",
"Space Battleship Kirishima, the sole surviving battleship of": "El acorazado Kirishima, único superviviente de la",
"the M Operation, makes its way back to Earth with the": "Operación M, regresa a la Tierra con la",
"hip of": "la de",
"capsule collected from the escape pod on Mars.": "cápsula recuperada en Marte.",
"th the": "con la",
"apsule collected from the escape pod on Mars.": "ápsula recuperada en Marte.",
"At the same time, a man from the moon returns to Earth,": "Al mismo tiempo, un hombre de la Luna regresa a la Tierra,",
"with another symbol of hope.": "con otra símbolo de esperanza.",
"ymbol of hope from the moon.": "mbolo de esperanza de la Luna.",
"aits the arrival of another": "espera la llegada de otro",
"Meanwhile, a woman on Earth awaits the arrival of another": "Mientras, una mujer en la Tierra espera la llegada de otro",
"symbol of hope from the moon.": "símbolo de esperanza de la Luna.",
"he ship known as the Yamato.": "la nave conocida como Yamato.",
"the crew of one ship...": "la tripulación de una nave...",
"The Planet Bomb launched from Pluto wiped out the space": "La Bomba Planetaria desde Plutón aniquiló las colonias",
"colonies. When it hit Earth, the oceans evaporated, the air": "espaciales. Al impactar la Tierra, los mares se evaporaron,",
"was polluted, and cities were leveled. The loss of life was": "el aire se contaminó y las ciudades quedaron arrasadas.",
"staggering.": "abrumador.",
", and cities were leveled. The loss of life was": ", las ciudades quedaron arrasadas.",
"Those who survived fled to underground shelters, where": "Los supervivientes huyeron a refugios subterráneos, donde",
"scientists estimated humanity would survive only a year": "los científicos calcularon que la humanidad viviría un año",
"before collapsing completely.": "antes de desaparecer por completo.",
"would survive only a year": "viviría un año",
"efore collapsing completely.": "antes de desaparecer por completo.",
"Those scientists underestimated humanity's resilience.": "Aquellos científicos subestimaron la resistencia humana.",
"hose scientists underestimated humanity's resilience.": "quellos científicos subestimaron la resistencia humana.",
"Humanity's fate now rests with the crew of one ship...": "El destino de la humanidad está en una sola tripulación...",
"The ship known as the Yamato.": "La nave conocida como Yamato.",
}
# Rellenar claves restantes desde v3 (o vacio)
for k in sizes:
    if k not in T: T[k] = old.get(k,'')
json.dump(T, open(r'C:/Dev/Default Project/srwv/datos/prologue_trans_v4.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
# informe de ajuste
print('claves',len(T))
long=[]
for k,es in T.items():
    if k in sizes and es:
        n=len(es.encode('utf-8'))
        if n>sizes[k]: long.append((sizes[k],n,k,es))
print('traducciones demasiado largas:',len(long))
for item in sorted(long)[:30]: print(' %d>%d %r -> %r'%(item[0],item[1],item[2][:40],item[3][:40]))
