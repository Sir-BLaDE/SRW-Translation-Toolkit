import sys
sys.path.insert(0,'/tmp/b')
from cpk_util import load
L=open('/tmp/lst.txt').read().split('\n')[int(sys.argv[1])::4]
for f in L:
    if not f: continue
    try: k=load(f); print('OK',len(k.rows),f.split('Super Robot Wars V/')[-1],flush=True)
    except Exception as e: print('FAIL',f.split('Super Robot Wars V/')[-1],str(e)[:60],flush=True)
