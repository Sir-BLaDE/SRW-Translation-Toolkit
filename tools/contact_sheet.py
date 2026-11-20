"""contact_sheet.py - rejilla de miniaturas para localizar pantallas con dialogo."""
import os
import sys
from PIL import Image, ImageDraw

folder = sys.argv[1]
files = sorted(f for f in os.listdir(folder) if f.endswith('.png'))[:int(sys.argv[2]) if len(sys.argv) > 2 else 99]
tw, th = 384, 216
cols = 5
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * tw, rows * th), (0, 0, 0))
dr = ImageDraw.Draw(sheet)
for i, fn in enumerate(files):
    im = Image.open(os.path.join(folder, fn)).convert('RGB').resize((tw, th))
    x, y = (i % cols) * tw, (i // cols) * th
    sheet.paste(im, (x, y))
    dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(255, 0, 0))
    dr.text((x + 4, y + 4), fn, fill=(255, 255, 0))
out = os.path.join(folder, '_hoja.png')
sheet.save(out)
print(out, sheet.size)
