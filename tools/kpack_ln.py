"""Parseo y construccion de los ficheros de KPACK_P4_LN (formato propio).

id0: cadena de registros {key[4], 0, next_off, 0, texto NUL, relleno} alineados a 16.
id1: {magic[4], count, offs_start=0x10, str_start, offsets u32[n], cadenas alineadas a 4}.
id3: secuencia {u32 total, texto NUL rellenado} con total = 4 + align4(len(texto)+1).
id4: registros {key[4], ..., len en +0x3c, titulo en +0x40} tamano 72 + align4(len+1).
"""
import struct


def align(v, a):
    return (v + a - 1) & ~(a - 1)


# ---------- id0 ----------
def parse0(pt):
    recs = []
    off = 0
    while off + 16 <= len(pt):
        key = pt[off:off + 4]
        a, nxt, d = struct.unpack_from('<3I', pt, off + 4)
        end = nxt if nxt else len(pt)
        raw = pt[off + 16:end]
        nul = raw.find(b'\0')
        if nul >= 0:
            raw = raw[:nul]
        recs.append({'key': key, 'next': nxt, 'a': a, 'd': d, 'text': raw})
        if nxt <= off or nxt > len(pt):
            break
        off = nxt
    return recs


def build0(recs):
    out = bytearray()
    starts = []
    for r in recs:
        starts.append(len(out))
        body = r['text'] + b'\0'
        size = align(16 + len(body), 16)
        out += r['key'] + struct.pack('<3I', r['a'], 0, r['d'])
        out += body + b'\0' * (size - 16 - len(body))
    # rellenar next
    for i, r in enumerate(recs):
        nxt = starts[i + 1] if i + 1 < len(recs) else 0
        struct.pack_into('<I', out, starts[i] + 8, nxt)
    return bytes(out)


# ---------- id1 ----------
def parse1(pt):
    magic = pt[:4]
    count, os_, ss = struct.unpack_from('<3I', pt, 4)
    offs = list(struct.unpack_from('<%dI' % count, pt, os_))
    strs = []
    for o in offs:
        raw = pt[ss + o:]
        nul = raw.find(b'\0')
        strs.append(raw[:nul] if nul >= 0 else raw)
    return {'magic': magic, 'os': os_, 'ss': ss, 'offs': offs, 'strs': strs}


def build1(d):
    n = len(d['strs'])
    os_ = d['os']
    str_start = os_ + 4 * n
    str_start = align(str_start, 16)
    blob = bytearray()
    offs = []
    for s in d['strs']:
        offs.append(len(blob))
        body = s + b'\0'
        blob += body + b'\0' * (align(len(body), 4) - len(body))
    out = bytearray(d['magic'] + struct.pack('<3I', n, os_, str_start))
    if len(out) < os_:
        out += b'\0' * (os_ - len(out))
    for o in offs:
        out += struct.pack('<I', o)
    if len(out) < str_start:
        out += b'\0' * (str_start - len(out))
    out += blob
    return bytes(out)


# ---------- id3 ----------
def parse3(pt):
    strs = []
    pos = 0
    while pos + 4 <= len(pt):
        total = struct.unpack_from('<I', pt, pos)[0]
        if total < 4 or pos + total > len(pt):
            break
        raw = pt[pos + 4:pos + total]
        nul = raw.find(b'\0')
        strs.append(raw[:nul] if nul >= 0 else raw)
        pos += total
    return strs, pos


def build3(strs):
    out = bytearray()
    for s in strs:
        body = s + b'\0'
        body += b'\0' * (align(len(body), 4) - len(body))
        out += struct.pack('<I', 4 + len(body)) + body
    return bytes(out)


# ---------- id4 ----------
def parse4(pt):
    count = struct.unpack_from('<I', pt, 0)[0]
    recs = []
    off = 0x10
    while off + 0x40 <= len(pt):
        key = pt[off:off + 4]
        ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
        if ln == 0 or ln > 0x400:
            break
        raw = pt[off + 0x40:off + 0x40 + ln]
        nul = raw.find(b'\0')
        if nul >= 0:
            raw = raw[:nul]
        size = 0x48 + align(len(raw) + 1, 4)
        recs.append({'key': key, 'off': off, 'len': ln, 'text': raw,
                     'f': struct.unpack_from('<15I', pt, off + 4)})
        if off + size > len(pt):
            break
        off += size
    return count, recs


def build4(count, recs):
    out = bytearray(struct.pack('<4I', count, 0, 0, 0))
    for r in recs:
        f = list(r['f'])
        body = r['text'] + b'\0'
        body += b'\0' * (align(len(body), 4) - len(body))
        f[14] = len(body)   # +0x3c
        out += r['key'] + struct.pack('<15I', *f)
        out += body
        out += b'\x00' * 8
    return bytes(out)
