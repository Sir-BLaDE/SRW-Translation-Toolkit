import struct
def build_exact(orig,strings,pad_to=None):
    h=list(struct.unpack_from('<12I',orig,0)); st=h[6]
    n=h[9]; assert len(strings)==n
    ids=orig[h[10]:h[10]+32*h[11]]
    blob=bytearray(); offs=[]
    for s in strings:
        offs.append(len(blob)); blob+=s.encode()+b'\0'
    if pad_to is not None:
        assert len(blob)<=pad_to,(len(blob),pad_to)
        blob+=b'\0'*(pad_to-len(blob))
    h[7]=len(blob); h[8]=(st+len(blob)+7)&~7; h[10]=(h[8]+4*n+7)&~7
    out=bytearray(struct.pack('<12I',*h)); out+=orig[48:st]; out+=blob
    while len(out)<h[8]: out.append(0)
    out+=struct.pack(f"<{n}I",*offs)
    while len(out)<h[10]: out.append(0)
    out+=ids
    return bytes(out)
