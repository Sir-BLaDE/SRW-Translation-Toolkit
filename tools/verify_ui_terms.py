# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

cf = load(r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk")
blob = b"".join(cf.plain(r) for r in cf.rows)

terms = [b"Beginner's Mode", b"Standard Mode", b"Guidance Mode",
         b"Protagonist Settings", b"First Name", b"Nickname",
         b"Blood Type", b"Blood-Type", b"Reading switching",
         b"End Settings", b"End-Settings", b"Reading Switching"]

for t in terms:
    i = blob.find(t)
    print(t.decode(), "ENCONTRADO (sin traducir)" if i >= 0 else "OK (traducido)")
