# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from layout_map import ES

terms = ["Beginner's Mode", "Standard Mode", "Guidance Mode",
         "Protagonist Settings", "First Name", "Nickname",
         "Blood Type", "Blood-Type", "Reading switching",
         "End Settings", "End-Settings", "Reading Switching"]

for t in terms:
    v = ES.get(t)
    print(repr(t), "->", repr(v) if v else "NOT IN MAP")
