"""build_test3.py - mantiene acentos espanoles core (aeiou n u A E I O U N, ¿¡)
y mapea el resto de no-ASCII (comillas «», guiones, griegas, U+3000...) a ASCII."""
import story_build

KEEP = set('áéíóúñüÁÉÍÓÚÑÜ¿¡')

def fold3(s):
    if not isinstance(s, str):
        return s
    out = []
    for c in s:
        o = ord(c)
        if o <= 0x7F:
            out.append(c)
        elif c in KEEP:
            out.append(c)
        elif c in '«»':
            out.append('"')
        elif c in '—–':
            out.append('-')
        elif c == 'º':
            out.append('o')
        elif c == 'ª':
            out.append('a')
        elif c == '…':
            out.append('...')
        else:
            # U+3000, griegas, fullwidth, 「」... -> espacio o nada
            if c in '\u3000\u300c\u300d～':
                out.append(' ' if c == '\u3000' else '')
            else:
                out.append('')
    return ''.join(out)

_orig_lt = story_build.load_translations
_orig_tm = story_build.load_tm
story_build.load_translations = lambda: {k: fold3(v) for k, v in _orig_lt().items()}
story_build.load_tm = lambda: {k: fold3(v) for k, v in _orig_tm().items()}
story_build.OUT = 'C:/Dev/Default Project/srwv/outputs/STGEST_EN_test_acentos.cpk'

story_build.build()
print('OK ->', story_build.OUT)
