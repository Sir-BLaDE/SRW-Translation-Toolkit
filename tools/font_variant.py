"""font_variant.py - Genera variantes del parche de fuente para aislar que cambio
hace crashear el juego.

  python font_variant.py tex    -> solo textura (glifos con registro existente)
  python font_variant.py ids    -> textura + 7 registros reapuntados
  python font_variant.py all    -> textura + registros + mapa (completo)
"""
import sys

import font_patch as fp
from srwv_cpkbuild2 import build_ordered


def save(font, out, ids=(1, 3, 4)):
    new = {}
    for fid in ids:
        f = font.rows[fid]
        plain = bytes(font.parts[fid])
        new[fid] = (font.cf.cipher(f, plain), len(plain))
    blob = build_ordered(fp.GAME, new)
    open(out, 'wb').write(blob)
    print('escrito', len(blob), '->', out, '| reencode:', ids)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    font = fp.Font(fp.GAME)
    font.parts = {1: font.p1, 3: font.p3, 4: font.tex}

    if mode.startswith('repack'):
        sub = mode[6:]
        ids = {'': (1, 3, 4), '1': (1,), '3': (3,), '4': (4,)}[sub]
        print('modo repack: contenido identico, solo recomprimir', ids)
        save(font, 'C:/Dev/Default Project/srwv/outputs/FontInfo_variant_%s.cpk' % mode, ids)
        return

    do_tex = True
    do_ids = mode in ('ids', 'all')
    do_map = mode == 'all'

    targets = {}
    reuse_iter = iter(fp.REUSE)
    for ch, base, kind in fp.GLYPHS:
        g = font.byc.get(ord(ch))
        if g is not None:
            targets[ch] = (g, ord(ch))
        elif do_ids:
            cp = next(reuse_iter)
            targets[ch] = (font.byc[cp], cp)

    print('modo', mode, '| glifos a pintar:', ''.join(targets))

    for ch, base, kind in fp.GLYPHS:
        if ch not in targets:
            continue
        g, src = targets[ch]
        img = fp.compose(font, base, kind)
        bb = font.ink_bbox(img)
        font.put(g, img)
        uid, fl = font.rec(g)
        fl[7] = float(bb[2] + 1)
        if do_ids:
            font.write_rec(g, ord(ch), fl)
        else:
            font.write_rec(g, uid, fl)

    if do_map:
        p1 = bytes(font.p1)
        for old_cp, new_cp in zip(fp.MAP_REMOVE, fp.MAP_ADD):
            ob = chr(old_cp).encode('utf-8')
            nb = chr(new_cp).encode('utf-8')
            i = p1.index(ob)
            p1 = p1[:i] + nb + p1[i + 2:]
        font.parts[1] = bytearray(p1)
        print('mapa parcheado')

    save(font, 'C:/Dev/Default Project/srwv/outputs/FontInfo_variant_%s.cpk' % mode)


if __name__ == '__main__':
    main()
