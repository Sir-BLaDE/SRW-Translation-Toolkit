# -*- coding: utf-8 -*-
"""Volcado de pila del hilo que falla, mapeada a modulos."""
import struct
import sys

path = sys.argv[1]
d = open(path, "rb").read()
sig, ver, nstreams, rva_dir, _ = struct.unpack_from("<4sIIII", d, 0)
streams = {}
for i in range(nstreams):
    t, size, rva = struct.unpack_from("<III", d, rva_dir + i * 12)
    streams.setdefault(t, (size, rva))

# modulos
mods = []
size, rva = streams[4]
n = struct.unpack_from("<I", d, rva)[0]
for i in range(n):
    base = rva + 4 + i * 108
    mod_base, mod_size, _c1, _c2, name_rva = struct.unpack_from("<QIIII", d, base)
    ln = struct.unpack_from("<I", d, name_rva)[0]
    nm = d[name_rva + 4:name_rva + 4 + ln].decode("utf-16-le")
    mods.append((mod_base, mod_size, nm))


def who(addr):
    for b, s, nm in mods:
        if b <= addr < b + s:
            return "%s+0x%X" % (nm.split("\\")[-1], addr - b)
    return None


# excepcion
size, rva = streams[6]
tid, align, code, flags, rec, addr = struct.unpack_from("<IIIIQQ", d, rva)
print("hilo %d excepcion 0x%08X en %s" % (tid, code, who(addr) or hex(addr)))


def read_mem(vaddr, length):
    """Busca un bloque de memoria que contenga la direccion (MemoryList 5)."""
    size, rva = streams[5]
    cnt = struct.unpack_from("<I", d, rva)[0]
    best = None
    for i in range(cnt):
        base = rva + 4 + i * 16
        start, msize, mrva = struct.unpack_from("<QII", d, base)
        if start <= vaddr and vaddr + length <= start + msize:
            off = mrva + (vaddr - start)
            return d[off:off + length]
        if start <= vaddr < start + msize:
            off = mrva + (vaddr - start)
            take = min(length, start + msize - vaddr)
            best = d[off:off + take]
    return best


# hilos
size, rva = streams[3]
cnt = struct.unpack_from("<I", d, rva)[0]
for i in range(cnt):
    base = rva + 4 + i * 48
    thid, susp, pc, prio = struct.unpack_from("<IIII", d, base)
    teb, sstart, ssize, srva, csize, crva = struct.unpack_from("<QQIIII", d, base + 16)
    if thid != tid:
        continue
    print("pila: 0x%X tam %d" % (sstart, ssize))
    blob = d[srva:srva + ssize]
    hits = []
    for k in range(0, len(blob) - 8, 8):
        v = struct.unpack_from("<Q", blob, k)[0]
        w = who(v)
        if w and ("SRWV" in w or "ucrtbase" in w):
            hits.append((k, v, w))
    for k, v, w in hits[:60]:
        print("  +0x%04X  %s" % (k, w))
