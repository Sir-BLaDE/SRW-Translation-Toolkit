"""
pe_analyze.py - Analisis basico de un PE de 64 bits: secciones, busqueda de
referencias RIP-relative a una direccion y desensamblado con capstone.
"""
import struct, sys


class PE:
    def __init__(self, path):
        self.data = open(path, "rb").read()
        d = self.data
        pe_off = struct.unpack_from("<I", d, 0x3C)[0]
        assert d[pe_off:pe_off+4] == b"PE\0\0"
        coff = pe_off + 4
        self.machine = struct.unpack_from("<H", d, coff)[0]
        self.num_sections = struct.unpack_from("<H", d, coff + 2)[0]
        opt_off = coff + 20
        self.magic = struct.unpack_from("<H", d, opt_off)[0]
        self.image_base = struct.unpack_from("<Q", d, opt_off + 24)[0]
        self.entry_rva = struct.unpack_from("<I", d, opt_off + 16)[0]
        sec_off = opt_off + (0xF0 if self.magic == 0x20B else 0xE0)
        self.sections = []
        for i in range(self.num_sections):
            o = sec_off + i * 40
            name = d[o:o+8].rstrip(b"\0").decode("latin1")
            vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", d, o + 8)
            chars = struct.unpack_from("<I", d, o + 36)[0]
            self.sections.append(dict(name=name, vsize=vsize, vaddr=vaddr,
                                     rsize=rsize, raddr=raddr, chars=chars))

    def rva_to_off(self, rva):
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
                return s["raddr"] + (rva - s["vaddr"])
        return None

    def off_to_rva(self, off):
        for s in self.sections:
            if s["raddr"] <= off < s["raddr"] + s["rsize"]:
                return s["vaddr"] + (off - s["raddr"])
        return None

    def section(self, name):
        for s in self.sections:
            if s["name"] == name:
                return s
        return None


def find_dword(data, value):
    pat = struct.pack("<I", value)
    out = []
    start = 0
    while True:
        i = data.find(pat, start)
        if i < 0:
            break
        out.append(i)
        start = i + 1
    return out


def find_bytes(data, pat):
    out = []
    start = 0
    while True:
        i = data.find(pat, start)
        if i < 0:
            break
        out.append(i)
        start = i + 1
    return out


def xrefs_to(pe, target_va, text_section=".text"):
    """Busca referencias RIP-relative dentro de la seccion de codigo."""
    sec = pe.section(text_section)
    if sec is None:
        return []
    data = pe.data[sec["raddr"]:sec["raddr"] + sec["rsize"]]
    base_va = pe.image_base + sec["vaddr"]
    hits = []
    for i in range(len(data) - 4):
        disp = struct.unpack_from("<i", data, i)[0]
        for L in (2, 3, 4, 5, 6, 7, 8):
            if i + L > len(data):
                break
            if base_va + i + L + disp == target_va:
                hits.append((sec["raddr"] + i, base_va + i, L))
    return hits


if __name__ == "__main__":
    path = sys.argv[1]
    pe = PE(path)
    print("ImageBase: 0x%X  Entry RVA: 0x%X" % (pe.image_base, pe.entry_rva))
    for s in pe.sections:
        print(f"  {s['name']:<10} VA=0x{s['vaddr']:08X} VSize=0x{s['vsize']:08X} "
              f"Raw=0x{s['raddr']:08X} RawSize=0x{s['rsize']:08X} chars=0x{s['chars']:08X}")
