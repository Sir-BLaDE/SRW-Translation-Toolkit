# -*- coding: utf-8 -*-
"""Reconstruye los 30 CPK de DLC con el dialogo y los objetivos traducidos.

Uso:
    python dlc_build.py                  # traduce con los mapas de datos/dlc_work
    python dlc_build.py --identity        # solo comprueba la identidad estructural
    python dlc_build.py --only dlc003_en.cpk

Los CPK se reconstruyen SIEMPRE desde backup/dlc_en (nunca desde el juego).
"""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

BAK = r"C:/Dev/Default Project/srwv/backup/dlc_en"
WORK = r"C:/Dev/Default Project/srwv/datos/dlc_work"
OUT = r"C:/Dev/Default Project/srwv/outputs/dlc_es"
BLOCK = re.compile(r"\[\[(.*?)\]\]", re.S)
STRTBL = re.compile(r"(str_tbl\s*=\s*\{)(.*?)(\};)", re.S)

OBJECTIVES = {
    "Defeat all enemies.": "Derrota a todos los enemigos.",
    "Any ally unit is defeated.": "Cualquier unidad aliada ha sido derrotada.",
    "Ally unit is defeated.": "Una unidad aliada ha sido derrotada.",
    "Ally battleship is defeated.": "Un acorazado aliado ha sido derrotado.",
    "SR points are not included in download contents.":
        "Los puntos SR no se incluyen en los contenidos descargables.",
    "SR points are not included in Special Scenarios.":
        "Los puntos SR no se incluyen en los escenarios especiales.",
    "SR points are not included in this scenario.":
        "Los puntos SR no se incluyen en este escenario.",
    "SR Points are not included\\nin downloadable content.":
        "Los puntos SR no se incluyen\\nen los contenidos descargables.",
    "Tobia is defeated.": "Tobia ha sido derrotado.",
    "Maito is defeated.": "Maito es derrotado.",
    "Yatenko's HP falls below 5,000.": "Los PV de Yatenko bajan de 5.000.",
    "Any enemy unit reaches the map edge.":
        "Cualquier unidad enemiga llega al borde del mapa.",
    "Any enemy unit reaches the line.":
        "Cualquier unidad enemiga alcanza la línea.",
    "Any enemy unit enters the target zone.":
        "Cualquier unidad enemiga entra en la zona objetivo.",
    "Defeat Shaomai (Hoi).": "Derrota a Shaomai (Hoi).",
    "Deal damage against Paozu.": "Causa daño a Paozu.",
    "Defeat Geara Zulu (Angelo.)": "Derrota al Geara Zulu (Angelo).",
    "Defeat Geara Zulu (Angelo).": "Derrota al Geara Zulu (Angelo).",
    "Defeat PLAN-1056 Chodar I.": "Derrota al PLAN-1056 Chodar I.",
    "Defeat Rozen Zulu.": "Derrota al Rozen Zulu.",
    "Defeat Mazin Emperor G.": "Derrota al Mazin Emperor G.",
    "Reach 4th turn of ally phase.": "Alcanza el cuarto turno de la fase aliada.",
    "SR_MF_nickname_SR is defeated.": "SR_MF_nickname_SR ha sido derrotado.",
    "Adjacent units at the same height (such as both on the ground \\nor in the air) "
    "can receive effects such as Support Attack and\\nSupport Defense to help each "
    "other out. Use Support Attack when\\nit's ally phase and Support Defense when "
    "it's enemy phase.":
        "Las unidades adyacentes a la misma altura (por ejemplo, ambas en el suelo\\n"
        "o ambas en el aire) pueden recibir efectos como Ataque de Apoyo y\\n"
        "Defensa de Apoyo para ayudarse mutuamente. Usa el Ataque de Apoyo en\\n"
        "la fase aliada y la Defensa de Apoyo en la fase enemiga.",
    "Adjacent units can use Support Attack and Support\\nDefense. Keep units with "
    "these capabilities adjacent to each\\nother at all times during battle.":
        "Las unidades adyacentes pueden usar Ataque de Apoyo y Defensa de\\n"
        "Apoyo. Mantén siempre juntas a las unidades con estas\\n"
        "capacidades durante la batalla.",
    "???": "???",
}


