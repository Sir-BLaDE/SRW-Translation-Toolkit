# -*- coding: utf-8 -*-
"""Reconstruye LayoutImage.cpk (formato TOC, sin ITOC) con texturas modificadas."""
import os
import shutil
import struct
import sys
sys.path.insert(0, "/tmp/b")
from cpk_util import load, CpkFiles

SRC = os.environ["HOME"]+"/mnt/srwv/backup/LayoutImage_original_20261118.cpk"
BAK = SRC
OUT = os.environ["HOME"]+"/mnt/srwv/outputs/LayoutImage_EN_es_tex2.cpk"
WORK = r"C:/Dev/Default Project/srwv/outputs/layout_image_work"

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

cf = load(SRC)
cpk = cf.cpk
raw = bytearray(cpk.raw)
align = cpk.align

new_blobs = {}
for r in cf.rows:
    f="/tmp/tx/row%d.bin"%r["id"]
    if os.path.exists(f):
        pt=open("/tmp/tx/row%d.pt"%r["id"],"rb").read(); assert len(pt)==r["ex"]
        new_blobs[r["id"]]=(open(f,"rb").read(),len(pt))
    else:
        new_blobs[r["id"]]=(bytes(raw[r["offset"]:r["offset"]+r["size"]]),r["ex"])
# Reconstruir contenido
content = bytearray()
new_offsets = {}
for i, r in enumerate(cf.rows):
    blob, ex = new_blobs[r["id"]]
    new_offsets[r["id"]] = cpk.content_offset + len(content)
    content += blob
    # padding de alineacion
    while len(content) % align:
        content.append(0)
    # actualizar toc
    toc = cpk.toc
    for rr in range(toc.rows_count):
        d = toc.row(rr)
        if d["ID"] == r["id"]:
            # actualizar FileSize, ExtractSize, FileOffset
            off_fs = cpk.cell_offset(toc, "FileSize", rr)
            off_fo = cpk.cell_offset(toc, "FileOffset", rr)
            struct.pack_into(">I", raw, off_fs, len(blob))
            struct.pack_into(">Q", raw, off_fo, new_offsets[r["id"]] - cpk.toc_offset)
            break

# Actualizar header
header = cpk.header
hrow = 0
# ContentSize
off = cpk.cell_offset(header, "ContentSize", hrow)
struct.pack_into(">Q", raw, off, len(content))
# EnabledPackedSize
old_packed = cpk.cell_offset(header, "EnabledPackedSize", hrow)
# calcular delta
old_packed_sum = sum(r["size"] for r in cf.rows)
new_packed_sum = sum(len(new_blobs[r["id"]][0]) for r in cf.rows)
old_enabled_packed = struct.unpack_from(">Q", raw, old_packed)[0]
struct.pack_into(">Q", raw, old_packed, old_enabled_packed + (new_packed_sum - old_packed_sum))
# EnabledDataSize
old_data = cpk.cell_offset(header, "EnabledDataSize", hrow)
old_enabled_data = struct.unpack_from(">Q", raw, old_data)[0]
# ex size is same (4194432 each), so no change needed
# FileSize (total file size) - update at end

# Reconstruir archivo
# header + toc area stays, content area replaced, etoc stays
content_start = cpk.content_offset
content_end = content_start + cpk.content_size
# etoc starts at etoc_offset
etoc_start = cpk.etoc_offset
prefix = bytes(raw[:content_start])
suffix = bytes(raw[etoc_start:])  # etoc + rest
out = bytearray(prefix) + content + suffix

# update EtocOffset
off_etoc = cpk.cell_offset(header, "EtocOffset", hrow)
struct.pack_into(">Q", raw, off_etoc, content_start + len(content))
# but raw is the original, we need to update in out
# find the header position in out (same as prefix start)
# header is at the beginning, so cell_offset is same
struct.pack_into(">Q", out, off_etoc, content_start + len(content))

# FileSize (total) - esta columna no esta habilitada (flag 0x10), se omite
pass

# EnabledPackedSize in out
struct.pack_into(">Q", out, old_packed, old_enabled_packed + (new_packed_sum - old_packed_sum))
# ContentSize in out
struct.pack_into(">Q", out, off, len(content))

with open(OUT, "wb") as f:
    f.write(out)
print("escrito", OUT, len(out))

import hashlib
chk=load(OUT); pass
for r in chk.rows:
    pl=chk.plain(r); assert r["ex"]==len(pl)
    f="/tmp/tx/row%d.pt"%r["id"]
    exp=open(f,"rb").read() if os.path.exists(f) else cf.plain([x for x in cf.rows if x["id"]==r["id"]][0])
    assert pl==exp,r["id"]
print("ok",len(out),hashlib.sha256(bytes(out)).hexdigest()[:12])
