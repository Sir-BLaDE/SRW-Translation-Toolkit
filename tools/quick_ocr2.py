import glob, os, re, sys
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

tag = sys.argv[1]
for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/tools/_intro_%s/f*.png' % tag)):
    im = Image.open(f).convert('RGB')
    w, h = im.size
    crop = im.crop((0, int(h*0.2), w, int(h*0.95))).resize((w*2, int(h*0.75)*2))
    crop = ImageEnhance.Contrast(crop).enhance(2.0).filter(ImageFilter.SHARPEN)
    t = pytesseract.image_to_string(crop, config='--psm 11')
    t = ' '.join(t.split())
    t = re.sub(r'[^\w\sáéíóúñ¿¡.,!?()\-:;\"\']', ' ', t)
    t = ' '.join(t.split())
    print(os.path.basename(f), ':', t[:200])
