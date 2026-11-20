"""pe.py - utilidades minimas de PE: secciones, RVA->offset, desensamblado."""
import struct
import capstone

EXE = "D:/Juegos/-SPARROW-/Super Robot Wars V/SRWV.EXE"


def load(exe=EXE):
    d = open(exe, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, e_lfanew + 6)[0]
    opt_size = struct.unpack_from("<H", d, e_lfanew + 20)[0]
    base = struct.unpack_from("<Q", d, e_lfanew + 24 + 24)[0]
    secs = []
    off = e_lfanew + 24 + opt_size
    for _ in range(nsec):
        name = d[off:off + 8].rstrip(b"\0").decode("latin1")
        vsize, va, rawsize, rawptr = struct.unpack_from("<IIII", d, off + 8)
        secs.append((name, va, vsize, rawptr, rawsize))
        off += 40
    return d, base, secs


def rva2off(secs, rva):
    for name, va, vsize, rawptr, rawsize in secs:
        if va <= rva < va + max(vsize, rawsize):
            return rawptr + (rva - va)
    return None


def disas(d, secs, rva, before=0x60, after=0x30, base=0):
    o = rva2off(secs, rva - before)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False
    code = d[o:o + before + after]
    out = []
    cur = rva - before
    for ins in md.disasm(code, base + cur):
        out.append(ins)
    return out


if __name__ == "__main__":
    import sys
    d, base, secs = load()
    print("image base 0x%X" % base)
    for s in secs:
        print("  %-8s va=0x%08X vsize=0x%08X raw=0x%08X rawsize=0x%08X" % s)
    for a in sys.argv[1:]:
        rva = int(a, 16)
        print("=== disasm RVA 0x%X ===" % rva)
        for ins in disas(d, secs, rva):
            mark = ">>" if ins.address == rva else "  "
            print("%s 0x%08X  %-10s %s" % (mark, ins.address, ins.mnemonic, ins.op_str))
