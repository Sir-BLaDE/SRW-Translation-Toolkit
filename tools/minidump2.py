"""minidump2.py - minidump con pila, contexto de la excepcion y modulos."""
import struct
import sys


def parse(path):
    d = open(path, "rb").read()
    if d[:4] != b"MDMP":
        raise ValueError("no es un minidump")
    n_streams = struct.unpack_from("<I", d, 8)[0]
    streams = {}
    for i in range(n_streams):
        stype, size, rva = struct.unpack_from("<III", d, 32 + i * 12)
        streams[stype] = (rva, size)

    mem = []
    if 5 in streams:
        rva, size = streams[5]
        n = struct.unpack_from("<I", d, rva)[0]
        off = rva + 4
        for _ in range(n):
            start, msize, mrva = struct.unpack_from("<QII", d, off)
            off += 16
            mem.append((start, msize, mrva))

    def read_mem(addr, size):
        for start, msize, mr in mem:
            if start <= addr < start + msize:
                o = mr + (addr - start)
                return d[o:o + min(size, start + msize - addr)]
        return None

    mods = []
    if 4 in streams:
        rva, size = streams[4]
        n = struct.unpack_from("<I", d, rva)[0]
        off = rva + 4
        for _ in range(n):
            base = struct.unpack_from("<Q", d, off)[0]
            msize = struct.unpack_from("<I", d, off + 8)[0]
            namerva = struct.unpack_from("<I", d, off + 20)[0]
            off += 108
            slen = struct.unpack_from("<I", d, namerva)[0]
            name = d[namerva + 4:namerva + 4 + slen].decode("utf-16-le", "replace")
            mods.append((base, msize, name))

    def module_of(addr):
        for base, size, name in mods:
            if base <= addr < base + size:
                return name, addr - base
        return None, None

    exc = None
    ctx = None
    if 6 in streams:
        rva, size = streams[6]
        thread_id = struct.unpack_from("<I", d, rva)[0]
        code, flags = struct.unpack_from("<II", d, rva + 8)
        address = struct.unpack_from("<Q", d, rva + 16)[0]
        nparams = struct.unpack_from("<I", d, rva + 24)[0]
        params = list(struct.unpack_from("<15Q", d, rva + 32))
        ctx_size, ctx_rva = struct.unpack_from("<II", d, rva + 160)
        # el RVA del contexto es relativo al inicio del fichero .dmp
        raw = d[ctx_rva: ctx_rva + ctx_size] if ctx_rva else None
        exc = dict(thread=thread_id, code=code, flags=flags, address=address,
                   params=params[:nparams], raw_ctx=raw, ctx_size=ctx_size,
                   ctx_off=ctx_rva if ctx_rva else None)

    regs = {}
    if exc and exc["raw_ctx"] and len(exc["raw_ctx"]) >= 0x100:
        c = exc["raw_ctx"]
        for name, off in [("rax", 0x78), ("rcx", 0x80), ("rdx", 0x88), ("rbx", 0x90),
                          ("rsp", 0x98), ("rbp", 0xA0), ("rsi", 0xA8), ("rdi", 0xB0),
                          ("r8", 0xB8), ("r9", 0xC0), ("r10", 0xC8), ("r11", 0xD0),
                          ("r12", 0xD8), ("r13", 0xE0), ("r14", 0xE8), ("r15", 0xF0),
                          ("rip", 0xF8)]:
            regs[name] = struct.unpack_from("<Q", c, off)[0]

    def stack_walk(rsp, limit=40):
        out = []
        if not rsp:
            return out
        blk = read_mem(rsp, 0x2000) or b""
        for i in range(0, len(blk) - 8, 8):
            v = struct.unpack_from("<Q", blk, i)[0]
            name, off = module_of(v)
            if name and "SRWV" in name.upper():
                out.append((rsp + i, v, name, off))
                if len(out) >= limit:
                    break
        return out

    return dict(streams=sorted(streams), mem=mem, mods=mods, exc=exc, regs=regs,
                walk=stack_walk(regs.get("rsp", 0)) if regs else [],
                module_of=module_of, read_mem=read_mem, size=len(d))


def fmt_exc(code):
    return {
        0xC0000005: "ACCESS_VIOLATION", 0xC0000006: "IN_PAGE_ERROR",
        0xC000001D: "ILLEGAL_INSTRUCTION", 0xC0000409: "STACK_BUFFER_OVERRUN",
        0xC0000374: "HEAP_CORRUPTION", 0xE06D7363: "C++_EXCEPTION",
        0x80000003: "BREAKPOINT",
    }.get(code, "0x%08X" % code)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print("=" * 78)
        print(p)
        try:
            r = parse(p)
        except Exception as e:
            print("  error:", e)
            continue
        print("  tamano %.1f MB | streams %s" % (r["size"] / 1048576, r["streams"]))
        print("  modulos: %d | regiones de memoria: %d" % (len(r["mods"]), len(r["mem"])))
        e = r["exc"]
        if e:
            print("  EXCEPCION %s | hilo %d | addr=0x%X | params %s" % (
                fmt_exc(e["code"]), e["thread"], e["address"],
                [hex(x) for x in e["params"]]))
        g = r["regs"]
        if g:
            name, off = r["module_of"](g["rip"])
            print("  RIP=0x%X (%s+0x%X)  RSP=0x%X  RBP=0x%X" % (
                g["rip"], name or "?", off or 0, g["rsp"], g["rbp"]))
            print("  RAX=0x%X RBX=0x%X RCX=0x%X RDX=0x%X" % (
                g["rax"], g["rbx"], g["rcx"], g["rdx"]))
            print("  RSI=0x%X RDI=0x%X R8=0x%X R9=0x%X" % (
                g["rsi"], g["rdi"], g["r8"], g["r9"]))
            print("  --- posibles retornos en la pila (solo modulos del juego) ---")
            for addr, v, mname, moff in r["walk"][:18]:
                print("    [rsp+0x%03X] 0x%X  %s+0x%X" % (addr - g["rsp"], v, mname, moff))
        print("  --- modulos cargados ---")
        for base, size, name in r["mods"]:
            short = name.split("\\")[-1]
            if any(k in short.upper() for k in ("SRWV", "STEAM", "NTDLL", "KERNEL", "D3D", "DXGI", "NV", "AMD", "ATI", "IG")):
                print("    %-24s base=0x%X tam=0x%X" % (short, base, size))
