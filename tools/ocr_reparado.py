import glob, os, re, sys
import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

tag = sys.argv[1] if len(sys.argv) > 1 else 'reparado_op'
files = sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_%s/f*.png' % tag))
print('capturas:', len(files))
for f in files:
    if not any(x in os.path.basename(f) for x in ('f005.png','f010.png','f015.png','f020.png','f025.png','f030.png','f035.png','f040.png','f045.png')):
        continue
    im = Image.open(f)
    w, h = im.size
    for name, region in [('bottom', (0, int(h*0.5), w, h)), ('full', (0, 0, w, h))]:
        r = ImageEnhance.Contrast(im.crop(region)).enhance(2.0)
        t = pytesseract.image_to_string(r, config='--psm 6')
        t = ' '.join(t.split())
        t = re.sub(r'[^\w\sáéíóúñ¿¡.,!?()\-:;\'"]', ' ', t)
        t = ' '.join(t.split())
        if len(t) > 8:
            print(os.path.basename(f), name + ':', t[:220])
            break
