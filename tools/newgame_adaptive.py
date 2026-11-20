# -*- coding: utf-8 -*-
"""Lanzar SRWV, esperar a que aparezca el menu principal por OCR,
pulsar LEFT x3, Enter, y capturar hasta seleccion de personaje.

Uso: python newgame_adaptive.py <tag> [prologue_cpk_o_None]
"""
import ctypes
import glob
import os
import re
import subprocess
import sys
import time

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageGrab

pytesseract.pytesseract.tesseract_cmd = r'C:/Dev/Default Project/srwv/tools/tess/tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "C:/Dev/Default Project/srwv/tools/tess/tessdata"'

GAME = r'D:/Juegos/-SPARROW-/Super Robot Wars V'
PROLOGUE = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
ORIG = r'C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk'
tag = sys.argv[1]
new_prologue = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].lower() != 'none' else None
out = r'C:/Dev/Default Project/srwv/tools/_intro_%s' % tag
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*.png')):
    os.remove(f)

user32 = ctypes.windll.user32
VK = {'ENTER': 0x0D, 'LEFT': 0x25, 'RIGHT': 0x27, 'UP': 0x26, 'DOWN': 0x28}

def key(name):
    user32.keybd_event(VK[name], 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK[name], 0, 2, 0)
    print('  key', name, flush=True)

def focus_game():
    # FindWindow por titulo
    hwnd = user32.FindWindowW(None, 'Super Robot Wars V')
    if not hwnd:
        # buscar cualquier ventana de SRWV
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        found = []
        def cb(h, l):
            length = user32.GetWindowTextLengthW(h)
            if length:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(h, buf, length + 1)
                if 'Robot' in buf.value or 'SRWV' in buf.value:
                    found.append(h)
            return True
        user32.EnumWindows(EnumWindowsProc(cb), 0)
        if found:
            hwnd = found[0]
    if hwnd:
        user32.ShowWindow(hwnd, 9)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.3)
    return hwnd

def shot(n, label=''):
    im = ImageGrab.grab()
    p = os.path.join(out, 'f%03d_%s.png' % (n, label))
    im.save(p)
    return im

def ocr_menu(im):
    w, h = im.size
    crop = im.crop((0, int(h*0.4), w, h)).convert('RGB')
    crop = ImageEnhance.Contrast(crop).enhance(2.5)
    t = pytesseract.image_to_string(crop, config='--psm 11')
    t = ' '.join(t.split())
    low = t.lower()
    # el menu tiene Settings, Library, Continue, Start
    score = sum(1 for k in ('settings', 'library', 'continue', 'start', 'config') if k in low)
    press = 'press any' in low or 'pulse' in low or 'pressyan' in low
    return score, t, press

# instalar variante si se pide
if new_prologue:
    import shutil
    shutil.copy2(new_prologue, PROLOGUE)
    print('instalado', new_prologue, flush=True)
else:
    import shutil
    shutil.copy2(ORIG, PROLOGUE)
    print('instalado ORIGINAL', flush=True)

subprocess.Popen([os.path.join(GAME, 'SRWV.EXE')], cwd=GAME)
print('lanzado', flush=True)
time.sleep(6)
focus_game()

# esperar a que aparezca el menu principal
menu_frame = None
pressed = False
for i in range(1, 91):
    im = shot(i, 'wait')
    score, t, press = ocr_menu(im)
    if score >= 2:
        print('MENU detectado en f%d: %s' % (i, t[:160]), flush=True)
        menu_frame = i
        break
    if press and not pressed:
        key('ENTER')
        pressed = True
        print('ENTER en pantalla de titulo f%d' % i, flush=True)
        time.sleep(2)
    if i % 5 == 0:
        print('f%d score=%d press=%s: %s' % (i, score, press, t[:100]), flush=True)
    time.sleep(1)

if not menu_frame:
    print('NO SE DETECTO MENU', flush=True)
    sys.exit(2)

time.sleep(1)
n = menu_frame + 100
for _ in range(3):
    key('LEFT')
    time.sleep(0.4)
shot(n, 'after_lefts')
key('ENTER')
time.sleep(3)
shot(n+1, 'after_start')
key('ENTER')
time.sleep(3)
shot(n+2, 'after_mode')
for j in range(1, 21):
    time.sleep(1)
    shot(n+2+j, 'charselect')
    if glob.glob(os.path.join(GAME, '*.dmp')):
        pass
print('capturas', len(glob.glob(os.path.join(out, '*.png'))), flush=True)
