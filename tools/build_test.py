"""build_test.py - construye un STGEST de prueba con traducciones plegadas a ASCII
para aislar si los caracteres no-ASCII (acentos, ¿¡, «») causan el crasheo."""
import story_build

def fold(s):
    if not isinstance(s, str):
        return s
    import unicodedata
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')

_orig_lt = story_build.load_translations
_orig_tm = story_build.load_tm

def folded_lt():
    return {k: fold(v) for k, v in _orig_lt().items()}

def folded_tm():
    return {k: fold(v) for k, v in _orig_tm().items()}

story_build.load_translations = folded_lt
story_build.load_tm = folded_tm
story_build.OUT = 'C:/Dev/Default Project/srwv/outputs/STGEST_EN_test_ascii.cpk'

story_build.build()
print('OK ->', story_build.OUT)
