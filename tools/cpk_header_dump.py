import sys, pathlib, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
for p in sys.argv[1:]:
    b=pathlib.Path(p).read_bytes()
    print('===',p,len(b))
    print(b[:256].hex(' ',4))
    print('ascii:', ''.join(chr(c) if 32<=c<127 else '.' for c in b[:256]))
