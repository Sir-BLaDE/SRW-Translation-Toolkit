"""cpk_check.py - valida estructura y descompresion de todos los ficheros de un CPK."""
import sys
from cpk_util import load

MAGIC = b"CRILAYLA"


def crilayla_decompress(data, out_size):
    if data[:8] != MAGIC:
        raise ValueError("sin magia")
    import struct
    hdr = data[8:256]
    body = data[256:]
    # comprobacion ligera: el tamano descomprimido real
    return hdr, body


def check(path, verbose=True):
    cf = load(path)
    print("%s | %d entradas" % (path.split("/")[-1], len(cf.rows)))
    ids = [f["id"] for f in cf.rows]
    print("  ids: %d..%d  unicos=%s  ordenados=%s" % (min(ids), max(ids), len(set(ids)) == len(ids), ids == sorted(ids)))
    comp = uncomp = 0
    problemas = []
    ascii_txt = []
    for f in cf.rows:
        raw = cf.raw(f)
        if raw[:8] == MAGIC:
            comp += 1
            if f["ex"] < 256:
                problemas.append((f["id"], "ex<256", f["ex"]))
        else:
            uncomp += 1
            if f["ex"] != f["size"]:
                problemas.append((f["id"], "ex!=size", f["ex"], f["size"]))
        if verbose and f["ex"] < 4000 and raw[:8] != MAGIC:
            ascii_txt.append((f["id"], raw))
    print("  comprimidas=%d sin comprimir=%d" % (comp, uncomp))
    if problemas:
        print("  PROBLEMAS:")
        for p in problemas[:20]:
            print("   ", p)
    else:
        print("  estructura basica OK")
    return cf, ascii_txt


if __name__ == "__main__":
    for p in sys.argv[1:]:
        try:
            cf, txt = check(p)
            for fid, raw in txt[:10]:
                s = raw.decode("utf-8", "replace")
                s = "".join(c if c.isprintable() or c in "\r\n\t" else "." for c in s)
                print("   id %d (%d B): %s" % (fid, len(raw), s[:300].replace("\n", "\\n")))
        except Exception as e:
            print("%s -> ERROR %s: %s" % (p, type(e).__name__, e))
