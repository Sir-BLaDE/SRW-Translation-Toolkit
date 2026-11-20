import glob,os,pytesseract,re
from PIL import Image,ImageEnhance
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_fromlaunch_v6/f*.png')):
    im=Image.open(f); w,h=im.size
    for name,region in [('bottom',(0,int(h*0.5),w,h)),('full',(0,0,w,h))]:
        r=ImageEnhance.Contrast(im.crop(region)).enhance(2.0)
        t=' '.join(pytesseract.image_to_string(r,config='--psm 6').split())
        t=re.sub(r'[^\w\sáéíóúñ¿¡.,!?()\-:;\'"]',' ',t)
        t=' '.join(t.split())
        if len(t)>15:
            print(os.path.basename(f),name+':',t[:180])
            break
