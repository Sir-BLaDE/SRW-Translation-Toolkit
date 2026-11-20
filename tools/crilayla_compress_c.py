# -*- coding: utf-8 -*-
"""Port exacto del compresor CRILAYLA de LibCRIComp/hacktools (cmp_cri.c)."""
import struct

MAGIC = b"CRILAYLA"
PREFIX_SIZE = 0x100


def compress(data):
    src = data
    srclen = len(src)
    if srclen < PREFIX_SIZE:
        raise ValueError("CRILAYLA: se necesitan al menos 0x100 bytes")

    # El compresor original usa un buffer del tamano del original y puede
    # desbordar si los datos no comprimen; damos margen para evitarlo.
    buflen = srclen * 2 + 0x100
    dest = bytearray(buflen)
    n = srclen - 1
    m = buflen - 1
    d = 0
    T = 0

    while n >= PREFIX_SIZE:
        j = n + 3 + 0x2000
        if j > srclen:
            j = srclen
        p = 0
        q = 0
        for i in range(n + 3, j):
            k = 0
            limit = n - PREFIX_SIZE
            while k <= limit and src[n - k] == src[i - k]:
                k += 1
            if k > p:
                q = i - n - 3
                p = k

        if p < 3:
            d = (d << 9) | src[n]
            n -= 1
            T += 9
        else:
            d = (((d << 1) | 1) << 13) | q
            T += 14
            n -= p
            if p < 6:
                d = (d << 2) | (p - 3)
                T += 2
            elif p < 13:
                d = (((d << 2) | 3) << 3) | (p - 6)
                T += 5
            elif p < 44:
                d = (((d << 5) | 0x1F) << 5) | (p - 13)
                T += 10
            else:
                d = (d << 10) | 0x3FF
                T += 10
                p -= 44
                while True:
                    while T >= 8:
                        dest[m] = (d >> (T - 8)) & 0xFF
                        m -= 1
                        T -= 8
                        d &= (1 << T) - 1 if T else 0
                    if p < 255:
                        break
                    d = (d << 8) | 0xFF
                    T += 8
                    p -= 0xFF
                d = (d << 8) | p
                T += 8

        while T >= 8:
            dest[m] = (d >> (T - 8)) & 0xFF
            m -= 1
            T -= 8
            d &= (1 << T) - 1 if T else 0

    if T != 0:
        dest[m] = (d << (8 - T)) & 0xFF
        m -= 1
    dest[m] = 0
    m -= 1
    dest[m] = 0
    while (buflen - m) & 3:
        dest[m] = 0
        m -= 1

    payload = bytes(dest[m:])
    comp_size = len(payload)
    out = bytearray(MAGIC)
    out += struct.pack("<II", srclen - PREFIX_SIZE, comp_size)
    out += payload
    out += src[:PREFIX_SIZE]
    return bytes(out)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
    from cpk_util import load
    from crilayla import maybe_decompress

    for name, path, fid in [
        ("SysText", r"C:/Dev/Default Project/srwv/backup/SysText_antes_es.cpk", 2),
        ("KPACK_LN", r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk", 3),
    ]:
        cf = load(path)
        row = [x for x in cf.rows if x["id"] == fid][0]
        orig_raw = cf.raw(row)
        plain = cf.plain(row)
        mine = compress(plain)
        print(name, "orig", len(orig_raw), "mine", len(mine),
              "identico", mine == orig_raw,
              "roundtrip", maybe_decompress(mine) == plain)
