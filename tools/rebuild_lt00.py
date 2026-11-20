"""Reconstruye LT00_EN.cpk aplicando las traducciones pendientes del menu."""
import shutil
import struct
import sys
import os

from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data, encrypt_data
from crilayla_compress import compress
from srwv_cpkbuild import build_cpk
from lt00 import load

GAME = 'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk'
OUT = 'C:/Dev/Default Project/srwv/outputs/LT00_EN_es.cpk'


def plaintext(path):
    cpk = Cpk(path)
    raw = cpk.read_file(0)
    return cpk, decrypt_data(maybe_decompress(raw))


# traducciones que faltaban (indice -> texto)
FIX = {
    1074: 'BG:Cambio de Brillo',
    1075: 'BG:Cambio de Color',
    1076: 'Cambio de Modo:ordenar Título',
    1077: 'Cambio de Modo:ordenar Datos',
    1078: 'Información:Act/Des',
    1079: '  Sí',
    1081: '¿Salir de esta escena?',
    1082: 'Cambio de cara',
    1190: 'Alc',
}


def main():
    cpk, pt = plaintext(GAME)
    t = load(pt)
    strings = list(t.strings)
    changed = 0
    for idx, new in FIX.items():
        if idx < len(strings) and strings[idx] != new:
            strings[idx] = new
            changed += 1
    print('cadenas cambiadas:', changed)

    new_plain = t.build(strings)
    print('plain original', len(pt), '-> nuevo', len(new_plain))

    enc = encrypt_data(new_plain)
    blob = compress(enc)
    print('blob CRILAYLA', len(blob), '(original', cpk.file_list()[0]['size'], ')')

    out = build_cpk(cpk, {0: blob}, {0: len(new_plain)})
    open(OUT, 'wb').write(out)
    print('CPK escrito', len(out), '->', OUT)

    # verificacion completa de ida y vuelta
    c2 = Cpk(OUT)
    raw2 = c2.read_file(0)
    pt2 = decrypt_data(maybe_decompress(raw2))
    t2 = load(pt2)
    print('verificacion: cadenas', len(t2.strings), 'cambio aplicado:',
          t2.strings[1081] == FIX[1081], '|', repr(t2.strings[1074]))
    print('diagnostico:', c2.diagnose())


if __name__ == '__main__':
    main()
