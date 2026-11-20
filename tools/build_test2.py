"""build_test2.py - construye STGEST manteniendo Latin-1 (acentos/¿¡/«»),
pero eliminando cualquier caracter por encima de 0xFF (U+3000, CJK...)."""
import story_build

def fold2(s):
    if not isinstance(s, str):
        return s
    return ''.join(c for c in s if ord(c) <= 0xFF)

_orig_lt = story_build.load_translations
_orig_tm = story_build.load_tm

story_build.load_translations = lambda: {k: fold2(v) for k, v in _orig_lt().items()}
story_build.load_tm = lambda: {k: fold2(v) for k, v in _orig_tm().items()}
story_build.OUT = 'C:/Dev/Default Project/srwv/outputs/STGEST_EN_test_latin1.cpk'

story_build.build()
print('OK ->', story_build.OUT)
