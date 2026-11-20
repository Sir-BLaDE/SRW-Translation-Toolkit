"""font_jp.py - Inspecciona FontInfo.cpk de JP: tamano de textura, registros y
localiza los glifos acentuados reales (si existen)."""
from cpk_util import load
import struct
from PIL import Image

for lang in ('JP', 'EN'):
    cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/%s/FontInfo.cpk' % lang
    cf = load(cpk)
    print('==== %s ====' % lang)
    for r in cf.rows:
        try:
            pt = cf.plain(r)
            print('  id', r['id'], 'plain', len(pt), 'extract', r.get('extract_size'))
        except Exception as e:
            print('  id', r['id'], 'ERROR', e)
