import sys
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

path = sys.argv[1]
im = Image.open(path).convert('RGB')
w, h = im.size
regions = {
    'bottom': (0, int(h*0.55), w, h),
    'bottom_left': (0, int(h*0.5), int(w*0.5), h),
    'bottom_right': (int(w*0.5), int(h*0.5), w, h),
    'left_strip': (0, int(h*0.25), int(w*0.35), int(h*0.9)),
}
for name, box in regions.items():
    crop = im.crop(box)
    crop = crop.resize((crop.width*2, crop.height*2))
    crop = ImageEnhance.Contrast(crop).enhance(2.0).filter(ImageFilter.SHARPEN)
    for psm in (6, 11):
        t = pytesseract.image_to_string(crop, config='--psm %d' % psm)
        t = ' '.join(t.split())
        if len(t) > 3:
            print(name, psm, ':', t[:250])
