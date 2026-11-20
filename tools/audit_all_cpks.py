# -*- coding: utf-8 -*-
"""Auditor global: recorre TODOS los CPK del juego y busca texto ingles visible.

- Explora cada fila de cada CPK: UTF-8 directo, XOR 0x5E y (si aplica) BLTU.
- No descarta una linea por contener espanol: solo descarta ruido conocido.
- Respeta un limite de tamano por fila para no cargar gigas de imagenes/audio.
"""
import glob
import os
import re
import sys
from collections import Counter, OrderedDict

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load as load_cpk
from srwv_bltu import load as load_bltu

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
MAX_ROW = 2 * 1024 * 1024        # filas mas grandes: solo scan ASCII en crudo
MAX_CPK = 40 * 1024 * 1024       # CPK mas grandes: solo scan ASCII en crudo

# STGEST_EN ya se audita en audit_english_full.py; aqui se omite por su tamano.
TEXT_BIG = set()

# Carpetas de otros idiomas: no se usan en la instalacion EN, se omiten.
SKIP_DIRS = ("/HG/", "/HK/", "/JP/", "/KR/", "/TW/", "/CN/", "/JPN/", "/TWN/")

# Palabras inglesas inequivocas (senales fuertes). Se evitan articles sueltos
# que aparecen en texto espanol ("a", "no", "me", "el"...) para reducir ruido.
EN = re.compile(
    r"\b(the|and|you|your|yours|that|this|these|those|with|have|has|from|"
    r"they|them|their|what|would|there|about|just|like|know|going|been|"
    r"because|before|after|when|will|were|was|are|but|for|his|her|"
    r"she|him|one|all|out|get|got|can|don't|it's|i'm|we're|you're|"
    r"attack|defeat|defeated|enemy|allies|ally|weapon|damage|level|"
    r"turn|phase|start|press|select|confirm|cancel|continue|yes|no|"
    r"move|range|hit|miss|point|ability|skill|unit|pilot|mission|"
    r"commander|captain|soldier|officer|successor|empire|king|queen|"
    r"where|who|why|how|need|want|should|could|must|shall|"
    r"receive|increase|decrease|effective|only|also|very|more|most|"
    r"less|than|then|here|its|our|my|we|he|be|is|do|does|did|of|in|on|at|to|by|or|an)\b",
    re.I)

# Marcadores espanoles claros: si estan, la cadena ya es traducible.
ES = re.compile(r"[áéíóúñÁÉÍÓÚ¿¡]|\b(el|la|los|las|un|una|de|del|al|que|es|son|y|con|"
                r"por|para|si|su|sus|este|esta|más|pero|como|cuando|donde|porque|"
                r"nada|todo|también|puede|puedes|hay|hasta|desde|entre|sobre|bajo|"
                r"muy|mucho|poco|ahora|aquí|así|bien|mal|te|se|nos|os|les|lo|le|"
                r"sido|ser|era|fue|tan|tanto|ella|él|nosotros|usted|tu|tus|nuestro)\b", re.I)

# Terminos propios / tecnicos que no se traducen (nombre de mecha, serie, etc.).
KEEP = re.compile(
    r"\b(Gundam|Mazinger|Getter|Nadesico|Yamato|Gamillas|Grungust|Huckebein|"
    r"Amuro|Char|Kamille|Banagher|Newtype|I-Field|Psycommu|Funnel|Reflector|"
    r"AMBAC|Vernier|Trans-Am|Innovator|X-Rounder|Crossbone|Vanguard|Celestial|"
    r"Zeon|Federation|Jupiter|Mars|Nadesico|Gundam|Zegapain|Zaminger)\b", re.I)

# Ruido conocido: texto codificado, etiquetas, marcadores internos.
NOISE = re.compile(
    r"(<srw-tag|\$kw|\$kwe|\[STORY_NO\]|\[SCENARIO|\[TURN_CNT\]|\[MONEY\]|"
    r"\[PARTS\*\]|\[ROBOT\*\]|\[SKILL\*\]|\[PILOT\]|\[TACP\]|"
    r"[~^]{2,}|[A-Z]\^{4,}|^[0-9\W]+$|GNF|CRILAYLA|@|#|%)")

