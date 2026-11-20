"""ocr_frames2.py - OCR de la captura larga, enfocado en Yamato y creditos."""
import os,glob,re
import pytesseract
from PIL import Image,ImageEnhance
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
d=r'C:/Dev/Default Project/srwv/tools/_intro_long'
for f in sorted(glob.glob(d+r'/f*.png')):
    im=Image.open(f); w,h=im.size
    strs=[]
    for name,box in [('full',(0,0,w,h)),('mid',(0,int(h*0.3),w,int(h*0.8))),('bot',(0,int(h*0.6),w,h))]:
        r=ImageEnhance.Contrast(im.crop(box)).enhance(1.8)
        try: strs.append(pytesseract.image_to_string(r,config='--psm 11'))
        except Exception: pass
    text=' '.join(' '.join(s.split()) for s in strs)
    if re.search(r'Yamato|Yam|Kira|voice|cast|Seiyuu|Hoshi|credit|2199|¥|\$\s*',text,re.I):
        print('%s: %s'%(os.path.basename(f),text[:300]))
