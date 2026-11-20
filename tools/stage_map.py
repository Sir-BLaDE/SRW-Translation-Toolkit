"""stage_map.py - mapa id de entrada STGEST -> nombre de fichero Lua."""
import re

from cpk_util import load

PATH = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
LUA = re.compile(r'([A-Za-z0-9_]+\.lua)')


def build():
    c = load(PATH)
    out = {}
    for f in c.rows:
        pt = c.plain(f)
        head = pt[:3000].decode('utf-8', 'replace')
        names = LUA.findall(head)
        out[f['id']] = names[0] if names else None
    return out


def save(path='C:/Dev/Default Project/srwv/datos/stgest_entries.txt'):
    m = build()
    with open(path, 'w', encoding='utf-8') as fh:
        for k in sorted(m):
            fh.write('%d\t%s\n' % (k, m[k]))
    return m


if __name__ == '__main__':
    m = save()
    print('entradas', len(m), 'sin nombre', sum(1 for v in m.values() if not v))
    for k in sorted(m)[:20]:
        print(k, m[k])
