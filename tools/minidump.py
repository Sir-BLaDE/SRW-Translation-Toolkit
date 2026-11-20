"""
minidump.py - Analizador de minidumps de Windows (.dmp).
Extrae la excepcion, el contexto del hilo (RIP/RSP) y los modulos.
"""
import struct
import sys


def _u(d, off, fmt):
    return struct.unpack_from(fmt, d, off)


def parse(path):
    d = open(path, "rb").read()
    if d[:4] != b"MDMP":
        raise ValueError("no es un minidump")
    n_streams = struct.unpack_from("<I", d, 8)[0]
    streams = {}
    for i in range(n_streams):
        stype, size, rva = struct.unpack_from("<III", d, 32 + i * 12)
        streams[stype] = (rva, size)

    out = {"streams": sorted(streams), "exceptions": [], "threads": [], "modules": []}

    # Memoria: mapa RVA -> offset en el fichero
    mem = []
    if 5 in streams:
        rva, size = streams[5]
        n = struct.unpack_from("<I", d, rva)[0]
        off = rva + 4
        for _ in range(n):
            start, msize, mrva = struct.unpack_from("<QII", d, off)
            off += 16
            mem.append((start, msize, mrva))

    def read_mem(rva, size):
        for start, msize, mrva in mem:
            if start <= rva < start + msize:
                o = mrva + (rva - start)
                return d[o:o + size]
        return None

    # Excepciones
    if 6 in streams:
        rva, size = streams[6]
        thread_id = struct.unpack_from("<I", d, rva)[0]
        code, flags = struct.unpack_from("<II", d, rva + 8)
        address = struct.unpack_from("<Q", d, rva + 16)[0]
        nparams = struct.unpack_from("<I", d, rva + 24)[0]
        params = list(struct.unpack_from("<15Q", d, rva + 32))
        ctx_size, ctx_rva = struct.unpack_from("<II", d, rva + 160)
        out["exceptions"].append({
            "thread": thread_id, "code": code, "flags": flags,
            "address": address, "params": params[:nparams],
            "context_rva": ctx_rva,
        })

    # Lista de hilos
    if 3 in streams:
        rva, size = streams[3]
        n = struct.unpack_from("<I", d, rva)[0]
        off = rva + 4
        for _ in range(n):
            tid, susp, pri_class, pri, teb = struct.unpack_from("<IIIIQ", d, off)
            stack_start, stack_size, stack_rva = struct.unpack_from("<QII", d, off + 24)
            ctx_size, ctx_rva = struct.unpack_from("<II", d, off + 40)
            off += 48
            ctx = read_mem(ctx_rva, ctx_size) if ctx_rva else None
            rec = {"tid": tid, "ctx_size": ctx_size, "ctx_rva": ctx_rva}
            if ctx and len(ctx) >= 0x100:
                rec["rip"] = struct.unpack_from("<Q", ctx, 0xF8)[0]
                rec["rsp"] = struct.unpack_from("<Q", ctx, 0x98)[0]
                rec["rax"] = struct.unpack_from("<Q", ctx, 0x78)[0]
                rec["rcx"] = struct.unpack_from("<Q", ctx, 0x80)[0]
                rec["rdx"] = struct.unpack_from("<Q", ctx, 0x88)[0]
            out["threads"].append(rec)

    # Modulos
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
            out["modules"].append((base, msize, name))
    return out


def fmt_exc(code):
    return {
        0xC0000005: "ACCESS_VIOLATION",
        0xC0000006: "IN_PAGE_ERROR",
        0xC000001D: "ILLEGAL_INSTRUCTION",
        0xC0000409: "STACK_BUFFER_OVERRUN",
        0xC0000374: "HEAP_CORRUPTION",
        0xE06D7363: "C++_EXCEPTION",
    }.get(code, f"0x{code:08X}")


def module_of(mods, addr):
    for base, size, name in mods:
        if base <= addr < base + size:
            return name, addr - base
    return None, None


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print("=" * 70)
        print(p)
        try:
            r = parse(p)
        except Exception as e:
            print("  error:", e)
            continue
        for e in r["exceptions"]:
            print(f"  excepcion: {fmt_exc(e['code'])} dir={e['flags']} addr=0x{e['address']:X} "
                  f"hilo={e['thread']}")
            print("   params:", [hex(x) for x in e["params"][:4]])
        for t in r["threads"]:
            if "rip" in t:
                name, off = module_of(r["modules"], t["rip"])
                print(f"  hilo {t['tid']}: RIP=0x{t['rip']:X} "
                      f"({name}+0x{(off or 0):X}) RSP=0x{t['rsp']:X} "
                      f"RAX=0x{t['rax']:X} RCX=0x{t['rcx']:X} RDX=0x{t['rdx']:X}")
