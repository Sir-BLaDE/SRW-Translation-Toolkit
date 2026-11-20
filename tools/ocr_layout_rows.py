import glob, os, re
import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

for f in sorted(glob.glob(r'C:/Dev/Default Project/srwv/outputs/img_LayoutImage/row_*.png')):
    im = Image.open(f).convert('RGB')
    w, h = im.size
    r = ImageEnhance.Contrast(im).enhance(2.0)
    t = pytesseract.image_to_string(r, config='--psm 11')
    t = ' '.join(t.split())
    t = re.sub(r'[^\w\sáéíóúñ¿¡.,!?()\-:;\'"]', ' ', t)
    t = ' '.join(t.split())
    print(os.path.basename(f), '(%dx%d)' % (w, h), ':', t[:300])
