"""
srwv_cpk.py - Lector (y reparador) de archivos CPK de CRI Middleware usados por
Super Robot Wars V / X (PC Steam).

Estructura:

    +0x00  char[4]  "CPK "
    +0x04  u32      version (0xFF)        (little endian)
    +0x08  u32      tamaño de la tabla @UTF de cabecera
    +0x0C  u32      reservado (0)
    +0x10  @UTF     tabla CpkHeader (1 fila)
    ...    frames TOC/ETOC/ITOC y contenido de los ficheros

Los ficheros dentro del CPK pueden ir comprimidos con CRILAYLA y cifrados
con Blowfish (variante de B.B. Studio, clave "SRVW Steam Game").
"""

import os
import struct

from cri_utf import UtfTable

try:
    from Cryptodome.Cipher import Blowfish
except ImportError:  # pragma: no cover
    from Crypto.Cipher import Blowfish

KEY_SRWV = b"SRVW Steam Game"
KEY_SRVX = b"SRVX Steam Game"


def blowfish_decrypt(data, key=KEY_SRWV):
    """Descifra bloques Blowfish ECB estandar (no es el del juego)."""
    if len(data) % 8:
        data = data + b"\0" * (8 - len(data) % 8)
    return Blowfish.new(key, Blowfish.MODE_ECB).decrypt(data)


class CpkEntry:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        return (f"<Entry id={getattr(self, 'id', None)} size={getattr(self, 'size', 0)} "
                f"off={getattr(self, 'offset', 0)}>")


