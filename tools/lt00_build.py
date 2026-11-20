"""Reconstruye LT00_EN.cpk con el compresor bueno a partir del texto ya traducido."""
import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')

from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
from lt00 import load, Lt00
from cpk_util import load as load_cpk
from srwv_cpkbuild2 import build_ordered

BASE = 'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk'
ES = r'C:/Dev/Default Project/srwv/outputs/LT00_EN_es.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/LT00_EN_es2.cpk'


def plaintext(path):
    return decrypt_data(maybe_decompress(Cpk(path).read_file(0)))


src = load(plaintext(ES))
strings = list(src.strings)

# etiqueta de idioma
idx = [i for i, s in enumerate(strings) if s == '‧EN']
for i in idx:
    strings[i] = '‧ES'
print('etiqueta idioma en', idx)

plain = Lt00(src.raw).build(strings)
chk = load(plain)
assert chk.strings == strings, 'roundtrip de cadenas'
print('plain nuevo', len(plain), 'cadenas', chk.count, 'ids', chk.id_count)

cf = load_cpk(BASE)
f = cf.rows[0]
blob = cf.cipher(f, plain)
new_files = {f['id']: (blob, len(plain))}
out = build_ordered(BASE, new_files)
open(OUT, 'wb').write(out)
print('escrito', len(out), '->', OUT)

c2 = load_cpk(OUT)
f2 = c2.rows[0]
pt = c2.plain(f2)
t2 = load(pt)
print('diag', c2.cpk.diagnose() or 'ok')
print('plain identico', pt == plain, 'cadenas', t2.count)
print('FileSize', f2['size'], 'ExtractSize', f2['ex'], 'plain', len(pt))
print('hdr', [hex(x) for x in t2.header])
