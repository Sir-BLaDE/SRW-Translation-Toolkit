# -*- coding: utf-8 -*-
"""Audita el CSV de batalla: tokens de formato, saltos y crecimiento de longitud."""
import csv
import io
import re

CSV = r"C:/Dev/Default Project/srwv/datos/lineas_batalla_final_es6.csv"

tok = re.compile(r"(%[ds]|\\c[01]|\\a\d\d|\\n|\\r\\n|\$[nlrfcFkwbe]|[A-Z]+\[[^\]]*\])")


def toks(s):
    return sorted(tok.findall(s))


rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig", newline="")))
print("filas:", len(rows))

bad_tok = []
grow = []
nas = []
for r in rows:
    en, es = r["en"], r["es"]
    if not es.strip():
        continue
    te, ts = toks(en), toks(es)
    if te != ts:
        bad_tok.append((r["id"], en, es, te, ts))
    ge = len(en.encode("utf-8"))
    gs = len(es.encode("utf-8"))
    grow.append((gs - ge, r["id"], en, es))
    if "\\n" in en and "\\n" not in es:
        nas.append((r["id"], en, es))

print("tokens distintos:", len(bad_tok))
for b in bad_tok[:25]:
    print("  id %s\n    EN %r\n    ES %r\n    tokEN %s tokES %s" % b)

grow.sort(reverse=True)
print("\nmayor crecimiento en bytes:")
for g, i, en, es in grow[:15]:
    print("  +%4d id=%-6s %r -> %r" % (g, i, en[:60], es[:60]))
print("\ncrecimiento medio %.1f | >80 bytes: %d | >150: %d"
      % (sum(g for g, *_ in grow) / len(grow),
         sum(1 for g, *_ in grow if g > 80),
         sum(1 for g, *_ in grow if g > 150)))

print("\nsin \\n donde el EN lo tenia:", len(nas))
for n in nas[:10]:
    print("  id %s %r -> %r" % n)
