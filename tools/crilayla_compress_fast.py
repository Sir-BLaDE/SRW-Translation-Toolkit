# -*- coding: utf-8 -*-
"""Compresor CRILAYLA rapido, byte-identico al port de LibCRIComp.

Busca coincidencias con un indice de tripletas en vez de recorrer los 0x2000
bytes de la ventana para cada posicion. La seleccion de coincidencia y la emision de bits
son exactamente las mismas que en crilayla_compress_c.py.
"""
import bisect
import struct

MAGIC = b"CRILAYLA"
PREFIX_SIZE = 0x100
WINDOW = 0x2000


def compress(data):
    src = data
    srclen = len(src)
    if srclen < PREFIX_SIZE:
        raise ValueError("CRILAYLA: se necesitan al menos 0x100 bytes")

    # Indice de tripletas: p -> posiciones donde empieza src[p:p+3].
    pos = {}
    for p in range(srclen - 2):
        key = src[p:p + 3]
        lst = pos.get(key)
        if lst is None:
            pos[key] = [p]
        else:
            lst.append(p)

    buflen = srclen * 2 + 0x100
    dest = bytearray(buflen)
    n = srclen - 1
    m = buflen - 1
    d = 0
    T = 0

    while n >= PREFIX_SIZE:
        j = n + 3 + WINDOW
        if j > srclen:
            j = srclen
        p = 0
        q = 0

        # i en [n+3, j)  <=>  p=i-2 en [n+1, j-2).
        lo = n + 1
        hi = j - 2
        lst = pos.get(src[n - 2:n + 1]) if hi > lo else None
        if lst:
            limit = n - PREFIX_SIZE
            for pp in lst[bisect.bisect_left(lst, lo):bisect.bisect_left(lst, hi)]:
                i = pp + 2
                k = 0
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
    out = bytearray(MAGIC)
    out += struct.pack("<II", srclen - PREFIX_SIZE, len(payload))
    out += payload
    out += src[:PREFIX_SIZE]
    return bytes(out)
