# Guía de traducción — Super Robot Wars V (STGEST)

## Objetivo
Traducir al **español de España** los diálogos de historia del juego. Registro coloquial
y natural, como en un anime doblado: tuteo, contracciones normales, sin sonar acartonado.
**Obligatorio**: acentos correctos (á é í ó ú ü ñ) y signos de apertura ¡ ¿.
La fuente ya está parcheada en el juego, así que se pueden usar sin miedo.

## Dónde están los textos
`C:/Dev/Default Project/srwv/datos/story_dialogues.jsonl`
Una línea JSON por registro, en orden. Campos: `entry`, `speaker`, `text` (inglés).
El número de línea (empezando en 0) **es el id** que se usa como clave.

Para ver un rango:
```
cd C:/Dev/Default Project/srwv/tools
$env:PYTHONIOENCODING='utf-8'; python show_batch.py 49300 49499
```

## Formato de salida
Un fichero JSON por lote, en `C:/Dev/Default Project/srwv/datos/es_batches/`,
con nombre `bNNN_<inicio>_<fin>.json` (fin = inicio + 199), por ejemplo
`b198_49300_49499.json`:

```json
{
  "49300": "Primera línea del diálogo.\r\n　Segunda línea.",
  "49301": "Otra frase."
}
```

Reglas exactas:

1. **Solo el cuerpo del diálogo**. NO incluir 「 」 (los pone el programa al construir).
2. El nombre del hablante NO se traduce (lo conserva el programa); no lo incluyas.
3. Los saltos de línea van como `\r\n` y **cada línea de continuación empieza por U+3000**
   (espacio ideográfico de ancho completo), igual que el original:
   `"Texto de la primera línea.\r\n　Texto de la segunda línea."`
   Mantén un número de líneas parecido al original (2-3 líneas). No metas líneas de más
   de ~65 caracteres.
4. Preserva **tal cual** los marcadores y variables: `$n`, `$c`, `$l`, `$r`, `$f`, `$F`,
   `%d`, `%s`, `\n`, `\r\n`, `【 】`, `《 》`, `『 』`.
   - `$n` = nombre del protagonista. `$c` = un número. No los traduzcas ni los cambies de sitio.
   - Los bloques `$kwb...$kwe` son términos técnicos resaltados: **déjalos en inglés**
     (se conserva el contenido literal).
5. Nombres propios de **personajes, mechs, ataques, series y facciones** se dejan en
   **inglés** (Crossbone Vanguard, Amakusa, VangRay, Gundam, Banshee, Great Mightgaine,
   Goryu, Madivia, Rozen Zulu, Mazinger, Daitarn 3, Zambot 3, Yamato, Neo Zeong...).
   Los **topónimos y organizaciones** sí se traducen (ver glosario).
6. Nada de comillas tipográficas raras: usa comillas normales si hacen falta, pero el
   texto va sin comillas envolventes.
7. Si el original es solo "..." o un grito, traduce igual ("...", "¡Ah!", etc.).

## Glosario fijo (usar siempre)
- ExC → Cuenta Extra · SP → PE · Tac Pts → Pts Tác
- Focus → Enfoque · Great Ace → Gran As · Skill Programs → Programas de Habilidad
- Boost Dash → Impulso Veloz · Smash Hit → Golpe Demoledor
- Direct Attack → Ataque Directo · Multi Action → Multiacción
- Innocent Wave → Ola Innocente · Getter Radiation → Radiación Getter
- Cosmo Reverse System → Sistema Cosmo Reverse (o "el Cosmo Reverse")
- Brave Express Corps → Cuerpo Express Valiente
- Diamond Rose Knights → Caballeros de la Rosa de Diamante
- Colony Laser → Cañón de Colonia · Laplace's Box → la Caja de Laplace
- Great General of Darkness → Gran General de la Oscuridad
- Emperor of Darkness → Emperador de la Oscuridad
- Mycenae → Mycenae (se deja) · Hades → Hades · Olympus → Olimpo
- Irregulars → Irregulares · Martian Successors → Sucesores Marcianos
- Jovian Federation → Federación Joviana · Coordinators → Coordinators
- Black Noir → Black Noir · Meganoids → Meganoids

## Verificación (obligatoria antes de terminar)
```
cd C:/Dev/Default Project/srwv/tools
$env:PYTHONIOENCODING='utf-8'; python check_batch.py "C:/Dev/Default Project/srwv/datos/es_batches/bNNN_inicio_fin.json" inicio fin+1
```
Debe decir `sin problemas`. Se toleran los avisos:
- `identica al original` cuando la frase es realmente igual en español ("...", "No.", "¡Grr!").
- `lineas de mas de 70 caracteres` (aviso, no error).

NO ejecutes `story_build.py` ni toques nada dentro de `D:/Juegos/...`.
Solo creas tu fichero de lote.

## Estilo
- Natural y directo, con la personalidad de cada personaje (niños, militares, robots
  arrogantes, chicas enérgicas...).
- Nada de calcos del inglés: "¡Ya veo!" mejor que "¡Veo!"; "¡Maldita sea!" por "Damn it!".
- Mantén el tono de las traducciones ya hechas en `datos/es_batches/` (mira 2-3 lotes
  cercanos al tuyo con `python show_batch.py` y el JSON correspondiente).

## REGLA 5 (REVISADA 2026-11-19, orden del usuario)
Ya NO se dejan en inglés nombres de robots, ataques, armas ni personajes: siempre se usan los nombres del doblaje/subtitulado oficial en español de España de cada serie (p. ej. gamilas, no gamillanos). Si no existe versión oficial en España, se usa la forma oficial en español más extendida y se anota en glosario_españa.json.
