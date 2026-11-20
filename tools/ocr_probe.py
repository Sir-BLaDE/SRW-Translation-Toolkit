import glob
import os
import sys

import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r"C:/Dev/Default Project/srwv/tools/tess/tesseract.exe"
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

folder = sys.argv[1] if len(sys.argv) > 1 else r"C:/Dev/Default Project/srwv/tools/_intro_probe_window"
for f in sorted(glob.glob(os.path.join(folder, "f*.png")))[-3:]:
    im = Image.open(f)
    w, h = im.size
    r = ImageEnhance.Contrast(im.crop((0, int(h * 0.4), w, h))).enhance(2.0)
    t = " ".join(pytesseract.image_to_string(r, config="--psm 6").split())
    print(os.path.basename(f), t[:200])
