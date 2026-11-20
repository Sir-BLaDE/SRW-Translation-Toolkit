# -*- coding: utf-8 -*-
"""Verifica el rpw_jstr traducido: offsets i2i, cadenas intactas y muestras."""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

ORIG = r"C:/Dev/Default Project/srwv/backup/rpw_jstr_original.cpk"
NEW = r"C:/Dev/Default Project/srwv/outputs/rpw_jstr_es.cpk"
TM = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"

POOL = 0x48


def pool_of(pt):
    """Pool: cadenas NUL hasta el primer '<chunk-foot>'."""
    end = pt.find(b"<chunk-foot>", POOL)
    assert end > 0
    out = []
    pos = POOL
    while pos < end:
        z = pt.find(b"\0", pos)
        assert z >= 0
        out.append((pos - POOL, pt[pos:z]))
        pos = z + 1
    assert pos == end, (pos, end)
    return out


def i2i_of(pt, start):
    # localizar chunk jstr-i2i
    p = pt.find(b"jstr-i2i")
    assert p > 0
    data = p + 16  # name(8) + next(4) + len(4)
    ln = struct.unpack_from("<I", pt, p + 12)[0]
    n = ln // 8
    return [struct.unpack_from("<2I", pt, data + i * 8) for i in range(n)], data


def main():
    a = load(ORIG)
    b = load(NEW)
    pa = a.plain(a.rows[0])
    pb = b.plain(b.rows[0])
    print("len original %d | nuevo %d | ExtractSize %d"
          % (len(pa), len(pb), b.rows[0]["ex"]))
    assert b.rows[0]["ex"] == len(pb)

    # cabecera
    assert pa[:0x20] == pb[:0x20], "cabecera distinta"
    total, foot = struct.unpack_from("<2I", pb, 0x20)
    print("total-4 %d (real %d) | footer %d" % (total, len(pb) - 4, foot))
    assert total == len(pb) - 4
    assert foot < len(pb)

    sa = pool_of(pa)
    sb = pool_of(pb)
    print("cadenas pool: %d -> %d" % (len(sa), len(sb)))
    assert len(sa) == len(sb)

    # todas las cadenas deben ser o la original o la traduccion
    tm = json.load(io.open(TM, encoding="utf-8"))
    changed = same = other = 0
    for (_, ra), (_, rb) in zip(sa, sb):
        if ra == rb:
            same += 1
        else:
            s = ra.decode("utf-8")
            if s in tm and tm[s].encode("utf-8") == rb:
                changed += 1
            else:
                other += 1
                if other < 6:
                    print("  CAMBIO INESPERADO:", repr(s[:60]), "->", repr(rb[:60]))
    print("intactas %d | traducidas %d | inesperadas %d" % (same, changed, other))
    assert other == 0

    # i2i
    ia, offa = i2i_of(pa, 0)
    ib, offb = i2i_of(pb, 0)
    print("i2i entradas %d -> %d | offset tabla %d -> %d"
          % (len(ia), len(ib), offa, offb))
    assert len(ia) == len(ib)

    starts = set(o for o, _ in sb)
    bad = sum(1 for _, o in ib if o not in starts)
    print("offsets i2i invalidos:", bad)
    assert bad == 0

    # misma cadena destino antes y despues
    mapa = {o: r for o, r in sa}
    mapb = {o: r for o, r in sb}
    diff = 0
    for (idx, oa), (idx2, ob) in zip(ia, ib):
        assert idx == idx2
        if mapa[oa] != mapb[ob]:
            diff += 1
    print("entradas i2i cuyo texto cambia:", diff)

    # muestras
    print("\n-- muestras --")
    for s in ["Great Mazinger", "Destiny Gundam", "Unicorn Gundam",
              "Beam Rifle", "Funnel", "Newtype LV1", "AAM-4 Murasame"]:
        enc = s.encode("utf-8")
        hit = [r for _, r in sb if r == enc]
        print("  %-22s presente=%s" % (s, bool(hit)))
    for es in ["Rifle de haz", "Funnel", "Newtype NV1", "Comandante NV1"]:
        hit = [r for _, r in sb if r == es.encode("utf-8")]
        print("  ES %-20s presente=%s" % (es, bool(hit)))

    # duplicados exactos del mapa aplicados
    print("\nOK")


if __name__ == "__main__":
    main()
