"""font_patch.py - Sintetiza los glifos acentuados que faltan en la fuente EN y
parchea FontInfo.cpk (mapa de caracteres + metricas + textura).

Estrategia sin cambiar tamanos:
  * Textura : se repintan las cajas 40x44 de los registros ya existentes
              (que contenian un cuadrado de relleno 6x6).
  * Metricas: 7 registros de relleno no usados se reapuntan a los codepoints
              nuevos (solo cambia el u32 del id y el ancho de tinta fl[7]).
  * Mapa    : se sustituyen 7 caracteres de 2 bytes no usados por los nuevos,
              en el sitio -> los offsets de la tabla no cambian.

Uso:  python font_patch.py [--dry]
Salida: outputs/FontInfo_es.cpk
"""
import math
import os
import struct
import sys

from PIL import Image, ImageDraw

from cpk_util import load
from srwv_cpkbuild2 import build_ordered

GAME = os.environ.get('SRW_FONT_IN', 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')
OUT = os.environ.get('SRW_FONT_OUT', 'C:/Dev/Default Project/srwv/outputs/FontInfo_es.cpk')
PREV = os.environ.get('SRW_FONT_PREV', 'C:/Dev/Default Project/srwv/tools/_font_render')
W = 4096
HDR = 40
BASELINE = 32
XHEIGHT = 12          # fila superior de las minusculas
CAPTOP = 4            # fila superior de las mayusculas

# --- definicion de los glifos a sintetizar ---------------------------------
# (destino, base, tipo)   tipo: acc_l / tilde_l / dia_l / acc_u / dia_u / inv
GLYPHS = [
    ('\u00e1', 'a', 'acc_l'),   # á
    ('\u00e9', 'e', 'acc_l'),   # é
    ('\u00ed', 'i', 'acc_l'),   # í   (se le quita el punto)
    ('\u00f3', 'o', 'acc_l'),   # ó
    ('\u00fa', 'u', 'acc_l'),   # ú
    ('\u00f1', 'n', 'tilde_l'),  # ñ
    ('\u00c1', 'A', 'acc_u'),   # Á
    ('\u00c9', 'E', 'acc_u'),   # É
    ('\u00d3', 'O', 'acc_u'),   # Ó
    ('\u00da', 'U', 'acc_u'),   # Ú
    ('\u00fc', 'u', 'dia_l'),   # ü
    ('\u00a1', '!', 'invl'),    # ¡  (voltear !)
    ('\u00bf', '?', 'invl'),    # ¿  (voltear ?)
]

# codepoints nuevos que no tienen registro: se reapuntan estos (2 bytes, no usados)
REUSE = [0xE0, 0xE8, 0xF9, 0xE2, 0xEA, 0xEB, 0xEF]   # à è ù â ê ë ï
NEW = [0xE1, 0xED, 0xFA, 0xF1, 0xC1, 0xD3, 0xDA]      # á í ú ñ Á Ó Ú

# mapa de caracteres: se sustituyen estos (todos de 2 bytes) por los necesarios.
# ó ya tiene registro pero no estaba en el mapa, asi que es una sustitucion extra.
MAP_REMOVE = REUSE + [0xFF]                            # ... + ÿ
MAP_ADD = NEW + [0xF3]                                 # ... + ó

if os.environ.get('SRW_GAME', 'V').upper() == 'X':
    # SRW X: é É ü ¡ ¿ tienen registro (relleno) y estan en el mapa; faltan 10.
    GLYPHS = GLYPHS + [('\u00cd', 'I', 'acc_u'), ('\u00d1', 'N', 'tilde_u')]
    NEW = [0xE1, 0xED, 0xF3, 0xFA, 0xF1, 0xC1, 0xCD, 0xD3, 0xDA, 0xD1]  # á í ó ú ñ Á Í Ó Ú Ñ
    REUSE = [0xE0, 0xE8, 0xF9, 0xE2, 0xEA, 0xEB, 0xEF, 0xEE, 0xF4, 0xFB]  # à è ù â ê ë ï î ô û
    MAP_REMOVE = REUSE
    MAP_ADD = NEW


class Font:
    def __init__(self, path):
        self.cf = load(path)
        self.rows = {r['id']: r for r in self.cf.rows}
        self.p1 = bytearray(self.cf.plain(self.rows[1]))
        self.p3 = bytearray(self.cf.plain(self.rows[3]))
        self.tex = bytearray(self.cf.plain(self.rows[4]))
        self.n = (len(self.p3) - HDR) // 36
        self.byc = {}
        for g in range(self.n):
            u = struct.unpack_from('<I', self.p3, HDR + g * 36)[0]
            self.byc.setdefault(u, g)

    # --- acceso a registros
    def rec(self, g):
        off = HDR + g * 36
        uid = struct.unpack_from('<I', self.p3, off)[0]
        fl = list(struct.unpack_from('<8f', self.p3, off + 4))
        return uid, fl

    def write_rec(self, g, uid, fl):
        off = HDR + g * 36
        struct.pack_into('<I', self.p3, off, uid)
        struct.pack_into('<8f', self.p3, off + 4, *fl)

    def rec_of(self, ch):
        g = self.byc.get(ord(ch))
        if g is None:
            raise KeyError('sin registro para %r U+%04X' % (ch, ord(ch)))
        return g

    def box(self, g):
        _, fl = self.rec(g)
        x = int(round(fl[0] * W)); y = int(round(fl[1] * W))
        w = int(round(fl[2] * W)); h = int(round(fl[3] * W))
        return x, y, w, h

    # --- pixeles
    def get(self, g):
        x, y, w, h = self.box(g)
        data = bytearray()
        for yy in range(h):
            base = (y + yy) * W + x
            data += self.tex[base:base + w]
        return Image.frombytes('L', (w, h), bytes(data))

    def put(self, g, img):
        x, y, w, h = self.box(g)
        if img.size != (w, h):
            img = img.resize((w, h))
        d = img.tobytes()
        for yy in range(h):
            base = (y + yy) * W + x
            self.tex[base:base + w] = d[yy * w:(yy + 1) * w]

    def ink_w(self, g):
        _, fl = self.rec(g)
        return int(round(fl[7]))

    def ink_bbox(self, img):
        mnx = mny = 10 ** 9
        mxx = mxy = -1
        px = img.load()
        for yy in range(img.height):
            for xx in range(img.width):
                if px[xx, yy]:
                    mnx = min(mnx, xx); mxx = max(mxx, xx)
                    mny = min(mny, yy); mxy = max(mxy, yy)
        if mxx < 0:
            return None
        return mnx, mny, mxx, mxy


def cx_of(w):
    return (w - 1) / 2.0


def draw_acute(d, cx, top, bottom, thick=3, slope=0.6):
    """Trazo inclinado de `bottom` a `top`."""
    n = bottom - top + 1
    for i in range(n):
        r = bottom - i
        x0 = int(round(cx - 4 + i * slope))
        d.rectangle([x0, r, x0 + thick - 1, r], fill=255)


def draw_tilde(d, cx, top, width=14, amp=2.0, thick=3):
    # onda completa (~): sube a la izquierda y baja a la derecha
    for i in range(width):
        t = i / float(width - 1)
        yc = top + amp - amp * math.sin(2 * math.pi * t)
        y0 = int(round(yc))
        d.rectangle([int(cx - width / 2) + i, y0, int(cx - width / 2) + i, y0 + thick - 1], fill=255)


def draw_dia(d, cx, top, size=3, gap=3):
    half = gap / 2.0 + size / 2.0
    for sgn in (-1, 1):
        x0 = int(round(cx + sgn * half - size / 2.0))
        d.rectangle([x0, top, x0 + size - 1, top + size - 1], fill=255)


def compose(font, base_ch, kind):
    gb = font.rec_of(base_ch)
    base = font.get(gb).copy()
    iw = font.ink_w(gb)
    cx = cx_of(iw)

    if kind in ('acc_l', 'tilde_l', 'dia_l'):
        img = base
        if kind == 'acc_l':
            if base_ch == 'i':
                # quitar el punto: filas 3..9 a cero
                d0 = ImageDraw.Draw(img)
                d0.rectangle([0, 3, img.width - 1, 9], fill=0)
        d = ImageDraw.Draw(img)
        if kind == 'acc_l':
            if base_ch == 'i':
                draw_acute(d, cx, 1, 9)
            else:
                draw_acute(d, cx, 2, 10)
        elif kind == 'tilde_l':
            draw_tilde(d, cx, 3)
        else:
            draw_dia(d, cx, 3)
        return img

    if kind in ('acc_u', 'dia_u', 'tilde_u'):
        hgt = BASELINE - CAPTOP + 1          # 29
        newh = 24
        crop = base.crop((0, CAPTOP, base.width, BASELINE + 1))
        crop = crop.resize((base.width, newh), Image.LANCZOS)
        px = crop.load()
        for yy in range(newh):
            for xx in range(crop.width):
                px[xx, yy] = 255 if px[xx, yy] >= 110 else 0
        img = Image.new('L', base.size, 0)
        img.paste(crop, (0, BASELINE - newh + 1))
        d = ImageDraw.Draw(img)
        if kind == 'acc_u':
            draw_acute(d, cx, 0, 6, thick=3, slope=0.55)
        elif kind == 'tilde_u':
            draw_tilde(d, cx, 1)
        else:
            draw_dia(d, cx, 0, size=3, gap=3)
        return img

    if kind == 'invl':
        # girar 180 grados (no solo voltear) y recolocar la tinta donde estaba la del original
        bb = font.ink_bbox(base)
        rot = base.transpose(Image.ROTATE_180)
        rb = font.ink_bbox(rot)
        out = Image.new('L', base.size, 0)
        out.paste(rot.crop((rb[0], rb[1], rb[2] + 1, rb[3] + 1)), (bb[0], bb[1]))
        return out

    raise ValueError(kind)


def main():
    dry = '--dry' in sys.argv
    font = Font(GAME)
    print('registros:', font.n, '| chars en mapa:', len(set(font.p1[48:].decode('utf-8', 'ignore'))))

    # comprobar que los codepoints a reutilizar son relleno
    for cp in REUSE:
        g = font.byc.get(cp)
        if g is None:
            raise SystemExit('U+%04X no tiene registro' % cp)
        bb = font.ink_bbox(font.get(g))
        if bb != (0, 15, 5, 20):
            raise SystemExit('U+%04X no es relleno: %s' % (cp, bb))
    print('rellenos verificados:', ['U+%04X' % c for c in REUSE])

    # mapa: comprobar que los caracteres a sustituir estan presentes
    mapstr = font.p1[48:].decode('utf-8', 'ignore')
    for cp in MAP_REMOVE:
        ch = chr(cp)
        if mapstr.count(ch) != 1:
            raise SystemExit('mapa: %r aparece %d veces' % (ch, mapstr.count(ch)))
    print('mapa: los %d caracteres a quitar aparecen 1 vez cada uno' % len(MAP_REMOVE))

    # destinos: los que ya tienen registro + los reutilizados
    targets = {}
    reuse_iter = iter(REUSE)
    for ch, base, kind in GLYPHS:
        g = font.byc.get(ord(ch))
        if g is None:
            cp = next(reuse_iter)
            g = font.byc[cp]
            targets[ch] = (g, cp)
        else:
            targets[ch] = (g, ord(ch))
    print('destinos:', {ch: 'g%d (de U+%04X)' % v for ch, v in targets.items()})

    # pintar glifos
    for ch, base, kind in GLYPHS:
        g, src_cp = targets[ch]
        img = compose(font, base, kind)
        bb = font.ink_bbox(img)
        font.put(g, img)
        uid, fl = font.rec(g)
        fl[7] = float(bb[2] + 1)          # ancho de tinta
        # metricas horizontales (fl[4]=avance izq., fl[5]=avance total) de la letra base;
        # los registros de relleno traen 7/20 y descolocan el glifo
        _, bfl = font.rec(font.rec_of(base))
        fl[4], fl[5] = bfl[4], bfl[5]
        font.write_rec(g, ord(ch), fl)
        print('  %r U+%04X g=%4d base=%r tipo=%-7s ink=%s ancho=%.0f'
              % (ch, ord(ch), g, base, kind, bb, fl[7]))

    # verificar que no queda ningun relleno en los destinos
    for ch, (g, src_cp) in targets.items():
        bb = font.ink_bbox(font.get(g))
        if bb == (0, 15, 5, 20):
            raise SystemExit('%r sigue siendo relleno' % ch)

    # mapa: sustitucion en sitio (2 bytes -> 2 bytes)
    p1 = bytes(font.p1)
    for old_cp, new_cp in zip(MAP_REMOVE, MAP_ADD):
        ob = chr(old_cp).encode('utf-8')
        nb = chr(new_cp).encode('utf-8')
        assert len(ob) == len(nb) == 2
        i = p1.index(ob)
        p1 = p1[:i] + nb + p1[i + 2:]
    font.p1 = bytearray(p1)
    print('mapa parcheado: nuevos', ['U+%04X' % c for c in MAP_ADD])

    mapstr2 = font.p1[48:].decode('utf-8', 'ignore')
    for cp in MAP_ADD:
        assert chr(cp) in mapstr2, 'no se anadio U+%04X' % cp
    print('verificado: los %d nuevos estan en el mapa' % len(MAP_ADD))

    # guardar preview
    os.makedirs(PREV, exist_ok=True)
    tiles = []
    for ch, base, kind in GLYPHS:
        g, _ = targets[ch]
        tiles.append(font.get(g).resize((40 * 4, 44 * 4), Image.NEAREST))
    sheet = Image.new('L', (7 * 168, ((len(tiles) + 6) // 7) * 184), 24)
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 7) * 168, (i // 7) * 184))
    sheet.save(PREV + '/nuevos_glifos.png')
    print('preview ->', PREV + '/nuevos_glifos.png')

    if dry:
        print('(--dry: no se escribe nada)')
        return

    # reconstruir CPK
    new = {}
    for fid, data in ((1, font.p1), (3, font.p3), (4, font.tex)):
        f = font.rows[fid]
        plain = bytes(data)
        new[fid] = (font.cf.cipher(f, plain), len(plain))
    print('comprimiendo...')
    out = build_ordered(GAME, new)
    open(OUT, 'wb').write(out)
    print('escrito', len(out), 'bytes ->', OUT)


if __name__ == '__main__':
    main()
