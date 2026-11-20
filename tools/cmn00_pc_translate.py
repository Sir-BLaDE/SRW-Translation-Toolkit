# -*- coding: utf-8 -*-
"""Edita las texturas de CMN00_PC.CPK: traduce textos ingleses a espanol."""
import os
import sys
import struct
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/CMN00_PC.CPK"
BAK = r"C:/Dev/Default Project/srwv/backup/CMN00_PC_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/CMN00_PC_es.cpk"
WORK = r"C:/Dev/Default Project/srwv/outputs/cmn00_pc_work"
os.makedirs(WORK, exist_ok=True)

import shutil
if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

# Regiones manuales: (fila, x, y, w, h, texto_espanol)
REGIONS = [
    # Fila 19: Counterattack, Support Defend, Support Attack, Second Attack, Combo Attack, Map Weapon
    (19, 60, 5, 282, 35, "Contraataque"),
    (19, 43, 53, 307, 42, "Apoyo Defensa"),
    (19, 45, 97, 293, 54, "Apoyo Ataque"),
    (19, 50, 145, 302, 48, "Segundo Ataque"),
    (19, 55, 193, 292, 48, "Ataque Combo"),
    (19, 79, 241, 243, 47, "Arma de Mapa"),
    # Fila 20: Artifacts, Return Attacks, Cannot Attack
    (20, 50, 5, 90, 25, "Artefactos"),
    (20, 10, 98, 165, 40, "Contraataques"),
    (20, 15, 163, 150, 32, "No puede atacar"),
]

cf = load(SRC)
images = {}
for r in cf.rows:
    images[r["id"]] = __import__("PIL.Image", fromlist=["Image"]).open(__import__("io").BytesIO(cf.plain(r)))

font_path = r"C:\Windows\Fonts\arialbd.ttf"


def sample_bg(img, x, y, w, h):
    pad = 6
    colors = []
    for yy in range(max(0, y - pad), min(img.height, y + h + pad)):
        for xx in range(max(0, x - pad), min(img.width, x + w + pad)):
            if (x - pad <= xx < x or x + w <= xx < x + w + pad or
                y - pad <= yy < y or y + h <= yy < y + h + pad):
                colors.append(img.getpixel((xx, yy)))
    if not colors:
        return (0, 0, 0, 255)
    rs = sorted(c[0] for c in colors)
    gs = sorted(c[1] for c in colors)
    bs = sorted(c[2] for c in colors)
    as_ = sorted(c[3] for c in colors)
    n = len(colors)
    return (rs[n // 2], gs[n // 2], bs[n // 2], as_[n // 2])


for (row, x, y, w, h, text) in REGIONS:
    img = images[row]
    draw = ImageDraw.Draw(img) if False else None
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    bg = sample_bg(img, x, y, w, h)
    pad = 3
    draw.rectangle([x - pad, y - pad, x + w + pad, y + h + pad], fill=bg)
    font_size = max(8, h - 4)
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    while tw > w + 6 and font_size > 6:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    tx = x + (w - tw) // 2
    ty = y + (h - th) // 2 - bbox[1]
    brightness = (bg[0] + bg[1] + bg[2]) / 3
    text_color = (255, 255, 255, 255) if brightness < 128 else (0, 0, 0, 255)
    draw.text((tx, ty), text, font=font, fill=text_color)
    print("row %d: %r en (%d,%d) %dx%d" % (row, text, x, y, w, h))

# Guardar DDS y reconstruir CPK
new_files = {}
for r in cf.rows:
    img = images[r["id"]]
    dds_path = os.path.join(WORK, "row_%02d.dds" % r["id"])
    img.save(dds_path, format="DDS")
    with open(dds_path, "rb") as f:
        blob = f.read()
    new_files[r["id"]] = (blob, len(cf.plain(r)))
    print("fila %d: %d bytes" % (r["id"], len(blob)))

# Rebuild CPK (toc format, same as layout_image_build.py)
raw = bytearray(open(SRC, "rb").read())
cpk = cf.cpk
align = cpk.align
content = bytearray()
new_offsets = {}
for r in cf.rows:
    blob, ex = new_files[r["id"]]
    from srwv_crypto import encrypt_data
    from crilayla_compress_fast import compress
    enc = encrypt_data(blob)
    comp = compress(enc)
    new_files[r["id"]] = (comp, ex)
    new_offsets[r["id"]] = cpk.content_offset + len(content)
    content += comp
    while len(content) % align:
        content.append(0)

toc = cpk.toc
for rr in range(toc.rows_count):
    d = toc.row(rr)
    rid = d["ID"]
    if rid in new_offsets:
        off_fs = cpk.cell_offset(toc, "FileSize", rr)
        off_fo = cpk.cell_offset(toc, "FileOffset", rr)
        struct.pack_into(">I", raw, off_fs, len(new_files[rid][0]))
        struct.pack_into(">Q", raw, off_fo, new_offsets[rid] - cpk.toc_offset)

header = cpk.header
hrow = 0
off_cs = cpk.cell_offset(header, "ContentSize", hrow)
struct.pack_into(">Q", raw, off_cs, len(content))
off_ep = cpk.cell_offset(header, "EnabledPackedSize", hrow)
old_ep = struct.unpack_from(">Q", raw, off_ep)[0]
old_packed_sum = sum(r["size"] for r in cf.rows)
new_packed_sum = sum(len(new_files[r["id"]][0]) for r in cf.rows)
struct.pack_into(">Q", raw, off_ep, old_ep + (new_packed_sum - old_packed_sum))
off_eo = cpk.cell_offset(header, "EtocOffset", hrow)
struct.pack_into(">Q", raw, off_eo, cpk.content_offset + len(content))

content_start = cpk.content_offset
etoc_start = cpk.etoc_offset
prefix = bytes(raw[:content_start])
suffix = bytes(raw[etoc_start:])
out = bytearray(prefix) + content + suffix

with open(OUT, "wb") as f:
    f.write(out)
print("escrito", OUT, len(out))

chk = load(OUT)
for r in chk.rows:
    pt = chk.plain(r)
    print("fila %d: ex=%d len=%d igual=%s" % (r["id"], r["ex"], len(pt), r["ex"] == len(pt)))
