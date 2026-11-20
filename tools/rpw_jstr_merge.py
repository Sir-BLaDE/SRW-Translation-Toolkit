# -*- coding: utf-8 -*-
"""Fusiona los lotes traducidos en el mapa final rpw_jstr_es.json."""
import io
import json

D = r"C:/Dev/Default Project/srwv/datos/"


def load(name):
    return json.load(io.open(D + name, encoding="utf-8"))


def main():
    work = load("rpw_jstr_worklist.json")
    pend_a = load("rpw_pend_A.json")
    pend_b = load("rpw_pend_B.json")
    a1 = load("rpw_es_A1.json")
    a2 = load("rpw_es_A2.json")
    b1 = load("rpw_es_B1.json")
    b2 = load("rpw_es_B2.json")
    c = load("rpw_es_C.json")
    reuse = load("rpw_jstr_reuse.json")

    assert len(a1) + len(a2) == len(pend_a), (len(a1), len(a2), len(pend_a))
    assert len(b1) + len(b2) == len(pend_b), (len(b1), len(b2), len(pend_b))

    out = {}
    out.update(reuse)
    for k, v in zip(pend_a, a1 + a2):
        out[k] = v
    for k, v in zip(pend_b, b1 + b2):
        out[k] = v
    for k, v in c.items():
        if k not in work:
            raise SystemExit("clave C inexistente en worklist: %r" % k)
        out[k] = v

    # claves del mapa que no existen en el pool -> error
    missing = [k for k in out if k not in work]
    if missing:
        print("CLAVES INVALIDAS:", len(missing))
        for k in missing[:20]:
            print("   ", repr(k))
        raise SystemExit(1)

    # traducciones vacias o identicas
    empty = [k for k, v in out.items() if not v.strip()]
    same = [k for k, v in out.items() if v == k]
    print("claves finales:", len(out), "de", len(work))
    print("vacias:", len(empty), "identicas:", len(same))
    for k in same[:20]:
        print("   identica:", repr(k))

    json.dump(out, io.open(D + "rpw_jstr_es.json", "w", encoding="utf-8",
                           newline="\n"),
              ensure_ascii=False, indent=0, sort_keys=True)
    print("escrito datos/rpw_jstr_es.json")

    rest = sorted(set(work) - set(out), key=lambda s: (-len(s), s))
    print("sin traducir (se conservan):", len(rest))
    for s in rest[:40]:
        print("   ", repr(s[:90]))


if __name__ == "__main__":
    main()
