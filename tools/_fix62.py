# -*- coding: utf-8 -*-
"""Acorta traducciones del lote b008 para que la entrada 62 (tabla L, u16)
vuelva a quedar por debajo de 65.535 bytes de texto plano."""
import json

P = 'C:/Dev/Default Project/srwv/datos/es_batches/b008_2500_2899.json'
d = json.load(open(P, encoding='utf-8'))

S = {
"2774": "Cuando invadieron nuestro sistema, Plutón cayó el primero. ¿Desde dónde\r\n　lanzaron la Bomba Planetaria que arrasó la Tierra? Desde Plutón.",
"2786": "Parte del condensador del motor de ondulación se fundió, señor.\r\n　Seguramente por disparar el cañón de ondulación.",
"2782": "No podemos ignorar una señal de socorro ya recibida.\r\n　Comandante, aunque haya pocos supervivientes,\r\n　¡debemos acudir en su ayuda!",
"2775": "¡Plutón es la raíz de todo mal! ¡Debemos arrancarla,\r\n　dejemos o no este sistema!",
"2583": "Estaba muy bien oculto, pero averiguamos que\r\n　las órdenes para que tú y la alférez Kisaragi abordarais\r\n　el Yamato no vinieron de nosotros.",
"2831": "No tenemos tiempo. Es la única forma\r\n　de que todo siga funcionando.",
"2647": "Será una máquina, pero para mí es un copiloto\r\n　que me salva la vida, y seguiré luchando a su lado.",
"2822": "Si quienes partieron a los confines exteriores\r\n　olvidaron la Tierra, me debo averiguar\r\n　qué tiene ese poder.",
"2824": "Pero puede que no vuelvas con vida, ¿verdad?",
"2580": "Solo una advertencia. Lo que llamas una «amenaza».",
"2621": "Solo una advertencia. Lo que llamas una «amenaza».",
"2665": "Solo una advertencia. Lo que llamas una «amenaza».",
"2705": "Solo una advertencia. Lo que llamas una «amenaza».",
"2808": "Lo siento. Sabía que me dirías que no\r\n　si te contaba que quería venir contigo.",
"2589": "He establecido que el Sistema Nine-Nine y yo\r\n　tenemos estructuras de archivos distintas.",
"2630": "He establecido que el Sistema Nine-Nine y yo\r\n　tenemos estructuras de archivos distintas.",
"2674": "He establecido que el Sistema Nine-Nine y yo\r\n　tenemos estructuras de archivos distintas.",
"2714": "He establecido que el Sistema Nine-Nine y yo\r\n　tenemos estructuras de archivos distintas.",
"2652": "¡Eso le ha tocado la fibra!\r\n　Lo usaré contra ella más tarde.",
"2735": "¡Eso le ha tocado la fibra!\r\n　Lo usaré contra ella más tarde.",
"2713": "¡Pero eres parte del subsistema del Yamato,\r\n　el ordenador más potente de la Tierra!\r\n　¿No puedes hackear y entrar?",
"2791": "Lo comprobé al recibir el aviso del oficial Sanada.\r\n　Estamos muy por debajo de lo necesario.",
"2599": "Lo que no sabemos es por qué el sistema\r\n　eligió revelarse justo cuando lo hizo.",
"2640": "Lo que no sabemos es por qué el sistema\r\n　eligió revelarse justo cuando lo hizo.",
"2622": "¿Las IA entienden las amenazas?",
"2706": "¿Las IA entienden las amenazas?",
"2588": "¿No eres un subsistema del Yamato,\r\n　el ordenador más potente de la Tierra?\r\n　¿No puedes averiguarlo?",
"2629": "¿No eres un subsistema del Yamato,\r\n　el ordenador más potente de la Tierra?\r\n　¿No puedes averiguarlo?",
"2590": "Necesitaré bastante tiempo\r\n　para un análisis completo.",
"2631": "Necesitaré bastante tiempo\r\n　para un análisis completo.",
"2675": "Necesitaré bastante tiempo\r\n　para un análisis completo.",
"2715": "Necesitaré bastante tiempo\r\n　para un análisis completo.",
"2605": "¡¿Amenaza?! ¡Intento ponerme de su lado!",
"2689": "¡¿Amenaza?! ¡Intento ponerme de su lado!",
"2606": "Es más que una máquina. Hoy fue mi copiloto\r\n　y me mantuvo con vida. Solo quería mostrarle mi respeto.",
"2690": "Es más que una máquina. Hoy fue mi copiloto\r\n　y me mantuvo con vida. Solo quería mostrarle mi respeto.",
"2711": "Analyzer, ¿puedes investigar eso?",
"2793": "Quizá no. Hay una mina de Cosmonita abandonada\r\n　en Encélado. Podemos conseguir algo allí.",
"2828": "No podemos llevarla de vuelta a Júpiter.\r\n　Tendremos que...",
"2849": "No podemos llevarla de vuelta a Júpiter.\r\n　Tendremos que...",
"2766": "Oficial Ota, ¿cuántos días perderíamos\r\n　aterrizando en Encélado?",
"2801": "Como hija del antiguo líder supremo de Júpiter,\r\n　usted controlaba a la población. ¿Se coló a bordo\r\n　del Yamato para huir de Júpiter?",
"2779": "Entiendo tus sentimientos, Kodai, pero no nos sobra\r\n　el tiempo.",
"2772": "Tú tienes una misión: destruir las bases enemigas de Plutón\r\n　con tanta fuerza como las de Júpiter. ¿Eso ibas a decir?",
"2768": "Como oficial táctico, recomiendo no detenernos.\r\n　No podemos perder más tiempo.",
"2770": "¡Digo que no deberíamos perder tiempo buscando\r\n　supervivientes que quizá no existen!",
"2802": "Dudo que cambie su percepción,\r\n　pero rechazo la palabra «huir».",
"2769": "¡¿Qué dices, Kodai?! ¿Sugieres abandonar\r\n　a otra tripulación de la Federación?",
"2604": "Alférez $l, si las amenazas no funcionan\r\n　con las IA, ¿por qué la amenazas tú?",
"2645": "Alférez $l, si las amenazas no funcionan\r\n　con las IA, ¿por qué la amenazas tú?",
"2688": "Alférez $l, si las amenazas no funcionan\r\n　con las IA, ¿por qué la amenazas tú?",
"2728": "Alférez $l, si las amenazas no funcionan\r\n　con las IA, ¿por qué la amenazas tú?",
"2646": "A mí no me gustaría que jugaran conmigo.\r\n　¡Yo me pondría a hablar!",
"2729": "A mí no me gustaría que jugaran conmigo.\r\n　¡Yo me pondría a hablar!",
"2819": "Qué buscan en los confines exteriores quienes\r\n　siguieron a mi padre... los que atacaron la Tierra.",
"2823": "Al darme cuenta, fue liberador, Tobia.\r\n　Por primera vez siento que puedo guiar a Júpiter\r\n　hacia un futuro mejor.",
"2837": "¡Ahora soy Bernadette Briett!\r\n　Y trabajaré duro para redimirme.",
"2858": "¡Ahora soy Bernadette Briett!\r\n　Y trabajaré duro para redimirme.",
"2838": "A su servicio. Me presento para el deber.",
"2859": "A su servicio. Me presento para el deber.",
"2796": "¡Comandante! ¡El oficial Ito informa\r\n　de que hay un polizón capturado!",
}

applied = 0
for k, v in S.items():
    if k in d:
        d[k] = v
        applied += 1

json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('aplicados', applied)

# comprobar el nuevo tamano de la entrada 62
import story_build as sb
from story import find_dialogs, rebuild_block
from cpk_util import load

trans = sb.load_translations()
tm = sb.load_tm()
by_entry = sb.load_dialogues()
recs = by_entry['_rec']
per_entry = {}
for i, dd in recs.items():
    per_entry.setdefault(dd['entry'], []).append(dd)

GAME = 'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk'
cf = load(GAME)
f = [r for r in cf.rows if r['id'] == 62][0]
pt = cf.plain(f)
dialogs = find_dialogs(62, pt)
by_start = {x.start: x for x in dialogs}
ds = per_entry.get(62, [])
out = bytearray(); last = 0
for dd in ds:
    if dd['start'] not in by_start: continue
    es = trans.get(dd['id'])
    if es is None: es = tm.get(dd['text'])
    if es is None: continue
    dlg = by_start[dd['start']]
    out += pt[last:dlg.start]
    out += rebuild_block(dlg.speaker, es)
    last = dlg.end
out += pt[last:]
print('entrada 62 plano:', len(out), '(limite 65535)')
