import sys
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

path = sys.argv[1]
im = Image.open(path).convert('RGB')
w, h = im.size
print('size', w, h)
# menu suele estar en la columna izquierda / centro-izquierda
for boxname, box in [
    ('full', (0, 0, w, h)),
    ('left', (0, int(h*0.3), int(w*0.5), h)),
    ('centerleft', (int(w*0.1), int(h*0.35), int(w*0.6), int(h*0.95))),
]:
    crop = im.crop(box)
    crop = crop.resize((crop.width*3, crop.height*3))
    crop = ImageEnhance.Contrast(crop).enhance(2.2).filter(ImageFilter.SHARPEN)
    print('---', boxname, '---')
    d = pytesseract.image_to_data(crop, config='--psm 11', output_type=pytesseract.Output.DICT)
    for i, txt in enumerate(d['text']):
        txt = txt.strip()
        if len(txt) < 3:
            continue
        try:
            conf = int(d['conf'][i])
        except (ValueError, TypeError):
            continue
        if conf < 10:
            continue
        x, y, bw, bh = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
        # devolver a coordenadas originales
        ox = box[0] + x/3
        oy = box[1] + y/3
        print('  %-18s conf=%3d  x=%4d y=%4d  (orig x=%4d y=%4d)' % (txt[:18], conf, x, y, ox, oy))
