# -*- coding: utf-8 -*-
"""Crea prologue_trans_v7.json: anade los creditos visibles de la fila 7.

Las claves se buscan como subcadena dentro de cada parte, de modo que se
conservan el relleno U+3000 y las etiquetas \\t1 / \\t2 de los actores.
Solo se toca la fila 7; el resto de filas ya estaban traducidas.
"""
import io
import json

D = r"C:/Dev/Default Project/srwv/datos"
SRC = D + "/prologue_trans_v6.json"
OUT = D + "/prologue_trans_v7.json"
DATA = D + "/prologue_full_v2.json"

# Titles and role labels visible in the credits. Unverified official ES titles
# use descriptive Spanish fallbacks and are documented as such in the glossary.
BASE = {
    "Voice Cast": "Reparto de voces",
    "「The Unchallengeable Daitarn 3」": "「Daitarn 3, el invencible」",
    "「Mobile Suit Crossbone Gundam: The Steel Seven」": "「Mobile Suit Crossbone Gundam: Los Siete de Acero」",
    "「Mobile Suit Gundam 00 the Movie: A Wakening of the Trailblazer」":
        "「Mobile Suit Gundam 00: la película - El despertar del pionero」",
    "「Martian Successor Nadesico: The Motion Picture - Prince of Darkness」":
        "「Nadesico, la sucesora marciana: la película - El príncipe de la oscuridad」",
    "「True Mazinger Edition Z: The Impact!」": "「Mazinger Edición Z: ¡El impacto!」",
    "「True Mazinger ZERO vs Great General of Darkness」":
        "「Mazinger ZERO vs. Gran General de la Oscuridad」",
    "「Full Metal Panic! The Second Raid」": "「Full Metal Panic! El segundo asalto」",
    "「Full Metal Panic! (Original Novel Version)」":
        "「Full Metal Panic! (versión original de la novela)」",
    "「EVANGELION 1.0 YOU ARE (NOT) ALONE.」": "「EVANGELION 1.0 TÚ (NO) ESTÁS SOLO.」",
    "「EVANGELION 2.0 YOU CAN (NOT) ADVANCE.」": "「EVANGELION 2.0 TÚ (NO) PUEDES AVANZAR.」",
    "「EVANGELION 3.0 YOU CAN (NOT) REDO.」": "「EVANGELION 3.0 TÚ (NO) PUEDES REHACER.」",
    "「Cross Ange: Rondo of Angels and Dragons」":
        "「Cross Ange: Rondo de ángeles y dragones」",
    "Tri Bomber／Battle Bomber": "Tri Bomber／Bombardero de Batalla",
    "Nine/System Nine-Nine": "Nueve/Sistema Nueve-Nueve",
    "Emperor of Darkness": "Emperador de la Oscuridad",
    "Great General of Darkness": "Gran General de la Oscuridad",
    "Development": "Desarrollo",
    "Planning": "Planificación",
    "Director": "Director",
    "Scenario Writers": "Guionistas",
    "Event Script": "Guion de eventos",
    "Original Mechanic Design": "Diseño mecánico original",
    "Original Character Design": "Diseño original de personajes",
    "Programming Directors": "Directores de programación",
    "Programming": "Programación",
    "Graphic Directors": "Directores gráficos",
    "Art Directors": "Directores de arte",
    "Battle Graphic Production Manager": "Jefe de producción gráfica de combate",
    "System Graphic Production Manager": "Jefe de producción gráfica del sistema",
    "UI Design": "Diseño de IU",
    "System Graphics": "Gráficos del sistema",
    "Battle Animation": "Animación de combate",
    "Character Cut-in Graphics": "Gráficos de retratos de personajes",
    "Battle Background Graphics": "Gráficos de fondos de combate",
    "Original Robot Art": "Arte original de robots",
    "Character Graphic Manager": "Jefe de gráficos de personajes",
    "Character Graphic Editors": "Editores de gráficos de personajes",
    "Library/Glossary Production Assistants": "Asistentes de producción de biblioteca y glosario",
    "Voice Editing/Sound Effects": "Edición de voz y efectos de sonido",
    "Sound Effects&Voice Editor": "Editor de efectos de sonido y voz",
    "Sound Effects": "Efectos de sonido",
    "Sound Arts": "Artes de sonido",
    "System Manager": "Jefe de sistema",
    "Support": "Apoyo",
    "Sound Director": "Director de sonido",
    "Compose&Arrangement": "Composición y arreglos",
    "Synth Programming": "Programación de sintetizadores",
    "Music Preparation": "Preparación musical",
    "Recording&Mixing Engineer": "Ingeniero de grabación y mezcla",
    "Recording&Mixing Studio": "Estudio de grabación y mezcla",
    "Mixing Engineer": "Ingeniero de mezcla",
    "Mixing Studio": "Estudio de mezcla",
    "Dan Rudin`s Studio (the Heart of Nashville,TN)":
        "Estudio Dan Rudin (el corazón de Nashville, TN)",
    "Dan Rudin Coordinator": "Coordinador de Dan Rudin",
    "Mastering Engineer": "Ingeniero de masterización",
    "Mastering Supervisor": "Supervisor de masterización",
    "2nd Mastering & Music Editor": "Editor de masterización y música (2.º)",
    "Mix Assistant": "Asistente de mezcla",
    "Music Production & Management": "Producción y gestión musical",
    "B.B.Studio Co.,Ltd Sound Team": "Equipo de sonido de B.B.Studio Co.,Ltd",
    "Kitashiro Music Production": "Producción Musical Kitashiro",
    "3D Map Graphics": "Gráficos de mapas 3D",
    "Conversation Background Graphics": "Gráficos de fondos de conversación",
    "Battle Cut-in Original Art Support": "Apoyo de arte original para retratos de combate",
    "「Full Metal Panic!」 Original Character Design":
        "Diseño original de personajes de 「Full Metal Panic!」",
    "Audio Director": "Director de audio",
    "Audio Producer": "Productor de audio",
    "Recording Engineers": "Ingenieros de grabación",
    "Studio Desk Support": "Apoyo de estudio",
    "Recording Studio": "Estudio de grabación",
    "Opening Theme Song": "Canción de apertura",
    "pening Theme Song": "Canción de apertura",
    "Ending Theme Song": "Canción de cierre",
    "nding Theme Song": "Canción de cierre",
    "Lyrics:": "Letra:",
    "Composition:": "Composición:",
    "Arrangement:": "Arreglos:",
    "Vocals:": "Voz:",
    "Printing Production": "Producción de impresión",
    "rinting Production": "Producción de impresión",
    "Package Illustration": "Ilustración del paquete",
    "Development Support": "Apoyo al desarrollo",
    "Quality Assurance": "Garantía de calidad",
    "QUALITY ASSURANCE": "GARANTÍA DE CALIDAD",
    "Promotion & Marketing": "Promoción y marketing",
    "Sales": "Ventas",
    "Produce Support": "Apoyo a la producción",
    "Lead Programmer": "Programador principal",
    "Additional Art": "Arte adicional",
    "Super Robot Wars GAME TEAM": "EQUIPO DE JUEGO DE SUPER ROBOT WARS",
    "uper Robot Wars GAME TEAM": "EQUIPO DE JUEGO DE SUPER ROBOT WARS",
    "Production Project Manager": "Jefe de proyecto de producción",
    "Localization Project Manager": "Jefe de proyecto de localización",
    "Quality Control Project Manager": "Jefe de proyecto de control de calidad",
    "EXECUTIVE TEAM": "EQUIPO DIRECTIVO",
    "President & CEO": "Presidente y consejero delegado",
    "Executive VP & COO": "Vicepresidente ejecutivo y director de operaciones",
    "Executive VP & CFO": "Vicepresidente ejecutivo y director financiero",
    "PUBLISHING & IP STRATEGY": "PUBLICACIÓN Y ESTRATEGIA DE PROPIEDAD INTELECTUAL",
    "UBLISHING & IP STRATEGY": "PUBLICACIÓN Y ESTRATEGIA DE PROPIEDAD INTELECTUAL",
    "VP, Publishing & IP Strategy": "Vicepresidente de publicación y estrategia de PI",
    "Senior Director, Production Services": "Director senior de servicios de producción",
    "Production Manager": "Jefe de producción",
    "Senior Localization Manager": "Jefe senior de localización",
    "Software Tools Engineer": "Ingeniero de herramientas de software",
    "Director, IP Strategy": "Director de estrategia de PI",
    "Additional Testing Provided By:": "Pruebas adicionales a cargo de:",
    "Operations Director": "Director de operaciones",
    "Sr. QA Manager": "Jefe senior de garantía de calidad",
    "Project Lead": "Jefe de proyecto",
    "Testers": "Probadores",
    "Additional Language Testing Provided By:": "Pruebas lingüísticas adicionales a cargo de:",
    "LQA Manager": "Jefe de LQA",
    "LQA Test Manager": "Jefe de pruebas LQA",
    "LQA Test Lead": "Responsable de pruebas LQA",
    "LQA Engineers (English)": "Ingenieros de LQA (inglés)",
    "Managing Director": "Director general",
    "Sales Manager": "Jefe de ventas",
    "Sales Representative": "Representante de ventas",
    "Marketing Manager": "Jefe de marketing",
    "PR Assistant Manager": "Jefe adjunto de relaciones públicas",
    "Product Manager": "Jefe de producto",
    "Product Executive": "Ejecutivo de producto",
    "Art Designer & Operations Coodinator": "Diseñador artístico y coordinador de operaciones",
    "Asia Localisation Manager": "Jefe de localización de Asia",
    "Localisation Manager (Taiwan)": "Jefe de localización (Taiwán)",
    "Chinese QA Project Leader": "Jefe de proyecto de garantía de calidad en chino",
    "Chinese Localization Tester": "Probador de localización en chino",
    "Acting General Manager (Sales & Marketing) Korea":
        "Director general en funciones (ventas y marketing), Corea",
    "Product Assistant": "Asistente de producto",
    "Marketing Assistant": "Asistente de marketing",
    "Marketing Coordinator": "Coordinador de marketing",
    "Logistics & Product Coordinator": "Coordinador de logística y producto",
    "Localization Manager": "Jefe de localización",
    "Localization Assistant": "Asistente de localización",
    "Localization Senior Specialist": "Especialista senior de localización",
    "Localization Specialist": "Especialista de localización",
    "Korean Localization Tester": "Probador de localización en coreano",
    "Managing Director & Senior VP Of Asia Pacific":
        "Director general y vicepresidente senior de Asia-Pacífico",
    "General Manager (Sales & Marketing), Singapore & S.E.A":
        "Director general (ventas y marketing), Singapur y Sureste Asiático",
    "SVP Marketing Asia": "Vicepresidente senior de marketing de Asia",
    "IP Strategy Manager Asia Pacific": "Jefe de estrategia de PI de Asia-Pacífico",
    "Associate Product Manager": "Jefe de producto adjunto",
    "Director of Digital Sales": "Director de ventas digitales",
    "Digital Operations Manager": "Jefe de operaciones digitales",
    "Marketing Executive": "Ejecutivo de marketing",
    "Logistics And Account Coordinator": "Coordinador de logística y cuentas",
    "Production Support": "Apoyo a la producción",
    "Powered by \"CRIWARE\". CRIWARE is a trademark of CRI Middleware Co., Ltd":
        "Con tecnología «CRIWARE». CRIWARE es una marca registrada de CRI Middleware Co., Ltd",
    "WARE\". CRIWARE is a trademark of CRI Middleware Co., Ltd":
        "CRIWARE». CRIWARE es una marca registrada de CRI Middleware Co., Ltd",
    "IWARE is a trademark of CRI Middleware Co., Ltd":
        "CRIWARE es una marca registrada de CRI Middleware Co., Ltd",
    "(C) Copyright TypeBank Co., Ltd. All Rights Reserved.":
        "(C) Copyright TypeBank Co., Ltd. Todos los derechos reservados.",
    "eBank Co., Ltd. All Rights Reserved.": "TypeBank Co., Ltd. Todos los derechos reservados.",
    "o., Ltd. All Rights Reserved.": "TypeBank Co., Ltd. Todos los derechos reservados.",
    "Fonts used in-game are provided in part by TypeBank Co.,Ltd. All rights reserved.":
        "Las fuentes del juego las proporciona en parte TypeBank Co.,Ltd. Todos los derechos reservados.",
    "rovided in part by TypeBank Co.,Ltd. All rights reserved.":
        "proporciona en parte TypeBank Co.,Ltd. Todos los derechos reservados.",
    "ided in part by TypeBank Co.,Ltd. All rights reserved.":
        "proporciona en parte TypeBank Co.,Ltd. Todos los derechos reservados.",
    "ed in part by TypeBank Co.,Ltd. All rights reserved.":
        "proporciona en parte TypeBank Co.,Ltd. Todos los derechos reservados.",
    "d in part by TypeBank Co.,Ltd. All rights reserved.":
        "proporciona en parte TypeBank Co.,Ltd. Todos los derechos reservados.",
    "y TypeBank Co.,Ltd. All rights reserved.":
        "por TypeBank Co.,Ltd. Todos los derechos reservados.",
    "Promotion Video Production": "Producción de vídeo promocional",
    "otion Video Production": "Producción de vídeo promocional",
    "o Production": "Producción",
    "Developed by B.B.STUDIO CO.,LTD.": "Desarrollado por B.B.STUDIO CO.,LTD.",
    "eveloped by B.B.STUDIO CO.,LTD.": "Desarrollado por B.B.STUDIO CO.,LTD.",
    "Produced by BANDAI NAMCO Entertainment Inc.":
        "Producido por BANDAI NAMCO Entertainment Inc.",
    "roduced by BANDAI NAMCO Entertainment Inc.":
        "Producido por BANDAI NAMCO Entertainment Inc.",
    "Senior Specialist": "Especialista senior",
    "n Senior Specialist": "Especialista senior",
    "roduct Coordinator": "Coordinador de producto",
    "(English)": "(inglés)",
    "Provided By:": "A cargo de:",
    "rovided By:": "A cargo de:",
    "vided By:": "A cargo de:",
    "esting Provided By:": "Pruebas a cargo de:",
    "ting Provided By:": "Pruebas a cargo de:",
    "ing Provided By:": "Pruebas a cargo de:",
    "Music Production": "Producción musical",
    "Production": "Producción",
    "Graphics": "Gráficos",
    "Design": "Diseño",
    "und Graphics": "Gráficos de fondos",
    "nd Graphics": "Gráficos de fondos",
    "d Graphics": "Gráficos de fondos",
    "iginal Character Design": "Diseño original de personajes",
    "l Character Design": "Diseño de personajes",
    "tashiro Music Production)": "Producción Musical Kitashiro)",
    "Studio A-tone": "Estudio A-tone",
}

T = json.load(io.open(SRC, encoding="utf-8"))
d = json.load(io.open(DATA, encoding="utf-8"))
keys = sorted(BASE, key=len, reverse=True)

added = 0
changed_parts = 0
for row in d["7"]["rows"]:
    for part in row["parts"]:
        for en in keys:
            if en not in part:
                continue
            es = BASE[en]
            new = part.replace(en, es)
            if new == part:
                continue
            # prologue_rebuild.py busca por s.strip(), asi que la clave no
            # lleva el relleno, pero el valor si lo conserva.
            k = part.strip()
            if k not in T:
                added += 1
            T[k] = new
            changed_parts += 1
            break

with io.open(OUT, "w", encoding="utf-8") as fh:
    json.dump(T, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

print("claves base", len(BASE), "partes cambiadas", changed_parts,
      "claves nuevas", added, "total", len(T), "->", OUT)
