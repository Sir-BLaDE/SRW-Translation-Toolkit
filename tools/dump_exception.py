# -*- coding: utf-8 -*-
"""Lee el stream de excepcion de un minidump sin WinDbg."""
import struct
import sys
from pathlib import Path

p = Path(sys.argv[1])
b = p.read_bytes()
assert b[:4] == b"MDMP", "no es minidump"
num_streams, dir_rva = struct.unpack_from("<II", b, 8)
streams = {}
for i in range(num_streams):
    off = dir_rva + i * 12
    stype, data_size, rva = struct.unpack_from("<III", b, off)
    streams[stype] = (rva, data_size)

print("streams:", [(k, v) for k, v in sorted(streams.items())][:20])

# ModuleList (type 4)
mods = []
if 4 in streams:
    rva, size = streams[4]
    n = struct.unpack_from("<I", b, rva)[0]
    pos = rva + 4
    for _ in range(n):
        base, msize, checksum, ts, name_rva = struct.unpack_from("<QIIII", b, pos)
        pos += 108
        nlen = struct.unpack_from("<I", b, name_rva)[0]
        name = b[name_rva + 4:name_rva + 4 + nlen].decode("utf-16-le", "ignore")
        mods.append((base, msize, name))
    print("modulos:", len(mods))

if 6 in streams:
    rva, size = streams[6]
    tid, _ = struct.unpack_from("<II", b, rva)
    er = rva + 8
    code, flags, rec, addr, nparam, _unused = struct.unpack_from("<IIQQII", b, er)
    params = struct.unpack_from("<15Q", b, er + 32)
    print("thread", tid, "code=0x%08X" % code, "flags", flags, "addr=0x%016X" % addr, "nparam", nparam)
    print("params", [hex(x) for x in params[:nparam]])
    for base, msize, name in mods:
        if base <= addr < base + msize:
            print("MODULO:", name, "base=0x%X" % base, "offset=0x%X" % (addr - base))
            break
else:
    print("sin stream de excepcion")
