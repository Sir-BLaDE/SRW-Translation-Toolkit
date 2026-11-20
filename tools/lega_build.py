# -*- coding: utf-8 -*-
"""Reconstruye lega_zkn.cpk traduciendo el pool jstr-zkn.

Mantiene la estructura de 22 chunks:
  - jstr-zkn es el primero (0x28). Su payload es un bloque de cadenas NUL.
  - Los demas chunks tienen referencias u32 a offsets dentro de ese pool.
  - next = (fin de <endofchunk>) - inicio de <chunk-head>
  - len  = inicio de <chunk-foot> - inicio del payload
  - header[0x20] = longitud total - 4, header[0x24] = inicio de <file--foot>.
"""
import os
import re
import shutil
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")

from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from lega_map import ES

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
SRC = G + r"/CommonData/MtData/EN/lega_zkn.cpk"
BAK = r"C:/Dev/Default Project/srwv/backup/lega_zkn_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/lega_zkn_es.cpk"

HEAD = b"<chunk-head>\x00\x00\x00\x00"
FOOT = b"<chunk-foot>\x00\x00\x00\x00"
ENDC = b"<endofchunk>\x00\x00\x00\x00"
FILEFOOT = b"<file--foot>\x00\x00\x00\x00"


def parse(pt):
    chunks = []
    for m in re.finditer(re.escape(HEAD), pt):
        i = m.start()
        name = pt[i + 16:i + 24].rstrip(b"\0").decode("ascii")
        nxt, length = struct.unpack_from("<II", pt, i + 24)
        payload = i + 32
        foot = pt.find(FOOT, payload)
        endc = pt.find(ENDC, foot)
        chunks.append(dict(name=name, head=i, payload=payload, foot=foot,
                           endc=endc, data=pt[payload:foot], nxt=nxt, length=length))
    return chunks


def build(chunks):
    out = bytearray()
    out += pt_original[:0x28]           # header + <chunk-head> del primero se rellenan luego
    del out[0x28:]
    for k, c in enumerate(chunks):
        c["head"] = len(out)
        c["payload"] = c["head"] + 32
        out += HEAD
        out += c["name"].encode().ljust(8, b"\0")
        out += struct.pack("<II", 0, len(c["data"]))   # next/len se rellenan al final
        out += c["data"]
        foot = len(out)
        out += FOOT
        out += struct.pack("<Q", len(c["name"]) + 38)  # footval medido
        endc = len(out)      # inicio de <endofchunk> (mide 16 bytes)
        out += ENDC
        c["real_next"] = endc + 16 - c["head"]
        c["foot"] = foot
        c["endc"] = endc
    # <file--foot> + final
    filefoot = len(out)
    out += FILEFOOT
    out += struct.pack("<Q", 0x28)
    out += b"****<end-of-mt>.\x00\x00\x00\x00"
    # rellenar next/len de cada chunk
    for c in chunks:
        struct.pack_into("<II", out, c["head"] + 24, c["real_next"], len(c["data"]))
    struct.pack_into("<II", out, 0x20, len(out) - 4, filefoot)
    return bytes(out)


if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

cf = load(SRC)
pt_original = cf.plain(cf.rows[0])
chunks = parse(pt_original)
print("chunks", len(chunks), [c["name"] for c in chunks])
first = chunks[0]
assert first["name"] == "jstr-zkn"

# 1) Pool traducido + tabla old->new offset
pool_old = first["data"]
raws = []
pos = 0
while pos < len(pool_old):
    end = pool_old.find(b"\0", pos)
    assert end >= 0, "sin NUL en %d" % pos
    raws.append(pool_old[pos:end])
    pos = end + 1

newpool = bytearray()
for raw in raws:
    s = raw.decode("utf-8")
    if s in ES:
        new = ES[s].encode("utf-8")
        if s != ES[s]:
            print("  %-55s -> %s" % (s[:55], ES[s][:55]))
    else:
        new = raw
    newpool += new + b"\0"
first["data"] = bytes(newpool)

# 2) Los offsets antiguos son absolutos dentro del pool. Construir old->new.
old_offsets = []
p = 0
for raw in raws:
    old_offsets.append(p)
    p += len(raw) + 1
new_offsets = []
p = 0
for raw in raws:
    s = raw.decode("utf-8")
    new = ES.get(s, s).encode("utf-8")
    new_offsets.append(p)
    p += len(new) + 1
remap = {old: new for old, new in zip(old_offsets, new_offsets)}
starts_old = set(old_offsets)

# 3) Remapear referencias u32 en TODOS los chunks menos el pool.
patched = 0
for c in chunks[1:]:
    data = bytearray(c["data"])
    for i in range(0, len(data) - 3, 4):
        v = struct.unpack_from("<I", data, i)[0]
        if v in starts_old:
            struct.pack_into("<I", data, i, remap[v])
            patched += 1
    c["data"] = bytes(data)
print("referencias remapeadas", patched)

# 4) Reconstruir contenedor
out = build(chunks)
chk = parse(out)
assert len(chk) == len(chunks)
for a, b in zip(chunks, chk):
    assert b["name"] == a["name"]
    assert b["data"] == a["data"], a["name"]
    got = struct.unpack_from("<I", out, b["head"] + 24)[0]
    exp = b["endc"] + 16 - b["head"]
    if got != exp:
        print("DEBUG", b["name"], "head", b["head"], "endc", b["endc"], "got", got, "exp", exp)
    assert struct.unpack_from("<I", out, b["head"] + 28)[0] == len(b["data"])
    assert got == exp
print("roundtrip chunks OK, total", len(out),
      "header", [hex(struct.unpack_from("<I", out, i)[0]) for i in (0x20, 0x24)])

new_files = {cf.rows[0]["id"]: (cf.cipher(cf.rows[0], out), len(out))}
blob = build_ordered(SRC, new_files)
with open(OUT, "wb") as f:
    f.write(blob)
print("escrito", OUT, len(blob))

final = load(OUT)
r = final.rows[0]
print("diag", final.cpk.diagnose() or "ok", "ex", r["ex"], "len", len(final.plain(r)))
assert r["ex"] == len(final.plain(r))
