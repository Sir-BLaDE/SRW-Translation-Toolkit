"""font_render.py - Renderiza los 8 glifos acentuados que faltan (á í ó ú ñ Á Ó Ú)
componiendo las letras base + el acento agudo (de 'é') / tilde (~), y los guarda
como PNG para verificacion visual."""
from cpk_util import load
import struct, os
from PIL import Image

cf = load('D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')
f4 = [r for r in cf.rows if r['id'] == 4][0]
tex = cf.plain(f4)
f3 = [r for r in cf.rows if r['id'] == 3][0]
met = cf.plain(f3)
W = 4096

def gm(g):
    return struct.unpack_from('<9f', met, 24 + g * 36)

def region(x, y, w, h):
    return b''.join(tex[(y + yy) * W + x:(y + yy) * W + x + w] for yy in range(h))

# mapa char->indice (sin el marcador 'Fix')
f1 = [r for r in cf.rows if r['id'] == 1][0]
p1 = cf.plain(f1)
fixoff = struct.unpack_from('<I', p1, 0x18)[0]
end = struct.unpack_from('<I', p1, 0x1C)[0]
i = fixoff
chars = []
while i < end:
    j = p1.index(b'\x00', i)
    chars.append(p1[i:j].decode('utf-8', 'replace'))
    i = j + 1
if chars and chars[0] == 'Fix':
    chars = chars[1:]
full = ''.join(chars)

def gidx(ch):
    return full.index(ch)

def glyph_px(ch):
    f = gm(gidx(ch))
    x = int(f[5] * W); y = int(f[6] * W); w = max(1, int(f[7] * W)); h = max(1, int(f[8] * W))
    return region(x, y, w, h), w, h

# extraer 'e' y 'é' para obtener la mascara del acento agudo
e_px, w, h = glyph_px('e')
eacute_px, _, _ = glyph_px('é')
# mascara: pixeles de 'é' que no estan en 'e' (el acento)
accent_mask = bytes((0 if eacute_px[k] <= e_px[k] else eacute_px[k]) for k in range(w * h))

outdir = 'C:/Dev/Default Project/srwv/tools/_font_render'
os.makedirs(outdir, exist_ok=True)

def compose(base_ch, accent_bytes):
    base, w, h = glyph_px(base_ch)
    out = bytearray(base)
    for k in range(w * h):
        if accent_bytes[k]:
            out[k] = max(out[k], accent_bytes[k])
    return bytes(out), w, h

# tilde: extraer '~'
tilde_px, w, h = glyph_px('~')

targets = {'á': ('a', accent_mask), 'í': ('i', accent_mask), 'ó': ('o', accent_mask),
           'ú': ('u', accent_mask), 'Á': ('A', accent_mask), 'Ó': ('O', accent_mask),
           'Ú': ('U', accent_mask), 'ñ': ('n', tilde_px)}

for name, (base, acc) in targets.items():
    px, w, h = compose(base, acc)
    img = Image.frombytes('L', (w, h), px)
    img.save(os.path.join(outdir, name + '.png'))
    print('render', name, 'de', base, 'ok', w, h)

# tambien guardar las letras base y acento para comparar
for ch in ['a', 'e', 'é', '´', '~']:
    px, w, h = glyph_px(ch)
    Image.frombytes('L', (w, h), px).save(os.path.join(outdir, '_' + ch + '.png'))
print('listo ->', outdir)
