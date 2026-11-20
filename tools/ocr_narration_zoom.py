import glob,os,pytesseract,re
from PIL import Image,ImageEnhance,ImageFilter,ImageOps
pytesseract.pytesseract.tesseract_cmd=r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config=r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'
files=[f for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_fromlaunch_v6/f*.png')) if 12<=int(os.path.basename(f)[1:4])<=19]
for f in files:
    im=Image.open(f); w,h=im.size
    print('\n##',os.path.basename(f),'size',w,h)
    for name,region in [('mid',(0,int(h*0.30),w,int(h*0.75))),('lower',(0,int(h*0.55),w,int(h*0.9))),('full',(0,0,w,h))]:
        r=im.crop(region)
        r=r.resize((r.width*2,r.height*2))
        g=ImageOps.grayscale(r)
        g=ImageEnhance.Contrast(g).enhance(2.5)
        g=g.filter(ImageFilter.SHARPEN)
        for psm in [6,11]:
            t=' '.join(pytesseract.image_to_string(g,config=f'--psm {psm}').split())
            t=re.sub(r'[^\w\sáéíóúñ¿¡.,!?()\-:;\'"]',' ',t); t=' '.join(t.split())
            if re.search(r'[áéíóúñ]|Federación|gamillan|humanidad|Yamato|Plutón|espacio|Nov|2199|Nuevo|Siglo|Tierra|Luna|viaje|destino',t,re.I):
                print(' ',name,'psm',str(psm)+':',t[:220])
