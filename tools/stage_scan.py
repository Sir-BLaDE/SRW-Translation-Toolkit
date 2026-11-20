"""Escanea los ficheros de STGEST_EN: identifica tipo y si contienen texto de dialogo."""
import re
import sys

from srwv_cpk import Cpk
from stage_pack import entries, extract

PATH = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'


def main():
    cpk = Cpk(PATH)
    rows = entries(cpk)
    out = []
    for f in rows:
        pt = extract(cpk, f)
        head = pt[:400].decode('utf-8', 'replace')
        m = re.search(r'FILE\s*:\s*(\S+)', head)
        name = m.group(1) if m else ''
        if not name:
            m = re.search(r'([A-Za-z0-9_]+\.lua)', head)
            name = m.group(1) if m else '?'
        # contar cadenas largas con texto y saltos de linea
        longstr = len(re.findall(rb'[\x20-\x7e]{60,}', pt))
        nl = pt.count(b'\\n')
        out.append((f['id'], f['size'], f['ex'], name, longstr, nl, len(pt)))
    with open('C:/Dev/Default Project/srwv/datos/stgest_index.txt', 'w', encoding='utf-8') as fh:
        for r in out:
            fh.write('%d\t%d\t%d\t%s\t%d\t%d\t%d\n' % r)
    print('escritos', len(out))
    # resumen por tipo
    import collections
    kinds = collections.Counter()
    for r in out:
        n = r[3]
        kind = 'other'
        for k in ('preset', 'sdemo', 'dlgev', 'stage', 'ai_', 'aie'):
            if k in n:
                kind = k
                break
        if n.endswith('.lua'):
            kind = n.split('.')[0][-6:]
        kinds[kind] += 1
    print(kinds.most_common(20))
    print('top por nº de cadenas largas:')
    for r in sorted(out, key=lambda x: -x[4])[:15]:
        print(r)
    print('top por \\\\n:')
    for r in sorted(out, key=lambda x: -x[5])[:15]:
        print(r)


if __name__ == '__main__':
    main()
