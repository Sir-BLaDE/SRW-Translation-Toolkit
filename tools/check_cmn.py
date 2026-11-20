import sys, re, os
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

accent_re = re.compile(r'[\u00c0-\u00ff\u00a1\u00bf]')
base = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC'
for lang in ['EN0','CN0','JP0']:
    for name in ['CMN00.CPK','CMN00_PC.CPK']:
        p = os.path.join(base, lang, name)
        c = load(p)
        acc = 0; inv = 0; tot = 0; samp = []
        enc = {}
        for f in c.rows:
            pt = c.plain(f)
            for m in re.finditer(rb'[ -~]{8,}', pt):
                tot += 1
                s = m.group(0)
                if any(b >= 0x80 for b in s):
                    acc += 1
                    # try utf-8
                    u = s.decode('utf-8','ignore')
                    if accent_re.search(u):
                        if '¿' in u or '¡' in u: inv += 1
                        if len(samp) < 3: samp.append(u[:60])
        print('%s/%s rows=%d ascii-segs=%d hi-byte=%d utf8-accent=%d inv=%d' % (lang,name,len(c.rows),tot,acc,inv,len(samp)))
        for s in samp: print('   ',repr(s))
        # dump bytes of a known string
        pt0 = c.plain(c.rows[min(1,len(c.rows)-1)])
        i = pt0.find(b'\xc3\xa1')
        j = pt0.find(b'\xe1')
        print('   c3a1 at', i, ' lone e1 at', j)
