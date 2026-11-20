import glob, os, re, sys
import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

tag = sys.argv[1]
KEY = re.compile(r'new game|continue|start|load|settings|options|pilot|character|personaje|nuevo|empezar|guardar|salir|quit|select|selecc', re.I)

files = sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_%s/f*.png' % tag))
print('frames', len(files))
for f in files:
    im = Image.open(f)
    w, h = im.size
    # menu suele estar en la parte inferior/izquierda
    crop = im.crop((0, int(h*0.35), int(w*0.6), int(h*0.95)))
    crop = ImageEnhance.Contrast(crop).enhance(2.0)
    t = pytesseract.image_to_string(crop, config='--psm 11')
    t = ' '.join(t.split())
    if KEY.search(t):
        print(os.path.basename(f), ':', t[:250])
