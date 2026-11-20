"""font_map2.py - Decodifica la tabla de grupos de BLTUJAPN (id1) y BLTULATN (id2)."""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
rows = {r['id']: r for r in cf.rows}


def dump_map(fid):
    pt = cf.plain(rows[fid])
    magic = pt[:8]
    ver = struct.unpack_from('<I', pt, 8)[0]
    a, b, c, ngroups, e, f = struct.unpack_from('<6I', pt, 32)
    print('==== id%d %s ver=%d  fields(32..56)=%s ====' % (fid, magic, ver, (a, b, c, ngroups, e, f)))
    print('   len =', len(pt))
    # region entre 56 y a: cabecera de strings?
    print('   bytes 56..a:', pt[56:a].hex())
    print('   strings area %d..%d:' % (a, b), pt[a:min(a + 120, b)])
    offs = struct.unpack_from('<%dI' % ngroups, pt, c)
    print('   tabla de grupos en %d: %s' % (c, offs))
    print('   bytes tras la tabla (%d..%d): %s' % (c + 4 * ngroups, len(pt), pt[c + 4 * ngroups:].hex()))
    end_strings = b
    for i, o in enumerate(offs):
        e0 = pt.index(b'\x00', o)
        raw = pt[o:e0]
        try:
            s = raw.decode('utf-8')
        except UnicodeDecodeError:
            s = raw.decode('utf-8', 'replace')
        print('   grupo %2d @%4d..%4d (%3d B): %r' % (i, o, e0, len(raw), s))
    print('   fin zona strings (b) =', b, ' bytes b..c:', pt[b:c].hex())
    print()


dump_map(1)
dump_map(2)
