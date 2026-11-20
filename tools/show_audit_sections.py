import re
import io

t = io.open(r"C:/Dev/Default Project/srwv/datos/audit_english_full.txt", encoding="utf-8").read()
for sec in ["MTZKN_PT", "MTZKN_RT", "MTZKN_NM"]:
    m = re.search(r"={5,}\n" + sec + r":.*?(?=\n={5,}\n|\Z)", t, re.S)
    print("\n--- " + sec + " ---")
    print(m.group(0)[:12000] if m else "NA")