def load_maps():
    """Devuelve (bloques EN->ES, objetivos EN->ES)."""
    blocks = {}
    files = sorted(glob.glob(os.path.join(WORK, "batches", "batch_*.es.json")))
    for p in files:
        arr = json.load(io.open(p, encoding="utf-8"))
        src = p.replace(".es.json", ".json")
        en = json.load(io.open(src, encoding="utf-8"))
        assert len(arr) == len(en), (p, len(arr), len(en))
        for a, b in zip(en, arr):
            assert isinstance(b, str), (p, b)
            if a != b:
                assert "[[" not in b and "]]" not in b, (p, a[:40], b[:40])
                blocks[a] = b
    labels_path = os.path.join(WORK, "labels_es.json")
    if os.path.exists(labels_path):
        labels = json.load(io.open(labels_path, encoding="utf-8"))
        blocks.update(labels)
        print("etiquetas de lugar aplicadas:", len(labels))
    return blocks, dict(OBJECTIVES)


def apply_row(txt, blocks, objectives, is_row1):
    if is_row1:
        m = STRTBL.search(txt)
        if m:
            seg = m.group(2)
            for en, es in objectives.items():
                seg = seg.replace('"%s"' % en, '"%s"' % es)
            txt = txt[:m.start(2)] + seg + txt[m.end(2):]
        return txt

    def rep(m):
        body = m.group(1)
        new = blocks.get(body)
        return "[[" + (new if new is not None else body) + "]]"

    return BLOCK.sub(rep, txt)


def build_file(path, blocks, objectives, identity=False):
    base = os.path.basename(path)
    c = load(path)
    new_files = {}
    nrows = 0
    for r in c.rows:
        raw = c.plain(r)
        try:
            txt = raw.decode("utf-8")
        except Exception:
            continue
        if r["id"] == 2 or (r["id"] != 1 and "[[" not in txt):
            continue
        new = txt if identity else apply_row(txt, blocks, objectives,
                                             r["id"] == 1)
        if new == txt:
            continue
        plain = new.encode("utf-8")
        new_files[r["id"]] = (c.cipher(r, plain), len(plain))
        nrows += 1
    blob = build_ordered(path, new_files)
    out_path = os.path.join(OUT, base)
    with io.open(out_path, "wb") as f:
        f.write(blob)
    return out_path, nrows, len(new_files)


def verify(path, out_path, blocks, objectives_journal, identity=False):
    a = load(path)
    b = load(out_path)
    assert len(a.rows) == len(b.rows), (path, "filas")
    issues = []
    for ra, rb in zip(a.rows, b.rows):
        if rb["ex"] != len(b.plain(rb)):
            issues.append("fila %d ExtractSize %d != %d"
                          % (rb["id"], rb["ex"], len(b.plain(rb))))
        pa = a.plain(ra)
        pb = b.plain(rb)
        if pa.count(b"[[") != pb.count(b"[["):
            issues.append("fila %d delimitadores [[ %d -> %d"
                          % (ra["id"], pa.count(b"[" * 2), pb.count(b"[[")))
        if identity:
            continue
        # La fila 2 son comentarios Lua; el constructor la deja intacta a proposito.
        if ra["id"] == 2:
            continue
        try:
            ta = pa.decode("utf-8")
            tb = pb.decode("utf-8")
        except Exception:
            continue
        for m in BLOCK.finditer(ta):
            body = m.group(1)
            # Only flag blocks that DO have a translation: the original
            # [[body]] must no longer be present in the rebuilt row.
            if blocks.get(body, body) != body and "[[" + body + "]]" in tb:
                issues.append("fila %d bloque sin traducir %r"
                              % (ra["id"], body[:50]))
                break
        if ra["id"] == 1:
            for en, es in objectives_journal.items():
                if en != es and ('"%s"' % en) in ta and ('"%s"' % en) in tb:
                    issues.append("fila 1 objetivo sin traducir %r" % en[:50])
    return issues


def main():
    identity = "--identity" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    os.makedirs(OUT, exist_ok=True)
    blocks, objectives = ({}, {}) if identity else load_maps()
    print("mapa de bloques:", len(blocks), "| objetivos:", len(objectives))

    files = sorted(glob.glob(os.path.join(BAK, "dlc*.cpk")))
    total_rows = 0
    all_issues = []
    for p in files:
        base = os.path.basename(p)
        if only and base != only:
            continue
        out_path, _n, nr = build_file(p, blocks, objectives, identity)
        issues = verify(p, out_path, blocks, objectives, identity)
        total_rows += nr
        all_issues += ["%s: %s" % (base, i) for i in issues]
        print("  %-16s filas_mod=%d %s" % (base, nr, "OK" if not issues else issues))
    print("filas modificadas:", total_rows)
    if all_issues:
        print("PROBLEMAS:", len(all_issues))
        for i in all_issues[:30]:
            print("  ", i)
        raise SystemExit(1)
    print("verificacion OK")


if __name__ == "__main__":
    main()
