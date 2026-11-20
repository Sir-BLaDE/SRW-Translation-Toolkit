"""Detectar en qué fotograma aparece el menu (Settings/Library/Continue)."""
import glob, os, re, sys
import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

tag = sys.argv[1]
pat = re.compile(r'settings|library|continue|start\s|new game|game start|opciones|config', re.I)
for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_%s/f*.png' % tag)):
    im = Image.open(f).convert('RGB')
    w, h = im.size
    crop = im.crop((0, int(h*0.4), w, h))
    crop = ImageEnhance.Contrast(crop).enhance(2.5)
    t = pytesseract.image_to_string(crop, config='--psm 11')
    t = ' '.join(t.split())
    hit = [m.group(0) for m in pat.finditer(t)]
    print(os.path.basename(f), ('>>> MENU ' + ','.join(hit)) if hit else '', ':', t[:120])
