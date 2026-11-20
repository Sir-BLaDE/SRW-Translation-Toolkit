import glob, os, re, sys
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

tag = sys.argv[1]
a = int(sys.argv[2])
b = int(sys.argv[3])
for n in range(a, b + 1):
    p = r'C:/Dev/Default Project/srwv/tools/_intro_%s/f%03d.png' % (tag, n)
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert('RGB')
    w, h = im.size
    crop = im.crop((int(w*0.05), int(h*0.45), int(w*0.75), int(h*0.95)))
    crop = crop.resize((crop.width*4, crop.height*4))
    crop = ImageEnhance.Contrast(crop).enhance(2.0).filter(ImageFilter.SHARPEN)
    print('=== f%03d ===' % n)
    for psm in (6, 11):
        t = pytesseract.image_to_string(crop, config='--psm %d' % psm)
        t = ' '.join(t.split())
        if t:
            print(' psm%d: %s' % (psm, t[:400]))
