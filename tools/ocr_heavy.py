import sys
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

path = sys.argv[1]
im = Image.open(path).convert('RGB')
w, h = im.size
print('size', w, h)
for name, box in [
    ('full', (0, 0, w, h)),
    ('left', (0, int(h*0.2), int(w*0.45), int(h*0.9))),
    ('right', (int(w*0.5), int(h*0.2), w, int(h*0.9))),
    ('center', (int(w*0.2), int(h*0.25), int(w*0.8), int(h*0.8))),
]:
    crop = im.crop(box).resize(((box[2]-box[0])*3, (box[3]-box[1])*3))
    crop = ImageEnhance.Contrast(crop).enhance(2.5).filter(ImageFilter.SHARPEN)
    for psm in (3, 6, 11):
        t = pytesseract.image_to_string(crop, config='--psm %d' % psm)
        t = ' '.join(t.split())
        if t:
            print(name, psm, ':', t[:300])
