# -*- coding: utf-8 -*-
"""Extrae las imagenes DDS de PrologueImage.cpk a PNG para OCR/revision."""
import io
import os
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from PIL import Image

SRC = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/COMMON/PrologueImage.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/prologue_images"
os.makedirs(OUT, exist_ok=True)
c = load(SRC)
for r in c.rows:
    pt = c.plain(r)
    img = Image.open(io.BytesIO(pt))
    path = os.path.join(OUT, "row_%02d.png" % r["id"])
    img.save(path)
    print("id=%-2s %dx%d %s -> %s" % (r["id"], img.size[0], img.size[1], img.mode, path))
print("total", len(c.rows))