class Cpk:
    """Lector de CPK con informacion de offsets para poder parchear."""

    def __init__(self, path=None, raw=None):
        if raw is not None:
            self.path = "<mem>"
            self.raw = raw
        else:
            self.path = path
            with open(path, "rb") as f:
                self.raw = f.read()
        self._parse()

    # -- cabecera ---------------------------------------------------
    def _parse(self):
        d = self.raw
        if d[:4] != b"CPK ":
            raise ValueError("no es un CPK (magic=%r)" % d[:4])
        self.version = struct.unpack_from("<I", d, 0x04)[0]
        utf_size = struct.unpack_from("<I", d, 0x08)[0]
        self.header_base = 0x10
        self.header = UtfTable(d[0x10:0x10 + utf_size], base=0x10)
        h = self.header.row(0)
        self.h = h
        self.content_offset = h["ContentOffset"]
        self.content_size = h["ContentSize"]
        self.files_count = h["Files"]
        self.align = h["Align"] or 16
        self.toc_offset = h["TocOffset"]
        self.toc_size = h["TocSize"]
        self.etoc_offset = h["EtocOffset"]
        self.etoc_size = h["EtocSize"]
        self.itoc_offset = h["ItocOffset"]
        self.itoc_size = h["ItocSize"]
        self._toc = None
        self._itoc = None
        self._itoc_info = None

    # -- tablas -----------------------------------------------------
    def _load_table(self, offset, size):
        if offset in (0, 0xFFFFFFFFFFFFFFFF) or size == 0:
            return None
        blob = self.raw[offset:offset + size]
        if not blob:
            return None
        if blob[:4] == b"@UTF":
            return UtfTable(blob, base=offset)
        if len(blob) >= 16 and blob[:4] in (b"TOC ", b"TOC\x00", b"ETOC", b"ITOC", b"GTOC", b"HTOC"):
            idx = blob.find(b"@UTF", 0, 64)
            if idx >= 0:
                inner_size = struct.unpack_from("<I", blob, 8)[0]
                inner = blob[idx:idx + inner_size]
                if inner[:4] == b"@UTF":
                    return UtfTable(inner, base=offset + idx)
        return None

    @property
    def toc(self):
        if self._toc is None:
            self._toc = self._load_table(self.toc_offset, self.toc_size)
        return self._toc

    @property
    def itoc(self):
        if self._itoc is None:
            self._itoc = self._load_table(self.itoc_offset, self.itoc_size)
        return self._itoc

    @property
    def itoc_info(self):
        """Tabla CpkItocInfo (fila 0) y sus sub-tablas DataL / DataH."""
        if self._itoc_info is None:
            info = {}
            itoc = self.itoc
            if itoc is not None:
                row = itoc.row(0)
                info["row"] = row
                for name, val in row.items():
                    if isinstance(val, (bytes, bytearray)) and val[:4] == b"@UTF":
                        base = self._vldata_offset(itoc, name)
                        sub = UtfTable(bytes(val), base=base if base is not None else 0)
                        info[sub.name] = sub
                        # offset real de la sub-tabla dentro del fichero
                        info[sub.name + "_offset"] = base
            self._itoc_info = info
        return self._itoc_info

    def _vldata_offset(self, table, name):
        """Offset absoluto en el fichero de una columna vldata."""
        col = table.column(name)
        if col is None or col.row_offset is None:
            return None
        off = table.base + table.rows_offset + col.row_offset
        doff = struct.unpack_from(">I", self.raw, off)[0]
        return table.base + table.data_offset + doff

    # -- ficheros ---------------------------------------------------
    def file_list(self):
        """Lista de (id, offset_absoluto, FileSize, ExtractSize)."""
        info = self.itoc_info
        out = []
        if not info:
            return out
        off = self.content_offset
        for name in ("CpkItocL", "CpkItocH"):
            tab = info.get(name)
            if tab is None:
                continue
            for r in range(tab.rows_count):
                row = tab.row(r)
                size = row["FileSize"]
                out.append({
                    "id": row["ID"],
                    "table": name,
                    "row": r,
                    "offset": off,
                    "size": size,
                    "extract_size": row["ExtractSize"],
                })
                off += (size + (self.align - 1)) & ~(self.align - 1)
        return out

    def read_file(self, fid):
        for f in self.file_list():
            if f["id"] == fid:
                return self.raw[f["offset"]:f["offset"] + f["size"]]
        raise KeyError(fid)

    def cell_offset(self, table, column, row=0):
        """Offset absoluto del byte donde se guarda el valor de una celda."""
        col = table.column(column)
        if col is None:
            raise KeyError(column)
        if col.flag & 0x20:      # constante en el esquema
            return table.base + col.default_offset
        return table.base + table.rows_offset + row * table.row_width + col.row_offset

    def diagnose(self):
        """Comprueba la coherencia del CPK (para detectar construcciones malas)."""
        problems = []
        info = self.itoc_info
        files = self.file_list()
        stored = sum(f["size"] for f in files)
        extracted = sum(f["extract_size"] for f in files)
        h = self.h
        if h.get("ContentSize") is not None:
            expected = sum((f["size"] + (self.align - 1)) & ~(self.align - 1) for f in files)
            if self.content_size != expected:
                problems.append(f"ContentSize={self.content_size} pero los ficheros alineados ocupan {expected}")
        if h.get("EnabledDataSize") is not None:
            if h["EnabledDataSize"] != stored:
                problems.append(f"EnabledDataSize={h['EnabledDataSize']} pero los ficheros ocupan {stored}")
        if h.get("EnabledPackedSize") is not None:
            if h["EnabledPackedSize"] != extracted:
                problems.append(f"EnabledPackedSize={h['EnabledPackedSize']} pero el tamano descomprimido es {extracted}")
        if info:
            row = info.get("row", {})
            for k in ("FilesL", "FilesH"):
                v = row.get(k)
                tab = info.get("CpkItocL" if k == "FilesL" else "CpkItocH")
                if tab is not None and v is not None and v != tab.rows_count:
                    problems.append(f"{k}={v} pero la tabla tiene {tab.rows_count} filas")
        if h.get("FileSize") is not None and h["FileSize"] != len(self.raw):
            problems.append(f"FileSize={h['FileSize']} pero el fichero mide {len(self.raw)}")
        if self.content_offset + stored > len(self.raw):
            problems.append("el contenido se sale del fichero")
        return problems


def open_cpk(path):
    return Cpk(path)


if __name__ == "__main__":
    import sys
    c = Cpk(sys.argv[1])
    print("version   :", c.version)
    print("Tvers     :", c.h.get("Tvers"))
    print("content   :", c.content_offset, c.content_size)
    print("files     :", c.files_count)
    print("align     :", c.align)
    print("ITOC      :", c.itoc_offset, c.itoc_size)
    for f in c.file_list():
        print("   ", f)
    probs = c.diagnose()
    print("problemas :", probs if probs else "ninguno")
