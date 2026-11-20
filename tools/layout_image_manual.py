# -*- coding: utf-8 -*-
"""Edita manualmente las regiones de texto ingles en LayoutImage.cpk."""
import os
import sys
import struct
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"C:/Dev/Default Project/srwv/backup/LayoutImage_original.cpk"
BAK = r"C:/Dev/Default Project/srwv/backup/LayoutImage_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/LayoutImage_es.cpk"
WORK = r"C:/Dev/Default Project/srwv/outputs/layout_image_work"
os.makedirs(WORK, exist_ok=True)

# Regiones manuales: (fila, x, y, w, h, texto_espanol)
# Basadas en OCR TSV + analisis visual de las texturas
REGIONS = [
    # Fila 0: Support Defend, Support Attack, Second Attack
    (0, 10, 580, 240, 60, "Apoyo Defensa"),
    (0, 10, 640, 240, 60, "Apoyo Ataque"),
    (0, 10, 700, 120, 30, "Segundo Ataque"),
    # Fila 3: Weapon, Simulation, Money, DEF, HOT, Combat
    (3, 0, 550, 270, 90, "Arma"),
    (3, 920, 250, 100, 30, "Simulacion"),
    (3, 935, 290, 70, 35, "Dinero"),
    (3, 60, 335, 90, 40, "DEF"),
    (3, 925, 805, 85, 120, "CAL"),
    # Fila 6: SKL, DEF, Simulation, Money, Combo Attack
    (6, 55, 275, 100, 50, "HAB"),
    (6, 55, 335, 100, 45, "DEF"),
    (6, 920, 250, 100, 30, "Simulacion"),
    (6, 935, 290, 70, 35, "Dinero"),
    (6, 5, 100, 120, 35, "Ataque Combo"),
    # Fila 7: Combat (ya esta en espanol "Combate", no tocar)
]

cf = load(SRC)
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


# Cargar todas las texturas
images = {}
for r in cf.rows:
    images[r["id"]] = Image.open(__import__("io").BytesIO(cf.plain(r)))

# Aplicar regiones
for (row, x, y, w, h, text) in REGIONS:
    img = images[row]
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
    print("row %d: %r en (%d,%d) %dx%d bg=%s" % (row, text, x, y, w, h, bg))

# Guardar DDS y reconstruir
import shutil
new_files = {}
for r in cf.rows:
    img = images[r["id"]]
    dds_path = os.path.join(WORK, "row_%02d.dds" % r["id"])
    img.save(dds_path, format="DDS")
    with open(dds_path, "rb") as f:
        blob = bytearray(f.read())
    # usar el original para las flags del header DDS
    orig_cf = load(BAK)
    orig_flags = struct.unpack_from("<I", orig_cf.plain(r)[:12], 8)[0]
    struct.pack_into("<I", blob, 8, orig_flags)
    blob = bytes(blob)
    # recomprimir
    from srwv_crypto import encrypt_data
    from crilayla_compress_fast import compress
    enc = encrypt_data(blob)
    comp = compress(enc)
    new_files[r["id"]] = (comp, len(blob))
    print("fila %d: orig=%d new=%d" % (r["id"], r["size"], len(comp)))

# Rebuild CPK (toc format)
raw = bytearray(cf.cpk.raw if False else open(SRC, "rb").read())
# Use the build logic from layout_image_build.py
cpk = cf.cpk
align = cpk.align
content = bytearray()
new_offsets = {}
for r in cf.rows:
    comp, ex = new_files[r["id"]]
    new_offsets[r["id"]] = cpk.content_offset + len(content)
    content += comp
    while len(content) % align:
        content.append(0)

# Update toc
raw = bytearray(open(SRC, "rb").read())
toc = cpk.toc
for rr in range(toc.rows_count):
    d = toc.row(rr)
    rid = d["ID"]
    if rid in new_offsets:
        off_fs = cpk.cell_offset(toc, "FileSize", rr)
        off_fo = cpk.cell_offset(toc, "FileOffset", rr)
        struct.pack_into(">I", raw, off_fs, len(new_files[rid][0]))
        struct.pack_into(">Q", raw, off_fo, new_offsets[rid] - cpk.toc_offset)

# Update header
header = cpk.header
hrow = 0
off_cs = cpk.cell_offset(header, "ContentSize", hrow)
struct.pack_into(">Q", raw, off_cs, len(content))
# EnabledPackedSize
off_ep = cpk.cell_offset(header, "EnabledPackedSize", hrow)
old_ep = struct.unpack_from(">Q", raw, off_ep)[0]
old_packed_sum = sum(r["size"] for r in cf.rows)
new_packed_sum = sum(len(new_files[r["id"]][0]) for r in cf.rows)
struct.pack_into(">Q", raw, off_ep, old_ep + (new_packed_sum - old_packed_sum))
# EtocOffset
off_eo = cpk.cell_offset(header, "EtocOffset", hrow)
struct.pack_into(">Q", raw, off_eo, cpk.content_offset + len(content))

# Build output
content_start = cpk.content_offset
etoc_start = cpk.etoc_offset
prefix = bytes(raw[:content_start])
suffix = bytes(raw[etoc_start:])
out = bytearray(prefix) + content + suffix

with open(OUT, "wb") as f:
    f.write(out)
print("escrito", OUT, len(out))

# verify
chk = load(OUT)
for r in chk.rows:
    pt = chk.plain(r)
    print("fila %d: ex=%d len=%d igual=%s" % (r["id"], r["ex"], len(pt), r["ex"] == len(pt)))
