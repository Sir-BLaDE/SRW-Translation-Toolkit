import glob,os,re,pytesseract
from PIL import Image,ImageEnhance
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_es7/f*.png')):
    im=Image.open(f); w,h=im.size
    r=ImageEnhance.Contrast(im.crop((0,int(h*0.35),w,h))).enhance(1.8)
    t=' '.join(pytesseract.image_to_string(r,config='--psm 11').split())
    if re.search(r'[íéáóú¿¡]|Por qu|debes|Amuro|Tobia|Asi',t,re.I):
        print(os.path.basename(f)+': '+t[:230])
