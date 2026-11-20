"""
crilayla.py - Descompresor CRILAYLA (CRI Middleware), portado del C++ de
CriCodecs (Youjose) para poder leer los ficheros de los CPK de Super Robot Wars.

Formato:
    +0x00  char[8]  "CRILAYLA"
    +0x08  u32le    tamaño del cuerpo descomprimido
    +0x0C  u32le    tamaño del payload comprimido
    +0x10  payload comprimido (se lee de backwards, LZ77)
    ...    0x100 bytes de prefijo (copiados al principio de la salida)
"""

import struct

MAGIC = b"CRILAYLA"
HEADER_SIZE = 0x10
PREFIX_SIZE = 0x100


class ReverseBitReader:
    """Lee bits desde el final del buffer hacia el principio."""

    def __init__(self, data):
        self.data = data
        self.index = len(data) - 1
        self.bit_count = 0
        self.bit_data = 0

    def read(self, bit_count):
        # El decodificador del juego carga UN byte cada vez (get_next_bits).
        # Cargar de 4 en 4 como antes provocaba un falso fin de flujo cuando
        # quedaban menos de 4 bytes pero los bits necesarios si estaban ahi.
        while self.bit_count < bit_count:
            if self.index < 0:
                raise ValueError("CRILAYLA: fin del flujo de bits")
            self.bit_data = ((self.bit_data << 8) | self.data[self.index]) & 0xFFFFFFFFFFFFFFFF
            self.index -= 1
            self.bit_count += 8
        value = (self.bit_data >> (self.bit_count - bit_count)) & ((1 << bit_count) - 1)
        self.bit_count -= bit_count
        return value


def _read_match_length(reader):
    length = reader.read(2)
    if length < 3:
        return length + 3
    length += reader.read(3)
    if length < 10:
        return length + 3
    length += reader.read(5)
    if length == 41:
        while True:
            ext = reader.read(8)
            length += ext
            if ext != 255:
                break
    return length + 3


def decompress(src):
    """Descomprime un bloque CRILAYLA y devuelve los bytes."""
    if len(src) < HEADER_SIZE + PREFIX_SIZE:
        raise ValueError("CRILAYLA: cabecera invalida")
    if src[:8] != MAGIC:
        raise ValueError("CRILAYLA: magic incorrecto %r" % src[:8])
    body_size = struct.unpack_from("<I", src, 0x08)[0]
    comp_size = struct.unpack_from("<I", src, 0x0C)[0]
    if HEADER_SIZE + comp_size + PREFIX_SIZE > len(src):
        raise ValueError("CRILAYLA: tamaño de payload incoherente")
    payload = src[HEADER_SIZE:HEADER_SIZE + comp_size]
    prefix = src[HEADER_SIZE + comp_size:HEADER_SIZE + comp_size + PREFIX_SIZE]

    output = bytearray(body_size + PREFIX_SIZE)
    output[:PREFIX_SIZE] = prefix
    if body_size == 0:
        return bytes(output)

    reader = ReverseBitReader(payload)
    write_index = len(output) - 1

    def write_byte(b):
        nonlocal write_index
        output[write_index] = b
        write_index -= 1
        return write_index == PREFIX_SIZE - 1

    while write_index >= PREFIX_SIZE:
        marker = reader.read(1)
        if marker == 0:
            literal = reader.read(8)
            if write_byte(literal):
                break
            continue
        offset = reader.read(13)
        length = _read_match_length(reader)
        read_index = write_index + offset + 3
        while length > 0:
            if read_index < PREFIX_SIZE or read_index >= len(output):
                raise ValueError("CRILAYLA: referencia fuera de rango")
            b = output[read_index]
            read_index -= 1
            length -= 1
            if write_byte(b):
                break
    return bytes(output)


def is_crilayla(data):
    return data[:8] == MAGIC


def maybe_decompress(data):
    """Si el bloque es CRILAYLA lo descomprime; si no, lo devuelve tal cual."""
    if is_crilayla(data):
        return decompress(data)
    return data