SPLIT = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def strings_from(data, xor=0):
    if xor:
        data = bytes(b ^ xor for b in data)
    for part in SPLIT.split(data):
        if len(part) < 6:
            continue
        try:
            s = part.decode("utf-8")
        except Exception:
            continue
        for line in re.split(r"\r\n|\n", s):
            line = line.strip("\u3000 \t\r")
            if len(line) < 6:
                continue
            yield line


def is_en(s):
    if NOISE.search(s):
        return False
    if ES.search(s):
        return False
    if not EN.search(s):
        return False
    rest = EN.sub(" ", s)
    if not EN.search(rest) and KEEP.search(s):
        return False
    return True


def scan_raw(data):
    for m in re.finditer(rb"[ -~]{6,}", data):
        try:
            s = m.group().decode("ascii")
        except Exception:
            continue
        if is_en(s):
            yield s


report = OrderedDict()
skipped = []
paths = sorted({p.lower(): p for p in
                glob.glob(G + "/**/*.cpk", recursive=True) +
                glob.glob(G + "/**/*.CPK", recursive=True)}.values())
for path in paths:
    rel = os.path.relpath(path, G)
    if any(d in "/" + rel.replace("\\", "/") for d in SKIP_DIRS):
        skipped.append((rel, os.path.getsize(path), "otro idioma"))
        continue
    size = os.path.getsize(path)
    base = os.path.basename(path)
    if size > MAX_CPK and base not in TEXT_BIG:
        skipped.append((rel, size, "CPK demasiado grande"))
        continue
    print("ESCaneando", rel, flush=True)
    try:
        cf = load_cpk(path)
    except Exception as e:
        skipped.append((rel, size, "error carga: %s" % e))
        continue
    pool = Counter()
    for r in cf.rows:
        if r["size"] > MAX_ROW:
            # Solo inspeccion de ASCII crudo por chunks para no cargar la fila.
            with open(path, "rb") as f:
                f.seek(r["offset"])
                remaining = r["size"]
                while remaining > 0:
                    chunk = f.read(min(1024 * 1024, remaining))
                    if not chunk:
                        break
                    for s in scan_raw(chunk):
                        pool[s] += 1
                    remaining -= len(chunk)
            continue
        pt = cf.plain(r)
        for s in strings_from(pt):
            if is_en(s):
                pool[s] += 1
        for s in strings_from(pt, 0x5E):
            if is_en(s):
                pool[s] += 1
        if "CMN00" in rel.upper():
            try:
                t = load_bltu(pt)
                for x in t.all_strings():
                    s = x[3] if isinstance(x, (tuple, list)) else str(x)
                    if isinstance(s, str) and is_en(s):
                        pool[s] += 1
            except Exception:
                pass
    if pool:
        report[rel] = pool

out = r"C:/Dev/Default Project/srwv/datos/audit_all_cpks.txt"
with open(out, "w", encoding="utf-8") as f:
    for rel, pool in report.items():
        f.write("\n" + "=" * 70 + "\n%s: %d cadenas EN\n" % (rel, len(pool)))
        for s, n in pool.most_common():
            f.write("  %4d  %r\n" % (n, s[:200]))
    f.write("\n" + "=" * 70 + "\nOMITIDOS:\n")
    for rel, size, why in skipped:
        f.write("  %s (%d bytes) %s\n" % (rel, size, why))

print("%-60s %8s %8s" % ("CPK", "EN_UNIQ", "EN_TOT"))
for rel, pool in report.items():
    print("%-60s %8d %8d" % (rel[:60], len(pool), sum(pool.values())))
print("\nomitidos:", len(skipped))
for rel, size, why in skipped:
    print("  ", rel, size, why)
print("detalle ->", out)
