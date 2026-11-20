# -*- coding: utf-8 -*-
"""Edita las texturas de LayoutImage.cpk: borra el texto ingles y renderiza
el equivalente espanol usando PIL, conservando el formato DDS (RGBA 32-bit)."""
import os
import sys
import struct
import subprocess
import json
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutImage.cpk"
BAK = r"C:/Dev/Default Project/srwv/backup/LayoutImage_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/LayoutImage_es.cpk"
WORK = r"C:/Dev/Default Project/srwv/outputs/layout_image_work"
TESS = r"C:/Dev/Default Project/srwv/tools/tess/tesseract.exe"

# Traducciones de los textos ingleses detectados (OCR) a espanol corto
TR = {
    "Support Defend": "Apoyo Defensa",
    "Supa Defend": "Apoyo Defensa",
    "Support Attack": "Apoyo Ataque",
    "Suppat Attack": "Apoyo Ataque",
    "Second Attack": "Segundo Ataque",
    "Combo Attack": "Ataque Combo",
    "Simulation": "Simulacion",
    "Money": "Dinero",
    "DEF": "DEF",
    "HOT": "CAL",
    "Combat": "Combate",
    "START": "INICIO",
    "Weapon": "Arma",
    "Away": "Lejos",
    "Und": "Ind",
    "GRADE": "GRADO",
    "COREVUP": "COREVUP",
    "SKL": "HAB",
    "Second": "Segundo",
    "Attack": "Ataque",
    "Defend": "Defender",
}

os.makedirs(WORK, exist_ok=True)
if not os.path.exists(BAK):
    import shutil
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

cf = load(SRC)
font_path = r"C:\Windows\Fonts\arialbd.ttf"


def ocr_tsv(img_path):
    out = subprocess.run([TESS, img_path, "stdout", "-l", "eng", "tsv"],
                         capture_output=True, text=True)
    words = []
    for line in out.stdout.splitlines()[1:]:
        cols = line.split("\t")
        if len(cols) < 12:
            continue
        try:
            conf = float(cols[10])
            text = cols[11]
        except (ValueError, IndexError):
            continue
        if conf < 30 or not text.strip():
            continue
        words.append({
            "text": text, "left": int(cols[6]), "top": int(cols[7]),
            "width": int(cols[8]), "height": int(cols[9]), "conf": conf,
        })
    return words


def sample_bg(img, x, y, w, h):
    """Muestrea el color de fondo alrededor de una region de texto."""
    # tomar pixeles en el borde de la region expandida
    pad = 4
    colors = []
    for yy in range(max(0, y - pad), min(img.height, y + h + pad)):
        for xx in range(max(0, x - pad), min(img.width, x + w + pad)):
            if (x - pad <= xx < x or x + w <= xx < x + w + pad or
                y - pad <= yy < y or y + h <= yy < y + h + pad):
                colors.append(img.getpixel((xx, yy)))
    if not colors:
        return (0, 0, 0, 255)
    # mediana por canal
    rs = sorted(c[0] for c in colors)
    gs = sorted(c[1] for c in colors)
    bs = sorted(c[2] for c in colors)
    as_ = sorted(c[3] for c in colors)
    n = len(colors)
    return (rs[n // 2], gs[n // 2], bs[n // 2], as_[n // 2])


def edit_texture(img):
    """Edita una textura: borra textos ingleses y renderiza espanol."""
    tmp = os.path.join(WORK, "_tmp.png")
    img.save(tmp)
    words = ocr_tsv(tmp)
    draw = ImageDraw.Draw(img)
    # agrupar palabras en lineas por proximidad vertical
    # (simplificado: procesar palabra por palabra)
    for w in words:
        txt = w["text"].strip()
        if not txt:
            continue
        # Solo traducir si el texto tiene 3+ caracteres y es una palabra inglesa clara
        if len(txt) < 3:
            continue
        trans = None
        for en, es in TR.items():
            if en.lower() == txt.lower():
                trans = es
                break
        if trans is None:
            continue
        x, y, ww, hh = w["left"], w["top"], w["width"], w["height"]
        # borrar region (rellenar con fondo)
        bg = sample_bg(img, x, y, ww, hh)
        # expandir un poco la region de borrado
        pad = 2
        draw.rectangle([x - pad, y - pad, x + ww + pad, y + hh + pad], fill=bg)
        # renderizar texto espanol
        # ajustar tamano de fuente para que quepa
        font_size = max(8, hh - 2)
        font = ImageFont.truetype(font_path, font_size)
        # medir
        bbox = draw.textbbox((0, 0), trans, font=font)
        tw = bbox[2] - bbox[0]
        # reducir si no cabe
        while tw > ww + 4 and font_size > 6:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), trans, font=font)
            tw = bbox[2] - bbox[0]
        # centrar
        tx = x + (ww - tw) // 2
        ty = y + (hh - (bbox[3] - bbox[1])) // 2 - bbox[1]
        # color del texto: usar color medio de la region original (aproximar negro/blanco)
        # por defecto usar blanco si el fondo es oscuro, negro si es claro
        brightness = (bg[0] + bg[1] + bg[2]) / 3
        text_color = (255, 255, 255, 255) if brightness < 128 else (0, 0, 0, 255)
        draw.text((tx, ty), trans, font=font, fill=text_color)
        print("    traducido: %r -> %r  en (%d,%d) %dx%d" % (txt, trans, x, y, ww, hh))
    return img


new_files = {}
for r in cf.rows:
    img = Image.open(__import__("io").BytesIO(cf.plain(r)))
    print("fila %d: %dx%d" % (r["id"], img.size[0], img.size[1]))
    img2 = edit_texture(img)
    # guardar como DDS (RGBA 32-bit, sin compresion)
    dds_path = os.path.join(WORK, "row_%02d.dds" % r["id"])
    img2.save(dds_path, format="DDS")
    with open(dds_path, "rb") as f:
        blob = bytearray(f.read())
    # parchear dwFlags del header DDS para que coincida con el original
    orig_flags = struct.unpack_from("<I", cf.plain(r), 8)[0]
    struct.pack_into("<I", blob, 8, orig_flags)
    blob = bytes(blob)
    new_files[r["id"]] = (cf.cipher(r, blob), len(cf.plain(r)))
    print("  guardado %s (%d bytes)" % (dds_path, len(blob)))

# reconstruir CPK
from srwv_cpkbuild2 import build_ordered
out_blob = build_ordered(SRC, new_files)
with open(OUT, "wb") as f:
    f.write(out_blob)
print("escrito", OUT, len(out_blob))

# verificar
chk = load(OUT)
print("diag", chk.cpk.diagnose() or "ok")
for r in chk.rows:
    pt = chk.plain(r)
    print("fila %d: ex=%d len=%d igual=%s" % (r["id"], r["ex"], len(pt), r["ex"] == len(pt)))
