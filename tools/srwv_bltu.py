"""
srwv_bltu.py - Formato de tablas de texto "BLTU" de Super Robot Wars V.

Estructura del fichero (fichero 1 de CMN00.CPK, descifrado):

    Cabecera: 12 u32 (version, ... offsets de tablas ...)

    A partir de un offset (0x30) hay una secuencia de *bloques*:

        u32      count        numero de cadenas del bloque
        u32[]    offsets      offsets de cada cadena dentro del blob
        blob     bytes        cadenas concatenadas, terminadas en \0
        relleno  hasta el siguiente multiple de 16

    Los offsets son relativos al inicio del blob.  El relleno de ceros
    permite localizar el siguiente bloque: el final del blob se calcula
    con la longitud de la ultima cadena y se alinea a 16 bytes.
"""

import struct

ALIGN = 16


class BltuChunk:
    def __init__(self, index, offset, count, offsets, blob, strings):
        self.index = index
        self.offset = offset
        self.count = count
        self.offsets = offsets
        self.blob = blob
        self.strings = strings

    def __repr__(self):
        return f"<BltuChunk #{self.index} off=0x{self.offset:X} count={self.count}>"


class BltuTable:
    def __init__(self, data, align=ALIGN):
        self.data = data
        self.align = align
        if len(data) < 0x30:
            raise ValueError("BLTU: fichero demasiado corto")
        self.header = list(struct.unpack_from("<12I", data, 0))
        self.chunks = []
        self._parse()

    # -- utilidades ------------------------------------------------
    def _align(self, v):
        a = self.align
        return (v + a - 1) & ~(a - 1)

    def _parse(self):
        data = self.data
        pos = self.header[2] if self.header[2] else 0x30
        index = 0
        limit = len(data)
        while pos + 4 <= limit:
            count = struct.unpack_from("<I", data, pos)[0]
            pos += 4
            if count == 0 or count > 0x100000:
                break
            if pos + 4 * count > limit:
                break
            offsets = list(struct.unpack_from(f"<{count}I", data, pos))
            pos += 4 * count
            blob_start = pos
            strings = []
            end = blob_start
            for i, off in enumerate(offsets):
                if blob_start + off >= len(data):
                    break
                nul = data.find(b"\0", blob_start + off)
                if nul < 0:
                    nul = len(data)
                strings.append(data[blob_start + off:nul].decode("utf-8", "replace"))
                end = nul + 1
            self.chunks.append(BltuChunk(index, blob_start - 4 - 4 * count,
                                         count, offsets,
                                         data[blob_start:end], strings))
            index += 1
            pos = self._align(end)
            if pos >= limit:
                break

    # -- acceso ----------------------------------------------------
    def all_strings(self):
        """Lista de (id_global, chunk_index, indice, texto)."""
        out = []
        gid = 0
        for ch in self.chunks:
            for i, s in enumerate(ch.strings):
                out.append((gid, ch.index, i, s))
                gid += 1
        return out

    def __len__(self):
        return sum(c.count for c in self.chunks)


def load(data):
    return BltuTable(data)
