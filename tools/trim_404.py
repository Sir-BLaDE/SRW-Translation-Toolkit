import json, os

BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'

N = '\r\n'
I = '\u3000'

repl = {
31180: "Si yo no la conozco y tú sí," + N + I + "entonces la conocías de antes" + N + I + "de terminar el VangRay, ¿verdad?",
31191: "Capitán... ¿qué importa más en una" + N + I + "armadura móvil, la velocidad" + N + I + "o la potencia?",
31297: "Apuesto a que podrías crear un sistema" + N + I + "para restaurar la Tierra con las" + N + I + "materias primas adecuadas...",
31291: "En el Laboratorio Táctico Especial Lunar" + N + I + "era $kwbERS-100$kwe," + N + I + "Sistema de Regeneración Terrestre 100.",
31237: "El francotirador de nuestra unidad es bueno." + N + I + "Ya te tiene en su punto de mira.",
31136: "El ingeniero jefe Tokugawa, Sanada, Astonage," + N + I + "Uribatake y ese tal Ian..." + N + I + "Todos están impresionados contigo.",
31199: "Potencia, supongo." + N + I + "Compenso mi falta de habilidad" + N + I + "con fuerza bruta.",
31296: "¡Así que no eres solo el sistema operativo," + N + I + "sino un sistema de fabricación" + N + I + "autodidacta de uso general!",
31295: "Sí. El 3.er Laboratorio Táctico Especial" + N + I + "me dio materiales para medir" + N + I + "mis capacidades.",
31186: "Si te preocupan tus recuerdos," + N + I + "volvamos a nuestra Tierra y preguntemos" + N + I + "al que te fabricó.",
31060: "Así que si no es Gamillas," + N + I + "alguien más le ha echado el ojo..." + N + I + "y a nosotros también.",
31108: "Era como si esperara que alguien" + N + I + "le dijera que buscara a Nine.",
31195: "Velocidad, supongo." + N + I + "Me abalanzo de repente desde" + N + I + "la distancia y los elimino.",
31170: "La palabra de un hombre es su vínculo.",
31094: "Bueno, se construyó como prototipo." + N + I + "Nunca recibió pruebas de durabilidad" + N + I + "y ha aguantado un uso intenso.",
31055: "Análisis completo de la androide que" + N + I + "se infiltró en la Sala de Máquinas 2.",
31185: "Lo hecho, hecho está." + N + I + "No se puede cambiar." + N + I + "Solo queda pensar en el futuro.",
31098: "Esperad, vosotros dos." + N + I + "La culpa fue tanto de Nine como mía.",
31066: "Hasta que arreglen el motor de ondas," + N + I + "esperaremos en el Instituto de" + N + I + "Investigación de Energía Fotónica.",
31250: "Si un tipo tan estricto desobedece a propósito," + N + I + "algo pasa. Actuemos rápido.",
31249: "¿Nos dejó ir?",
31140: "Escucha, Nine..." + N + I + "Puedes ser un poco más abierta.",
31106: "¡Muy bien, iré a buscar a Nine" + N + I + "y le echaré una mano!",
}

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
