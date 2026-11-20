import json, os

BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'

# id -> nueva traduccion mas concisa (con CRLF real y U+3000)
N = '\r\n'
I = '\u3000'

repl = {
28953: "No importa lo noble que sea la misión, decido según" + N + I + "lo que he visto y entendido. Nadie decidirá por mí.",
28860: "Estas mutaciones inquietaban a la gente." + N + I + "Quienes no fueron creados por Dios no podían evitarlo." + N + I + "La naturaleza es la naturaleza.",
28941: "No podemos dejar que Libertus termine." + N + I + "Se lo debemos a nuestros camaradas caídos.",
28851: "Un pueblo pacífico que aborrecía la guerra, y" + N + I + "una avanzada tecnología de información operada" + N + I + "por el pensamiento... Mana.",
28913: "Por ejemplo, la capacidad de modificar" + N + I + "los genes para contrarrestar el Mana de Dios.",
28924: "Todo es voluntad de Dios, por así decirlo." + N + I + "Logos es su perro faldero.",
28949: "Suponiendo que lo dicho sobre Dios y Libertus" + N + I + "sea cierto, mi camino está claro.",
29009: "Así que huí." + N + I + "Viví en una isla desierta, creyendo" + N + I + "que al final moriría.",
28796: "Si es un Dragón, ¿qué son los demás" + N + I + "Dragones que hemos combatido?",
28806: "Si es un Dragón, ¿qué son los demás" + N + I + "Dragones que hemos combatido?",
28816: "Si es un Dragón, ¿qué son los demás" + N + I + "Dragones que hemos combatido?",
28823: "Si es un Dragón, ¿qué son los demás" + N + I + "Dragones que hemos combatido?",
28857: "Los nuevos humanos maduraron, y Dios debería" + N + I + "haberse conformado con un mundo pacífico." + N + I + "Pero entonces algo salió mal.",
28923: "Entonces, que Logos y Blue Cosmos maten" + N + I + "sin piedad a Coordinators es porque...",
28935: "Si eso es cierto," + N + I + "¡no me quedaré de brazos cruzados!",
28845: "La naturaleza humana en su esplendor.",
28894: "La Alektra exiliada cayó en desesperación." + N + I + "Pero su sangre real y el anillo" + N + I + "desbloquearon el Villkiss.",
28934: "¡Qué cretino!" + N + I + "¿Empieza una guerra que mata a incontables" + N + I + "solo por entretenerse?",
28775: "Hay que hacerlo." + N + I + "El silencio y la desconfianza arruinarían" + N + I + "nuestros preparativos.",
28893: "Comandante, ¿sois de la realeza Fundadora?",
28904: "¿Tusk es... de los Pueblos Antiguos?",
28780: "¿Y yo? Debería ser la jinete." + N + I + "He esperado mucho para servirte." + N + I + "¡He trabajado tan duro!",
28752: "Tu agitación es comprensible. La situación" + N + I + "es grave. Los Dragones vinieron a Misurugi" + N + I + "porque el Pilar del Amanecer está aquí.",
28793: "Sin ellos, el Villkiss no da su máximo." + N + I + "Mi brazo derecho y yo lo sabemos bien.",
28834: "No me presiones." + N + I + "Vine a contároslo," + N + I + "pero me pongo nerviosa si me empujan.",
28888: "Fueron a Arzenal. Allí se encontraron dos" + N + I + "grupos de humanos descartados:" + N + I + "los Pueblos Antiguos y las Normas.",
29039: "Bienvenidos, Pueblos Falsos," + N + I + "a la Verdadera Tierra.",
28789: "Nada me hará cambiar de opinión.",
28858: "Aun recreando el sistema," + N + I + "algunas bebés no podían usar Mana." + N + I + "Una mutación que expresaba un gen antiguo.",
28876: "Así que guerrearon contra Dios incontables" + N + I + "veces por un lugar propio, tras ser" + N + I + "negada su existencia.",
28887: "Entonces, desde los confines del mundo," + N + I + "llegó la noticia de Normas montando" + N + I + "Para-Mail contra Dragones.",
28889: "Se unieron y esperaron este día..." + N + I + "el día en que apareciera quien desbloqueara" + N + I + "el Villkiss. Y ella apareció.",
28906: "Es mis oídos, ojos, brazos y piernas," + N + I + "asumiendo todas mis misiones.",
28908: "Y entonces nos conocimos.",
28960: "¡Hmph! ¿Todo bien ahora que nos necesitas?",
}

# localizar cada id en su lote y actualizar
files = {}
for fn in sorted(os.listdir(BATCHES)):
    if not fn.endswith('.json'):
        continue
    p = os.path.join(BATCHES, fn)
    with open(p, encoding='utf-8') as fh:
        d = json.load(fh)
    changed = False
    for k in list(d):
        if int(k) in repl:
            d[k] = repl[int(k)]
            changed = True
    if changed:
        with open(p, 'w', encoding='utf-8') as fh:
            json.dump(d, fh, ensure_ascii=False, indent=0)
        files[fn] = changed

print('archivos actualizados:', list(files))
print('ids reemplazados:', len(repl))
