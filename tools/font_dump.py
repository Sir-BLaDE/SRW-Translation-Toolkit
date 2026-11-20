"""font_dump.py - Vuelca la fuente EN con el header de metricas CORRECTO (40 bytes)
para obtener la verdad sobre: mapa de caracteres, registro de metricas, y posiciones
de los glifos clave. Sirve para disenar el parche de acentos con datos fiables."""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)

W = H = 4096

# ---- id1: BLTUJAPN ----
f1 = [r for r in cf.rows if r['id'] == 1][0]
p1 = cf.plain(f1)
fixoff = struct.unpack_from('<I', p1, 0x18)[0]
end = struct.unpack_from('<I', p1, 0x1C)[0]
i = fixoff
groups = []
while i < end:
    j = p1.index(b'\x00', i)
    groups.append(p1[i:j].decode('utf-8', 'replace'))
    i = j + 1
# grupos: [0] es "Fix" (marcador)
assert groups[0] == 'Fix', groups[0]
char_groups = groups[1:]           # 20 grupos reales
full = ''.join(char_groups)        # lista de caracteres en orden de glifo
print('JAPN: %d grupos, %d codepoints (sin Fix)' % (len(char_groups), len(full)))

def gidx(ch):
    return full.index(ch)

# ---- id3: metricas (header 40, registros 36) ----
f3 = [r for r in cf.rows if r['id'] == 3][0]
met = cf.plain(f3)
HDR = 40
nrec = (len(met) - HDR) // 36
print('metricas: len=%d HDR=%d nrec=%d' % (len(met), HDR, nrec))

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', met, off)[0]
    fl = struct.unpack_from('<8f', met, off + 4)
    return u32, fl  # fl = (x, y, w, h, f5, f6, f7, f8)

# ---- textura ----
f4 = [r for r in cf.rows if r['id'] == 4][0]
tex = cf.plain(f4)

def show(g, flip=False):
    u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W)
    w = max(1, int(fl[2] * W)); h = max(1, int(fl[3] * W))
    rows = []
    for yy in range(0, h, 2):
        yy2 = (H - y - h + yy) if flip else (y + yy)
        row = tex[yy2 * W + x: yy2 * W + x + w]
        rows.append(''.join('#' if b > 128 else ('.' if b > 0 else ' ') for b in row))
    return u32, x, y, w, h, rows

def ascii_art(rows):
    return '\n'.join(rows)

# ---- caracteres clave ----
keys = ['0', 'a', 'e', 'i', 'o', 'u', 'n', 'A', 'O', 'U', 'é', 'É', '´', '~',
        'á', 'í', 'ó', 'ú', 'ñ', 'Á', 'Ó', 'Ú', 'ü', '¿', '¡', '«', '»']
print('\n=== mapa: caracter -> indice glifo ===')
for ch in keys:
    if ch in full:
        print('  %r -> glifo %d' % (ch, gidx(ch)))
    else:
        print('  %r -> FALTA' % ch)

print('\n=== registros de metricas de caracteres clave (sin flip) ===')
for ch in ['0', 'a', 'e', 'i', 'o', 'u', 'n', 'A', 'O', 'U', 'é', 'É', '´', '~']:
    g = gidx(ch)
    u32, fl = rec(g)
    print('glifo %d (%r): id=%d x=%d y=%d w=%d h=%d f5=%g f6=%g f7=%g f8=%g'
          % (g, ch, u32, int(fl[0]*W), int(fl[1]*W), int(fl[2]*W), int(fl[3]*W),
             fl[4], fl[5], fl[6], fl[7]))

print('\n=== render de glifo 0 (0), 11 (a), 851 (e), 852 (E) ===')
for ch in ['0', 'a', 'é', 'É']:
    g = gidx(ch)
    u32, x, y, w, h, rows = show(g)
    print('--- glifo %d (%r) pos (%d,%d) ---' % (g, ch, x, y))
    print(ascii_art(rows))
    print()

# patron de IDs
print('=== primeros 20 IDs de registro ===')
for g in range(20):
    u32, fl = rec(g)
    print('  g%03d id=%d' % (g, u32))

print('=== ultimos 20 IDs ===')
for g in range(nrec - 20, nrec):
    u32, fl = rec(g)
    print('  g%03d id=%d' % (g, u32))
