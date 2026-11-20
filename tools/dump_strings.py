import re
import sys
from pathlib import Path

p = Path(sys.argv[1])
b = p.read_bytes()
text = b.decode("latin-1", "ignore")
for pat in sys.argv[2:]:
    print("==", pat)
    for m in list(re.finditer(pat, text, re.I))[:8]:
        chunk = text[max(0, m.start() - 160):m.end() + 160]
        chunk = re.sub(r"[^\x20-\x7e]+", " ", chunk)
        print(" ", " ".join(chunk.split())[:320])
