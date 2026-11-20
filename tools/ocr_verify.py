"""ocr_verify.py - comprueba que 'Yamato¥' ya no aparece en la recaptura."""
import glob,os,re
import pytesseract
from PIL import Image,ImageEnhance
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
d=r'C:/Dev/Default Project/srwv/tools/_intro_verify'
for f in sorted(glob.glob(d+r'/f*.png')):
    im=Image.open(f); w,h=im.size
    txt=''
    for box in [(0,int(h*0.3),w,int(h*0.85)),(0,int(h*0.6),w,h)]:
        r=ImageEnhance.Contrast(im.crop(box)).enhance(1.8)
        txt+=' '+pytesseract.image_to_string(r,config='--psm 11')
    if re.search(r'Yamato|Yam|Sanada|poder de fuego|¥',txt,re.I):
        print('%s: %s'%(os.path.basename(f),' '.join(txt.split())[:280]))
