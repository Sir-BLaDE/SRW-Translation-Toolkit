"""ocr_frames.py - OCR de los frames de la intro para localizar 'Yamato' y simbolos."""
import os,glob,re,sys
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
d=r'C:/Dev/Default Project/srwv/tools/_intro_v2'
for f in sorted(glob.glob(d+r'/f*.png')):
    im=Image.open(f)
    # crop a la mitad inferior donde suelen ir los subtitulos
    w,h=im.size
    regions={'full':(0,0,w,h),'bottom':(0,int(h*0.55),w,h)}
    text=''
    for name,box in regions.items():
        r=im.crop(box)
        r=ImageEnhance.Contrast(r).enhance(1.6)
        try: text+=' '+pytesseract.image_to_string(r,config='--psm 6')
        except Exception as e: text+=' ERR '+str(e)[:30]
    hits=[x for x in ['Yamato','YAMATO','amato','¥','Yen','$','?'] if x in text]
    clean=' '.join(text.split())
    if hits or len(clean)>10:
        print('%s [%s]: %s'%(os.path.basename(f),','.join(hits),clean[:220]))
