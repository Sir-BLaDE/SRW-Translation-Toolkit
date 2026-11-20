import glob, os, re, sys
import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

tag = sys.argv[1] if len(sys.argv) > 1 else 'menu_es'
files = sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_%s/f*.png' % tag))
print('capturas:', len(files))
for f in files:
    n = int(re.search(r'f(\d+)\.png', os.path.basename(f)).group(1))
    if n > 20:
        continue
    im = Image.open(f)
    w, h = im.size
    for name, region in [('mid', (0, int(h*0.25), w, int(h*0.85))), ('full', (0, 0, w, h))]:
        r = ImageEnhance.Contrast(im.crop(region)).enhance(2.0)
        t = pytesseract.image_to_string(r, config='--psm 11')
        t = ' '.join(t.split())
        t = re.sub(r'[^\w\sáéíóúñ¿¡.,!?()\-:;\'"]', ' ', t)
        t = ' '.join(t.split())
        if len(t) > 10:
            print(os.path.basename(f), name + ':', t[:200])
            break
