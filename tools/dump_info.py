# -*- coding: utf-8 -*-
"""Lector minimo de minidumps para ver direccion de excepcion y modulo."""
import struct
import sys

path = sys.argv[1]
d = open(path, "rb").read()

sig, ver, nstreams, rva_dir, _ = struct.unpack_from("<4sIIII", d, 0)
assert sig == b"MDMP", sig
print("streams:", nstreams, "rva_dir:", rva_dir)

streams = {}
for i in range(nstreams):
    t, size, rva = struct.unpack_from("<III", d, rva_dir + i * 12)
    streams.setdefault(t, (size, rva))
print("tipos:", sorted(streams))

# 6 = ExceptionStream
if 6 in streams:
    size, rva = streams[6]
    tid, align, code, flags, rec, addr = struct.unpack_from("<IIIIQQ", d, rva)
    print("thread %d excepcion 0x%08X flags 0x%X direccion 0x%016X"
          % (tid, code, flags, addr))
else:
    print("sin ExceptionStream")

# 4 = ModuleListStream
mods = []
if 4 in streams:
    size, rva = streams[4]
    n = struct.unpack_from("<I", d, rva)[0]
    for i in range(n):
        base = rva + 4 + i * 108
        mod_base, mod_size, _c1, _c2, name_rva = struct.unpack_from("<QIIII", d, base)
        ln = struct.unpack_from("<I", d, name_rva)[0]
        nm = d[name_rva + 4:name_rva + 4 + ln].decode("utf-16-le")
        mods.append((mod_base, mod_size, nm))
    print("modulos:", len(mods))

if 6 in streams:
    for b, s, nm in mods:
        if b <= addr < b + s:
            print("modulo: %s base=0x%016X offset=+0x%X" % (nm, b, addr - b))
            break

# 7 = SystemInfo, 9 = MemoryList, 15 = MemoryInfoList (no usado)
# parametros de excepcion: los numeros de excepcion de C++ en Windows suelen 0xE06D7363
if 6 in streams:
    code, nparams = struct.unpack_from("<II", d, rva + 24)[0], None
