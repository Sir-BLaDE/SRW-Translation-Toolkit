"""overflow_audit.py - mide el ancho aproximado en pixeles de las cadenas
traducidas frente a las originales usando los avances reales de la fuente.
Detecta textos que probablemente se salen de su cuadro.
"""
import sys, os, re, struct, json, csv, pathlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

FONT = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(FONT); rows = {r['id']: r for r in cf.rows}
p3 = cf.plain(rows[3]); HDR = 40; W = 4096; N = (len(p3) - HDR) // 36
adv = {}
for g in range(N):
    off = HDR + g * 36
    u = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    adv.setdefault(u, fl[5])

CTRL = re.compile(r'\\c\d|\\a\d\d|\\n|\\r\\n|\$[A-Za-z]\w*|%[ds]|\【[^\】]*\】|「|」')
def clean(s):
    s = CTRL.sub('', s)
    return s
def line_width(s):
    s = clean(s)
    parts = re.split(r'\r?\n|\\n|\\r\\n|\n', s)
    return max((sum(adv.get(ord(c), 20.0) for c in p) for p in parts), default=0)
def ratio(en, es):
    a = line_width(en)
    return (line_width(es) / a) if a else 99

def report(name, pairs, limit=25, thr=1.12):
    bad = []
    for en, es, key in pairs:
        if not es or es == en: continue
        r = ratio(en, es)
        if r > thr or line_width(es) > 640:
            bad.append((r, key, en, es))
    bad.sort(reverse=True, key=lambda x: x[0])
    print('\n=== %s === pares=%d sospechosos=%d' % (name, len(pairs), len(bad)))
    for r, key, en, es in bad[:limit]:
        print('  %.2f [%s]' % (r, key))
        print('    EN %r' % en[:100])
        print('    ES %r' % es[:100])
    return bad

# ---- batalla ---------------------------------------------------------------
pairs = []
with open(r'C:/Dev/Default Project/srwv/datos/lineas_batalla.csv', encoding='utf-8-sig', newline='') as f:
    for row in csv.DictReader(f):
        pairs.append((row['en'], row['es'], row['id']))
report('BATTLE', pairs, 30)

# ---- systext ---------------------------------------------------------------
pairs = []
for p in [r'C:/Dev/Default Project/srwv/datos/systext_es_1.json',
          r'C:/Dev/Default Project/srwv/datos/systext_es_2.json']:
    if not os.path.exists(p): continue
    d = json.load(open(p, encoding='utf-8'))
    if isinstance(d, dict):
        for k, v in d.items():
            pairs.append((str(k), str(v), str(k)))
report('SYSTEXT(json)', pairs, 20)

# ---- mtzkn -----------------------------------------------------------------
for name, enp, esp in [
    ('MTZKN_PT', r'datos/mtzkn_pt_en.json', r'datos/mtzkn_pt_es.json'),
    ('MTZKN_RT', r'datos/mtzkn_rt_en.json', r'datos/mtzkn_rt_es.json'),
    ('MTZKN_NM', r'datos/mtzkn_nm_en.json', r'datos/mtzkn_nm_es.json'),
]:
    ep = r'C:/Dev/Default Project/srwv/' + enp
    sp = r'C:/Dev/Default Project/srwv/' + esp
    if not (os.path.exists(ep) and os.path.exists(sp)): continue
    en = json.load(open(ep, encoding='utf-8')); es = json.load(open(sp, encoding='utf-8'))
    pairs = []
    def walk(a, b, k=''):
        if isinstance(a, dict) and isinstance(b, dict):
            for kk in a:
                if kk in b: walk(a[kk], b[kk], k + '/' + str(kk))
        elif isinstance(a, list) and isinstance(b, list):
            for i, (x, y) in enumerate(zip(a, b)): walk(x, y, k + '/%d' % i)
        elif isinstance(a, str) and isinstance(b, str):
            pairs.append((a, b, k))
    walk(en, es)
    report(name, pairs, 15)
