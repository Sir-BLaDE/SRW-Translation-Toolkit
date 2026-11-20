import sys, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
from lt00 import load

BASE = 'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/'
c = Cpk(BASE + 'LT00_EN.cpk')
en = load(decrypt_data(maybe_decompress(Cpk(BASE + 'B_LT00_EN.cpk').read_file(0))))
cur = load(decrypt_data(maybe_decompress(c.read_file(0))))

IDENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
jp = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')

def looks_text(s):
    if not s.strip():
        return False
    if jp.search(s):
        return False
    if IDENT.match(s):
        return False
    if len(s.strip()) < 3:
        return False
    if not any(ch.isalpha() for ch in s):
        return False
    return True

pend = [(i, en.strings[i], cur.strings[i]) for i in range(en.count)
        if cur.strings[i] == en.strings[i] and looks_text(en.strings[i])]
print('sin tocar y con texto:', len(pend))
for p in pend:
    print(p[0], repr(p[1])[:100])
