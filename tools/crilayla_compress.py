"""
crilayla_compress.py - Compresor CRILAYLA (LZ77 real) para Super Robot Wars V.

Replica EXACTAMENTE el descompresor de crilayla.py:

  * El lector consume bits en orden: payload[-1] MSB..LSB, payload[-2]..., etc.
  * La salida se escribe HACIA ATRAS, por lo que el primer token del flujo
    corresponde al ULTIMO byte del cuerpo.

Formato:
    +0x00  "CRILAYLA"
    +0x08  u32le  body_size = len(data) - 256
    +0x0C  u32le  comp_size = len(payload)
    +0x10  payload
    ...    prefix (256 bytes) = PRIMEROS 256 bytes de los datos originales

Truco de implementacion: invertimos el cuerpo (body = data[256:]) y comprimimos
hacia adelante con LZ77 clasico.  Una coincidencia a distancia m = offset + 3
(3 <= m <= 8194) en el flujo invertido equivale exactamente a la copia que hace
el descompresor (que avanza hacia atras con read_index = write_index + offset
+ 3).
"""

import struct
from collections import deque

MAGIC = b"CRILAYLA"
HEADER_SIZE = 0x10
PREFIX_SIZE = 0x100
FRONT_PADDING = 8       # bytes de sobra al principio del payload
MAX_DISTANCE = 8194     # offset de 13 bits => m = offset + 3
MIN_MATCH = 3
MAX_MATCH = 4096        # tope practico para no degenerar en runs enormes
MAX_CHAIN = 32          # candidatos por hash


class BitStreamWriter:
    """Acumula bits en el orden en que los lee ReverseBitReader."""

    __slots__ = ("bits",)

    def __init__(self):
        self.bits = []

    def write_bit(self, bit):
        self.bits.append(1 if bit else 0)

    def write(self, value, count):
        bits = self.bits
        for i in range(count - 1, -1, -1):
            bits.append((value >> i) & 1)

    def to_payload(self):
        bits = self.bits
        pad = (-len(bits)) % 8
        if pad:
            bits = bits + [0] * pad
        chunks = bytearray()
        for i in range(0, len(bits), 8):
            b = 0
            for j in range(8):
                b = (b << 1) | bits[i + j]
            chunks.append(b)
        return bytes(reversed(chunks))


def _write_match_length(w, length):
    """Inversa exacta de crilayla._read_match_length (length real >= 3)."""
    v = length - 3
    if v < 3:
        w.write(v, 2)
        return
    if v < 10:
        w.write(3, 2)
        w.write(v - 3, 3)
        return
    v3 = v - 3
    if v3 < 38:
        w.write(3, 2)
        w.write(7, 3)
        w.write(v3 - 7, 5)
        return
    w.write(3, 2)
    w.write(7, 3)
    w.write(31, 5)
    rest = v3 - 38
    while rest >= 255:
        w.write(255, 8)
        rest -= 255
    w.write(rest, 8)


def _pack_match(w, distance, length):
    w.write_bit(1)
    w.write(distance - 3, 13)
    _write_match_length(w, length)


def _compress_rev(rev, match_search=True):
    """LZ77 greedy sobre `rev` (cuerpo invertido), emitido en orden."""
    n = len(rev)
    w = BitStreamWriter()
    heads = {}
    t = 0
    while t < n:
        best_len = 0
        best_m = 0
        if match_search and t + MIN_MATCH <= n:
            key = rev[t] | (rev[t + 1] << 8) | (rev[t + 2] << 16)
            chain = heads.get(key)
            if chain:
                maxl = min(MAX_MATCH, n - t)
                count = 0
                for pos in reversed(chain):
                    m = t - pos
                    if m < MIN_MATCH:
                        continue
                    if m > MAX_DISTANCE:
                        break
                    l = 0
                    # comparacion rapida por bloques
                    while l < maxl and rev[pos + l] == rev[t + l]:
                        l += 1
                    if l > best_len:
                        best_len = l
                        best_m = m
                        if l >= maxl:
                            break
                    count += 1
                    if count >= MAX_CHAIN:
                        break

        if best_len >= MIN_MATCH:
            _pack_match(w, best_m, best_len)
            end = min(t + best_len, n - 2)
            for u in range(t, end):
                key = rev[u] | (rev[u + 1] << 8) | (rev[u + 2] << 16)
                lst = heads.get(key)
                if lst is None:
                    heads[key] = deque([u], maxlen=MAX_CHAIN)
                else:
                    lst.append(u)
            t += best_len
        else:
            w.write_bit(0)
            w.write(rev[t], 8)
            if t + 2 < n:
                key = rev[t] | (rev[t + 1] << 8) | (rev[t + 2] << 16)
                lst = heads.get(key)
                if lst is None:
                    heads[key] = deque([t], maxlen=MAX_CHAIN)
                else:
                    lst.append(t)
            t += 1
    return w


def compress(data, match_search=True):
    """Comprime `data` (incluido su prefijo de 256 bytes) a un bloque CRILAYLA."""
    if len(data) < PREFIX_SIZE:
        raise ValueError("CRILAYLA: el bloque debe tener al menos 256 bytes")
    prefix = data[:PREFIX_SIZE]
    body = data[PREFIX_SIZE:]
    rev = body[::-1]
    w = _compress_rev(rev, match_search=match_search)
    payload = b"\0" * FRONT_PADDING + w.to_payload()
    return MAGIC + struct.pack("<II", len(body), len(payload)) + payload + prefix


def compress_file(src_bytes):
    return compress(src_bytes)


if __name__ == "__main__":
    import os
    import time

    from crilayla import maybe_decompress

    tests = [bytes(range(256)) + b"ABC", bytes(range(256)) * 3,
             bytes(range(256)) + "Ñandú acción ¡hola!".encode("utf-8"),
             b"A" * 5000, (b"La Tierra esta en peligro. " * 300)]
    for t in tests:
        t0 = time.time()
        comp = compress(t)
        dec = maybe_decompress(comp)
        print(f"len={len(t):7} comp={len(comp):7} "
              f"ratio={len(comp)/len(t):.3f} OK={dec == t} "
              f"({time.time()-t0:.2f}s)")

    # fichero real del juego
    real = "D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk"
    if os.path.exists(real):
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from srwv_cpk import Cpk
        raw = Cpk(real).read_file(0)
        original = maybe_decompress(raw)
        t0 = time.time()
        mine = compress(original)
        ok = maybe_decompress(mine) == original
        print("real LT00:", len(original), "-> original", len(raw),
              "| mio", len(mine), "ratio", round(len(mine) / len(raw), 3),
              "OK", ok, f"({time.time()-t0:.2f}s)")
