import sys, io, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
path = r'C:/Dev/Default Project/srwv/datos/ln_id0_es.json'
m = json.load(io.open(path, encoding='utf-8'))

# fallback keys currently have value==key
fb = [k for k,v in m.items() if v==k]
print('fallbacks:', len(fb))

# map by a short prefix -> spanish translation
trans_by_prefix = {
 "Maito has vouched": "Maito ha dado fe de nuestro héroe, pero su cálida\nbienvenida se ve interrumpida por otro ataque de los\nrobots villanos. Maito y Gaine se unen en\nMightgaine, aplastando al enemigo. En medio de la\nbatalla, nuestro héroe descubre que la chica de la\npelea anterior es en realidad el SO del VangRay,\nSystem Nine-Nine, y decide llamarla \"Nine\".",
 "Momoka, Ange's": "Momoka, la antigua asistente de Ange, se cuela\na bordo del vuelo de vuelta a Arzenal. Le jura\nlealtad eterna a Ange, pero Ange la rechaza. Las\nincessantes disputas del Primer Escuadrón Para-Mail\npor el sueldo se calman cuando Sumeragi los contrata\npara un trabajo. Tras la batalla, Ange compra a\nMomoka, salvándola así del castigo por haberse\ncolado.",
 "The crew clash with the Martian": "La tripulación se enfrenta a los Sucesores Marcianos\nen Amaterasu. El Nadesico B logra un mortal Salto\nBosón y es capaz de paralizar Amaterasu usando el\nvirus que programó Sanada. Akito y Banjo irrumpen\ny descubren el ? Gundam y a Amuro.\nCon el Yamato liberado y la base de la Esfera\nTerrestre destruida, Akito y la tripulación se\ndirigen al bastión de los Sucesores en Marte.",
 "Shinji tries to fend": "Shinji intenta repeler a un Ángel que ataca a NERV,\npero el EVA Unidad-01 entra en frenesí. El Mazinger\nZ y otros detienen al EVA, y Shinji y Rei vuelven\na combatir al Ángel y a los Dragones.\nTras la batalla, Tetsuya exige que Ryoma vaya\ncon él; cuando Ryoma se niega, Tetsuya abandona\nel grupo por su cuenta.",
 "Sousuke takes Kaname": "Sousuke lleva a Kaname a Jindai High para ayudarla\na calmarse. Allí se encuentran con Leonard, que se\nha convertido en el líder de Amalgam. Sousuke es\nderrotado por el abrumador poder del Belial de\nLeonard, y el Arbalest es destruido. Tras unirse a\nAmalgam, Kalinin traiciona a Mithril durante la\nbatalla y captura a Kaname antes de marcharse con\nLeonard.",
 "The crew clashes with G-Hound": "La tripulación se enfrenta a G-Hound cuando intentan\napoderarse de un EVA. Cuando aparece un Ángel,\nG-Hound, Tetsuya e incluso Neo Zeon se alían con\nla tripulación para repelerlo. Con la ayuda de\nAsuka y Shinji, lo derrotan y salvan el mundo.\nAmuro y los demás toman esta cooperación entre\nenemigos como señal de que aún queda un rayo de\nesperanza.",
 "The crew prepares for the Eighth": "La tripulación se prepara para el ataque del Octavo\nÁngel, Embryo trae a Joe y a la Alianza DG de\nvuelta desde la dimensión AD, pero Maito los\nderrota combinando el Mightgaine y el Might Kaiser\nen el Great Mightgaine. Con la ayuda de Joe, Maito\nderriba al Octavo Ángel, y los tres EVAs trabajan\njuntos para destruir su núcleo.",
 "Our hero and Nine decide to make time": "Nuestro héroe y Nine deciden sacar tiempo para\nhablar a solas y así se acercan cada vez más. Sin\nembargo, nuestro héroe es herido por Ghuli, y el\nVangRay es destruido en un ataque llevado a cabo\npor el comandante de Gardim, Jamie. Nine le da a\nnuestro héroe un nuevo mecha que fue construido en\nsecreto, con el que nuestro héroe finalmente\nderrota a Ghuli.",
 "The crew heads into space": "La tripulación se dirige al espacio para evitar la\nCaída de Colonia de Neo Zeon. Leonard y Embryo\naparecen con Kaname, Salia y los demás. La\ntripulación lucha junto a Mineva y Kamille, y la\ncolonia es destruida por su Cañón de Colonia. La\ntripulación salta a Axis para evadir el láser,\ndonde encuentran a Inez, una exmiembro del Nadesico.",
 "G-Hound seizes control": "G-Hound se apodera del Cañón de Colonia, comienza\nla invasión a gran escala del Dr. Hell, y la\nalianza de Embryo y Leonard produce resultados\ncompletamente inesperados. La tripulación se divide\nen tres grupos para hacer frente a todo lo que\nocurre.",
 "The crew battles with G-Hound for control": "La tripulación combate con G-Hound por el control\ndel Cañón de Colonia. Riddhe anhela derrotar a\nBanagher, pero vuelve en sí gracias a Marida y\nse reincorpora a Londo Bell. La tripulación gana\nventaja en la lucha contra G-Hound, pero no antes\nde que el Cañón de Colonia esté listo para\ndisparar. Desesperado por evitarlo, Banagher\ndestruye el láser.",
 "The crew creates a Boson": "La tripulación crea un transmisor y un receptor\nBosón para despistar a los gamillanos que los\npersiguen, y decide dividirse en dos fuerzas. Okita\ndesea lo mejor a todos en la próxima batalla y los\ndespide con la esperanza de que se reencuentren.",
 "The crew and the Seven-Color": "La tripulación y la Alianza de la Estrella de\nSiete Colores combaten contra las fuerzas de Domel.\nLa tripulación lucha desesperadamente contra su\nejército, pero la llegada de los Invaders hace\nque se unan a Domel contra este enemigo.\nLa tripulación logra una victoria decisiva contra\nDomel, pero durante esta lucha, un escuadrón\nenviado por Dessler para capturar a Yurisha captura\naccidentalmente a Mori.",
 "A confrontation with Ahlforz": "Un enfrentamiento con Ahlforz lleva a nuestro héroe\na conocer el Sistema de Reconstrucción de la\nCivilización Nevanlinna, y que Nine es su terminal.\nNuestro héroe y Nine escapan de Ahlforz y ajustan\ncuentas con Ghuli. Mientras Gamillas y Gardim\ncombaten, Dessler intenta destruir Baleras, pero\nOkita lo detiene usando el cañón de onda motriz.",
 "The crew turns back toward Earth after obtaining": "El grupo regresa hacia la Tierra tras obtener el\nSistema Cosmo Reverse de Iscandar. Mori es herida\nde gravedad por Dessler, y Lacus es capturada por\nEmbryo. Tras ser transportados a la Verdadera\nArzenal, la tripulación conoce la verdad sobre la\ninmortalidad de Embryo. Regresan al espacio normal,\ny luego derrotan a Embryo y Leonard, que habían\nplaneado una fusión espacio-temporal.",
 "Our hero and others aboard the Yamato": "Nuestro héroe y otros a bordo del Yamato son\narrestados por seguridad, que los sospecha de ser\npolizones. Mientras tanto, el Huckebein y el\nGrungust se unen a la tripulación tras ayudar a\nderrotar a los hostiles gamillanos. Mientras el\nYamato abandona la atmósfera, el destino de\nnuestro héroe y los demás sigue sin decidirse.",
 "Velt and Lottie run into Gardim": "Velt y Lottie se encuentran con Gardim mientras\nestán juntos en una misión de reconocimiento.\nJamie también aparece; Velt retira los limitadores\ndel motor de agujero negro del Huckebein y el\nGrungust, y los dos son capaces de destruir a\nJamie con su nuevo poder.\nRegresan, sin embargo, con la noticia de una crisis\nque amenaza a la Tierra y al cosmos por igual.",
}

changed = 0
for k in fb:
    for prefix, val in trans_by_prefix.items():
        if k.startswith(prefix):
            m[k] = val
            changed += 1
            break

io.open(path, 'w', encoding='utf-8').write(json.dumps(m, ensure_ascii=False, indent=2))
print('updated', changed, 'of', len(fb))
print('remaining fallbacks:', sum(1 for k,v in m.items() if v==k))