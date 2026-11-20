"""Busca texto natural (dialogos) dentro de los ficheros de STGEST_EN."""
import re

from srwv_cpk import Cpk
from stage_pack import entries, extract

PATH = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
NAT = re.compile(rb"[A-Z][A-Za-z'\-]*(?:[ ,.!?;:\"'-]+[A-Za-z'\-]+){6,}[.!?]")


def main():
    cpk = Cpk(PATH)
    tot = 0
    hits = []
    for f in entries(cpk):
        pt = extract(cpk, f)
        ms = NAT.findall(pt)
        # descartar lineas de codigo lua
        ms = [m for m in ms if not re.search(rb'\b(SC_|function|return|elseif|local)\b', m)]
        if ms:
            hits.append((len(ms), f['id'], f['ex'], ms[:2]))
            tot += len(ms)
    print('entradas con texto natural:', len(hits), 'frases:', tot)
    for n, fid, ex, sample in sorted(hits, reverse=True)[:10]:
        print(n, fid, ex)
        for s in sample:
            print('    ', s[:120])


if __name__ == '__main__':
    main()
