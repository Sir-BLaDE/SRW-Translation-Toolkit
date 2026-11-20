"""
cri_utf.py - Lector/editor de tablas @UTF de CRI Middleware.

Formato (big-endian), segun la documentacion de vgmstream (src/util/cri_utf.c):

    +0x00  char[4]  "@UTF"
    +0x04  u32      tamano de la tabla - 8
    +0x08  u16      version (0 o 1)
    +0x0A  u16      offset de las filas - 8
    +0x0C  u32      offset del pool de strings - 8
    +0x10  u32      offset del pool de datos - 8
    +0x14  u32      offset del nombre de la tabla (dentro del pool de strings)
    +0x18  u16      numero de columnas
    +0x1A  u16      ancho de fila
    +0x1C  u32      numero de filas
    +0x20  esquema de columnas:
              u8  info  (nibble alto = flags, nibble bajo = tipo)
              u32be offset del nombre de la columna (en el pool de strings)
              [u32be constante, solo si flag 0x20]

Tipos: 0=u8 1=s8 2=u16 3=s16 4=u32 5=s32 6=u64 7=s64 8=float
       9=double 0xA=string(u32 offset a string) 0xB=vldata(u32 offset+u32 size)
Flags: 0x10=tiene nombre, 0x20=valor por defecto (en el esquema),
       0x40=valor en cada fila, 0x80=indefinido
"""

import struct

COL_FLAG_NAME = 0x10
COL_FLAG_DEFAULT = 0x20
COL_FLAG_ROW = 0x40

TYPE_SIZES = {
    0x00: 1, 0x01: 1,
    0x02: 2, 0x03: 2,
    0x04: 4, 0x05: 4, 0x08: 4, 0x0A: 4,
    0x06: 8, 0x07: 8, 0x09: 8, 0x0B: 8,
    0x0C: 16,
}


class Column:
    __slots__ = ("index", "info", "flag", "type", "name", "name_offset",
                 "row_offset", "default_offset", "default_value")

    def __init__(self, index):
        self.index = index
        self.info = 0
        self.flag = 0
        self.type = 0
        self.name = ""
        self.name_offset = 0
        self.row_offset = None      # offset dentro de la fila
        self.default_offset = None  # offset dentro de la seccion de esquema
        self.default_value = None

    def __repr__(self):
        return f"<Col {self.index} {self.name} type={self.type:#x} flag={self.flag:#x}>"


class UtfTable:
    """Tabla @UTF."""

    def __init__(self, data, base=0):
        """data: bytes de la tabla completa. base: offset de la tabla dentro del fichero."""
        self.base = base
        self.data = data
        if data[:4] != b"@UTF":
            raise ValueError(f"no es una tabla @UTF (magic={data[:4]!r})")

        self.table_size = struct.unpack_from(">I", data, 0x04)[0] + 0x08
        self.version = struct.unpack_from(">H", data, 0x08)[0]
        self.rows_offset = struct.unpack_from(">H", data, 0x0A)[0] + 0x08
        self.strings_offset = struct.unpack_from(">I", data, 0x0C)[0] + 0x08
        self.data_offset = struct.unpack_from(">I", data, 0x10)[0] + 0x08
        self.name_offset = struct.unpack_from(">I", data, 0x14)[0]
        self.columns_count = struct.unpack_from(">H", data, 0x18)[0]
        self.row_width = struct.unpack_from(">H", data, 0x1A)[0]
        self.rows_count = struct.unpack_from(">I", data, 0x1C)[0]

        self.schema_offset = 0x20
        self.schema_size = self.rows_offset - self.schema_offset
        self.rows_size = self.strings_offset - self.rows_offset
        self.strings_size = self.data_offset - self.strings_offset
        self.data_size = self.table_size - self.data_offset

        self.string_table = data[self.strings_offset:self.data_offset]
        self.name = self._str(self.name_offset)

        self.columns = []
        self._parse_schema()

    # -- utilidades -------------------------------------------------
    def _str(self, offset):
        end = self.string_table.find(b"\0", offset)
        if end < 0:
            end = len(self.string_table)
        return self.string_table[offset:end].decode("utf-8", "replace")

    def _parse_schema(self):
        pos = self.schema_offset
        row_pos = 0
        for i in range(self.columns_count):
            info = self.data[pos]
            name_off = struct.unpack_from(">I", self.data, pos + 1)[0]
            pos += 5
            col = Column(i)
            col.info = info
            col.flag = info & 0xF0
            col.type = info & 0x0F
            col.name_offset = name_off
            if col.flag & COL_FLAG_NAME:
                col.name = self._str(name_off)
            size = TYPE_SIZES.get(col.type)
            if size is None:
                raise ValueError(f"tipo de columna desconocido {col.type:#x}")
            if col.flag & COL_FLAG_DEFAULT:
                col.default_offset = pos
                col.default_value = self._read_value(self.data, pos, col.type)
                pos += size
            elif col.flag & COL_FLAG_ROW:
                col.row_offset = row_pos
                row_pos += size
            self.columns.append(col)

    @staticmethod
    def _read_value(buf, off, ctype):
        if ctype == 0x00:
            return buf[off]
        if ctype == 0x01:
            return struct.unpack_from(">b", buf, off)[0]
        if ctype == 0x02:
            return struct.unpack_from(">H", buf, off)[0]
        if ctype == 0x03:
            return struct.unpack_from(">h", buf, off)[0]
        if ctype == 0x04:
            return struct.unpack_from(">I", buf, off)[0]
        if ctype == 0x05:
            return struct.unpack_from(">i", buf, off)[0]
        if ctype == 0x06:
            return struct.unpack_from(">Q", buf, off)[0]
        if ctype == 0x07:
            return struct.unpack_from(">q", buf, off)[0]
        if ctype == 0x08:
            return struct.unpack_from(">f", buf, off)[0]
        if ctype == 0x09:
            return struct.unpack_from(">d", buf, off)[0]
        return buf[off:off + TYPE_SIZES.get(ctype, 4)]

    # -- acceso -----------------------------------------------------
    def column(self, name):
        for c in self.columns:
            if c.name == name:
                return c
        return None

    def value(self, name, row=0):
        """Valor de una columna en la fila indicada (int/str/bytes)."""
        col = self.column(name)
        if col is None:
            return None
        if col.flag & COL_FLAG_DEFAULT:
            return col.default_value
        if col.flag & COL_FLAG_ROW:
            off = self.rows_offset + row * self.row_width + col.row_offset
            if col.type == 0x0A:
                soff = struct.unpack_from(">I", self.data, off)[0]
                return self._str(soff)
            if col.type == 0x0B:
                doff, dsize = struct.unpack_from(">II", self.data, off)
                return self.data[self.data_offset + doff:self.data_offset + doff + dsize]
            return self._read_value(self.data, off, col.type)
        return None

    def row(self, row=0):
        return {c.name: self.value(c.name, row) for c in self.columns}

    def rows(self):
        for r in range(self.rows_count):
            yield self.row(r)

    def string(self, offset):
        return self._str(offset)

    def __repr__(self):
        return (f"<UtfTable {self.name!r} cols={self.columns_count} "
                f"rows={self.rows_count} width={self.row_width}>")
