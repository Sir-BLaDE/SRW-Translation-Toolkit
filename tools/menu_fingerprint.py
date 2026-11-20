# -*- coding: utf-8 -*-
"""Huella visual del menu: comparar pantalla actual con f145.png (menu manual)."""
import sys
from PIL import Image, ImageChops, ImageStat

REF = r'C:/Dev/Default Project/srwv/tools/_intro_menu_240/f145.png'
ref = Image.open(REF).convert('L').resize((160, 90))

def score(path):
    im = Image.open(path).convert('L').resize((160, 90))
    d = ImageChops.difference(ref, im)
    m = ImageStat.Stat(d).mean[0]
    return m

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print('%-45s diff=%.2f' % (p.split('\\')[-1], score(p)))
