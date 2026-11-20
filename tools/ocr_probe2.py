import glob
import os
import sys

import pytesseract
from PIL import Image, ImageEnhance, ImageOps

pytesseract.pytesseract.tesseract_cmd = r"C:/Dev/Default Project/srwv/tools/tess/tesseract.exe"
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

folder = sys.argv[1] if len(sys.argv) > 1 else r"C:/Dev/Default Project/srwv/tools/_intro_fg_ok"
for f in sorted(glob.glob(os.path.join(folder, "f*.png"))):
    im = Image.open(f).convert("L")
    w, h = im.size
    print("==", os.path.basename(f), im.size, "extrema", im.getextrema())
    regions = {
        "full": (0, 0, w, h),
        "top": (0, 0, w, int(h * 0.4)),
        "mid": (0, int(h * 0.3), w, int(h * 0.75)),
        "bot": (0, int(h * 0.6), w, h),
    }
    for name, box in regions.items():
        r = ImageEnhance.Contrast(im.crop(box)).enhance(2.2)
        for psm in (6, 11):
            t = " ".join(pytesseract.image_to_string(r, config=f"--psm {psm}").split())
            if len(t) > 12:
                print(f"  {name}/{psm}: {t[:220]}")
                break
