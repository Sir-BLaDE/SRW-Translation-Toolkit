"""
story.py - Extraccion y reconstruccion de los dialogos de historia (STGEST).

Los dialogos van en cadenas largas de Lua con esta forma:

    {WPos_c, 0, FDMode_Normal, pid_NINE,
    [[Nine
「Congratulations on becoming an ace pilot, Kappei.
　I'm sure you worked very hard to get to this point.」]],
     0, NULL},

Se conserva el nombre del hablante (primera linea) y el texto entre 「」.
"""
import re

BLOCK = re.compile(rb'\[\[(.*?)\]\]', re.S)
QUOTE_OPEN = '\u300c'
QUOTE_CLOSE = '\u300d'


class Dialog:
    __slots__ = ('entry', 'start', 'end', 'raw', 'speaker', 'lines', 'body')

    def __init__(self, entry, start, end, raw):
        self.entry = entry
        self.start = start
        self.end = end
        self.raw = raw
        text = raw.decode('utf-8', 'replace')
        parts = text.split('\n', 1)
        self.speaker = parts[0]
        rest = parts[1] if len(parts) > 1 else ''
        self.body = rest
        self.lines = rest.split('\n')

    def __repr__(self):
        return f'<Dialog e{self.entry} {self.speaker} {len(self.lines)} lineas>'


def find_dialogs(entry_id, data):
    out = []
    for m in BLOCK.finditer(data):
        txt = m.group(1).decode('utf-8', 'replace')
        if QUOTE_OPEN in txt:
            out.append(Dialog(entry_id, m.start(1), m.end(1), m.group(1)))
    return out


def translatable(d):
    """Texto a traducir (sin los corchetes japoneses)."""
    body = d.body
    if body.startswith(QUOTE_OPEN):
        body = body[1:]
    if body.rstrip().endswith(QUOTE_CLOSE):
        body = body.rstrip()[:-1]
    return body


# La fuente EN no tiene glifo para estos caracteres (o no estan en el mapa de
# caracteres, lo que provoca cierre del juego). Se sustituyen al construir.
SUSTITUCIONES = {
    '\u00ab': '\u201c',   # « -> “
    '\u00bb': '\u201d',   # » -> ”
    '\u2014': '\u2015',   # — -> ―  (barra horizontal, si existe en la fuente)
    '\u00ba': 'o',        # º -> o   (25.o Escuadron)
    '\u00aa': 'a',        # ª -> a   (2.a Generacion)
}


def sanitize(text):
    for bad, good in SUSTITUCIONES.items():
        text = text.replace(bad, good)
    return text


def rebuild_block(speaker, new_body):
    return (speaker + '\n' + QUOTE_OPEN + sanitize(new_body).rstrip('\n')
            + QUOTE_CLOSE).encode('utf-8')


def replace_dialogs(data, dialogs, translations):
    """translations: {(entry, start): nuevo_cuerpo_texto}"""
    out = bytearray()
    last = 0
    for d in sorted(dialogs, key=lambda x: x.start):
        key = (d.entry, d.start)
        if key not in translations:
            continue
        out += data[last:d.start]
        out += rebuild_block(d.speaker, translations[key])
        last = d.end
    out += data[last:]
    return bytes(out)
