# -*- coding: utf-8 -*-
"""Esperar a que aparezca el menu principal (por huella visual),
pulsar LEFT x3 -> Start, confirmar, y capturar hasta seleccion de personaje.

Uso: python newgame_final.py <tag> [ruta_cpk | ORIG]
"""
import ctypes
import glob
import os
import shutil
import subprocess
import sys
import time

from PIL import Image, ImageChops, ImageGrab, ImageStat

GAME = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
PROLOGUE = os.path.join(GAME, 'Data/AIDDATA/EN/Prologue.cpk')
ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
REF = r'C:/Dev/Default Project/srwv/tools/_intro_menu_240/f145.png'

tag = sys.argv[1]
which = sys.argv[2] if len(sys.argv) > 2 else 'ORIG'
src = ORIG if which.upper() == 'ORIG' else which

out = r'C:/Dev/Default Project/srwv/tools/_intro_%s' % tag
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*.png')):
    os.remove(f)

user32 = ctypes.windll.user32
VK = {'ENTER': 0x0D, 'LEFT': 0x25, 'RIGHT': 0x27, 'UP': 0x26, 'DOWN': 0x28}

def key(name):
    user32.keybd_event(VK[name], 0, 0, 0)
    time.sleep(0.06)
    user32.keybd_event(VK[name], 0, 2, 0)
    print('  key', name, flush=True)

def focus_game():
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    found = []
    def cb(h, l):
        n = user32.GetWindowTextLengthW(h)
        if n:
            buf = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(h, buf, n + 1)
            if 'Robot' in buf.value or 'SRWV' in buf.value:
                found.append(h)
        return True
    user32.EnumWindows(EnumWindowsProc(cb), 0)
    if found:
        user32.ShowWindow(found[0], 9)
        user32.SetForegroundWindow(found[0])
        time.sleep(0.3)
    return found[0] if found else None

ref = Image.open(REF).convert('L').resize((160, 90))

def menu_diff(im):
    small = im.convert('L').resize((160, 90))
    return ImageStat.Stat(ImageChops.difference(ref, small)).mean[0]

def shot(n, label=''):
    im = ImageGrab.grab()
    p = os.path.join(out, 'f%03d_%s.png' % (n, label))
    im.save(p)
    return im

shutil.copy2(src, PROLOGUE)
print('instalado:', src, flush=True)
subprocess.Popen([os.path.join(GAME, 'SRWV.EXE')], cwd=GAME)
print('lanzado', flush=True)
time.sleep(6)
focus_game()

# esperar al menu: pulsar ENTER cuando aparezca "press any button"
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

menu_frame = None
pressed_once = False
for i in range(1, 241):
    im = shot(i, 'wait')
    d = menu_diff(im)
    if d < 30:
        print('MENU detectado en f%d (diff=%.1f)' % (i, d), flush=True)
        menu_frame = i
        break
    # detectar "press any button"
    w, h = im.size
    crop = im.crop((0, int(h*0.4), w, h)).convert('RGB')
    from PIL import ImageEnhance
    crop = ImageEnhance.Contrast(crop).enhance(2.5)
    txt = pytesseract.image_to_string(crop, config='--psm 11').lower().replace(' ', '')
    if ('pressany' in txt or 'pressyan' in txt or 'anybutton' in txt) and not pressed_once and i >= 100:
        print('f%d press-any-button -> ENTER (unico)' % i, flush=True)
        focus_game()
        key('ENTER')
        pressed_once = True
        time.sleep(2)
    if i % 10 == 0:
        print('f%d menu_diff=%.1f' % (i, d), flush=True)
    time.sleep(1)

if not menu_frame:
    print('NO SE DETECTO MENU', flush=True)
    sys.exit(2)

time.sleep(1)
n = menu_frame + 200
for _ in range(3):
    key('LEFT')
    time.sleep(0.45)
shot(n, 'after_lefts')
key('ENTER')
time.sleep(3)
shot(n+1, 'after_start')
key('ENTER')
time.sleep(3)
shot(n+2, 'after_mode')
for j in range(1, 25):
    time.sleep(1)
    shot(n+2+j, 'charselect')
print('capturas', len(glob.glob(os.path.join(out, '*.png'))), flush=True)
print('FIN', flush=True)
