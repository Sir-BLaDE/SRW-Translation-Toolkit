# -*- coding: utf-8 -*-
"""v6: completa las 26 cadenas que v5 dejo sin traducir."""
import json, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
T = json.load(open(r'C:/Dev/Default Project/srwv/datos/prologue_trans_v5.json', encoding='utf-8'))

ADD = {
# falsos positivos (ya espanol) -> identidad
"na batalla final les espera al otro lado.": "na batalla final les espera al otro lado.",
"del planeta Balun para acelerar su regreso a la Tierra.": "del planeta Balun para acelerar su regreso a la Tierra.",
"planeta Balun para acelerar su regreso a la Tierra.": "planeta Balun para acelerar su regreso a la Tierra.",
"Una batalla final les espera al otro lado.": "Una batalla final les espera al otro lado.",
# ingles real
"is pressed into service aboard the Tuatha de Danaan in order": "es reclutado a bordo del Tuatha de Danaan para",
"Our heroes have been transported to the Universal Century": "Nuestros héroes han sido transportados al Siglo Universal,",
"dimension, and their only tactical analyst, Nine, finds": "y su única analista táctica, Nine, se",
"Surrounded on all sides by Neo Zeon, G-Hound, Dr. Hell, and": "Rodeados por Neo Zeon, G-Hound, el Dr. Hell y",
"the Angels, our intrepid heroes hunker down in Japan while": "los Ángeles, nuestros héroes se atrincheran en Japón",
"her toward Arzenal. Elsewhere, the Nadesico C makes a brief": "hacia Arzenal. En otro lugar, el Nadesico C hace una",
"Shinji's team of Eva pilots have successfully executed their": "El equipo de pilotos de Eva de Shinji ha ejecutado con éxito su",
"d to the": "do a la",
"Their plan? To turn the tables by taking control of the": "¿Su plan? Dar la vuelta a la situación tomando el control del",
"Colony Laser and using it to put a definitive end to the": "Láser de Colonia y usarlo para poner fin definitivo a la",
"Federation and Neo Zeon, has been entrusted with the power": "y Neo Zeon, ha recibido el encargo del poder",
"as been entrusted with the power": "ha recibido el encargo del poder",
"As they carefully consider the course of the battles ahead,": "Mientras consideran el rumbo de las batallas venideras,",
"Uribatake's factories in his absence. Little does he know": "las fábricas de Uribatake en su ausencia. No sabe que",
"Large Magellanic Cloud on the other side, where they pause": "Gran Nube de Magallanes, donde se",
"Passing through the Balun gate, the fleet reaches the Large": "Al cruzar la puerta de Balun, la flota llega a la Gran",
"fleet reaches the Large": "la flota llega a la Gran",
"As multiple paths stretch out into the sea of stars before": "Múltiples caminos se abren ante ella en el mar de estrellas",
"their eyes, tensions are running high throughout the fleet.": "sus ojos, la tensión crece en toda la flota.",
"With a decisive battle looming, a series of squabbles might": "Con una batalla decisiva en perspectiva, una serie de disputas",
"erupt at any moment as the crew makes final preparations.": "pueden estallar en cualquier momento mientras se ultiman los preparativos.",
"As the fleet pauses to make final preparations ahead of the": "Cuando la flota se detiene para ultimar los preparativos antes de la",
}
for k,v in ADD.items(): T[k]=v
json.dump(T, open(r'C:/Dev/Default Project/srwv/datos/prologue_trans_v6.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('claves v6:',len(T))
