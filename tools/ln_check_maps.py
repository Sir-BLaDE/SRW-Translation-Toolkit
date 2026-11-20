# -*- coding: utf-8 -*-
import io
import json

D = r"C:/Dev/Default Project/srwv/datos"
m3 = json.load(io.open(D + "/ln_id3_compact_es.json", encoding="utf-8"))
m1 = json.load(io.open(D + "/ln_id1_es.json", encoding="utf-8"))
for k in ["AT Field", "Anti-Spirit Attack", "Chain of Command", "Mazin Power",
          "All attributes' damage reduced to 10%."]:
    print("m3", repr(k), "->", repr(m3.get(k, "NO ESTA")))
for k in ['"Player, Come Here"',
          '"Ange, Brimming with Confidence (1)"',
          '"Ange, Brimming with Confidence (2)"']:
    print("m1", repr(k), "->", repr(m1.get(k, "NO ESTA")))
