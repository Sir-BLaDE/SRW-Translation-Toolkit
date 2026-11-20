# -*- coding: utf-8 -*-
"""Traducciones de B_LT00, lote 6 (residuos finales)."""
import json
import os

D = r"C:/Dev/Default Project/srwv/datos"

T = {
"Mode Change:sort Data": "Cambio de modo: ordenar datos",
"Information:On/Off": "Información: activar/desactivar",
"  Yes": "  Sí",
"Exit this scene?": "¿Salir de esta escena?",
"Critical Boost": "Impulso Crítico",
"when sortied.": "al desplegarse.",
"Damage": "Daño",
"Triple Action": "Acción Triple",
"is considered L size.)": "se considera tamaño L).",
"Adds 1 extra movement to unit.": "Añade 1 de movimiento extra a la unidad.",
"Double Action ": "Acción Doble ",
"Triple Action ": "Acción Triple ",
"Acquired at Robot Customization Lv. 10": "Se consigue al personalizar robots a nivel 10",
"Add a power part slot by 1.": "Añade 1 hueco para partes de poder.",
"Earn a Custom Bonus": "Consigue una Bonificación de Personalización",
"to 120 or greater.": "hasta 120 o más.",
"Emblem acquisition.": "Consecución de emblemas.",
"Use Tac Pts to enhance units.": "Usa Pts Tác para mejorar unidades.",
"Yes/No": "Sí/No",
"Batch execute all orders.": "Ejecutar todas las órdenes de una vez.",
"Return to Sub Order menu to execute orders.": "Vuelve al menú de subórdenes para ejecutarlas.",
"This bonus may be acquired.": "Se puede conseguir esta bonificación.",
"On": "Activado",
"Updateable MP3 file not found.": "No se ha encontrado el archivo MP3 actualizable.",
"Cheer on pilots provided with": "Animar a los pilotos que tengan",
"Critical % by 20%.": "el crítico un 20 %.",
"Air and Spc.": "Aire y Espacio.",
"Accel is used.": "se usa Acelerar.",
"ExC by 1 when sortied.": "la ExC en 1 al desplegarse.",
"Critical % by 5%.": "el crítico un 5 %.",
"while TRANS-AM is active.": "mientras TRANS-AM esté activo.",
"Increases Max EN to 80.": "Aumenta la EN máxima a 80.",
# falsos positivos del clasificador: se dejan tal cual para marcarlos como revisados
"Aumenta la EXP obtenida en combate un 100 %. El comando espiritual Ganancia se puede acumular.": "Aumenta la EXP obtenida en combate un 100 %. El comando espiritual Ganancia se puede acumular.",
"Ataque Total": "Ataque Total",
"Mejora HIT": "Mejora HIT",
"Contraataque Total": "Contraataque Total",
"Aumenta HIT, EVN y SKL conforme sube el Enfoque.": "Aumenta HIT, EVN y SKL conforme sube el Enfoque.",
"DEF, EVN y HIT.": "DEF, EVN y HIT.",
"Contraataque Total ": "Contraataque Total ",
"Aumenta en 5 el HIT del piloto.": "Aumenta en 5 el HIT del piloto.",
"(El 50% del DMG original causado).": "(El 50 % del DMG original causado).",
"HIT, EVN y SKL ganan 20.": "HIT, EVN y SKL ganan 20.",
"RNG, SKL, DEF, EVN y HIT aumentan en 5.": "RNG, SKL, DEF, EVN y HIT aumentan en 5.",
"y el efecto del campo AT. La magnitud del efecto depende": "y el efecto del Campo AT. La magnitud del efecto depende",
"Entrena a un piloto con CQB, HIT y SKL": "Entrena a un piloto con CQB, HIT y SKL",
"Entrena a un piloto con RNG, HIT y SKL": "Entrena a un piloto con RNG, HIT y SKL",
"Consigue un total de 3.000.000 de dinero.": "Consigue un total de 3.000.000 de dinero.",
"Reduce a la mitad el CQB, RNG, HIT, EVD, DEF y SKL de una unidad enemiga": "Reduce a la mitad el CQB, RNG, HIT, EVD, DEF y SKL de una unidad enemiga",
"‧Total de enemigos atacantes": "‧Total de enemigos atacantes",
"%d EXP obtenida respectivamente.": "%d EXP obtenida respectivamente.",
"%d de dinero obtenido en total.": "%d de dinero obtenido en total.",
"Los pilotos activos obtienen %d de EXP.": "Los pilotos activos obtienen %d de EXP.",
"Aumenta la EXP obtenida un 50%.": "Aumenta la EXP obtenida un 50 %.",
"Aumenta el dinero y la EXP obtenidos en": "Aumenta el dinero y la EXP obtenidos en",
"RNG, SKL, DEF, EVD y HIT de los enemigos": "RNG, SKL, DEF, EVD y HIT de los enemigos",
"Aumenta el dinero y la EXP obtenidos un": "Aumenta el dinero y la EXP obtenidos un",
"EVD y HIT.": "EVD y HIT.",
"El CQB, RNG, SKL, DEF, EVD y HIT del piloto aumentan": "El CQB, RNG, SKL, DEF, EVD y HIT del piloto aumentan",
"Space-time Convergence Cannon cuesta 30 menos de EN": "El Cañón de Convergencia Espaciotemporal cuesta 30 menos de EN",
}

with open(os.path.join(D, "b_lt00_rest_es_p6.json"), "w", encoding="utf-8") as fh:
    json.dump(T, fh, ensure_ascii=False, indent=1)
print("lote 6:", len(T))
