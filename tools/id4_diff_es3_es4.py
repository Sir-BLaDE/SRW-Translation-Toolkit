import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

def get4(path):
    c = load(path)
    f4 = [f for f in c.rows if f['id'] == 4][0]
    return c.plain(f4)

a = get4(r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es3.cpk')
b = get4(r'C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es4.cpk')
print('len', len(a), len(b))

# group contiguous diffs
i = 0
groups = []
while i < len(a):
    if a[i] != b[i]:
        j = i
        while j < len(a) and a[j] != b[j]:
            j += 1
        groups.append((i, j))
        i = j
    else:
        i += 1
print('diff groups', len(groups))
for s, e in groups:
    print('%s-%s len=%d' % (hex(s), hex(e), e-s))
    print('  A:', repr(a[s:e]))
    print('  B:', repr(b[s:e]))
