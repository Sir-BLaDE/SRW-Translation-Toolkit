"""font_patch2.py - completa el parche de fuente:
  * anyade el glifo de 'I' acentuada (Í) reutilizando un registro de relleno
  * agrega Í al mapa de la fila 1 (BLTLJUMPN)
  * agrega todos los caracteres espanoles al mapa de la fila 2 (BLTLLAYDN),
    que es la que usan los dialogos de batalla y los menus/UI.
"""
import os, struct, sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
import font_patch as fp

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
OUT = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es2.cpk'

# caracteres que se sustituyen en el mapa de la fila 2 (cirilicos, nunca usados
# en los textos EN/ES del juego). Todos son de 2 bytes en UTF-8.
R2_OLD = list('ЁЪЫЬЭЮЯёъыьэюя')
R2_NEW = list('áéíóúñÁÉÍÓÚü¿¡')

font = fp.Font(SRC)

# --- 1. glifo de Í ----------------------------------------------------------
g_idx, old_uid = 249, 0x0178   # registro de relleno (Ÿ)
assert font.byc.get(old_uid) == g_idx, (font.byc.get(old_uid), g_idx)
img = fp.compose(font, 'I', 'acc_u')
bb = font.ink_bbox(img)
font.put(g_idx, img)
uid, fl = font.rec(g_idx)
fl[7] = float(bb[2] + 1)
font.write_rec(g_idx, 0x00CD, fl)
font.byc[0x00CD] = g_idx
print('Í -> g%d bb=%s ink=%.0f' % (g_idx, bb, fl[7]))

# --- 2. mapas ---------------------------------------------------------------
def replace_in_map(row_id, old_ch, new_ch):
    r = font.rows[row_id]
    d = bytearray(font.cf.plain(r))
    h = [struct.unpack_from('<I', d, i * 4)[0] for i in range(12)]
    a, b = h[6], h[7]
    s = bytes(d[a:b])
    ob, nb = old_ch.encode('utf-8'), new_ch.encode('utf-8')
    assert len(ob) == len(nb) == 2, (old_ch, new_ch)
    assert s.count(ob) == 1, ('row%d: %r count=%d' % (row_id, old_ch, s.count(ob)))
    i = s.index(ob)
    d[a + i:a + i + 2] = nb
    return bytes(d)

p1 = replace_in_map(1, 'Ÿ', 'Í')
print('fila 1: Ÿ -> Í')

r = font.rows[2]
p2 = bytearray(font.cf.plain(r))
h = [struct.unpack_from('<I', p2, i * 4)[0] for i in range(12)]
a, b = h[6], h[7]
s = bytes(p2[a:b])
for old, new in zip(R2_OLD, R2_NEW):
    ob, nb = old.encode('utf-8'), new.encode('utf-8')
    assert len(ob) == len(nb) == 2, (old, new)
    assert s.count(ob) == 1, ('fila 2: %r count=%d' % (old, s.count(ob)))
    i = s.index(ob)
    p2[a + i:a + i + 2] = nb
    print('fila 2: %s -> %s' % (old, new))
p2 = bytes(p2)

s2 = p2[a:h[7]].decode('utf-8', 'ignore')
for ch in R2_NEW:
    assert ch in s2, 'falta %r en fila 2' % ch
print('fila 2 verificada: %d/%d caracteres' % (len(R2_NEW), len(R2_NEW)))

# --- 3. reconstruir ----------------------------------------------------------
new = {}
for fid, data in ((1, p1), (2, p2), (3, bytes(font.p3)), (4, bytes(font.tex))):
    f = font.rows[fid]
    plain = bytes(data)
    new[fid] = (font.cf.cipher(f, plain), len(plain))
print('comprimiendo...')
open(OUT, 'wb').write(build_ordered(SRC, new))
print('escrito', OUT)
