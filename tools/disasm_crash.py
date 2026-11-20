# -*- coding: utf-8 -*-
"""Desensambla alrededor de una RVA del exe usando capstone."""
import struct
import sys
from pathlib import Path

import capstone

exe = Path(r"D:/Juegos/-SPARROW-/Super Robot Wars V/SRWV.EXE")
b = exe.read_bytes()
pe = struct.unpack_from("<I", b, 0x3C)[0]
assert b[pe:pe + 4] == b"PE\0\0"
machine, nsec, _, _, _, opt_size, _ = struct.unpack_from("<HHIIIHH", b, pe + 4)
opt = pe + 24
magic = struct.unpack_from("<H", b, opt)[0]
imgbase = struct.unpack_from("<Q", b, opt + 24)[0] if magic == 0x20B else struct.unpack_from("<I", b, opt + 28)[0]
print("machine", hex(machine), "sections", nsec, "magic", hex(magic), "imagebase", hex(imgbase))

secs = []
sp = opt + opt_size
for i in range(nsec):
    name = b[sp:sp + 8].rstrip(b"\0").decode("ascii", "ignore")
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", b, sp + 8)
    secs.append((name, vaddr, vsize, raddr, rsize))
    sp += 40

rva = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x13DEE2
span = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x60
print("RVA", hex(rva), "secciones", [(s[0], hex(s[1]), hex(s[2])) for s in secs])

foff = None
for name, vaddr, vsize, raddr, rsize in secs:
    if vaddr <= rva < vaddr + max(vsize, rsize):
        foff = raddr + (rva - vaddr)
        break
if foff is None:
    foff = rva
print("file offset", hex(foff))
code = b[max(0, foff - span):foff + span]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False
for ins in md.disasm(code, (rva - span) & 0xFFFFFFFFFFFFFFFF):
    mark = " <== CRASH" if ins.address == rva else ""
    print("%016X  %-28s %s%s" % (imgbase + ins.address, ins.bytes.hex(), ins.mnemonic + " " + ins.op_str, mark))
