# -*- coding: utf-8 -*-
"""MtZkn_Pt: reconstruye DSCR/DSC2 y traduce los campos de nombre CHFN/CHNN.

Uso: python mtzkn_pt_build_acc2.py [salida.cpk] [--names ruta.json]
Si el mapa de nombres esta vacio, la salida debe coincidir con la version anterior
(outputs/MtZkn_Pt_es_acc.cpk).
"""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_crypto import encrypt_data

SRC = r"C:/Dev/Default Project/srwv/backup/MtZkn_Pt_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/MtZkn_Pt_es_acc2.cpk"
TM = r"C:/Dev/Default Project/srwv/datos/mtzkn_pt_es_accent.json"
TM2 = r"C:/Dev/Default Project/srwv/datos/mtzkn_pt_dsc2_es.json"
NAMES = r"C:/Dev/Default Project/srwv/datos/mtzkn_names_es.json"

NAME_TAGS = (b"RBTN", b"RBN2", b"CHFN", b"CHNN", b"PLTN", b"PRDC")


def rewrite_names(data, trans):
    """Reescribe TAG + len + '^^^' + texto cuando el texto esta en el mapa."""
    if not trans:
        return data, 0
    out = bytearray()
    pos = 0
    changed = 0
    while True:
        best = None
        for t in NAME_TAGS:
            i = data.find(t, pos)
            if i >= 0 and (best is None or i < best[0]):
                best = (i, t)
        if best is None:
            out += data[pos:]
            break
        i, t = best
        p = i + 4
        if p >= len(data):
            out += data[pos:]
            break
        ln = data[p]
        if data[p + 1:p + 4] != b"^^^":
            out += data[pos:i + 4]
            pos = i + 4
            continue
        val = data[p + 4:p + 4 + ln]
        try:
            txt = val.decode("utf-8")
        except Exception:
            out += data[pos:i + 4]
            pos = i + 4
            continue
        new = trans.get(txt)
        out += data[pos:i]
        if new is not None and new != txt:
            nb = new.encode("utf-8")
            if len(nb) > 255:
                raise SystemExit("nombre demasiado largo: %r" % new)
            out += t + bytes([len(nb)]) + b"^^^" + nb
            changed += 1
        else:
            out += data[i:p + 4 + ln]
        pos = p + 4 + ln
    return bytes(out), changed


def parse_pt(data):
    idx = data.find(b"^^^DSCR")
    assert idx >= 0
    size = struct.unpack_from("<H", data, idx + 7)[0]
    desc_start = idx + 9
    desc = data[desc_start:desc_start + size]
    tail = data[desc_start + size:]
    prefix = data[:desc_start]
    return prefix, desc, tail, idx


def build_pt(prefix, desc_bytes, tail):
    dsiz_pos = prefix.find(b"^^^DSIZ")
    new_total = len(prefix) + len(desc_bytes) + len(tail)
    new_dsiz = new_total - 24
    new_data = new_dsiz - 8
    new_dscr = len(desc_bytes)
    prefix = prefix[:dsiz_pos + 7] + struct.pack("<H", new_dsiz) + prefix[dsiz_pos + 9:]
    data_pos = prefix.find(b"^^DATA")
    prefix = prefix[:data_pos + 6] + struct.pack("<H", new_data) + prefix[data_pos + 8:]
    dscr_pos = prefix.find(b"^^^DSCR")
    prefix = prefix[:dscr_pos + 7] + struct.pack("<H", new_dscr) + prefix[dscr_pos + 9:]
    return prefix + desc_bytes + tail


def translate_dsc2(tail, trans2):
    i = tail.find(b"DSC2")
    if i < 0 or i + 6 > len(tail):
        return tail, 0
    size = struct.unpack_from("<H", tail, i + 4)[0]
    start = i + 6
    end = start + size
    blob = tail[start:end]
    k = blob.find(b"KANA")
    text = (blob[:k] if k >= 0 else blob).decode("utf-8", "replace")
    es = trans2.get(text, text)
    if es == text:
        return tail, 0
    rest = blob[len(text.encode("utf-8")):]
    new_blob = es.encode("utf-8") + rest
    new_tail = tail[:i + 4] + struct.pack("<H", len(new_blob)) + new_blob + tail[end:]
    return new_tail, 1


def main():
    out_path = OUT
    names_path = NAMES
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--names":
            names_path = args[i + 1]
            i += 2
        else:
            out_path = args[i]
            i += 1

    trans = {}
    try:
        trans = json.load(io.open(TM, encoding="utf-8"))
    except Exception:
        print("sin mapa DSCR")
    trans2 = {}
    try:
        trans2 = json.load(io.open(TM2, encoding="utf-8"))
    except Exception:
        pass
    names = {}
    try:
        names = json.load(io.open(names_path, encoding="utf-8"))
    except Exception:
        print("sin mapa de nombres:", names_path)

    cf = load(SRC)
    new_files = {}
    changed = changed2 = changedn = 0
    for f in cf.rows:
        dec = bytes(b ^ 0x5E for b in cf.plain(f))
        dec, n3 = rewrite_names(dec, names)
        changedn += n3
        prefix, desc, tail, idx = parse_pt(dec)
        full_en = desc.decode("utf-8", "replace")
        full_es = trans.get(full_en, full_en)
        if full_es != full_en:
            changed += 1
        tail, n2 = translate_dsc2(tail, trans2)
        changed2 += n2
        new_dec = build_pt(prefix, full_es.encode("utf-8"), tail)
        new_enc = bytes(b ^ 0x5E for b in new_dec)
        new_files[f["id"]] = (encrypt_data(new_enc), len(new_enc))

    print("DSCR %d | DSC2 %d | nombres %d | filas %d"
          % (changed, changed2, changedn, len(cf.rows)))
    out = build_ordered(SRC, new_files)
    open(out_path, "wb").write(out)
    print("escrito", out_path, len(out))

    cf2 = load(out_path)
    print("diag", cf2.cpk.diagnose() or "ok")
    bad = [r["id"] for r in cf2.rows if r["ex"] != len(cf2.plain(r))]
    print("ex_mismatch:", bad)


if __name__ == "__main__":
    main()
