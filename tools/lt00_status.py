"""Analiza que cadenas de LT00 siguen en ingles y exporta las pendientes."""
import re, csv

from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data
from lt00 import load

BASE = 'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/'


def plaintext(fn):
    return decrypt_data(maybe_decompress(Cpk(BASE + fn).read_file(0)))


en = load(plaintext('B_LT00_EN.cpk'))
cur = load(plaintext('LT00_EN.cpk'))
assert en.count == cur.count

SPANISH_CHARS = set('áéíóúÁÉÍÓÚñÑüÜ¡¿')
IDENT = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')


def has_es(s):
    return any(c in SPANISH_CHARS for c in s)


def is_ident(s):
    if not s:
        return True
    if not IDENT.match(s):
        return False
    # identificadores tipicos del juego
    if '_' in s:
        return True
    # CamelCase con 2+ mayusculas internas suele ser clave
    ups = sum(1 for c in s[1:] if c.isupper())
    return ups >= 2


rows = []
stats = {'already_es': 0, 'ident': 0, 'pending': 0}
for i, (e, c) in enumerate(zip(en.strings, cur.strings)):
    if c != e and has_es(c):
        stats['already_es'] += 1
    elif is_ident(e):
        stats['ident'] += 1
    else:
        stats['pending'] += 1
        rows.append((i, e, c))

print(stats)
print('pendientes:', len(rows))
with open('C:/Dev/Default Project/srwv/datos/lt00_pendientes.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['idx', 'en', 'actual'])
    w.writerows(rows)

for r in rows[:60]:
    print(r[0], repr(r[1])[:90], '|', repr(r[2])[:40])
