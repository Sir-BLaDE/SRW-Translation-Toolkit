# -*- coding: utf-8 -*-
"""Restaura el hablante/parentesis de b_18 sin tocar los carteles de lugar."""
import io
import json

P = r"C:/Dev/Default Project/srwv/datos/stgest_bracket_work/b_18_out.json"
data = json.load(io.open(P, encoding="utf-8"))
fixed = {}
for k, v in data.items():
    if "（" in k:
        prefix = k.split("\r\n", 1)[0] + "\r\n（"
        body = v
        if body.startswith(prefix):
            pass
        else:
            if body.startswith("（"):
                body = body[1:]
            if body.endswith("）"):
                body = body[:-1]
            body = prefix + body + "）"
        fixed[k] = body
    else:
        # Cartel de localizacion: quitar el envoltorio anadido por error
        prefix = k.split("\r\n", 1)[0] + "\r\n（"
        body = v
        if body.startswith(prefix):
            body = body[len(prefix):]
        if body.endswith("）"):
            body = body[:-1]
        fixed[k] = body

with io.open(P, "w", encoding="utf-8") as fh:
    json.dump(fixed, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("revisadas", len(fixed))
