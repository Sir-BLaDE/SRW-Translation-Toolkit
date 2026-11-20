# -*- coding: utf-8 -*-
"""Reconstruye LayoutImage.cpk (formato TOC, sin ITOC) con texturas modificadas."""
import os
import shutil
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load, CpkFiles
from srwv_crypto import encrypt_data
from crilayla_compress_fast import compress

SRC = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutImage.cpk"
BAK = r"C:/Dev/Default Project/srwv/backup/LayoutImage_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/LayoutImage_es.cpk"
WORK = r"C:/Dev/Default Project/srwv/outputs/layout_image_work"

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

cf = load(SRC)
cpk = cf.cpk
raw = bytearray(cpk.raw)
align = cpk.align

# Cargar las texturas modificadas (DDS) y recomprimir
new_blobs = {}  # id -> (compressed_blob, ex_size)
for r in cf.rows:
    dds_path = os.path.join(WORK, "row_%02d.dds" % r["id"])
    if not os.path.exists(dds_path):
        print("FALTA", dds_path, "- usando original")
        new_blobs[r["id"]] = (bytes(raw[r["offset"]:r["offset"] + r["size"]]), r["ex"])
        continue
    with open(dds_path, "rb") as f:
        dds = f.read()
    enc = encrypt_data(dds)
    comp = compress(enc)
    new_blobs[r["id"]] = (comp, len(dds))
    print("fila %d: orig=%d new=%d ex=%d" % (r["id"], r["size"], len(comp), len(dds)))

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

# verificar
chk = load(OUT)
print("diag", chk.cpk.diagnose() or "ok")
for r in chk.rows:
    pt = chk.plain(r)
    print("fila %d: ex=%d len=%d igual=%s" % (r["id"], r["ex"], len(pt), r["ex"] == len(pt)))
