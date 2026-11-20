"""ocr_es5.py - OCR de la captura es5 para ver texto acentuado."""
import glob,os,re
import pytesseract
from PIL import Image,ImageEnhance
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
d=r'C:/Dev/Default Project/srwv/tools/_intro_es5b'
for f in sorted(glob.glob(d+r'/f*.png')):
    im=Image.open(f); w,h=im.size
    r=ImageEnhance.Contrast(im.crop((0,int(h*0.35),w,h))).enhance(1.8)
    txt=' '.join(pytesseract.image_to_string(r,config='--psm 11').split())
    if re.search(r'[áéíóú¿¡]|Por qu|debes|Tobia|Amuro',txt,re.I):
        print('%s: %s'%(os.path.basename(f),txt[:230]))
