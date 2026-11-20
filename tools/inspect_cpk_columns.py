# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from srwv_cpk import Cpk

p = r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"
cpk = Cpk(p)

print("HEADER:")
for k, v in sorted(cpk.h.items()):
    print("  %-24s %s" % (k, v))
print("\nITOC tables:", list(cpk.itoc_info.keys()))
for name, tab in cpk.itoc_info.items():
    print("  tabla", name, "columnas:")
    for col in tab.columns:
        print("    ", col)
