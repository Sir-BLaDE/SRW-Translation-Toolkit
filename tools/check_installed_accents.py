import sys, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

paths = {
 'STGEST': r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/SRTools/EN/STGEST_EN.CPK',
}
import os
# find installed cpks
for root, dirs, files in os.walk(r'D:/Juegos/-SPARROW-/Super Robot Wars V'):
    for f in files:
        if f.upper() in ('STGEST_EN.CPK','CMN00_EN.CPK','CMN00.CPK','STGEST.CPK'):
            paths[f] = os.path.join(root, f)

accent_re = re.compile(r'[\u00c0-\u00ff\u00a1\u00bf]')
for label, p in paths.items():
    try:
        c = load(p)
    except Exception as e:
        print(label, 'LOAD ERR', e); continue
    total = 0; accented = 0; inv = 0; qmarks = 0
    samples = []
    for f in c.rows:
        try:
            pt = c.plain(f)
        except Exception:
            continue
        txt = pt.decode('utf-8', 'ignore')
        for m in re.finditer(r'[ -~¡¿ÁÉÍÓÚáéíóúñÑ]{8,}', txt):
            s = m.group(0)
            total += 1
            if accent_re.search(s):
                accented += 1
                if '¿' in s or '¡' in s: inv += 1
                if len(samples) < 5: samples.append(s[:70])
    print('%s: segments=%d accented=%d with¿¡=%d' % (label, total, accented, inv))
    for s in samples: print('   ', repr(s))
