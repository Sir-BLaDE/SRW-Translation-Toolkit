"""
blowfish_tables.py - Tablas estandar de Blowfish (P-array y S-boxes),
extraidas del ejecutable de Super Robot Wars V.

El EXE contiene las 4 S-boxes estandar (los hexadecimales de pi) en el
offset 0x42BBD0 y las 18 constantes iniciales del P-array en 0x121972.
"""
import struct

import os
EXE = os.environ.get("SRW_EXE", r"D:\Juegos\-SPARROW-\Super Robot Wars V\SRWV.EXE")
# El init del juego copia 0x1000 bytes a ctx+0x48 desde esta tabla
# (VA 0x14042CFD0 -> offset 0x42BBD0)
SBOX_OFF = 0x42BBD0
PINIT_OFF = 0x121972  # constantes del P-array escritas como inmediatos

# valores de referencia (Blowfish estandar)
S0_CHECK = 0xD1310BA6
S3_LAST = 0x3AC372E6
P0 = 0x243F6A88
P17 = 0x8979FB1B


def load():
    data = open(EXE, "rb").read()
    global SBOX_OFF
    if struct.unpack_from("<I", data, SBOX_OFF)[0] != S0_CHECK:
        # otro EXE (p. ej. SRWX.EXE): localizar la S-box por su primer valor
        SBOX_OFF = data.find(struct.pack("<I", S0_CHECK))
    pinit = list(struct.unpack_from("<18I", data, PINIT_OFF))
    raw = struct.unpack_from("<1024I", data, SBOX_OFF)
    sboxes = [list(raw[i * 256:(i + 1) * 256]) for i in range(4)]
    return sboxes, pinit


SBOXES, PINIT = load()

# P-array inicial estandar de Blowfish (constantes escritas en el init del EXE)
PINIT = [
    0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344, 0xA4093822, 0x299F31D0,
    0x082EFA98, 0xEC4E6C89, 0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
    0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917, 0x9216D5D9, 0x8979FB1B,
]

if __name__ == "__main__":
    print("P[0]  =", hex(PINIT[0]), "P[17] =", hex(PINIT[17]))
    print("S0[0] =", hex(SBOXES[0][0]), "S3[255] =", hex(SBOXES[3][255]))
    ok = (PINIT[0] == P0 and PINIT[17] == P17 and
          SBOXES[0][0] == S0_CHECK and SBOXES[3][255] == S3_LAST)
    print("tablas estandar correctas:", ok)
    if not ok:
        raise SystemExit("las tablas del EXE no son las estandar de Blowfish")
