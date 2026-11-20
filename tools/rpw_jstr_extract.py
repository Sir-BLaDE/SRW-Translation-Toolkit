# -*- coding: utf-8 -*-
"""Extrae la lista de trabajo de rpw_jstr: cadenas unicas traducibles.

Genera datos/rpw_jstr_worklist.json con {texto_original: veces} y estadisticas.
"""
import io
import json
import re
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk"
OUT = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_worklist.json"

POOL = 0x48
PEND = 0x1EE10
I2I = 0x1EE58
IEND = 0x3BCE8

JP = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff\uff66-\uff9f]")
LAT = re.compile(r"[A-Za-z]{2,}")


def parse_pool(pt):
    """Devuelve [(off, raw)] de cadenas NUL contiguas en el pool."""
    out = []
    pos = POOL
    while pos < PEND:
        end = pt.find(b"\0", pos)
        assert end >= 0 and end < PEND + 1, "pool sin NUL en %d" % pos
        out.append((pos - POOL, pt[pos:end]))
        pos = end + 1
    assert pos == PEND, "pool no termina en limite: %d != %d" % (pos, PEND)
    return out


def is_candidate(s):
    if not s:
        return False
    if JP.search(s):
        return False
    if not LAT.search(s):
        return False
    if s.startswith(("<", "rid_", "pid_", "bgm_", "se_", "me_", "vo_")):
        return False
    if re.match(r"^(prod|data)#\d+$", s):
        return False
    if re.match(r"^\d+\.\d+$", s):
        return False
    if "/" in s or "\\" in s or ":" in s:
        return False
    if re.match(r"^[A-Z0-9_]+$", s):
        return False
    if re.match(r"^[%$A-Za-z0-9_]+$", s) and "_" in s:
        return False
    return True


def main():
    c = load(SRC)
    pt = c.plain(c.rows[0])
    strs = parse_pool(pt)
    print("cadenas en pool:", len(strs))

    # offsets referenciados por i2i
    n = (IEND - I2I) // 8
    starts = set(off for off, _ in strs)
    bad = 0
    for i in range(n):
        idx, off = struct.unpack_from("<2I", pt, I2I + i * 8)
        if off not in starts:
            bad += 1
            if bad <= 5:
                print("  i2i offset no es inicio de cadena:", idx, off)
    print("i2i entradas:", n, "offsets invalidos:", bad)

    counts = {}
    for off, raw in strs:
        try:
            s = raw.decode("utf-8")
        except Exception:
            continue
        if is_candidate(s):
            counts[s] = counts.get(s, 0) + 1

    print("candidatos unicos:", len(counts), "apariciones:", sum(counts.values()))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(counts, f, ensure_ascii=False, indent=0, sort_keys=True)
    print("escrito", OUT)

    # muestras por tamano
    by_len = sorted(counts.items(), key=lambda kv: -len(kv[0]))
    print("\n-- 40 mas largos --")
    for s, k in by_len[:40]:
        print("  %4d %r" % (k, s[:110]))
    short = sorted(counts.items(), key=lambda kv: len(kv[0]))
    print("\n-- 40 mas cortos --")
    for s, k in short[:40]:
        print("  %4d %r" % (k, s))


if __name__ == "__main__":
    main()
