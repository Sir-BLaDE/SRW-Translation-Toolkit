"""
lt00.py - Parser y constructor del fichero LT00 (tabla de textos de interfaz).

Formato (descifrado), verificado sobre LT00_EN.cpk / B_LT00_EN.cpk:

    +0x00  'BLTU' + 11 u32 de cabecera
           [6]  offset del blob de textos      (0x30)
           [7]  offset del final del blob      (ultima cadena + 1)
           [8]  offset de la tabla de offsets
           [9]  numero de cadenas
           [10] offset de la tabla de IDs
           [11] numero de entradas de IDs

    blob de textos: cadenas UTF-8 terminadas en \\0, concatenadas desde [6]
    tabla de offsets: [9] u32, relativos al inicio del blob
    tabla de IDs: [11] entradas de 32 bytes: u32 indice, u32 flag, u32 id, 20 bytes
"""

import struct

HEADER_WORDS = 12
ENTRY_SIZE = 32


class Lt00:
    def __init__(self, data):
        if data[:4] != b"BLTU":
            raise ValueError("LT00: falta el magic BLTU")
        self.raw = data
        self.header = list(struct.unpack_from("<12I", data, 0))
        self.blob_start = self.header[6] or 0x30
        self.blob_end = self.header[7]
        self.off_start = self.header[8]
        self.count = self.header[9]
        self.id_start = self.header[10]
        self.id_count = self.header[11]
        self.strings = []
        pos = self.blob_start
        for i in range(self.count):
            nul = data.find(b"\0", pos)
            if nul < 0:
                nul = len(data)
            self.strings.append(data[pos:nul].decode("utf-8", "replace"))
            pos = nul + 1
        self.ids = []
        for i in range(self.id_count):
            off = self.id_start + i * ENTRY_SIZE
            if off + ENTRY_SIZE > len(data):
                break
            a, b, c = struct.unpack_from("<3I", data, off)
            self.ids.append((a, b, c))

    def entry_index_to_string(self, idx):
        if 0 <= idx < len(self.strings):
            return self.strings[idx]
        return None

    def build(self, new_strings=None):
        strings = new_strings if new_strings is not None else self.strings
        if len(strings) != self.count:
            raise ValueError(f"LT00: se esperaban {self.count} cadenas, hay {len(strings)}")

        # 1. blob + tabla de offsets
        blob = bytearray()
        offsets = []
        for s in strings:
            offsets.append(len(blob))
            blob += s.encode("utf-8") + b"\0"

        header = list(self.header)
        header[6] = self.blob_start
        header[7] = self.blob_start + len(blob)
        off_start = (header[7] + 15) & ~15
        header[8] = off_start
        header[9] = len(strings)
        id_start = (off_start + 4 * len(strings) + 15) & ~15
        header[10] = id_start
        header[11] = self.id_count

        out = bytearray(struct.pack("<12I", *header))
        if len(out) < self.blob_start:
            out += b"\0" * (self.blob_start - len(out))
        out += blob
        if len(out) < off_start:
            out += b"\0" * (off_start - len(out))
        for o in offsets:
            out += struct.pack("<I", o)
        if len(out) < id_start:
            out += b"\0" * (id_start - len(out))
        for (a, b, c) in self.ids:
            out += struct.pack("<3I", a, b, c) + b"\0" * (ENTRY_SIZE - 12)
        return bytes(out)


def load(data):
    return Lt00(data)
