import sys, io, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')

en = json.load(open(r'C:/Dev/Default Project/srwv/datos/mtzkn_nm_en.json', encoding='utf-8'))

es_text = {
"0": "^^Sin previo aviso, un misterioso alienigena conocido como Gaizok ha venido a\ninvadir la Tierra. Kappei Jin, descendiente de los Bealianos, que fueron\nerradicados por Gaizok, se une a sus parientes Uchuta Kamie y\nKeiko Kamikita para proteger el planeta de Gaizok. Cuando sus tres\nmechas de combate se combinan, se convierten en el gigantesco robot Zambot 3.\nLa batalla entre Gaizok y la familia Jin continua, y las tacticas despiadadas\nde Gaizok causan estragos en la Tierra. Pronto, la gente\nde la Tierra llega a creer que Gaizok solo invade el planeta\npor culpa de la familia Jin, asi que comienzan a perseguirla. Aun asi,\nalgunas personas empiezan a darse cuenta de lo desesperadamente que la familia Jin\nlucha por salvar el planeta, justo cuando la familia decide\nlanzarse a la batalla final contra Gaizok. Tras perder\na muchos familiares y aliados, Kappei derrota a Gaizok y regresa\na la Tierra, solo para ser recibido con los brazos abiertos.",
"1": "^^En un futuro no muy lejano, la raza humana ha lanzado la expansion\nespacial a gran escala, comenzando con una base en Marte.\nPara ayudar al desarrollo en Marte, el Dr. Sozo Haran desarrolla una nueva forma\nde ciborg. Pero en una loca pasion por su investigacion, el Dr. Haran convierte\nincluso a su propia esposa e hijo en ciborgs. Esta nueva linea de ciborgs\nse considera una version mejorada de la especie humana,\ndenominandose Meganoides, y lanzan una lucha para convertir a toda\nla raza humana en Meganoides.\nEl hijo del Dr. Haran, Banjo Haran, roba el super robot Daitarn 3\ny una fortuna en oro, y huye de Marte a la Tierra.\nDesde alli el y sus companeros trabajan para salvar el planeta,\ny la raza humana, de las terribles aspiraciones de los Meganoides.\nEn una batalla decisiva en Marte, Banjo derrota al lider de los Meganoides,\nDon Zauser, poniendo fin a la guerra, pero luego desaparece\nen lo desconocido. Sin dueno, la lujosa mansion en la que\nvivia cae en un sereno silencio.",
"2": "^^Ambientada en el ano 0087 de la Era Universal. Siete anos han pasado desde\nla Guerra de un Ano, en la que las Fuerzas de la Federacion Terrestre lucharon y\nvencieron a las tropas del Principado de Zeon. Una nueva fuerza de elite\ndentro de la Federacion llamada los Titanes ahora oprime a los\nEspacianos que viven en las colonias y en la superficie lunar.",
"3": "^^Ano 0088 de la Era Universal. La guerra entre AEUG y los\nTitanes llega a su climax en el Conflicto Gryps.",
"4": "^^Ano 0093 de la Era Universal. Tras el Conflicto Gryps, Char\nAznable regresa con Neo Zeon para amenazar la paz.",
"5": "^^Ano 0105 de la Era Universal. Han pasado mas de diez anos desde\nla Segunda Guerra de Neo Zeon. Una nueva amenaza emerge.",
"6": "^^Ano 0133 de la Era Universal. Tras la Guerra de Cosmo Babylonia,\nla Esfera Terrestre se enfrenta a nuevas amenazas.",
"7": "^^Ano 71 de la Era Cosmica. Ha estallado un conflicto\nentre la Alianza Terrestre y ZAFT.",
"8": "^^A principios del siglo XXIV, una organizacion militar privada\nllamada Mithril protege al mundo de amenazas terroristas.",
"9": "^^Ano 0096 de la Era Universal. Tres anos han pasado desde\nla Segunda Guerra de Neo Zeon. Los remanentes de Neo Zeon emergen.",
"10": "^^En el ano 2050, una repentina escasez de petroleo fuerza a la sociedad a\nbuscar nuevas fuentes de energia.",
"11": "^^La Guerra de los Lagartos se libra entre la Tierra y los descendientes de\nlos reptiles que evolucionaron en el interior del planeta.",
"12": "^^Rayos Getter: misteriosos haces de energia emitidos desde el confin\ndel universo.",
"13": "^^A medida que la crisis energetica empeora, la raza humana desarrolla un\nsistema de energia supereficiente.",
"14": "^^En varias dimensiones existen Mazinger Z. Estan destinados\na proteger sus respectivos mundos del mal.",
"15": "^^Mithril: una organizacion militar secreta, sin vinculacion a ninguna nacion,\ndedicada a combatir el terrorismo.",
"16": "^^Han pasado quince anos desde el Segundo Impacto, un evento sin precedentes\nque devasto la Tierra. Los EVAs se alzan para defenderla.",
"17": "^^En el ano 2199 d.C., formas de vida alienigenas conocidas como Gamillas lanzan un\nataque contra la Tierra. La humanidad construye el Yamato.",
"18": "^^El desarrollo del revolucionario sistema de transferencia de informacion\nabre nuevas posibilidades para la humanidad.",
}

en_to_es = {}
for k, v in en.items():
    en_to_es[v] = es_text[k]

json.dump(en_to_es, open(r'C:/Dev/Default Project/srwv/datos/mtzkn_nm_es.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', len(en_to_es))