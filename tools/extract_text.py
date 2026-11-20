"""
extract_text.py - Extrae las cadenas legibles de los ficheros internos de un
CPK de Super Robot Wars V (descifra y descomprime segun corresponda) y las
compara entre dos versiones para recuperar traducciones.
"""
import sys, re, struct
sys.path.insert(0, r"C:\Dev\Default Project\srwv\tools")
from srwv_cpk import Cpk
from cri_utf import UtfTable
from crilayla import maybe_decompress, is_crilayla
from srwv_crypto import decrypt_data


def files_of(path):
    c = Cpk(path)
    out = []
    for f in c.file_list():
        data = c.raw[f["offset"]:f["offset"] + f["size"]]
        out.append((f, data))
    return c, out


def decode(data):
    """Devuelve (bytes_planos, etiqueta)"""
    tag = []
    if is_crilayla(data):
        try:
            data = maybe_decompress(data)
            tag.append("crilayla")
        except Exception as e:
            tag.append(f"crilayla-fallo({e})")
    dec = decrypt_data(data)
    if dec[:4] == b"\x00\x00\x00\x00" or sum(1 for b in dec[:512] if 32 <= b < 127) > 200:
        tag.append("texto-plano")
        return dec, "+".join(tag)
    tag.append("cifrado")
    return dec, "+".join(tag)


def strings(data, minlen=4):
    return [m.decode("latin1") for m in re.findall(rb"[\x20-\x7e]{%d,}" % minlen, data)]


if __name__ == "__main__":
    orig_path, mod_path = sys.argv[1], sys.argv[2]
    co, fo = files_of(orig_path)
    cm, fm = files_of(mod_path)
    print(f"{'id':>4} {'orig_size':>10} {'mod_size':>10}  estado")
    for (fo_, do), (fm_, dm) in zip(fo, fm):
        do_dec, tag_o = decode(do)
        dm_dec, tag_m = decode(dm)
        print(f"{fo_['id']:>4} {fo_['size']:>10} {fm_['size']:>10}  orig={tag_o} mod={tag_m}")
        so = strings(do_dec)
        sm = strings(dm_dec)
        print(f"      cadenas orig={len(so)} mod={len(sm)}")
        if len(so) != len(sm):
            print("      !! distinto numero de cadenas")
            continue
        diffs = [(a, b) for a, b in zip(so, sm) if a != b]
        print(f"      diferencias: {len(diffs)}")
        for a, b in diffs[:15]:
            print(f"        {a[:80]!r}\n     -> {b[:80]!r}")
