# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

cf = load(r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK")
pt = b"".join(cf.plain(r) for r in cf.rows)

import re
# Find all ASCII strings that were likely translated
# Compare with original
cf0 = load(r"C:/Dev/Default Project/srwv/backup/OP_CK_original.cpk")
pt0 = b"".join(cf0.plain(r) for r in cf0.rows)

# Find differences
diffs = []
for i in range(len(pt0)):
    if pt0[i] != pt[i]:
        # find the string region
        start = i
        while start > 0 and pt0[start-1] != 0:
            start -= 1
        end = i
        while end < len(pt0) and pt0[end] != 0:
            end += 1
        orig_str = pt0[start:end].decode("ascii", "replace")
        # find new string
        nend = start
        while nend < len(pt) and pt[nend] != 0:
            nend += 1
        new_str = pt[start:nend].decode("utf-8", "replace")
        if orig_str != new_str and orig_str not in [d[0] for d in diffs]:
            diffs.append((orig_str, new_str, len(orig_str.encode()), len(new_str.encode())))
        i = end

for orig, new, lo, ln in diffs:
    flag = " *** LONGER ***" if ln > lo else ""
    print("%d -> %d %s: %r -> %r%s" % (lo, ln, "bytes", orig, new, flag))
print("total diffs:", len(diffs))
