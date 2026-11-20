import sys
from PIL import Image, ImageChops

a = Image.open(sys.argv[1]).convert('RGB')
b = Image.open(sys.argv[2]).convert('RGB')
print('size', a.size, b.size)
d = ImageChops.difference(a, b)
bbox = d.getbbox()
print('bbox cambio global:', bbox)
# resumir cambios por bloques de 80x80
w, h = a.size
pa, pb = a.load(), b.load()
blocks = []
for by in range(0, h, 80):
    for bx in range(0, w, 80):
        n = 0
        for y in range(by, min(by+80, h), 4):
            for x in range(bx, min(bx+80, w), 4):
                r1, g1, b1 = pa[x, y]
                r2, g2, b2 = pb[x, y]
                if abs(r1-r2) + abs(g1-g2) + abs(b1-b2) > 60:
                    n += 1
        if n > 8:
            blocks.append((n, bx, by))
blocks.sort(reverse=True)
print('bloques con mas cambios (n, x, y):')
for n, x, y in blocks[:40]:
    print('  n=%4d  x=%4d y=%4d' % (n, x, y))
