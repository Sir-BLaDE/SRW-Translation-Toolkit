import json, io
path = r'C:/Dev/Default Project/srwv/datos/ln_id0_es.json'
m = json.load(io.open(path, encoding='utf-8'))

# Spanish translations for the 18 unmatched entries (keyed by exact source text)
extra = {
 "Maito has vouched for our hero, but his warm\nwelcome is interrupted by another attack by the\nvillainous robots. Maito and Gaine unite into\nMightgaine, crushing the enemy. In the middle of\nbattle, our hero learns that the girl from the\nprevious fight is actually the VangRay's OS,\nSystem Nine-Nine, and decides to call her \"Nine.\"":
  "Maito ha dado fe de nuestro héroe, pero su cálida\nbienvenida se ve interrumpida por otro ataque de los\nrobots villanos. Maito y Gaine se unen en\nMightgaine, aplastando al enemigo. En medio de la\nbatalla, nuestro héroe descubre que la chica de la\npelea anterior es en realidad el SO del VangRay,\nSystem Nine-Nine, y decide llamarla \"Nine\".",
 "Momoka, Ange's former attendant, sneaks aboard\nthe flight back to Arzenal. She pledges her\nundying loyalty to Ange, but Ange rejects her. The\nPara-Mail First Squad's incessant squabbles over\npay calm down when Sumeragi hires them on for a\njob. After the battle, Ange buys Momoka, thus\nsaving her from being punished for stowing away.":
  "Momoka, la antigua asistente de Ange, se cuela\na bordo del vuelo de vuelta a Arzenal. Le jura\nlealtad eterna a Ange, pero Ange la rechaza. Las\nincessantes disputas del Primer Escuadrón Para-Mail\npor el sueldo se calman cuando Sumeragi los contrata\npara un trabajo. Tras la batalla, Ange compra a\nMomoka, salvándola así del castigo por haberse\ncolado.",
 "The crew clash with the Martian Successors on\nAmaterasu. Nadesico B succeeds in a deadly Boson\nJump and is able to paralyze Amaterasu using the\nvirus that Sanada programmed. Akito and Banjo\nbreak in and discover the ? Gundam and Amuro.\nWith the Yamato freed and the Earth Sphere base\ndestroyed, Akito and the crew make their way to\nthe Successors' stronghold on Mars.":
  "La tripulación se enfrenta a los Sucesores Marcianos\nen Amaterasu. El Nadesico B logra un mortal Salto\nBosón y es capaz de paralizar Amaterasu usando el\nvirus que programó Sanada. Akito y Banjo irrumpen\ny descubren el ? Gundam y a Amuro.\nCon el Yamato liberado y la base de la Esfera\nTerrestre destruida, Akito y la tripulación se\ndirigen al bastión de los Sucesores en Marte.",
 "Shinji tries to fend off an Angel attacking NERV,\nbut Eva Unit-01 goes berserk. The Mazinger Z and\nothers stop the Eva, and Shinji and Rei fight the\nAngel and Dragons once more.\nAfter the battle, Tetsuya demands that Ryoma\ncome with him; when Ryoma refuses, Tetsuya leaves\nthe group on his own.":
  "Shinji intenta repeler a un Ángel que ataca a NERV,\npero el EVA Unidad-01 entra en frenesí. El Mazinger\nZ y otros detienen al EVA, y Shinji y Rei vuelven\na combatir al Ángel y a los Dragones.\nTras la batalla, Tetsuya exige que Ryoma vaya\ncon él; cuando Ryoma se niega, Tetsuya abandona\nel grupo por su cuenta.",
 "Sousuke takes Kaname to Jindai High to help calm\nher down. There, they encounter Leonard, who has\nbecome Amalgam's leader. Sousuke is defeated by\nthe overwhelming power of Leonard's Belial, and\nthe Arbalest is destroyed. Having joined Amalgam,\nKalinin betrays Mithril during the battle and\ncaptures Kaname before leaving with Leonard.":
  "Sousuke lleva a Kaname a Jindai High para ayudarla\na calmarse. Allí se encuentran con Leonard, que se\nha convertido en el líder de Amalgam. Sousuke es\nderrotado por el abrumador poder del Belial de\nLeonard, y el Arbalest es destruido. Tras unirse a\nAmalgam, Kalinin traiciona a Mithril durante la\nbatalla y captura a Kaname antes de marcharse con\nLeonard.",
 "The crew clashes with G-Hound when they try to\nseize an Eva. When an Angel appears, G-Hound,\nTetsuya, and even Neo Zeon ally with the crew to\nfend it off. With Asuka and Shinji's help, they\ndefeat it and save the world. Amuro and the others\ntake this cooperation between enemies as a sign\nthat a glimmer of hope yet remains.":
  "La tripulación se enfrenta a G-Hound cuando intentan\napoderarse de un EVA. Cuando aparece un Ángel,\nG-Hound, Tetsuya e incluso Neo Zeon se alían con\nla tripulación para repelerlo. Con la ayuda de\nAsuka y Shinji, lo derrotan y salvan el mundo.\nAmuro y los demás toman esta cooperación entre\nenemigos como señal de que aún queda un rayo de\nesperanza.",
 "The crew prepares for the Eighth Angel's attack,\nEmbryo brings Joe and the DG Alliance back from\nthe AD dimension, but Maito defeats them by\ncombining the Mightgaine and Might Kaiser into\nthe Great Mightgaine. With Joe's help, Maito\nshoots down the Eighth Angel, and the three Evas\nwork together to destroy its core.":
  "La tripulación se prepara para el ataque del Octavo\nÁngel, Embryo trae a Joe y a la Alianza DG de\nvuelta desde la dimensión AD, pero Maito los\nderrota combinando el Mightgaine y el Might Kaiser\nen el Great Mightgaine. Con la ayuda de Joe, Maito\nderriba al Octavo Ángel, y los tres EVAs trabajan\njuntos para destruir su núcleo.",
 "Our hero and Nine decide to make time to talk\none-on-one and so grow ever closer. However,\nour hero is injured by Ghuli, and the VangRay is\ndestroyed in an attack carried out by Gardim's\ncommander, Jamie. Nine gives our hero a new mech\nthat was constructed in secret, with which our\nhero finally destroys Ghuli.":
  "Nuestro héroe y Nine deciden sacar tiempo para\nhablar a solas y así se acercan cada vez más. Sin\nembargo, nuestro héroe es herido por Ghuli, y el\nVangRay es destruido en un ataque llevado a cabo\npor el comandante de Gardim, Jamie. Nine le da a\nnuestro héroe un nuevo mecha que fue construido en\nsecreto, con el que nuestro héroe finalmente\nderrota a Ghuli.",
 "Our hero and Nine decide to make time to talk\none-on-one and so grow ever closer. However,\nGhuli appears, and the VangRay is destroyed in an\nattack carried out by Gardim's commander, Jamie.\nNine gives our hero a new mech that was\nconstructed in secret, with which our hero finally\ndestroys Ghuli.":
  "Nuestro héroe y Nine deciden sacar tiempo para\nhablar a solas y así se acercan cada vez más. Sin\nembargo, aparece Ghuli, y el VangRay es destruido\nen un ataque llevado a cabo por el comandante de\nGardim, Jamie. Nine le da a nuestro héroe un nuevo\nmecha que fue construido en secreto, con el que\nnuestro héroe finalmente destruye a Ghuli.",
 "The crew heads into space in order to prevent Neo\nZeon's Colony Drop. Leonard and Embryo appear with\nKaname, Salia, and the others in tow. The crew\nfights together with Mineva and Kamille, and the\ncolony is destroyed by their Colony Laser. The\ncrew jumps to Axis in order to evade the laser, \nwhere they find Inez, an ex-member of Nadesico.":
  "La tripulación se dirige al espacio para evitar la\nCaída de Colonia de Neo Zeon. Leonard y Embryo\naparecen con Kaname, Salia y los demás en tow. La\ntripulación lucha junto a Mineva y Kamille, y la\ncolonia es destruida por su Cañón de Colonia. La\ntripulación salta a Axis para evadir el láser, \ndonde encuentran a Inez, una exmiembro del Nadesico.",
 "G-Hound seizes control of the Colony Laser, Dr.\nHell's large-scale invasion begins, and Embryo and\nLeonard's alliance produces utterly unexpected\nresults. The crew splits into three groups in\norder to deal with all that happens.":
  "G-Hound se apodera del Cañón de Colonia, comienza\nla invasión a gran escala del Dr. Hell, y la\nalianza de Embryo y Leonard produce resultados\ncompletamente inesperados. La tripulación se divide\nen tres grupos para hacer frente a todo lo que\nocurre.",
 "The crew battles with G-Hound for control of the\nColony Laser. Riddhe yearns to defeat Banagher,\nbut he comes back to himself thanks to Marida and\nrejoins Londo Bell. The crew gains the advantage\nin the fight against G-Hound, but not before the\nColony Laser is prepped to fire. Desperate to\nprevent this, Banagher destroys the laser.":
  "La tripulación combate con G-Hound por el control\ndel Cañón de Colonia. Riddhe anhela derrotar a\nBanagher, pero vuelve en sí gracias a Marida y\nse reincorpora a Londo Bell. La tripulación gana\nventaja en la lucha contra G-Hound, pero no antes\nde que el Cañón de Colonia esté listo para\ndisparar. Desesperado por evitarlo, Banagher\ndestruye el láser.",
 "The crew creates a Boson transmitter and receiver\nin order to throw off the pursuing Gamillans, and\ndecides to split into two forces. Okita wishes the\nbest for everyone in the upcoming battle and sends\nthem off in hopes they will meet again.":
  "La tripulación crea un transmisor y un receptor\nBosón para despistar a los gamillanos que los\npersiguen, y decide dividirse en dos fuerzas. Okita\ndesea lo mejor a todos en la próxima batalla y los\ndespide con la esperanza de que se reencuentren.",
 "The crew and the Seven-Color Star Alliance battle\nwith Domel's forces. The crew fights desperately\nagainst his army, but the arrival of Invaders\ncauses them to unite with Domel against this foe.\nThe crew wins a decisive victory against Domel,\nbut during this fight, a squad sent by Dessler\nto capture Yurisha accidentally captures Mori.":
  "La tripulación y la Alianza de la Estrella de\nSiete Colores combaten contra las fuerzas de Domel.\nLa tripulación lucha desesperadamente contra su\nejército, pero la llegada de los Invaders hace\nque se unan a Domel contra este enemigo.\nLa tripulación logra una victoria decisiva contra\nDomel, pero durante esta lucha, un escuadrón\nenviado por Dessler para capturar a Yurisha captura\naccidentalmente a Mori.",
 "A confrontation with Ahlforz leads our hero to\nlearn of the Civilization Reconstruction System\nNevanlinna, and that Nine is its terminal. Our\nhero and Nine escape from Ahlforz and settle the\nscore with Ghuli. As Gamillas and Gardim battle,\nDessler attempts to destroy Baleras, but Okita\nstops him by using the wave motion gun.":
  "Un enfrentamiento con Ahlforz lleva a nuestro héroe\na conocer el Sistema de Reconstrucción de la\nCivilización Nevanlinna, y que Nine es su terminal.\nNuestro héroe y Nine escapan de Ahlforz y ajustan\ncuentas con Ghuli. Mientras Gamillas y Gardim\ncombaten, Dessler intenta destruir Baleras, pero\nOkita lo detiene usando el cañón de onda motriz.",
 "The crew turns back toward Earth after obtaining\nthe Cosmo Reverse System from Iscandar. Mori is\ncritically wounded by Dessler, and Lacus is taken\nby Embryo. After being transported to True\nArzenal, the crew learns the truth about Embryo's\nimmortality. They return to normal space, then\ndefeat Embryo and Leonard, who had been plotting\na space-time fusion.":
  "El grupo regresa hacia la Tierra tras obtener el\nSistema Cosmo Reverse de Iscandar. Mori es herida\nde gravedad por Dessler, y Lacus es capturada por\nEmbryo. Tras ser transportados a la Verdadera\nArzenal, la tripulación conoce la verdad sobre la\ninmortalidad de Embryo. Regresan al espacio normal,\ny luego derrotan a Embryo y Leonard, que habían\nplaneado una fusión espacio-temporal.",
 "Our hero and others aboard the Yamato are arrested\nby security, who suspect they are stowaways.\nMeanwhile, Huckebein and Grungust join the crew\nafter helping to defeat the Gamillan hostiles. As\nthe Yamato leaves the atmosphere, the fate of our\nhero and the others remains undecided.":
  "Nuestro héroe y otros a bordo del Yamato son\narrestados por seguridad, que los sospecha de ser\npolizones. Mientras tanto, el Huckebein y el\nGrungust se unen a la tripulación tras ayudar a\nderrotar a los hostiles gamillanos. Mientras el\nYamato abandona la atmósfera, el destino de\nnuestro héroe y los demás sigue sin decidirse.",
 "Velt and Lottie run into Gardim while out on a\nreconnaissance mission together. Jamie appears as\nwell; Velt removes Huckebein and Grungust's\nblack hole engine limiters, and the two are able\nto destroy Jamie with their new power.\nThey return, however, to news of a crisis that\nthreatens the Earth and the cosmos alike.":
  "Velt y Lottie se encuentran con Gardim mientras\nestán juntos en una misión de reconocimiento.\nJamie también aparece; Velt retira los limitadores\ndel motor de agujero negro del Huckebein y el\nGrungust, y los dos son capaces de destruir a\nJamie con su nuevo poder.\nRegresan, sin embargo, con la noticia de una crisis\nque amenaza a la Tierra y al cosmos por igual.",
}

# apply
changed = 0
for k, v in extra.items():
    if k in m:
        if m[k] == k:  # was fallback
            m[k] = v
            changed += 1
    else:
        # try normalized key match
        pass

# Also need to handle keys that are fallback (value==key) by matching normalized
# Build normalized index of extra
def norm(s): return s.replace('\u2014','-').replace('\u2013','-')
extra_norm = {norm(k): v for k,v in extra.items()}
for k in list(m.keys()):
    if m[k] == k:  # fallback untranslated
        nk = norm(k)
        if nk in extra_norm:
            m[k] = extra_norm[nk]
            changed += 1

io.open(path, 'w', encoding='utf-8').write(json.dumps(m, ensure_ascii=False, indent=2))
print('updated', changed)
# count remaining fallbacks
fb = sum(1 for k,v in m.items() if v==k)
print('remaining fallbacks:', fb)