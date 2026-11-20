import glob
import json
import os

BATCHES = 'C:/Dev/Default Project/srwv/datos/es_batches'

fixed = 0
for p in sorted(glob.glob(BATCHES + '/*.json')):
    with open(p, encoding='utf-8') as fh:
        d = json.load(fh)
    changed = False
    for k, v in d.items():
        if not isinstance(v, str):
            continue
        if '\\r' in v or '\\n' in v:
            nv = v.replace('\\r\\n', '\r\n').replace('\\n', '\n')
            if nv != v:
                d[k] = nv
                changed = True
    if changed:
        with open(p, 'w', encoding='utf-8') as fh:
            json.dump(d, fh, ensure_ascii=False, indent=0)
        fixed += 1
        print('fijado', os.path.basename(p))

print('total fijados:', fixed)
