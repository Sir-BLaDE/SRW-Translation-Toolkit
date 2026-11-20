# -*- coding: utf-8 -*-
"""Genera id3 compacto: traducciones que caben en el slot original."""
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from kpack_ln import parse3

D = r"C:/Dev/Default Project/srwv/datos"
SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
OUT = D + "/ln_id3_compact_es.json"

# (indice de la primera aparicion, traduccion compacta)
PAIRS = [
 (73, r"Resta 1.500 de daño de rayos a distancia recibidos.\nEnfoque >110. Cuesta 10 EN por activación."),
 (76, r"Anula atributos con daño <2.000.\nEnfoque >130. Cuesta 10 EN cada vez."),
 (78, r"Anula atributos con daño <2.500.\nCuesta 10 EN cada vez."),
 (79, r"Se anulan los atributos que no sean de rayo con daño inferior a 2.000.\nCuesta 15 EN cada vez."),
 (80, r"Resta 1.500 de daño a todos los atributos.\nEnfoque >110. Cuesta 15 EN cada vez."),
 (85, r"Resta 2.000 de daño de rayos a distancia recibidos.\nEnfoque >100. Cuesta 5 EN cada vez."),
 (86, r"Resta 500 de daño a todos los atributos. Enfoque >100.\nEfecto +1 por cada 10 de Enfoque. Cuesta 10 EN cada vez."),
 (87, r"Resta 2.000 de daño a todos los atributos. Enfoque >100.\nEfecto +1 por cada 10 de Enfoque. Cuesta 10 EN cada vez."),
 (88, r"Anula atributos con daño <3.000; el efecto sube con la Sincronía.\nEnfoque >100. Cuesta 20 EN cada vez.\nNo sirve contra armas cuerpo a cuerpo de Ángeles."),
 (90, r"Anula atributos con daño <3.500 y Perforación de Barrera.\nEnfoque >100. Cuesta 10 EN cada vez.\nNo sirve contra el arma cuerpo a cuerpo del EVA."),
 (92, r"El atributo de rayo a distancia y el de gravedad con daño inferior a 3.000 se \nanulan. Resta 1.000 de daño a los atributos que no sean esos. \nCuesta 10 EN cada vez."),
 (95, r"Resta 1.000 de daño de rayos a distancia recibidos.\nCuesta 5 EN por activación."),
 (96, r"Si eliges Defender, resta un 60% de daño.\nEfecto parecido con otras opciones\npor la diferencia de HAB."),
 (97, r"Recupera todo el EN y la munición del aliado adyacente con Reabastecer.\n(Tras moverse, no.)"),
 (98, r"Recupera tu HP y el del aliado adyacente con Reparar.\n(Se puede usar tras moverse.)"),
 (99, r"Inicio de fase: recupera el 10% de HP."),
 (100, r"Inicio de fase: recupera el 20% de HP."),
 (101, r"Inicio de fase: recupera el 30% de HP."),
 (102, r"Inicio de fase: recupera el 10% de EN."),
 (103, r"Inicio de fase: recupera el 20% de EN."),
 (104, r"Inicio de fase: recupera el 30% de EN."),
 (105, r"Te permite cambiar de forma usando el comando Transformar."),
 (106, r"Te permite cambiar de forma usando el comando Dividir.\nNo puedes volver a tu forma original una vez dividido en el mismo mapa."),
 (107, r"Tú y aliado adyacente: +10% Precisión Final y Evasión."),
 (108, r"Anula efectos de armas enemigas\nDrenaje de Estado, Inactividad, Drenaje de Enfoque y de PE."),
 (109, r"Anula efectos de armas enemigas: Drenaje de Estado, Inactividad, Drenaje de Enfoque,\nPE, EN, Movilidad, Vista, Blindaje y Erosión bajos."),
 (110, r"Enfoque >130 y Newtype >5. Mejora la unidad."),
 (112, r"Enfoque >130 y Newtype >5.\nTransformación en modo Destroy.\n5 turnos de efecto."),
 (113, r"Enfoque >130 y Newtype >5.\nTransformación en modo Destroy.\nSin límite de turnos."),
 (114, r"Activa TRANS-AM: 2 turnos en estado TRANS-AM.\nSolo una vez por mapa."),
 (115, r"Enfoque >130. Sube Vista, Movilidad,\nBlindaje y daño según el Enfoque."),
 (117, r"Enfoque >100. Suben Vista, Movilidad, Blindaje\ny daño según el Enfoque."),
 (120, r"Aplica Analizar y Agitar a todos los enemigos."),
 (121, r"Inicio de fase: EN completo a unidades con Antena de Onda Gravitatoria."),
 (122, r"Inicio de fase: EN completo a unidades con Rayo de Onda Gravitatoria."),
 (123, r"Enfoque >150: permite transformarte en Mazinger Zero."),
 (124, r"Enfoque >170 y Sincronía >90%: \npseudo-evolución de EVA Unidad-01 disponible."),
 (125, r"Precisión de aliados +nº de aliados en mapa/5.\nSe acumula con otras unidades con esta habilidad."),
 (126, r"Inicio de fase: HP completo."),
 (127, r"Derrotada, no se controla\ny ataca a enemigos y aliados."),
 (128, r"Al aparecer: efectos de Destello, Acelerar y Cargar."),
 (129, r"Enfoque >130: 40% de evadir todo ataque."),
 (130, r"Enfoque >130: 50% de evadir todo ataque."),
 (131, r"Enfoque >130: 30% de evadir todo ataque."),
 (133, r"Defensa única ante ataques.\nEfecto según barrera/blindaje."),
 (134, r"Inicio de fase: recupera HP.\nCantidad según habilidad."),
 (135, r"Inicio de fase: recupera EN.\nCantidad según habilidad."),
 (136, r"Evita por completo ataques enemigos.\nProbabilidad según habilidad."),
 (137, r"Enfoque >130 y Newtype >5.\nTransformación en modo Destroy."),
 (138, r"Enfoque >130: Perforación de Barrera con todas las armas,\ncrítico +30% y daño +10%."),
 (139, r"Inicio de fase: recupera 50 EN."),
]

cf = load(SRC)
pt = cf.plain([x for x in cf.rows if x["id"] == 3][0])
strs, _ = parse3(pt)
sizes = []
p = 0
for s in strs:
    total = struct.unpack_from("<I", pt, p)[0]
    sizes.append(total)
    p += total

out = {}
bad = []
for idx, es in PAIRS:
    en = strs[idx].decode("utf-8", "replace")
    need = 4 + ((len(es.encode("utf-8")) + 1 + 3) & ~3)
    if need > sizes[idx]:
        bad.append((idx, sizes[idx], need, es))
    out[en] = es

if bad:
    for idx, sz, need, es in bad:
        print("NO CABE idx=%d slot=%d need=%d dif=%d: %r" % (idx, sz, need, need - sz, es))
    sys.exit(1)

json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito", OUT, "entradas", len(out), "todas caben")
