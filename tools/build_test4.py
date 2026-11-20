"""build_test4.py - mantiene SOLO los caracteres acentuados que ya existen en el
mapa JAPN (é É ¿ ¡ « »), convierte el resto de acentos a base, y suelta el resto.
Sirve para determinar si el juego usa el mapa JAPN o LATN para la historia."""
import story_build
import unicodedata

KEEP = set('éÉ¿¡«»')

def fold4(s):
    if not isinstance(s, str):
        return s
    out = []
    for c in s:
        o = ord(c)
        if o <= 0x7F:
            out.append(c)
        elif c in KEEP:
            out.append(c)
        else:
            # descomponer acentos -> base ascii (á->a, ñ->n...)
            d = unicodedata.normalize('NFKD', c)
            asc = d.encode('ascii', 'ignore').decode('ascii')
            if asc:
                out.append(asc)
            # si no (griega, U+3000, etc.) -> se suelta
    return ''.join(out)

_orig_lt = story_build.load_translations
_orig_tm = story_build.load_tm
story_build.load_translations = lambda: {k: fold4(v) for k, v in _orig_lt().items()}
story_build.load_tm = lambda: {k: fold4(v) for k, v in _orig_tm().items()}
story_build.OUT = 'C:/Dev/Default Project/srwv/outputs/STGEST_EN_test_e_japn.cpk'

story_build.build()
print('OK ->', story_build.OUT)
