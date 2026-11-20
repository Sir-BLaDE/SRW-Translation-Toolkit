import glob,os,re,pytesseract
from PIL import Image,ImageEnhance
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_prologue_v6/f*.png')):
    im=Image.open(f); w,h=im.size
    # la narracion suele estar abajo; probar mitad inferior y luego toda
    for name,region in [('bottom',(0,int(h*0.45),w,h)),('full',(0,0,w,h))]:
        r=ImageEnhance.Contrast(im.crop(region)).enhance(2.0)
        t=' '.join(pytesseract.image_to_string(r,config='--psm 6').split())
        if re.search(r'[áéíóúñ¿¡]|Federación|gamillan|humanidad|Yamato|Plutón|espacio|noviembre|tierra|Luna',t,re.I):
            print(os.path.basename(f),name+':',t[:200])
            break
