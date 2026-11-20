# -*- coding: utf-8 -*-\n"""Acorta las 25 traducciones residuales que no caben en su hueco."""
import io
import json

P = r"C:/Dev/Default Project/srwv/datos/ln_residual_es_list.json"

NEW = {
    10: "Un regalo para quienes compraron el paquete completo de escenarios bonus.\nA ver... ¿qué hay dentro?",
    11: "El grupo de Akito para en un ramen de Japón.\nSe topan con un hombre en la ruina y su amigo.",
    12: "Al crecer la tensión, un grupo de hombres siente celos.\nEstalla un incidente en torno a una persona.",
    14: "G-Hound es la élite de la Federación.\nEn una misión secreta, se topan con Neo Zeon.",
    15: "Hathaway prueba el Ξ Gundam con Mithril.\nCon problemas en el entrenamiento, halla un peligro mayor.",
    16: "Rumbo al espacio profundo, el grupo afronta una simulación de Nine.\n¿Podrán vencer al equipo de sus peores enemigos?",
    19: "Koji pide ayuda a Tetsuya para las próximas batallas.\n¡Un ataque sorpresa hace chocar a los Mazin!",
    20: "Nuestro equipo afronta el simulador de Nine.\n¿Podrán vencer al equipo de sus peores enemigos?",
    22: "Tras la guerra de Júpiter, Tobia sigue luchando.\nLlega un punto de inflexión para Tobia y la Vanguardia Crossbone.",
    23: "Ante la batalla con Amaterasu, Kappei y Maito conocen a un informante.\nUn hombre con rencor contra el equipo ataca.",
    24: "Ruri intenta reponerse tras la muerte de un allegado.\nOtra Nadesico la espera al alistarse.",
    25: "Shinji, Rei y Asuka no logran trabajar juntos.\nLos hombres calman las preocupaciones de Misato.",
    27: "Los capitanes preparan su batalla en el espacio.\nReciben una clase de combate naval del comandante Okita.",
    28: "El protagonista y Nine envían a Tatsu un vídeo-carta al partir.\n¿Cuál es la mejor forma de presentar a sus preciosos amigos...?",
    29: "La tripulación del Yamato interroga al protagonista y su mech.\n¿Qué le espera al protagonista al subir de nuevo al VangRay...?",
    30: "Las soldados se pelean por una nimiedad.\n¿Quién será la más bella de todas?",
    31: "Tobia, separado de sus compañeros, se une al grupo de Setsuna.\nCelestial Being está siendo perseguido.",
    32: "El Yamato captura la base gamillana de Plutón, pero...\nEl teniente Kodai siente inquietud.",
    59: "Plutón: ocaso",
    60: "Plutón: ocaso",
    75: "Codicia y más",
    78: "Mares rojos, tierras rotas",
    79: "Mares rojos, tierras rotas",
    80: "Canto del dios oscuro",
    81: "Canto del dios oscuro",
}

data = json.load(io.open(P, encoding="utf-8"))
for i, v in NEW.items():
    old = data[i]
    if old == v:
        raise SystemExit("Ya aplicado en indice %d" % i)
    # Conservar la estructura basica (saltos de linea)
    assert old.count("\\n") == v.count("\\n"), (i, "LF")
    data[i] = v
    print("%3d  %d -> %d bytes  %r" % (i, len(old.encode("utf-8")),
                                       len(v.encode("utf-8")), v[:50]))
with io.open(P, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("escrito", P, len(data))
